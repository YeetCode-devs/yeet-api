# SPDX-License-Identifier: MIT

import os
import json
import logging

from pathlib import Path

# from typing import Any
from git.repo import Repo
from . import exceptions, CACHE_DIR, YEET_DEVICES_REPO

# Do not set up logging, since we're an API package,
# it makes more sense for the logging output to be
# controlled by the app using this package.
log: logging.Logger = logging.getLogger(__name__)


class _DeviceJSON:
    """Class for parsing device json.
    The path is going to be: /yeet-devices/brand/model.json.
    This is a private API, app should not use this, as it is subject
    to changes anytime.

    The basic structure that must be followed:
    {
        "fullname": str,
        "codename": str,
        "resources": {
            "recovery": {"name": "link"},
            "kernel": {"name": "link"},
            "roms": {"name": link}
        }
    }

    Returns:
        _type_: _description_
    """

    def __init__(self, devicejson: Path) -> None:
        self._json: dict

        with open(devicejson, "r") as f:
            self._json = json.load(f)

        # JSON sanity checks
        # We don't want array json
        if not isinstance(self._json, dict):
            raise exceptions.InvalidConfigError(
                "JSON must contain an object (dict), "
                f"not an array (list) [{devicejson.name}]"
            )

        if (
            not self._json.get("fullname")
            or not self._json.get("codename")
            or not self._json.get("resources")
        ):
            raise exceptions.InvalidConfigError(
                "Incomplete device config; must "
                "consist of: {fullname, codename, "
                f"resources}} [{devicejson.name}]"
            )

    @property
    def json(self) -> dict:
        """Get the parsed device JSON."""
        return self._json


class Device:
    """device class consisting of multiple useful functions."""

    def __init__(self, brand: str, model: str):
        """Get instance of device class.

        Args:
            brand (Phone brand): Phone brand to look into
            model (Phone model): Phone model to lookup for
        """
        self.brand: str = brand
        self.model: str = model
        self.repopath: os.PathLike = Path(CACHE_DIR).joinpath("yeet-devices")
        self.device: Path = (
            Path(self.repopath).joinpath(self.brand).joinpath(self.model + ".json")
        )
        self.repo: Repo
        self.devicejson: _DeviceJSON

        if not Path(CACHE_DIR).joinpath("yeet-devices").exists():
            Path(self.repopath).mkdir(parents=True)
            log.debug("Cloning device repo")
            self.repo = Repo().clone_from(YEET_DEVICES_REPO, self.repopath)
        else:
            log.debug(f"Using existing repo: {self.repopath}")
            self.repo = Repo(self.repopath)

        log.debug("Pulling remote changes")
        self.repo.remote().pull(rebase=True)

        if not self._exists():
            raise exceptions.NoSuchDevice(
                f"Device {self.brand}/{self.model}.json does not exist"
            )

        self.devicejson = _DeviceJSON(Path(self.device))

    def _exists(self) -> bool:
        """Returns true if such device exist, false otherwise."""
        if not self.device.is_file():
            return False
        return True

    @property
    def fullname(self) -> str:
        """Get full device name."""
        return self.devicejson.json.get("fullname", "")

    @property
    def codename(self) -> str:
        """Get device codename."""
        return self.devicejson.json.get("codename", "")

    def get_available_resources(self) -> tuple[str]:
        """Get available resources provided by the device JSON."""
        return tuple(self.devicejson.json.get("resources", {}).keys())

    def get_resource(self, resource_name: str) -> dict | None:
        """Get a resource for a device."""
        return self.devicejson.json["resources"].get(resource_name)

    def update_database(self, **kwargs) -> None:
        """Update device database by running a git pull.

        Args:
            **kwargs: Flags to be passed to git. By default rebase=True is
                set. Pass rebase=False to override.
        """
        self.repo.remote().pull(**{"rebase": True} | kwargs)
