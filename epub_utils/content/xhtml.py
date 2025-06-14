import re

from lxml import etree

from epub_utils.content.base import Content
from epub_utils.exceptions import ParseError, UnsupportedFormatError
from epub_utils.printers import XMLPrinter


class XHTMLContent(Content):
	"""
	Represents an XHTML content document within an EPUB file.
	"""

	MEDIA_TYPES = ['application/xhtml+xml', 'text/html']

	def __init__(self, xml_content: str, media_type: str, href: str) -> None:
		self.xml_content = xml_content

		self._tree = None

		if media_type not in self.MEDIA_TYPES:
			raise UnsupportedFormatError(
				f"Media type '{media_type}' is not supported for XHTML content",
				suggestions=[
					f'Use one of the supported media types: {", ".join(self.MEDIA_TYPES)}',
					'Check that this is an XHTML content file',
					'Verify the manifest declares the correct media type',
				],
			)
		super().__init__(media_type, href)

		self._parse(xml_content)

		self._printer = XMLPrinter(self)

	def __str__(self) -> str:
		return self.xml_content

	def to_str(self, *args, **kwargs) -> str:
		return self._printer.to_str(*args, **kwargs)

	def to_xml(self, *args, **kwargs) -> str:
		return self._printer.to_xml(*args, **kwargs)

	def to_plain(self) -> str:
		return self.inner_text

	def _parse(self, xml_content: str) -> None:
		try:
			self._tree = etree.fromstring(xml_content.encode('utf-8'))
		except etree.ParseError as e:
			raise ParseError(
				f'Invalid XML in XHTML content file: {str(e)}',
				suggestions=[
					'Check that the content file contains valid XHTML',
					'Verify the file is not corrupted',
					'Ensure all XML tags are properly closed',
					'Check for invalid characters in the XML',
				],
			) from e

	@property
	def tree(self):
		"""Lazily parse and cache the XHTML tree."""
		if self._tree is None:
			self._parse(self.xml_content)
		return self._tree

	@property
	def inner_text(self) -> str:
		tree = self.tree

		body_elements = tree.xpath('//*[local-name()="body"]')

		if body_elements:
			inner_text = ''.join(body_elements[0].itertext())
		else:
			inner_text = ''.join(tree.itertext())

		# Normalize whitespace
		inner_text = re.sub(r'\s+', ' ', inner_text).strip()

		return inner_text
