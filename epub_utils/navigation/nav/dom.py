"""DOM classes for structured access to EPUB 3 Navigation Documents."""

from typing import List, Optional

from lxml import etree


class NavElement:
	"""Base class for navigation document elements."""

	def __init__(self, element: etree.Element) -> None:
		self.element = element

	@property
	def id(self) -> Optional[str]:
		"""Get the id attribute."""
		return self.element.get('id')

	@id.setter
	def id(self, value: str) -> None:
		"""Set the id attribute."""
		self.element.set('id', value)


class NavAnchor(NavElement):
	"""Represents an anchor element (a) in navigation."""

	@property
	def href(self) -> Optional[str]:
		"""Get the href attribute."""
		return self.element.get('href')

	@href.setter
	def href(self, value: str) -> None:
		"""Set the href attribute."""
		self.element.set('href', value)

	@property
	def text(self) -> str:
		"""Get the text content of the anchor."""
		return self.element.text or ''

	@text.setter
	def text(self, value: str) -> None:
		"""Set the text content of the anchor."""
		self.element.text = value

	@property
	def epub_type(self) -> Optional[str]:
		"""Get the epub:type attribute."""
		return self.element.get('{http://www.idpf.org/2007/ops}type')

	@epub_type.setter
	def epub_type(self, value: str) -> None:
		"""Set the epub:type attribute."""
		self.element.set('{http://www.idpf.org/2007/ops}type', value)


