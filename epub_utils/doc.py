import zipfile
from pathlib import Path
from typing import Union

from epub_utils.container import Container
from epub_utils.package import Package


class Document:
    """
    Represents an EPUB document.

    Attributes:
        path (Path): The path to the EPUB file.
        _container (Container): The parsed container document.
        _package (Package): The parsed package document.
    """

    CONTAINER_FILE_PATH = "META-INF/container.xml"

    def __init__(self, path: Union[str, Path]) -> None:
        """
        Initialize the Document from a given path.

        Args:
            path (str | Path): The path to the EPUB file.
        """
        self.path: Path = Path(path)
        if not self.path.exists() or not zipfile.is_zipfile(self.path):
            raise ValueError(f"Invalid EPUB file: {self.path}")
        self._container: Container = None
        self._package: Package = None
        self._unzip_and_parse_container()

    def _unzip_and_parse_container(self) -> None:
        """
        Unzips the EPUB file and parses the container document.
        """
        with zipfile.ZipFile(self.path, 'r') as epub_zip:
            if self.CONTAINER_FILE_PATH not in epub_zip.namelist():
                raise ValueError("Missing container.xml in EPUB file.")
            container_xml_content = epub_zip.read(self.CONTAINER_FILE_PATH).decode("utf-8")
            self._container = Container(container_xml_content)

    @property
    def container(self) -> Container:
        if self._container is None:
            self._unzip_and_parse_container()
        return self._container
    
    def _unzip_and_parse_package(self, package_file_path) -> None:
        with zipfile.ZipFile(self.path, 'r') as epub_zip:
            if package_file_path not in epub_zip.namelist():
                raise ValueError(f"Missing {package_file_path} in EPUB file.")
            package_xml_content = epub_zip.read(package_file_path).decode("utf-8")
            self._package = Package(package_xml_content)

    @property
    def package(self) -> Package:
        if self._package is None:
            rootfile_path = self.container.rootfile_path
            self._unzip_and_parse_package(rootfile_path)
        return self._package
    
    def toc(self):
        #TODO
        return None
