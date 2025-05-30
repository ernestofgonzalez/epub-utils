import os
import zipfile
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Union

from epub_utils.container import Container
from epub_utils.content import XHTMLContent
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

	CONTAINER_FILE_PATH = 'META-INF/container.xml'

	def __init__(self, path: Union[str, Path]) -> None:
		"""
		Initialize the Document from a given path.

		Args:
		    path (str | Path): The path to the EPUB file.
		"""
		self.path: Path = Path(path)
		if not self.path.exists() or not zipfile.is_zipfile(self.path):
			raise ValueError(f'Invalid EPUB file: {self.path}')
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
			norm_namelist = {os.path.normpath(name): name for name in epub_zip.namelist()}
			norm_path = os.path.normpath(file_path)

			if norm_path not in norm_namelist:
				raise ValueError(f'Missing {norm_path} in EPUB file.')

			return epub_zip.read(norm_namelist[norm_path]).decode('utf-8')

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
		return os.path.dirname(self.container.rootfile_path)

	@property
	def toc(self):
		if self._toc is None:
			package = self.package
			if package.version.major == 3:
				if not package.nav_href:
					return None
				toc_href = package.nav_href
			else:
				if not package.toc_href:
					return None
				toc_href = package.toc_href

			toc_path = os.path.join(self.__package_href, toc_href)
			toc_xml_content = self._read_file_from_epub(toc_path)
			self._toc = TableOfContents(toc_xml_content)

		return self._toc

	def find_content_by_id(self, item_id: str) -> str:
		spine_item = self.package.spine.find_by_idref(item_id)
		if not spine_item:
			raise ValueError(f"Item id '{item_id}' not found in spine")

		manifest_item = self.package.manifest.find_by_id(item_id)
		if not manifest_item:
			raise ValueError(f"Item id '{item_id}' not found in manifest")

		content_path = os.path.join(self.__package_href, manifest_item['href'])
		xml_content = self._read_file_from_epub(content_path)

		content = XHTMLContent(xml_content, manifest_item['media_type'], manifest_item['href'])

		return content

	def find_pub_resource_by_id(self, item_id: str) -> str:
		manifest_item = self.package.manifest.find_by_id(item_id)
		if not manifest_item:
			raise ValueError(f"Item id '{item_id}' not found in manifest")

		content_path = os.path.join(self.__package_href, manifest_item['href'])
		xml_content = self._read_file_from_epub(content_path)

		content = XHTMLContent(xml_content, manifest_item['media_type'], manifest_item['href'])

		return content

	def list_files(self) -> List[Dict[str, str]]:
		"""
		List all files in the EPUB archive.

		Returns:
		    List[Dict[str, str]]: A list of dictionaries containing file information.
		"""
		with zipfile.ZipFile(self.path, 'r') as epub_zip:
			file_list = []
			for zip_info in epub_zip.infolist():
				file_info = {
					'filename': zip_info.filename,
					'file_size': zip_info.file_size,
					'compress_size': zip_info.compress_size,
					'file_mode': zip_info.external_attr >> 16,
					'last_modified': datetime(*zip_info.date_time),
				}
				file_list.append(file_info)
			return file_list

	def get_files_info(self) -> List[Dict[str, Union[str, int]]]:
		"""
		Get information about all files in the EPUB archive.

		Returns:
		    List[Dict]: A list of dictionaries containing file information.
		        Each dictionary contains: 'path', 'size', 'compressed_size', 'modified'.
		"""
		files_info = []

		with zipfile.ZipFile(self.path, 'r') as epub_zip:
			for zip_info in epub_zip.infolist():
				if zip_info.filename.endswith('/'):
					continue

				modified_time = datetime(*zip_info.date_time).strftime('%Y-%m-%d %H:%M:%S')

				file_info = {
					'path': zip_info.filename,
					'size': zip_info.file_size,
					'compressed_size': zip_info.compress_size,
					'modified': modified_time,
				}
				files_info.append(file_info)

		files_info.sort(key=lambda x: x['path'])
		return files_info

	def get_file_by_path(self, file_path: str):
		"""
		Retrieve a file from the EPUB archive by its path.

		Args:
		    file_path (str): Path to the file within the EPUB archive.

		Returns:
		    XHTMLContent or str: For XHTML files, returns XHTMLContent object.
		                        For other files, returns raw content as string.

		Raises:
		    ValueError: If the file is missing from the EPUB archive.
		"""
		file_content = self._read_file_from_epub(file_path)

		if file_path.lower().endswith(('.xhtml', '.html', '.htm')):
			media_type = 'application/xhtml+xml'

			try:
				for item in self.package.manifest.items:
					manifest_path = os.path.join(self._Document__package_href, item['href'])
					if os.path.normpath(manifest_path) == os.path.normpath(file_path):
						media_type = item.get('media_type', 'application/xhtml+xml')
						break
			except:
				pass

			return XHTMLContent(file_content, media_type, file_path)
		else:

			return file_content
