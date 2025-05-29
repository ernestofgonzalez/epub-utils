try:
	from lxml import etree
except ImportError:
	import xml.etree.ElementTree as etree

from epub_utils.exceptions import ParseError
from epub_utils.printers import highlight_xml


class Spine:
	"""
	Represents the spine section of an EPUB package document.
	The spine element defines the default reading order of the content.
	"""

	NAMESPACE = 'http://www.idpf.org/2007/opf'
	ITEMREF_XPATH = f'.//{{{NAMESPACE}}}itemref'

	def __init__(self, xml_content: str):
		self.xml_content = xml_content
		self.itemrefs = []
		self.toc = None
		self.page_progression_direction = None
		self._parse(xml_content)

	def __str__(self) -> str:
		return self.xml_content

	def to_str(self) -> str:
		return str(self)

	def to_xml(self, highlight_syntax=True, pretty_print=False) -> str:
		xml_content = self.xml_content

		if pretty_print:
			from epub_utils.printers import pretty_print_xml

			xml_content = pretty_print_xml(xml_content)

		if highlight_syntax:
			from epub_utils.printers import highlight_xml

			xml_content = highlight_xml(xml_content)

		return xml_content

	def _parse(self, xml_content: str) -> None:
		"""
		Parses the spine XML content.
		"""
		try:
			if isinstance(xml_content, str):
				xml_content = xml_content.encode('utf-8')
			root = etree.fromstring(xml_content)

			self.toc = root.get('toc')
			self.page_progression_direction = root.get('page-progression-direction', 'default')

			for itemref in root.findall(self.ITEMREF_XPATH):
				idref = itemref.get('idref')
				linear = itemref.get('linear', 'yes')
				properties = itemref.get('properties', '').split()

				if idref:
					self.itemrefs.append(
						{'idref': idref, 'linear': linear == 'yes', 'properties': properties}
					)

		except etree.ParseError as e:
			raise ParseError(f'Error parsing spine element: {e}')

	def find_by_idref(self, itemref_idref: str) -> dict:
		"""Find an itemref by its idref."""
		for item in self.itemrefs:
			if item['idref'] == itemref_idref:
				return item
		return None
