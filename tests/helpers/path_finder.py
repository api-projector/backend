import pathlib

ASSETS_FOLDER = "assets"


def find_path(current_dir, filename: str) -> pathlib.Path:
    """Find path for file."""
    path = current_dir

    while path.parents:
        pathfile = pathlib.Path(path, ASSETS_FOLDER, filename)
        if pathfile.is_file():
            return pathfile

        path = path.parent

    raise FileNotFoundError(filename)
