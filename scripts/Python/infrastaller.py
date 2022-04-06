#!/usr/bin/env python3

"""Downloads and installs binary packages.

Uses a provided config file of packages (and included metadata) to download, extract, and
install each package. It is also able to handle extracting binaries from certain archive types.

For more information, see the included README file.

Examples:

    For example usage, see `python3 infrastaller.py --help`.
"""

import json
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from collections.abc import Mapping
from pathlib import Path, PurePath
from typing import Union

import click
import logzero
from logzero import logger

DEFAULT_BIN_PATH = Path("/usr/local/bin")
DEFAULT_CONFIG_PATH = Path.cwd() / "packages.json"
#
# `SYSTEM` and `MACHINE` are used for replacing templated strings in the config file, namely
# the `url` and `file_to_extract` fields. `SYSTEM` should resolve to 'linux' or 'darwin', and
# `MACHINE` is normally 'x86_64' (this may change with new Apple hardware eventually). But most
# download links use 'amd64' instead of 'x86_64', so this replacement is done here.
#
SYSTEM = os.uname().sysname.lower()
MACHINE = os.uname().machine.lower().replace("x86_64", "amd64")


def configure_logging(verbosity: str) -> None:
    """Configures logzero verbosity."""

    logging_levels = {
        "quiet": {"output": logzero.NOTSET, "format": ""},
        "normal": {"output": logzero.INFO, "format": "%(color)s%(message)s%(end_color)s"},
        "verbose": {"output": logzero.DEBUG, "format": "%(color)s%(message)s%(end_color)s"},
        "debug": {
            "output": logzero.DEBUG,
            "format": (
                "[%(levelname)8s %(asctime)s %(funcName)s:%(lineno)d] "
                "%(color)s%(message)s%(end_color)s"
            ),
        },
    }

    logzero.loglevel(logging_levels[verbosity]["output"])
    logzero.formatter(formatter=logzero.LogFormatter(fmt=logging_levels[verbosity]["format"]))


@click.command()
@click.option(
    "-b",
    "--bin-path",
    default=DEFAULT_BIN_PATH,
    type=click.Path(exists=True),
    help=f"Full path to binary install location (default: {DEFAULT_BIN_PATH}).",
)
@click.option(
    "-c",
    "--config",
    default=DEFAULT_CONFIG_PATH,
    type=click.Path(exists=True),
    help=f"Full path to config file (default: {DEFAULT_CONFIG_PATH}).",
)
@click.option(
    "-p",
    "--package",
    type=str,
    multiple=True,
    help="Specific package(s), defined in config file, to install.",
)
@click.option(
    "-g",
    "--group",
    type=str,
    multiple=True,
    help="Specific group(s) of packages, defined in config file, to install.",
)
@click.option(
    "-o",
    "--output",
    default="normal",
    type=click.Choice(["quiet", "normal", "verbose", "debug"], case_sensitive=False),
    help="Set script output type (default: normal).",
)
def infrastaller(bin_path: str, config: str, package: tuple, group: tuple, output: str) -> None:
    """Downloads and installs binaries.

    \b
    Install all packages to default location:
        $ python3 infrastaller.py

    \b
    Install packages to a custom location:
        $ python3 infrastaller.py --bin-path /root/bin

    \b
    Read config from a custom location:
        $ python3 infrastaller.py --config /etc/my_packages.json

    \b
    Install specific packages from config file:
        $ python3 infrastaller.py --package binary2 --package binary3

    \b
    Install a group of packages and an individual package:
        $ python3 infrastaller.py --group my-packages --package binary2

    \b
    Enable verbose output:
        $ python3 infrastaller.py --output verbose
    """

    configure_logging(output)

    with open(config, "rb") as json_config:
        logger.debug("Reading config file %s", config)
        packages_data = json.loads(json_config.read())

    for pkg_group, binaries in packages_data.items():
        for binary, appinfo in binaries.items():
            #
            # Package should be installed if:
            #   - neither 'package' nor 'group' flags are set (i.e. install everything)
            #   - passed by 'package' flag (user specified a package)
            #   - the package is part of a group passed by 'group' flag (user specified a group)
            #
            if (package or group) and (binary in package or pkg_group in group):
                install_binary(Path(bin_path), binary, appinfo)

    logger.info("Installation complete")


