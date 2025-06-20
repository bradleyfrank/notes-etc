#!/usr/bin/env python3

"""
This script will query a Big-IP F5 appliance for information regarding a VIP
(returns IP, pool, pool members) or a pool (returns members).

See: https://f5-sdk.readthedocs.io/

requirements.txt
    argparse
    configparser
    f5-sdk
    fuzzywuzzy
    keyring
    logzero
    python-Levenshtein
    xdg
"""

import argparse
import configparser
import getpass
import keyring
import os
import re
import socket
import sys
import logzero
from logzero import logger
from f5.bigip import ManagementRoot
from fuzzywuzzy import fuzz
from icontrol.exceptions import iControlUnexpectedHTTPError
from xdg import XDG_CONFIG_HOME

#
# The F5 URLs. If adding or subtracting, make sure to update get_arguments().
#
F5_APP = {
    "TAB": "tab.domain.example.tld",
    "TSS": "tss.domain.example.tld",
}

#
# This is a Levenshtein distance ratio, a magical number representing the
# number of transformations required to get from one string to another. After
# some testing, all results under 50 looked like garbage so I set this
# accordingly. Maybe for some reason you want to change it, so here you go.
#
MATCH_THRESHOLD = 50


def get_arguments():
    """Get arguments to script."""

    parser = argparse.ArgumentParser(
        description="Retrieves VIP and pool information from the F5."
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enables debug messages"
    )

    parser.add_argument(
        "-a",
        "--appliance",
        choices=("TAB", "TSS", "ALL"),
        const="all",
        default="ALL",
        help="F5 to query: TSS or TAB (default: %(default)s)",
        nargs="?",
    )

    parser.add_argument(
        "-t",
        "--partition",
        default="default-partition",
        help="Partition to use (default: %(default)s)",
    )

    parser.add_argument(
        "-s",
        "--search",
        action="store_true",
        help="Fuzzy searches for supplied VIP name or pool name",
    )

    lookup_by = parser.add_mutually_exclusive_group(required=True)
    lookup_by.add_argument(
        "-v", "--vip", help="Name or IP of the VIP to lookup."
    )
    lookup_by.add_argument("-p", "--pool", help="Name of the pool to lookup.")

    return parser.parse_args()


def do_authenticate(device, url):
    """Authenticates to a specific F5 appliance."""

    logger.debug("Authenticating as %s to %s", USERNAME, device)

    try:
        mgmt = ManagementRoot(url, USERNAME, PASSWORD)
    except iControlUnexpectedHTTPError as msg:
        print("Authentication failed")
        logger.error("Error: %s", msg)
        sys.exit()

    logger.debug("Authentication successful")

    return mgmt


def load_credentials(config_file):
    """Reads the local config file for the username and password to the F5."""

    logger.debug("XDG_CONFIG_HOME is set to %s", XDG_CONFIG_HOME)

    if not os.path.exists(config_file):
        print("No config file found; please create " + config_file)
        sys.exit()

    creds = configparser.ConfigParser()
    creds.read(config_file)

    if not creds.has_section("f5"):
        print("Config file malformed; unable to read " + config_file)
        sys.exit()

    username = creds["f5"]["username"]
    password = None
    if "password" in creds["f5"]:
        password = creds["f5"]["password"]
        creds.remove_option("f5", "password")
        with open(config_file, 'w') as f:
            creds.write(f)
            keyring.set_password(service_name="tufts_utln", username=username, password=password)
    else:
        password = keyring.get_password(service_name="tufts_utln", username=username)

    if password is None:
        password = getpass.getpass(
            "\n" +
            "Please enter password for tufts_utln '{}' (will be saved in keyring): ".format(username)
        )
        keyring.set_password(service_name="tufts_utln", username=username, password=password )

    return username, password


def lookup_by_pool():
    """Performs the lookup by the provided pool name or search word."""

    logger.info("Initiating lookup by pool")
    matches = find_pool_or_vip_by_name(POOLS, ARGS.pool, ARGS.search)
    for match in matches:
        get_pool_info(match)
        print()


def lookup_by_vip():
    """Performs the lookup by the provided VIP name, IP, or search word."""

    search_is_address = True
    logger.info("Initiating lookup by VIP")

    #
    # Use the socket module to determine if a string is a valid IP address. If
    # it throws an exception than it is *not* an IP address.
    #
    try:
        socket.inet_aton(ARGS.vip)
    except socket.error:
        search_is_address = False

    if search_is_address:
        matches = find_vip_by_ip(VIPS, ARGS.vip)
    else:
        matches = find_pool_or_vip_by_name(VIPS, ARGS.vip, ARGS.search)

    if len(matches) > 0:
        for match in matches:
            vip_pool = get_vip_info(match)
            if not vip_pool:
                logger.debug("Skipping pool lookup")
            else:
                get_pool_info(vip_pool)
            print()
    else:
        print("No matches found.")


def find_vip_by_ip(all_vips, queried_ip):
    """Searches existing VIPs to find a match to the queried IP address."""

    for vip in all_vips:
        #
        # vip.destination returns a string in the format:
        #   /PARTITION/130.255.255.255:1234
        # So remove the prefix and split the string on the colon.
        #
        partition_str = "/" + ARGS.partition + "/"
        destination = vip.destination
        address = destination.replace(partition_str, "").split(":")[0]

        if address == queried_ip:
            vip_name = vip.name
            break
    else:
        return False

    return [vip_name]


