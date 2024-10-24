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

3. Install `flit`

```commandline
pip install flit
```

4. Check that `flit` is running from `venv`

```commandline
which flit
```

5. Install package with `flit`

```commandline
flit install --extras all
```

6. Install `pre-commit`

```commandline
pre-commit install
```

## Dependencies

Manage dependencies via `pyproject.toml`.

Dependencies are separated between:

- `[project.dependencies]`: dependencies required for the package to run
- `[project.optional-dependencies.dev]`: dependencies required for developing the package (_e.g._ `flit`)
- `[project.optional-dependencies.test]`: dependencies required specifically for testing (_e.g._ `pytest`)

## GitHub Actions

To run pull-request actions, ensure wokflow permissions are correctly set: 

0. If project belongs to organization, run **[ORGANISATION]** steps first
1. Go to `[your-repository]` > Settings > Actions: General > Workflow permissions
2. Select **Read and write permissions**
3. Check **Allow GitHub actions to create pull requests**
</br>

**[ORGANISATION]**:
1. Go to `[your-organisation]` > Settings > Actions: General > Workflow permissions
2. Check **Allow GitHub actions to create pull requests**