def install_binary(install_path: Path, binary_name: str, package_data: dict) -> None:
    """Parses package metadata and wraps all installation steps.

    Args:
        install_path: The full path to the install directory.
        binary_name: Filename to give the binary in the install_path.
        package_data: Package metadata from the JSON config file.
    """

    logger.info("Installing %s...", binary_name)

    #
    # The `url` field can be a string or dictionary depending on if the link is template-able.
    # See the README for more information.
    #
    if isinstance(package_data["url"], Mapping):
        url = replace_placeholder_in_string(package_data["url"][SYSTEM], package_data["version"])
    else:
        url = replace_placeholder_in_string(package_data["url"], package_data["version"])

    download_dir = Path(tempfile.mkdtemp())
    downloaded_file = download(url, download_dir)

    if "extract" in package_data:
        binary_to_install = extract(
            package_data["extract"]["type_of_archive"],
            replace_placeholder_in_string(
                package_data["extract"]["file_to_extract"], package_data["version"]
            ),
            downloaded_file,
        )
    else:
        binary_to_install = downloaded_file

    binary_full_path = PurePath.joinpath(install_path, binary_name)
    move_bin(binary_to_install, binary_full_path)
    chmod_exec(binary_full_path)

    logger.info("Installed %s to %s", binary_name, binary_full_path)

    if Path.is_dir(download_dir):
        logger.debug("Removing %s", download_dir)
        shutil.rmtree(download_dir)


def download(source: str, save_path: Path) -> str:
    """Download the package from a URL source."""
    destination = PurePath.joinpath(save_path, os.path.basename(source))
    logger.debug("Downloading from %s", source)
    logger.debug("Saving download to %s", destination)
    with urllib.request.urlopen(source) as response, open(destination, "wb") as output:
        output.write(response.read())
    return destination


def extract(type_of_archive: str, file_to_extract: str, archive: Path) -> str:
    """A wrapper method to extract tar.gz and zip archives.

    Args:
        type_of_archive: The file type of the archive (e.g. zip, targz).
        file_to_extract: The filename to extract from the archive.
        archive: The full path to the compressed file.
    """

    logger.debug("Extracting %s", archive)

    destination = archive.parent

    if type_of_archive == "targz":
        with tarfile.open(archive, "r:gz") as tar_file:
            tar_file.extract(file_to_extract, destination)
    elif type_of_archive == "zip":
        with zipfile.ZipFile(archive, "r") as zip_file:
            zip_file.extract(file_to_extract, destination)
    else:
        logger.error("Archive type %s not supported.", type_of_archive)
        sys.exit(1)

    logger.debug("Extracted %s to %s", file_to_extract, destination)
    return PurePath.joinpath(destination, file_to_extract)


def move_bin(source: Union[Path, str], destination: Union[Path, str]) -> None:
    """Moves the binary to a location in the PATH."""
    try:
        logger.debug("Moving %s to %s", source, destination)
        shutil.move(source, destination)
    except OSError as error:
        logger.exception(error)
        sys.exit(1)


def chmod_exec(filename: Union[Path, str]) -> None:
    """Makes a binary executable; unix 755 permissions."""
    logger.debug("Making %s executable", filename)
    os.chmod(filename, 0o0755)  # Octal in Python needs the leading '0o'.


def replace_placeholder_in_string(string: str, version: str) -> str:
    """Replaces instances of template variables with appropriate values."""
    conversions = {
        "{{ version }}": version,
        "{{ system }}": SYSTEM,
        "{{ machine }}": MACHINE,
    }
    for placeholder, replacement in conversions.items():
        string = string.replace(placeholder, replacement)
    return string


if __name__ == "__main__":
    # The following check is disabled because Click handles parameter values.
    # pylint: disable=no-value-for-parameter
    infrastaller()
