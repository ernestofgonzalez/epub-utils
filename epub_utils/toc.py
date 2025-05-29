from epub_utils.printers import highlight_xml, pretty_print_xml


class TableOfContents:
	"""
	Represents the Table of Contents (ToC) of an EPUB document.
	"""

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

	def to_xml(self, highlight_syntax=True, pretty_print=False) -> str:
		xml_content = self.xml_content

		if pretty_print:
			xml_content = pretty_print_xml(xml_content)

		if highlight_syntax:
			xml_content = highlight_xml(xml_content)

		return xml_content

	def _parse(self, xml_content: str) -> None:
		"""
		Parses the ToC XML content.

		Args:
		    xml_content (str): The raw XML content of the ToC file.

		Raises:
		    ParseError: If the XML is invalid or cannot be parsed.
		"""
		pass  # Implementation to be added later
