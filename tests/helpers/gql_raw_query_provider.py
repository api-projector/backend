import pathlib

from tests.helpers.path_finder import find_path


class GhlRawQueryProvider:
    """GraphQL raw query provider."""

    def __init__(self, fspath) -> None:
        """Init provider."""
        self._cwd: pathlib.Path = pathlib.Path(fspath)

    def __call__(self, filename: str) -> str:
        """Find and return file source."""
        filepath = find_path(self._cwd, "{0}.graphql".format(filename))

        with open(filepath, "r") as reader:
            return reader.read()
