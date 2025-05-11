from typing import Optional
from typing import TypedDict

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree


from epub_utils.exceptions import ParseError
from epub_utils.highlighters import highlight_xml


class TocEntry(TypedDict):
    path: str
    label: Optional[str]


class TableOfContents:
    """
    Represents the Table of Contents (ToC) of an EPUB document.
    """

    def __init__(self, xml_content: str, major_version: int) -> None:
        """
        Initialize the TableOfContents by parsing the NCX or Nav document.

        Args:
            xml_content (str): The raw XML content of the ToC file.
        """
        self.xml_content = xml_content

        if major_version == 3:
            self._entries = self._parse_nav(xml_content)
        else:
            self._entries = self._parse_ncx(xml_content)

    def __str__(self) -> str:
        return self.xml_content

    def __iter__(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)

    def to_str(self) -> str:
        return str(self)

    def to_xml(self, highlight_syntax=True) -> str:
        return highlight_xml(self.xml_content)

    def _parse_ncx(self, xml_content: str) -> list[TocEntry]:
        root = etree.fromstring(xml_content.encode("utf-8"))
        namespaces = {"ncx":root.nsmap[None]}

        entries = []
        elements = root.xpath("//ncx:navPoint", namespaces=namespaces)
        for element in elements:
            content_elements = element.xpath("./ncx:content", namespaces=namespaces)
            label_elements = element.xpath("./ncx:navLabel/ncx:text", namespaces=namespaces)
            entries.append({
                "path": content_elements[0].get("src") if content_elements else None,
                "label":label_elements[0].text if label_elements else None,

            })

        return entries

    def _parse_nav(self, xml_content: str) -> list[TocEntry]:
        root = etree.fromstring(xml_content.encode("utf-8"))
        namespaces = {"xhtml":root.nsmap[None], "epub": root.nsmap["epub"]}
        elements = root.xpath("//xhtml:nav[@epub:type=\"toc\"]", namespaces=namespaces)

        return [
            {"path": element.attrib["href"], "label": element.text}
            for element in root.xpath("//xhtml:nav[@epub:type=\"toc\"]/xhtml:ol/xhtml:li/xhtml:a", namespaces=namespaces)
        ]
