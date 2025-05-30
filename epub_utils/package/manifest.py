try:
	from lxml import etree
except ImportError:
	import xml.etree.ElementTree as etree

from epub_utils.exceptions import ParseError
from epub_utils.printers import XMLPrinter


class Manifest:
	"""
	Represents the manifest section of an EPUB package document.
	The manifest element provides an exhaustive list of the publication resources.
	"""

	NAMESPACE = 'http://www.idpf.org/2007/opf'
	ITEM_XPATH = f'.//{{{NAMESPACE}}}item'

	def __init__(self, xml_content: str):
		self.xml_content = xml_content
		self.items = []

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
		Parses the manifest XML content.
		"""
		try:
			if isinstance(xml_content, str):
				xml_content = xml_content.encode('utf-8')
			root = etree.fromstring(xml_content)

			for item in root.findall(self.ITEM_XPATH):
				item_data = {
					'id': item.get('id'),
					'href': item.get('href'),
					'media_type': item.get('media-type'),
					'properties': item.get('properties', '').split(),
				}
				if all(
					v is not None
					for v in [item_data['id'], item_data['href'], item_data['media_type']]
				):
					self.items.append(item_data)

		except etree.ParseError as e:
			raise ParseError(f'Error parsing manifest element: {e}')

	def find_by_property(self, property_name: str) -> dict:
		"""Find the first item with the given property."""
		for item in self.items:
			if property_name in item['properties']:
				return item
		return None

	def find_by_id(self, item_id: str) -> dict:
		"""Find an item by its ID."""
		for item in self.items:
			if item['id'] == item_id:
				return item
		return None

	def find_by_media_type(self, media_type: str) -> list:
		"""Find all items with the given media type."""
		return [item for item in self.items if item['media_type'] == media_type]
