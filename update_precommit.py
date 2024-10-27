"""
This file is used by .github/workflows/update-pre-commit-config.yaml
"""

from pathlib import Path
from yaml import safe_load, dump
from re import search
from requests import get, exceptions


def get_version_from_releases(owner: str, repo: str) -> str | None:
    try:
        res = get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest")
        res.raise_for_status()
    except exceptions.HTTPError:
        return None

    res_json = res.json()
    if "tag_name" not in res_json:
        raise KeyError(f"Could not find tag information in response {res_json}")

    return res_json["tag_name"]


def get_version_from_tags(owner: str, repo: str) -> str | None:
    try:
        res = get(f"https://api.github.com/repos/{owner}/{repo}/tags")
        res.raise_for_status()
    except exceptions.HTTPError:
        return None

    return res.json()[0]["name"]


def update_precommit_config(file_path: str | Path) -> list[str]:
    """
    Updates version of pre-commit repos

    Args:
        file_path (str | Path): Path to .pre-commit-config.yaml

    Returns:
        list[str]: List of repos whose versions have been updated

    Raises:
        TypeError: When failing to parse expected dict structure
        KeyError: When expected dict key is not found
        ValueError: When failing to regex-match repo owner and name

    Expects:
    .pre-commit-config.yaml file with structure:
        repos:
            - repo: url.com/repoowner/reponame
              rev: x.x.x
              hooks:
                - id: hookid
    """
    # Load config file
    with open(file_path, "r") as f:
        config = safe_load(f)

    if not isinstance(config, dict):
        raise TypeError(f"{file_path} could not be parsed into dictionary")

    if "repos" not in config:
        raise KeyError(f"{file_path} does not seem to contain a 'repos' key")

    updated: list[str] = []

    # Attempt to update each repo
    for repo in config["repos"]:
        if not isinstance(repo, dict):
            raise TypeError(
                f"Error reading {file_path}: Item '{repo}' in repos list is of type f{type(repo)}. Expected dict"
            )

        if "repo" not in repo:
            raise KeyError(
                f"Error reading {file_path}: Could not find repo url in dict {repo}"
            )

        url = repo["repo"]

        # Retrieve GitHub repo owner and name
        m = search(".*/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", url)

        if m is None or len(matchgroups := m.groups()) != 2:
            raise ValueError(
                f"Error parsing repo URL '{url}'. Expected 2 regex matches, found {m if m is None else len(matchgroups)}"
            )
        owner, repo_name = matchgroups

        # Attempt to find new version info
        new_version = get_version_from_releases(owner, repo_name)
        new_version = (
            get_version_from_tags(owner, repo_name)
            if new_version is None
            else new_version
        )

        # If new_version found, update
        old_version = repo["rev"]
        if (new_version is not None) and (new_version != old_version):
            repo["rev"] = new_version
            updated.append(repo_name)

        with open(file_path, "w") as f:
            dump(config, f, sort_keys=False)

    return updated


if __name__ == "__main__":
    file_path = ".pre-commit-config.yaml"
    updated_repos = update_precommit_config(file_path)
    print(updated_repos)
