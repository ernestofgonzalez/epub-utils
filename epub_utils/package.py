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

from epub_utils.exceptions import ParseError
from epub_utils.highlighters import highlight_xml


class Package:
    """
    Represents the parsed OPF package file of an EPUB.

    Attributes:
        xml_content (str): The raw XML content of the OPF package file.
    """

    NAMESPACE = "http://www.idpf.org/2007/opf"
    DC_NAMESPACE = "http://purl.org/dc/elements/1.1/"
    METADATA_XPATH = f".//{{{NAMESPACE}}}metadata"
    TITLE_XPATH = f".//{{{DC_NAMESPACE}}}title"
    CREATOR_XPATH = f".//{{{DC_NAMESPACE}}}creator"
    IDENTIFIER_XPATH = f".//{{{DC_NAMESPACE}}}identifier"

    def __init__(self, xml_content: str) -> None:
        """
        Initialize the Package by parsing the OPF package file.

        Args:
            xml_content (str): The raw XML content of the OPF package file.
        """
        self.xml_content = xml_content
        self._parse(xml_content)

    def __str__(self) -> str:
        return self.xml_content
    
    def tostring(self) -> str:
        return str(self)

    def toxml(self, highlight_syntax=True) -> str:
        return highlight_xml(self.xml_content)

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
                xml_content = xml_content.encode("utf-8")
            root = etree.fromstring(xml_content)
            metadata = root.find(self.METADATA_XPATH)
            if metadata is None:
                raise ValueError("Invalid OPF file: Missing metadata element.")

            self.title = self._get_text(metadata, self.TITLE_XPATH)
            self.author = self._get_text(metadata, self.CREATOR_XPATH)
            self.identifier = self._get_text(metadata, self.IDENTIFIER_XPATH)

            if not self.identifier:
                raise ValueError("Invalid OPF file: Missing identifier.")
        except etree.ParseError as e:
            raise ParseError(f"Error parsing OPF file: {e}")

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
