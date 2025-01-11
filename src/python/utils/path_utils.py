import os


def find_absolute_directory_path_upwards(
    dir_name: str, start_path: str = os.path.abspath(os.path.dirname(__file__))
) -> str:
    """Returns the absolute path of a directory with a given name by walking upwards.

    Args:
        dir_name: Name of the directory to find the absolute path of.
        start_path: Path to start the search at, by default the absolute path of the directory of
            `__file__`.

    Returns:
        The absolute path of the directory with the given name.

    Raises:
        `ValueError`: If `start_path` is not a valid existing path.
        `FileNotFoundError`: If no directory with the name `dir_name` could be found.
    """
    if not os.path.exists(start_path):
        raise ValueError(f'Invalid start path "{start_path}".')
    current_path: str = start_path
    # If we reached the root directory, path.dirname() simply returns the current path again.
    while current_path != os.path.dirname(current_path):
        if os.path.isdir(os.path.join(current_path, dir_name)):
            return os.path.join(current_path, dir_name)
        current_path = os.path.dirname(current_path)
    raise FileNotFoundError(f'Could not find a directory with the name "{dir_name}".')


SRC_PATH: str = find_absolute_directory_path_upwards("src")
"""Absolute path of the source folder."""

RESOURCES_PATH: str = find_absolute_directory_path_upwards("resources")
"""Absolute path of the resources folder."""
