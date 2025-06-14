import os
import zipfile
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional, Union

from epub_utils.container import Container
from epub_utils.content import XHTMLContent
from epub_utils.exceptions import FileNotFoundError as EPUBFileNotFoundError
from epub_utils.exceptions import InvalidEPUBError
from epub_utils.navigation import EPUBNavDocNavigation, Navigation, NCXNavigation
from epub_utils.package import Package


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

		Raises:
		    InvalidEPUBError: If the file is not a valid EPUB archive.
		"""
		self.path: Path = Path(path)

		if not self.path.exists():
			raise InvalidEPUBError(
				f'EPUB file does not exist: {self.path}',
				suggestions=[
					'Check that the file path is correct',
					'Verify the file has not been moved or deleted',
				],
				file_path=str(self.path),
			)

		if not zipfile.is_zipfile(self.path):
			raise InvalidEPUBError(
				f'File is not a valid ZIP archive: {self.path}',
				suggestions=[
					'Ensure the file is a valid EPUB (which is a ZIP archive)',
					'Check that the file is not corrupted',
					'Verify the file extension is .epub',
				],
				file_path=str(self.path),
			)

		self._container: Container = None
		self._package: Package = None

		self._toc: Navigation = None
		self._ncx: NCXNavigation = None
		self._nav: EPUBNavDocNavigation = None

	def _read_file_from_epub(self, file_path: str) -> str:
		"""
		Read and decode a file from the EPUB archive.

		Args:
		    file_path (str): Path to the file within the EPUB archive.

		Returns:
		    str: Decoded contents of the file.

		Raises:
		    EPUBFileNotFoundError: If the file is missing from the EPUB archive.
		"""
		with zipfile.ZipFile(self.path, 'r') as epub_zip:
			norm_namelist = {os.path.normpath(name): name for name in epub_zip.namelist()}
			norm_path = os.path.normpath(file_path)

			if norm_path not in norm_namelist:
				available_files = sorted(norm_namelist.keys())[:10]  # Show first 10 files
				suggestions = [
					'Check that the file path is correct',
					'Verify the EPUB file structure is complete',
				]
				if available_files:
					file_list = ', '.join(available_files)
					if len(norm_namelist) > 10:
						file_list += f' (and {len(norm_namelist) - 10} more)'
					suggestions.append(f'Available files include: {file_list}')

				raise EPUBFileNotFoundError(
					file_path, epub_path=str(self.path), suggestions=suggestions
				)

			try:
				return epub_zip.read(norm_namelist[norm_path]).decode('utf-8')
			except UnicodeDecodeError as e:
				raise InvalidEPUBError(
					f"Cannot decode file '{file_path}' as UTF-8",
					suggestions=[
						'Check that the file contains valid UTF-8 text',
						'Verify the EPUB file is not corrupted',
						'Ensure the file is a text-based format (XML, HTML, etc.)',
					],
					file_path=str(self.path),
				) from e

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
	def package_href(self):
		return os.path.dirname(self.container.rootfile_path)

	@property
	def toc(self) -> Optional[Navigation]:
		if self._toc is None:
			if self.nav is not None:
				# Default to newer EPUB3 Navigation Document when available
				self._toc = self.nav
			elif self.ncx is not None:
				self._toc = self.ncx

		return self._toc

	@property
	def ncx(self) -> Optional[NCXNavigation]:
		"""Access the Navigation Control eXtended (EPUB 2)"""
		if self._ncx is None:
			package = self.package

			if not package.toc_href:
				return None

			toc_href = package.toc_href
			toc_path = os.path.join(self.package_href, toc_href)
			toc_xml_content = self._read_file_from_epub(toc_path)

			self._ncx = NCXNavigation(toc_xml_content)

		return self._ncx

	@property
	def nav(self) -> Optional[EPUBNavDocNavigation]:
		"""Access the Navigation Document (EPUB 3)."""
		if self._nav is None:
			package = self.package

			if not package.nav_href:
				return None

			nav_href = package.nav_href
			nav_path = os.path.join(self.package_href, nav_href)
			nav_xml_content = self._read_file_from_epub(nav_path)

			self._nav = EPUBNavDocNavigation(nav_xml_content)

		return self._nav

	def find_content_by_id(self, item_id: str) -> str:
		"""
		Find and return content by its manifest item ID.

		Args:
		    item_id: The ID of the item in the manifest.

		Returns:
		    XHTMLContent: The content object for the specified item.

		Raises:
		    EPUBFileNotFoundError: If the item ID is not found in spine or manifest.
		"""
		spine_item = self.package.spine.find_by_idref(item_id)
		if not spine_item:
			spine_ids = [
				item.get('idref') for item in self.package.spine.itemrefs if item.get('idref')
			]
			suggestions = [
				'Check that the item ID is correct',
				'Verify the item is included in the spine',
			]
			if spine_ids:
				available_ids = ', '.join(spine_ids[:5])
				if len(spine_ids) > 5:
					available_ids += f' (and {len(spine_ids) - 5} more)'
				suggestions.append(f'Available spine IDs: {available_ids}')

			raise EPUBFileNotFoundError(
				f"spine item '{item_id}'", epub_path=str(self.path), suggestions=suggestions
			)

		manifest_item = self.package.manifest.find_by_id(item_id)
		if not manifest_item:
			manifest_ids = [
				item.get('id') for item in self.package.manifest.items if item.get('id')
			]
			suggestions = [
				'Check that the item ID is correct',
				'Verify the item is declared in the manifest',
			]
			if manifest_ids:
				available_ids = ', '.join(manifest_ids[:5])
				if len(manifest_ids) > 5:
					available_ids += f' (and {len(manifest_ids) - 5} more)'
				suggestions.append(f'Available manifest IDs: {available_ids}')

			raise EPUBFileNotFoundError(
				f"manifest item '{item_id}'", epub_path=str(self.path), suggestions=suggestions
			)

		content_path = os.path.join(self.package_href, manifest_item['href'])
		xml_content = self._read_file_from_epub(content_path)

		content = XHTMLContent(xml_content, manifest_item['media_type'], manifest_item['href'])

		return content

	def find_pub_resource_by_id(self, item_id: str) -> str:
		"""
		Find and return a publication resource by its manifest item ID.

		Args:
		    item_id: The ID of the item in the manifest.

		Returns:
		    str: The raw content of the resource.

		Raises:
		    EPUBFileNotFoundError: If the item ID is not found in manifest.
		"""
		manifest_item = self.package.manifest.find_by_id(item_id)
		if not manifest_item:
			manifest_ids = [
				item.get('id') for item in self.package.manifest.items if item.get('id')
			]
			suggestions = [
				'Check that the item ID is correct',
				'Verify the item is declared in the manifest',
			]
			if manifest_ids:
				available_ids = ', '.join(manifest_ids[:5])
				if len(manifest_ids) > 5:
					available_ids += f' (and {len(manifest_ids) - 5} more)'
				suggestions.append(f'Available manifest IDs: {available_ids}')

			raise EPUBFileNotFoundError(
				f"manifest item '{item_id}'", epub_path=str(self.path), suggestions=suggestions
			)

		content_path = os.path.join(self.package_href, manifest_item['href'])
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
					manifest_path = os.path.join(self._Documentpackage_href, item['href'])
					if os.path.normpath(manifest_path) == os.path.normpath(file_path):
						media_type = item.get('media_type', 'application/xhtml+xml')
						break
			except:
				pass

			return XHTMLContent(file_content, media_type, file_path)
		else:
			return file_content
