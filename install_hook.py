# SPDX-License-Identifier

from pathlib import Path


def main() -> None:
    print("Installing pre-commit hook")
    with open(".git/hooks/pre-commit", "w") as f:
        f.write("#!/bin/sh\npython -m black .")
    Path(".git/hooks/pre-commit").chmod(0o700)
