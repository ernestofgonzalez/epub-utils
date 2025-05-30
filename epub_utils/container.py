"""
Open Container Format: https://www.w3.org/TR/epub/#sec-ocf

This file includes the `Container` class, which is responsible for parsing the `container.xml` file
of an EPUB archive. The `container.xml` file is a required component of the EPUB Open Container
Format (OCF) and is located in the `META-INF` directory of the EPUB archive.

The `container.xml` file serves as the entry point for identifying the package document(s)
within the EPUB container. It must conform to the following structure as defined in the EPUB
specification:

- The root element is `<container>` and must include the `version` attribute with the value "1.0".
- The `<container>` element must contain exactly one `<rootfiles>` child element.
- The `<rootfiles>` element must contain one or more `<rootfile>` child elements.
- Each `<rootfile>` element must include a `full-path` attribute that specifies the location of
  the package document relative to the root of the EPUB container.

Namespace:
- All elements in the `container.xml` file are in the namespace
  `urn:oasis:names:tc:opendocument:xmlns:container`.

For more details on the structure and requirements of the `container.xml` file, refer to the
EPUB specification: https://www.w3.org/TR/epub/#sec-ocf
"""

try:
	from lxml import etree
except ImportError:
	import xml.etree.ElementTree as etree

from epub_utils.exceptions import ParseError
from epub_utils.printers import XMLPrinter


class Container:
	"""
	Represents the parsed container.xml file of an EPUB.

	Attributes:
	    xml_content (str): The raw XML content of the container.xml file.
	    rootfile_path (str): The path to the rootfile specified in the container.
	"""

	NAMESPACE = 'urn:oasis:names:tc:opendocument:xmlns:container'
	ROOTFILE_XPATH = f'.//{{{NAMESPACE}}}rootfile'

	def __init__(self, xml_content: str) -> None:
		"""
		Initialize the Container by parsing the container.xml data.

		Args:
		    xml_content (str): The raw XML content of the container.xml file.
		"""
		self.xml_content = xml_content
		self.rootfile_path: str = None

		self._parse(xml_content)

		self._printer = XMLPrinter(self)

	def __str__(self) -> str:
		return self.xml_content

	def to_str(self, *args, **kwargs) -> str:
		return self._printer.to_str(*args, **kwargs)

	def to_xml(self, *args, **kwargs) -> str:
		return self._printer.to_xml(*args, **kwargs)

	def _find_rootfile_element(self, root: etree.Element) -> etree.Element:
		"""
		Finds the rootfile element in the container.xml data.

		Args:
		    root (etree.Element): The root element of the parsed XML.

		Returns:
		    etree.Element: The rootfile element.

		Raises:
		    ValueError: If the rootfile element or its 'full-path' attribute is missing.
		"""
		rootfile_element = root.find(self.ROOTFILE_XPATH)
		if rootfile_element is None or 'full-path' not in rootfile_element.attrib:
			raise ValueError(
				'Invalid container.xml: Missing rootfile element or full-path attribute.'
			)
		return rootfile_element

	def _parse(self, xml_content: str) -> None:
		"""
		Parses the container.xml data to extract the rootfile path.

		Args:
		    xml_content (str): The raw XML content of the container.xml file.

		Raises:
		    ParseError: If the XML is invalid or cannot be parsed.
		"""
		try:
			if isinstance(xml_content, str):
				xml_content = xml_content.encode('utf-8')
			root = etree.fromstring(xml_content)
			rootfile_element = self._find_rootfile_element(root)
			self.rootfile_path = rootfile_element.attrib['full-path']
			if not self.rootfile_path.strip():
				raise ValueError("Invalid container.xml: 'full-path' attribute is empty.")
		except etree.ParseError as e:
			raise ParseError(f'Error parsing container.xml: {e}')
