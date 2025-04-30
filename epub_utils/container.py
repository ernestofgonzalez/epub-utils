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

This implementation uses the `lxml` library for XML parsing, falling back to Python's built-in 
`xml.etree.ElementTree` if `lxml` is unavailable.

Classes:
- `ContainerParseError`: A custom exception raised for errors encountered while parsing the 
  `container.xml` file.
- `Container`: Represents the parsed `container.xml` file and provides access to the `full-path` 
  attribute of the `<rootfile>` element.

Attributes:
- `NAMESPACE`: The XML namespace for the `container.xml` file.
- `ROOTFILE_XPATH`: The XPath expression to locate the `<rootfile>` element.

Methods:
- `__init__`: Initializes the `Container` object by parsing the raw XML content of the `container.xml` file.
- `_find_rootfile_element`: Locates the `<rootfile>` element and validates its `full-path` attribute.
- `_parse`: Parses the XML content and extracts the `full-path` attribute of the `<rootfile>` element.

For more details on the structure and requirements of the `container.xml` file, refer to the 
EPUB specification: https://www.w3.org/TR/epub/#sec-ocf
"""

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree


class ContainerParseError(Exception):
    """Custom exception for errors in parsing container.xml."""
    pass



class Container:
    """
    Represents the parsed container.xml file of an EPUB.

    Attributes:
        rootfile_path (str): The path to the rootfile specified in the container.
    """

    NAMESPACE = "urn:oasis:names:tc:opendocument:xmlns:container"
    ROOTFILE_XPATH = f".//{{{NAMESPACE}}}rootfile"

    def __init__(self, xml_content: str) -> None:
        """
        Initialize the Container by parsing the container.xml data.

        Args:
            xml_content (str): The raw XML content of the container.xml file.
        """
        self.rootfile_path: str = None
        self._parse(xml_content)

    def _find_rootfile_element(self, root: etree.Element) -> etree.Element:
        """
        Finds the rootfile element in the container.xml data.

        Args:
            root (etree.Element): The root element of the parsed XML.

        Returns:
            etree.Element: The rootfile element.

        Raises:
            ContainerParseError: If the rootfile element or its 'full-path' attribute is missing.
        """
        rootfile_element = root.find(self.ROOTFILE_XPATH)
        if rootfile_element is None or "full-path" not in rootfile_element.attrib:
            raise ContainerParseError("Invalid container.xml: Missing rootfile element or full-path attribute.")
        return rootfile_element


    def _parse(self, xml_content: str) -> None:
        """
        Parses the container.xml data to extract the rootfile path.

        Args:
            xml_content (str): The raw XML content of the container.xml file.

        Raises:
            ContainerParseError: If the XML is invalid or cannot be parsed.
        """
        try:
            root = etree.fromstring(xml_content)
            rootfile_element = self._find_rootfile_element(root)
            self.rootfile_path = rootfile_element.attrib["full-path"]
            if not self.rootfile_path.strip():
                raise ContainerParseError("Invalid container.xml: 'full-path' attribute is empty.")
        except etree.ParseError as e:
            raise ContainerParseError(f"Error parsing container.xml: {e}")
