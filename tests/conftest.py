from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers, isfunction
from os import PathLike
from pathlib import Path
from typing import Callable, List, Tuple

from pytest import FixtureRequest, fixture

src_folder = "CHANGE_ME"


@fixture(scope="session")
def ROOT() -> Path:
    def validate_dir(dir: str | Path, error_msg: str | None) -> Path:
        dir = Path(dir)
        error_msg = f"Directory {dir} not found" if not error_msg else error_msg

        if not dir.is_dir():
            raise FileNotFoundError(error_msg)

        return dir

    assumed_root = Path(__file__).resolve().parent.parent
    assumed_root = validate_dir(
        Path(assumed_root),
        f"The assumed project root directory {assumed_root} does not exist.",
    )
    _ = validate_dir(
        Path(assumed_root / src_folder),
        f"Expected root directory to contain '{src_folder}' folder. {assumed_root} does not contain a f'{src_folder}' folder.",
    )
    return assumed_root


@fixture(scope="session")
def SRC(ROOT) -> Path:
    return ROOT / src_folder


@fixture(scope="session")
def list_module_functions(ROOT, request: FixtureRequest) -> List[Tuple[str, Callable]]:
    """
    Lists all functions from the module located at a given path.

    Args:
        request (pytest.FixtureRequest): Fixture request object containing parameters:
            - module_name (str): Name of the module.
            - path (Path): Path to the .py file, relative to `ROOT`.

    Returns:
        List[Tuple[str, Callable]]: List of tuples, where each tuple represents a function:
            Tuple:
                - str: The function name.
                - Callable: The function object.

    Example:
        @pytest.mark.parametrize(
            "list_module_functions", [("CHANGE_ME.module2.", "CHANGE_ME/module2/main.py")], indirect=True
        )
        def myfunc(list_module_functions):
            [...]
    """

    # Get parameters from the request object
    module_name: str = request.param[0]
    path: Path = request.param[1]

    if not isinstance(module_name, str):
        raise TypeError(
            f"module_name '{module_name}' is of type {type(module_name).__name__}. Expected str"
        )

    if not isinstance(path, Path | PathLike | str):
        raise TypeError(
            f"path '{path}' is of type {type(path).__name__}. Expected pathlib.Path"
        )

    path = ROOT / path

    # Load the module from the specified path
    spec = spec_from_file_location(module_name, path)
    if spec is None:
        raise ImportError(f"Could not load module spec for {module_name} from {path}")

    module = module_from_spec(spec)
    if module is None or spec.loader is None:
        raise ImportError(f"Could not create or load module {module_name} from {path}")

    spec.loader.exec_module(module)

    # Return all functions in the module
    return getmembers(module, isfunction)
