# SPDX-License-Identifier: MIT

import os
import shutil

from pathlib import Path

_home_dir: str

if os.name == "posix":
    _home_dir = os.getenv("HOME", "")
elif os.name == "nt":
    _home_dir = os.getenv("USERPROFILE", "")
else:
    raise OSError("Unsupported OS: yeet-api only supports Windows and unix-like OSses.")

if not shutil.which("git"):
    raise FileNotFoundError("Git executable is not found."
                            "\nFor Windows, install it from https://git-scm.com/downloads"
                            "\nFor Linux, it is best to use your distro package manager. If "
                            "for some reason you can't, use the link for Windows.")

_config_dir = Path(_home_dir).joinpath(".config", "yeet")
if not _config_dir.exists():
    os.makedirs(_config_dir, exist_ok=True)

_cache_dir = Path(_home_dir).joinpath(".cache", "yeet")
if not _cache_dir.exists():
    os.makedirs(_cache_dir, exist_ok=True)

CONFIG_DIR: str = _config_dir.resolve().as_posix()
CACHE_DIR: str = _cache_dir.resolve().as_posix()
YEET_DEVICES_REPO = "https://github.com/YeetCode-devs/yeet-devices.git"
