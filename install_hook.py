# SPDX-License-Identifier

from pathlib import Path

SCRIPT = r"""#!/bin/sh
set -o noglob

python -m black .

for file in $(git diff --cached --name-only); do
    git add $file
done"""


def main() -> None:
    print("Installing pre-commit hook")
    with open(".git/hooks/pre-commit", "w") as f:
        f.write(SCRIPT)
    Path(".git/hooks/pre-commit").chmod(0o700)
