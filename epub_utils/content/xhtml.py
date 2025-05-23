from epub_utils.content.base import Content
from epub_utils.highlighters import highlight_xml


class XHTMLContent(Content):
	"""
	Represents an XHTML content document within an EPUB file.
	"""

	MEDIA_TYPES = ['application/xhtml+xml', 'text/html']

	def __init__(self, xml_content: str, media_type: str, href: str) -> None:
		self.xml_content = xml_content

		if media_type not in self.MEDIA_TYPES:
			raise ValueError(f'Invalid media type for XHTML content: {media_type}')
		super().__init__(media_type, href)

	def __str__(self) -> str:
		return self.xml_content

	def to_str(self) -> str:
		return str(self)

	def to_xml(self, highlight_syntax=True) -> str:
		return highlight_xml(self.xml_content)

	def _parse(self, xml_content: str) -> None:
		raise NotImplementedError