class NavListItem(NavElement):
	"""Represents a list item (li) in navigation."""

	@property
	def anchor(self) -> Optional[NavAnchor]:
		"""Get the first anchor child element."""
		anchors = self.element.xpath(
			'./xhtml:a', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		if anchors:
			return NavAnchor(anchors[0])
		return None

	@property
	def nested_list(self) -> Optional['NavList']:
		"""Get nested ordered list if present."""
		lists = self.element.xpath(
			'./xhtml:ol', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		if lists:
			return NavList(lists[0])
		return None

	@property
	def span(self) -> Optional[NavElement]:
		"""Get span element if present (for non-linked text)."""
		spans = self.element.xpath(
			'./xhtml:span', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		if spans:
			return NavElement(spans[0])
		return None

	def add_anchor(self, href: str, text: str, epub_type: Optional[str] = None) -> NavAnchor:
		"""Add an anchor element to this list item."""
		anchor_element = etree.SubElement(self.element, '{http://www.w3.org/1999/xhtml}a')
		anchor = NavAnchor(anchor_element)
		anchor.href = href
		anchor.text = text
		if epub_type:
			anchor.epub_type = epub_type
		return anchor

	def add_span(self, text: str) -> NavElement:
		"""Add a span element to this list item."""
		span_element = etree.SubElement(self.element, '{http://www.w3.org/1999/xhtml}span')
		span = NavElement(span_element)
		span.element.text = text
		return span

	def add_nested_list(self) -> 'NavList':
		"""Add a nested ordered list to this list item."""
		ol_element = etree.SubElement(self.element, '{http://www.w3.org/1999/xhtml}ol')
		return NavList(ol_element)


class NavList(NavElement):
	"""Represents an ordered list (ol) in navigation."""

	@property
	def list_items(self) -> List[NavListItem]:
		"""Get all list item children."""
		items = self.element.xpath(
			'./xhtml:li', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		return [NavListItem(item) for item in items]

	def add_list_item(self) -> NavListItem:
		"""Add a new list item to this list."""
		li_element = etree.SubElement(self.element, '{http://www.w3.org/1999/xhtml}li')
		return NavListItem(li_element)

	def get_all_items_recursive(self) -> List[NavListItem]:
		"""Get all list items recursively."""
		items = []

		def collect_items(nav_list: NavList):
			for item in nav_list.list_items:
				items.append(item)
				nested_list = item.nested_list
				if nested_list:
					collect_items(nested_list)

		collect_items(self)
		return items


class NavSection(NavElement):
	"""Represents a nav element with specific epub:type."""

	@property
	def epub_type(self) -> Optional[str]:
		"""Get the epub:type attribute."""
		return self.element.get('{http://www.idpf.org/2007/ops}type')

	@epub_type.setter
	def epub_type(self, value: str) -> None:
		"""Set the epub:type attribute."""
		self.element.set('{http://www.idpf.org/2007/ops}type', value)

	@property
	def heading(self) -> Optional[str]:
		"""Get the text of the heading element (h1-h6)."""
		for level in range(1, 7):
			headings = self.element.xpath(
				f'./xhtml:h{level}', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
			)
			if headings:
				return headings[0].text or ''
		return None

	@property
	def ordered_list(self) -> Optional[NavList]:
		"""Get the ordered list child element."""
		lists = self.element.xpath(
			'./xhtml:ol', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		if lists:
			return NavList(lists[0])
		return None

	def add_heading(self, level: int, text: str) -> NavElement:
		"""Add a heading element."""
		if not 1 <= level <= 6:
			raise ValueError('Heading level must be between 1 and 6')

		heading_element = etree.SubElement(
			self.element, f'{{http://www.w3.org/1999/xhtml}}h{level}'
		)
		heading = NavElement(heading_element)
		heading.element.text = text
		return heading

	def add_ordered_list(self) -> NavList:
		"""Add an ordered list to this nav section."""
		ol_element = etree.SubElement(self.element, '{http://www.w3.org/1999/xhtml}ol')
		return NavList(ol_element)


class NavDocument(NavElement):
	"""Represents the root html element of a navigation document."""

	@property
	def toc_nav(self) -> Optional[NavSection]:
		"""Get the table of contents nav section."""
		navs = self.element.xpath(
			'.//xhtml:nav[@epub:type="toc"]',
			namespaces={
				'xhtml': 'http://www.w3.org/1999/xhtml',
				'epub': 'http://www.idpf.org/2007/ops',
			},
		)
		if navs:
			return NavSection(navs[0])
		return None

	@property
	def page_list_nav(self) -> Optional[NavSection]:
		"""Get the page list nav section."""
		navs = self.element.xpath(
			'.//xhtml:nav[@epub:type="page-list"]',
			namespaces={
				'xhtml': 'http://www.w3.org/1999/xhtml',
				'epub': 'http://www.idpf.org/2007/ops',
			},
		)
		if navs:
			return NavSection(navs[0])
		return None

	@property
	def landmarks_nav(self) -> Optional[NavSection]:
		"""Get the landmarks nav section."""
		navs = self.element.xpath(
			'.//xhtml:nav[@epub:type="landmarks"]',
			namespaces={
				'xhtml': 'http://www.w3.org/1999/xhtml',
				'epub': 'http://www.idpf.org/2007/ops',
			},
		)
		if navs:
			return NavSection(navs[0])
		return None

	@property
	def all_nav_sections(self) -> List[NavSection]:
		"""Get all nav sections."""
		navs = self.element.xpath(
			'.//xhtml:nav', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		return [NavSection(nav) for nav in navs]

	@property
	def title(self) -> str:
		"""Get the document title."""
		title_elements = self.element.xpath(
			'.//xhtml:title', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		return title_elements[0].text if title_elements else ''

	@property
	def body(self) -> Optional[NavElement]:
		"""Get the body element."""
		bodies = self.element.xpath(
			'.//xhtml:body', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)
		if bodies:
			return NavElement(bodies[0])
		return None

	def add_nav_section(self, epub_type: str) -> NavSection:
		"""Add a new nav section to the body."""
		body = self.body
		if not body:
			# Create body if it doesn't exist
			body_element = etree.SubElement(self.element, '{http://www.w3.org/1999/xhtml}body')
			body = NavElement(body_element)

		nav_element = etree.SubElement(body.element, '{http://www.w3.org/1999/xhtml}nav')
		nav_section = NavSection(nav_element)
		nav_section.epub_type = epub_type
		return nav_section
