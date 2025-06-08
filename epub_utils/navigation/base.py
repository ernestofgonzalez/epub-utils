class Navigation:
	"""
	Base class for Navigation Documents.

	Attributes:
	    media_type (str): The MIME type of the content.
	    href (str): The path to the content file within the EPUB.
	"""

	def __init__(self, media_type: str, href: str) -> None:
		self.media_type = media_type
		self.href = href
