import os
import zipfile
from functools import cached_property
from pathlib import Path
from typing import Union

from epub_utils.container import Container
from epub_utils.package import Package
from epub_utils.toc import TableOfContents


class Document:
    """
    Represents an EPUB document.

    Attributes:
        path (Path): The path to the EPUB file.
        _container (Container): The parsed container document.
        _package (Package): The parsed package document.
        _toc (TableOfContents): The parsed table of contents document.
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
        self._toc: TableOfContents = None

    def _read_file_from_epub(self, file_path: str) -> str:
        """
        Read and decode a file from the EPUB archive.

        Args:
            file_path (str): Path to the file within the EPUB archive.

        Returns:
            str: Decoded contents of the file.

        Raises:
            ValueError: If the file is missing from the EPUB archive.
        """
        with zipfile.ZipFile(self.path, 'r') as epub_zip:
            file_normpath = os.path.normpath(file_path)
            namelist = [os.path.normpath(name) for name in epub_zip.namelist()]
            
            if file_normpath not in namelist:
                raise ValueError(f"Missing {file_normpath} in EPUB file.")
            return epub_zip.read(file_path).decode("utf-8")

    @property
    def container(self) -> Container:
        if self._container is None:
            container_xml_content = self._read_file_from_epub(self.CONTAINER_FILE_PATH)
            self._container = Container(container_xml_content)
        return self._container

    @property
    def package(self) -> Package:
        if self._package is None:
            package_xml_content = self._read_file_from_epub(self.container.rootfile_path)
            self._package = Package(package_xml_content)
        return self._package

    @cached_property
    def __package_href(self):
        return os.path.dirname(os.path.normpath(self.container.rootfile_path))

    @property
    def toc(self):
        if self._toc is None:
            package = self.package
            if package.major_version == "3" and package.nav_href is not None:
                toc_href = package.nav_href
            elif package.major_version == "2" and package.toc_href is not None:
                toc_href = package.toc_href
            else:
                return None

            toc_path = os.path.normpath(os.path.join(self.__package_href, toc_href))
            toc_xml_content = self._read_file_from_epub(toc_path)
            self._toc = TableOfContents(toc_xml_content)

        return self._toc
