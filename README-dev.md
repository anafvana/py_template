# Dev Docs

## Setup

Set up project locally:

1. Create and/or activate `venv`

```bash
if [ ! -d "$(pwd)/venv" ]; then python3 -m venv "$(pwd)/venv"; fi; source "$(pwd)/venv/bin/activate"
```

2. Check that pip is running from `venv`

```commandline
which pip
```

3. Install `poetry`

```commandline
pip install poetry
```

4. Check that `poetry` is running from `venv`

```commandline
which poetry
```

5. Install package with `poetry`

```commandline
poetry install --with dev,test
```

6. Install `pre-commit`

```commandline
pre-commit install
```

7. [RECOMMENDED (VSCode)] Install extension [runonsave](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave) by emeraldwalk
   - Set up `autoflake` on save by adding the following snippet to your `settings.json`
   ```json
    "emeraldwalk.runonsave": {
        "commands": [
            {
            // Remove unused imports on save (.py files)
            "match": "\\.(py)$",
            "cmd": "autoflake --remove-all-unused-imports --in-place --recursive --exclude __init__.py ${file}"
            }
        ]
    },
   ```

## Dependencies

Manage dependencies via `pyproject.toml`.

Dependencies are separated between:

- `[tool.poetry.dependencies]`: dependencies required for the package to run
- `[tool.poetry.group.dev.dependencies`: dependencies required for developing the package (_e.g._ `poetry`)
- `[tool.poetry.group.test.dependencies]`: dependencies required specifically for testing (_e.g._ `pytest`)

## GitHub Actions

To run pull-request actions, ensure wokflow permissions are correctly set:

0. If project belongs to organization, run **[ORGANISATION]** steps first
1. Go to `[your-repository]` > Settings > Actions: General > Workflow permissions
2. Select **Read and write permissions**
3. Check **Allow GitHub actions to create pull requests**
   </br>
   </br>

**[ORGANISATION]**:

1. Go to `[your-organisation]` > Settings > Actions: General > Workflow permissions
2. Check **Allow GitHub actions to create pull requests**