def find_pool_or_vip_by_name(full_list, queried_name, fuzzy_search):
    """Wrapper function for searching the pools or VIPs."""

    logger.debug(
        "Performing search for %s in %s partition",
        queried_name,
        ARGS.partition,
    )

    if fuzzy_search:
        matches = find_resource_by_fuzzysearch(full_list, queried_name)
    else:
        matches = find_resource_by_regex(full_list, queried_name)

    return matches


def find_resource_by_fuzzysearch(full_list, queried_name):
    """Searches for a resource name using the Levenshtein ratio."""

    logger.debug("Minimum threshold to match is set to %s", MATCH_THRESHOLD)

    top_match_score = 0
    top_matches = []

    for resource in full_list:
        #
        # If the Levenshtein ratio is above the threshold (see top of script)
        # and greater than the current top match score, (a) insert the pool/vip
        # into the match list in the first spot, and (b) set the score as the
        # newest top score, effectively performing sorting.
        #
        match_score = fuzz.partial_ratio(queried_name, resource.name)
        #
        # Pylint throws an error here regarding indentation, but it's a known
        # bug: https://github.com/PyCQA/pylint/issues/289
        #
        if (
            match_score >= top_match_score
            and match_score > MATCH_THRESHOLD
            and resource.partition == ARGS.partition
        ):
            logger.debug("resource %s scored %s", resource.name, match_score)
            top_matches.insert(0, resource.name)
            top_match_score = match_score
            logger.debug("Top match is now %s", top_matches[0])

    return top_matches


def find_resource_by_regex(full_list, queried_name):
    """Searches for a resource name using regex."""

    matches = []
    queried_name_re = queried_name.replace("*", ".*")
    logger.debug("Transformed query to regex: %s", queried_name_re)

    for resource in full_list:
        #
        # Pylint throws an error here regarding indentation, but it's a known
        # bug: https://github.com/PyCQA/pylint/issues/289
        #
        if (
            re.search(queried_name_re, resource.name)
            and resource.partition == ARGS.partition
        ):
            matches.append(resource.name)

    return matches


def get_vip_info(vip_name):
    """
    Displays information about the VIP.
    https://<f5-ip>/mgmt/tm/ltm/virtual?ver=11.6.0
    """

    logger.debug(
        "Looking up VIP %s under partition %s", vip_name, ARGS.partition
    )

    try:
        vip = MGMT.tm.ltm.virtuals.virtual.load(
            name=vip_name, partition=ARGS.partition
        )
    except iControlUnexpectedHTTPError:
        logger.error("VIP %s not found under %s", vip_name, ARGS.partition)
        sys.exit()

    #
    # vip.* returns a string prefixed with the parition, i.e. "/PARTITION/".
    # This function simply removes it.
    #
    def rps(_):
        return _.replace("/" + ARGS.partition + "/", "")

    print(vip_name)
    print("\tIP: " + rps(vip.destination).split(":")[0])
    print("\tPort: " + rps(vip.destination).split(":")[1])

    if hasattr(vip, "pool"):
        pool_name = rps(vip.pool)
        print("\tPool: " + pool_name)
    else:
        print("\tPool: None")
        return False

    return pool_name


def get_pool_info(pool_name):
    """
    Displays the host members of the pool.
    https://<f5-ip>/mgmt/tm/ltm/pool?ver=11.6.0
    """

    logger.debug(
        "Looking up pool %s in partition %s", pool_name, ARGS.partition
    )

    try:
        pool = MGMT.tm.ltm.pools.pool.load(
            name=pool_name, partition=ARGS.partition
        )
    except iControlUnexpectedHTTPError:
        logger.error("Pool %s not found under %s", pool_name, ARGS.partition)
        sys.exit()

    print(pool_name)
    for member in pool.members_s.get_collection():
        print("\t" + member.name)


#
# Configure script settings from arguments.
#
ARGS = get_arguments()

if ARGS.debug:
    logzero.loglevel()
else:
    logzero.loglevel(0)

#
# Read the config file for user's credentials. The module xdg handles locating
# the proper config directory.
#
CONFIG_FILE = os.path.join(XDG_CONFIG_HOME, "f5creds.conf")
USERNAME, PASSWORD = load_credentials(CONFIG_FILE)

#
# Loop through each F5 device specified.
#
for appliance, f5_url in F5_APP.items():
    logger.debug("Checking if %s matches requested device", appliance)
    if appliance == ARGS.appliance or ARGS.appliance == "ALL":
        print("Querying the " + appliance + " F5:\n")

        #
        # Authenticate to the proper F5 (will Duo push).
        #
        MGMT = do_authenticate(appliance, f5_url)

        #
        # Get a list of VIPs and pools from the F5.
        #
        VIPS = MGMT.tm.ltm.virtuals.get_collection()
        POOLS = MGMT.tm.ltm.pools.get_collection()

        #
        # Do the lookup by pool or VIP.
        #
        if ARGS.pool:
            lookup_by_pool()
        elif ARGS.vip:
            lookup_by_vip()
        else:
            logger.error("Lookup method unknown")
