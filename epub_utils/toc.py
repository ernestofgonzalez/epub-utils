try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from epub_utils.exceptions import ParseError
from epub_utils.highlighters import highlight_xml


class TableOfContents:
    """
    Represents the Table of Contents (ToC) of an EPUB document.
    """

    NCX_NAMESPACE = "http://www.daisy.org/z3986/2005/ncx/"
    XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
    EPUB_NAMESPACE = "http://www.idpf.org/2007/ops"

    def __init__(self, xml_content: str) -> None:
        """
        Initialize the TableOfContents by parsing the NCX or Nav document.

        Args:
            xml_content (str): The raw XML content of the ToC file.
        """
        self.xml_content = xml_content
        self._parse(xml_content)

    def __str__(self) -> str:
        return self.xml_content

    def to_str(self) -> str:
        return str(self)

    def to_xml(self, highlight_syntax=True) -> str:
        return highlight_xml(self.xml_content)
    
    def to_dict(self, flat: bool = False) -> dict:
        pass

    def to_list(self, flat: bool = False) -> list:
        return self.toc

    def _parse(self, xml_content: str) -> None:
        """
        Parses the ToC XML content.

        Args:
            xml_content (str): The raw XML content of the ToC file.

        Raises:
            ParseError: If the XML is invalid or cannot be parsed.
        """
        try:
            if isinstance(xml_content, str):
                xml_content = xml_content.encode("utf-8")
            root = etree.fromstring(xml_content)
            
            items = None
            if root.tag.endswith('ncx'): # Navigation control
                items = self._parse_ncx(root)
            elif root.tag.endswith('html'): # Navigation document or regular content document including a ToC
                items = self._parse_nav(root)
            
            self.items = items
            
        except etree.ParseError as e:
            raise ParseError(f"Error parsing TOC file: {e}")

    def _parse_ncx(self, root: etree.Element) -> list:
        """Parse NCX navigation control file."""
        nav_map = root.find(f'.//{{{self.NCX_NAMESPACE}}}navMap')
        
        # TODO

    def _parse_nav(self, root: etree.Element) -> list:
        """Parse EPUB3 Navigation Document."""
        ns = root.nsmap.get(None, self.XHTML_NAMESPACE)
        epub_ns = root.nsmap.get('epub', self.EPUB_NAMESPACE)
        
        toc_nav = root.find(f'.//{{{ns}}}nav[@{{{epub_ns}}}type="toc"]', 
                          namespaces={'epub': epub_ns})
        if toc_nav is None:
            toc_nav = root.find('.//nav[@epub:type="toc"]',
                             namespaces={'epub': epub_ns})
        if toc_nav is None:
            toc_nav = root.find(f'.//{{{ns}}}body')
            if toc_nav is None:
                toc_nav = root.find('.//body')
        
        # TODO
