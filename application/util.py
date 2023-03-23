import importlib
import os

from types import ModuleType


def import_module(path: str) -> ModuleType:
    """Import a module from a path.
    
    Args:
        `path` (`str`): The path to the module.
        
    Returns:
        `ModuleType`: The imported module.

    Raises:
        `ImportError`: If the path does not end with \".py\".
        `ImportError`: If the path does not exist.
    """
    if not path.endswith(".py"):
        raise ImportError("Module path must end with \".py\"")

    if not os.path.exists(path):
        raise ImportError("Module path does not exist")

    spec = importlib.util.spec_from_file_location(
        path.split("/")[-1][:-3], path
    )

    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)

    return m
