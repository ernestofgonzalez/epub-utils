"""
Open Packaging Format (OPF): https://www.w3.org/TR/epub/#sec-package-doc

This file includes the `Package` class, which is responsible for parsing the OPF package file
of an EPUB archive. The OPF file contains metadata, manifest, spine, and guide information
about the EPUB content.

Namespace:
- The OPF file uses the namespace `http://www.idpf.org/2007/opf`.

For more details on the structure and requirements of the OPF file, refer to the
EPUB specification: https://www.w3.org/TR/epub/#sec-package-doc
"""

try:
	from lxml import etree
except ImportError:
	import xml.etree.ElementTree as etree

import packaging.version

from epub_utils.exceptions import ParseError
from epub_utils.package.manifest import Manifest
from epub_utils.package.metadata import Metadata
from epub_utils.package.spine import Spine
from epub_utils.printers import XMLPrinter


class Package:
	"""
	Represents the parsed OPF package file of an EPUB.

	Attributes:
	    xml_content (str): The raw XML content of the OPF package file.
	    metadata (dict): The metadata section of the OPF file.
	    manifest (dict): The manifest section listing all resources.
	    spine (list): The spine section defining the reading order.
	    guide (dict): The guide section with navigation references.
	    cover (str): The cover image resource ID.
	    toc (str): The table of contents resource ID.
	    nav (str): The navigation document resource ID.
	"""

	NAMESPACE = 'http://www.idpf.org/2007/opf'
	DC_NAMESPACE = 'http://purl.org/dc/elements/1.1/'
	METADATA_XPATH = f'.//{{{NAMESPACE}}}metadata'
	SPINE_XPATH = f'.//{{{NAMESPACE}}}spine'
	MANIFEST_XPATH = f'.//{{{NAMESPACE}}}manifest'
	ITEM_XPATH = f'.//{{{NAMESPACE}}}item'
	NCX_MEDIA_TYPE = 'application/x-dtbncx+xml'
	TITLE_XPATH = f'.//{{{DC_NAMESPACE}}}title'
	CREATOR_XPATH = f'.//{{{DC_NAMESPACE}}}creator'
	IDENTIFIER_XPATH = f'.//{{{DC_NAMESPACE}}}identifier'

	def __init__(self, xml_content: str) -> None:
		"""
		Initialize the Package by parsing the OPF package file.

		Args:
		    xml_content (str): The raw XML content of the OPF package file.
		"""
		self.xml_content = xml_content

		self.metadata = None
		self.manifest = None
		self.spine = None
		self.guide = None
		self.cover = None
		self.toc_href = None
		self.nav_href = None
		self.version = None

		self._parse(xml_content)

		self._printer = XMLPrinter(self)

	def __str__(self) -> str:
		return self.xml_content

	def to_str(self, *args, **kwargs) -> str:
		return self._printer.to_str(*args, **kwargs)

	def to_xml(self, *args, **kwargs) -> str:
		return self._printer.to_xml(*args, **kwargs)

	def _parse(self, xml_content: str) -> None:
		"""
		Parses the OPF package file to extract metadata.

		Args:
		    xml_content (str): The raw XML content of the OPF package file.

		Raises:
		    ParseError: If the XML is invalid or cannot be parsed.
		"""
		try:
			if isinstance(xml_content, str):
				xml_content = xml_content.encode('utf-8')
			root = etree.fromstring(xml_content)
			self.version = self._parse_version(root.attrib['version'])

			# Parse metadata
			metadata_el = root.find(self.METADATA_XPATH)
			if metadata_el is None:
				raise ValueError('Invalid OPF file: Missing metadata element.')
			metadata_xml = etree.tostring(metadata_el, encoding='unicode')
			self.metadata = Metadata(metadata_xml)

			# Parse manifest
			manifest_el = root.find(self.MANIFEST_XPATH)
			if manifest_el is not None:
				manifest_xml = etree.tostring(manifest_el, encoding='unicode')
				self.manifest = Manifest(manifest_xml)

			# Parse spine
			spine_el = root.find(self.SPINE_XPATH)
			if spine_el is not None:
				spine_xml = etree.tostring(spine_el, encoding='unicode')
				self.spine = Spine(spine_xml)

			# Parse TOC references
			if self.version.major == 3:
				self.nav_href = self._find_nav_href(root)
			else:
				self.toc_href = self._find_toc_href(root)

		except etree.ParseError as e:
			raise ParseError(f'Error parsing OPF file: {e}')

	def _get_text(self, root: etree.Element, xpath: str) -> str:
		"""
		Helper method to extract text content from an XML element.

		Args:
		    root (etree.Element): The root element to search within.
		    xpath (str): The XPath expression to locate the element.

		Returns:
		    str: The text content of the element, or None if not found.
		"""
		element = root.find(xpath)
		return element.text.strip() if element is not None and element.text else None

	def _find_toc_href(self, root: etree.Element) -> str:
		"""
		Find the publication navigation control file.

		Args:
		    root (etree.Element): The root element of the OPF document.

		Returns:
		    str: The href to the NCX document, or None if not found.
		"""
		# First check for NCX media-type in manifest
		for item in root.findall(self.ITEM_XPATH):
			if item.get('media-type') == self.NCX_MEDIA_TYPE:
				return item.get('href')

		# Then check spine toc attribute
		spine = root.find(self.SPINE_XPATH)
		if spine is not None:
			toc_id = spine.get('toc')
			if toc_id:
				for item in root.findall(self.ITEM_XPATH):
					if item.get('id') == toc_id:
						href = item.get('href')
						if href:
							# Remove fragment identifier if present
							return href.split('#')[0]

		return None

	def _find_nav_href(self, root: etree.Element) -> str:
		"""
		Find the publication navigation file.

		Args:
		    root (etree.Element): The root element of the OPF document.

		Returns:
		    str: The href to navigation file, or None if not found.
		"""
		# Check for item with nav properties
		for item in root.findall(self.ITEM_XPATH):
			if item.get('properties') == 'nav':
				href = item.get('href')
				if href:
					return href.split('#')[0]

		# Fall back to guide TOC reference
		guide = root.find(f'.//{{{self.NAMESPACE}}}guide')
		if guide is not None:
			for reference in guide.findall(f'.//{{{self.NAMESPACE}}}reference'):
				if reference.get('type') == 'toc':
					href = reference.get('href')
					if href:
						return href.split('#')[0]

		return None

	def _parse_version(self, version):
		version = packaging.version.Version(version)
		if version.major not in (1, 2, 3):
			raise ValueError(f'Unsupported epub version: {version.major}')
		return version
