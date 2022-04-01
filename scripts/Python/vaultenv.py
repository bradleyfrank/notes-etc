#!/usr/bin/env python3

"""Manages multiple Hashicorp Vault instances.
"""

import argparse
import copy
import getpass
import json
import sys
from pathlib import PosixPath
from typing import Dict

import hvac

#
# {
#   "global": {
#     "email": "bfrank@example.com",
#     "auth": "okta"
#   },
#   "common-build": {
#     "address": "https://vault.example.com",
#     "token": ""
#   }
# }
#

VAULTENV_CONFIG = PosixPath.home() / ".config" / "vaultenv.json"
VAULT_HELPER_FILE = PosixPath.home() / ".vault-tokens"
CLIENT = None


def parse_args() -> argparse.Namespace:
    """Set command line arguments."""
    parser = argparse.ArgumentParser(description="Manages Vault environment variables.")
    parser.add_argument("-i", "--instance", help="Vault instance to use", required=True)
    return parser.parse_args()


def load_json(section: str) -> Dict:
    """Load json config."""
    with open(VAULTENV_CONFIG, encoding="ascii", mode="rt") as config_file:
        data = json.load(config_file)
    if section not in data:
        print(f"No instance '{section}' defined.")
        sys.exit(1)
    env_settings = copy.deepcopy(data[section])
    if "global" in data:
        env_settings.update(data["global"])
    return env_settings


def generate_token(email: str) -> str:
    """Connects to Vault to generate a new auth token."""
    okta_password = getpass.getpass(prompt="Enter your Okta password: ")
    result = CLIENT.auth.okta.login(username=email, password=okta_password)
    if not result:
        print("Error connecting to Vault.")
        sys.exit(1)
    return result["stdout"]


def write_vault_helper_file(address: str, token: str) -> None:
    """Writes Vault address and token to helper file."""
    try:
        with open(VAULT_HELPER_FILE, encoding="ascii", mode="wt") as helper_file:
            json.dump(helper_file, {"VAULT_ADDR": address, "VAULT_TOKEN": token})
    except IOError:
        print("Error writing vault helper file.")
        sys.exit(1)


args = parse_args()
config = load_json(args.instance)

CLIENT = hvac.Client(url=config["address"])

try:
    CLIENT.sys.read_health_status(method='GET')
except ConnectionError:
    print(f"Unable to connect to '{config['address']}'.")
    sys.exit(1)

if "token" not in config:
    config["token"] = generate_token(config["email"])

if CLIENT.secrets.kv.v2.list_secrets("secret"):
    write_vault_helper_file(config["address"], config["email"])
else:
    print("Token is out-of-date and will be regenerated.")
    config["token"] = generate_token(config["email"])
    write_vault_helper_file(config["address"], config["email"])
