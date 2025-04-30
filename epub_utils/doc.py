import zipfile
from pathlib import Path
from typing import Union
from epub_utils.container import Container


class Document:
    """
    Represents an EPUB document.

    Attributes:
        path (Path): The path to the EPUB file.
        container (Container): The parsed container document.
    """

    def __init__(self, path: Union[str, Path]) -> None:
        """
        Initialize the Document from a given path.

        Args:
            path (str | Path): The path to the EPUB file.
        """
        self.path: Path = Path(path)
        if not self.path.exists() or not zipfile.is_zipfile(self.path):
            raise ValueError(f"Invalid EPUB file: {self.path}")
        self.container: Container = None
        self._unzip_and_parse_container()

    def _unzip_and_parse_container(self) -> None:
        """
        Unzips the EPUB file and parses the container document.
        """
        with zipfile.ZipFile(self.path, 'r') as epub_zip:
            if "META-INF/container.xml" not in epub_zip.namelist():
                raise ValueError("Missing container.xml in EPUB file.")
            container_xml_content = epub_zip.read("META-INF/container.xml").decode("utf-8")
            self.container = Container(container_xml_content)