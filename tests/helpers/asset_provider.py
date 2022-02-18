import hashlib
import json
import pathlib
from typing import IO, Dict, List, Optional

from tests.helpers.path_finder import find_path

ASSETS_FOLDER = "assets"


class AssetsProvider:
    """Assets provider."""

    def __init__(self, fspath) -> None:
        """Init provider."""
        self._cwd: pathlib.Path = pathlib.Path(fspath)
        self._opened_files: List[object] = []

    def open_file(
        self,
        filename: str,
        mode: str = "rb",
        encoding: Optional[str] = None,
    ) -> IO[str]:
        """Open file and return a stream."""
        filepath = find_path(self._cwd, filename)

        file_handler = open(filepath, mode, encoding=encoding)  # noqa: WPS515
        self._opened_files.append(file_handler)
        return file_handler

    def read_json(self, filename: str) -> Dict[str, object]:
        """Read json file to dict."""
        return json.loads(
            self.open_file(
                "{0}.json".format(filename),
                mode="r",
            ).read(),
        )

    def get_hash(self, filename: str) -> str:
        """Get md5-hash of file."""
        filepath = find_path(self._cwd, filename)

        hash_md5 = hashlib.md5()  # noqa: S303
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
