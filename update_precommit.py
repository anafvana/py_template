import sys
from pathlib import Path

from yaml import dump, safe_load


def update_precommit_config(file_path: str | Path, new_version: str):
    with open(file_path, "r") as f:
        config = safe_load(f)

    config["repos"][0]["rev"] = new_version

    with open(file_path, "w") as f:
        dump(config, f, sort_keys=False)


if __name__ == "__main__":
    file_path = ".pre-commit-config.yaml"
    new_version = sys.argv[1]  # Get the new version from the command-line arguments
    update_precommit_config(file_path, new_version)
