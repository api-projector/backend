import hashlib
import json
import pathlib
import typing as ty

from tests.helpers.path_finder import find_path

ASSETS_FOLDER = "assets"


class AssetsProvider:
    """Assets provider."""

    def __init__(self, fspath) -> None:
        """Init provider."""
        self._cwd: pathlib.Path = pathlib.Path(fspath)
        self._opened_files: list[object] = []

    def open_file(
        self,
        filename: str,
        mode: str = "rb",
        encoding: str | None = None,
    ) -> ty.IO[str]:
        """Open file and return a stream."""
        filepath = find_path(self._cwd, filename)

        file_handler = open(filepath, mode, encoding=encoding)  # noqa: WPS515
        self._opened_files.append(file_handler)
        return file_handler

    def read_json(self, filename: str) -> dict[str, object]:
        """Read json file to dict."""
        return json.loads(
            self.open_file(
                "{0}.json".format(filename),
                mode="r",
            ).read(),
        )

    def read(self, filename: str) -> str:
        """Read file to string."""
        return self.open_file(filename, mode="r").read()

    def get_hash(self, filename: str) -> str:
        """Get md5-hash of file."""
        filepath = find_path(self._cwd, filename)

        hash_md5 = hashlib.md5(usedforsecurity=False)
        with open(filepath, "rb") as reader:
            for chunk in iter(lambda: reader.read(4096), b""):  # noqa: WPS426
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def close(self) -> None:
        """Close opened files."""
        for file_handler in self._opened_files:
            if not file_handler.closed:  # type: ignore
                file_handler.close()  # type: ignore
        self._opened_files.clear()
