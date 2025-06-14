"""NCX DOM classes for structured access to NCX navigation documents."""

from typing import List, Optional

from lxml import etree


class NCXElement:
	"""Base class for NCX DOM elements."""

	def __init__(self, element: etree.Element):
		self.element = element

	@property
	def id(self) -> Optional[str]:
		"""Get the id attribute."""
		return self.element.get('id')

	@id.setter
	def id(self, value: str) -> None:
		"""Set the id attribute."""
		self.element.set('id', value)


class NCXText(NCXElement):
	"""Represents a text element."""

	@property
	def text(self) -> str:
		"""Get the text content."""
		return self.element.text or ''

	@text.setter
	def text(self, value: str) -> None:
		"""Set the text content."""
		self.element.text = value


class NCXContent(NCXElement):
	"""Represents a content element."""

	@property
	def src(self) -> Optional[str]:
		"""Get the src attribute."""
		return self.element.get('src')

	@src.setter
	def src(self, value: str) -> None:
		"""Set the src attribute."""
		self.element.set('src', value)


class NCXNavLabel(NCXElement):
	"""Represents a navLabel element."""

	@property
	def text_element(self) -> Optional[NCXText]:
		"""Get the text child element."""
		text_elements = self.element.xpath(
			'./ncx:text', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if text_elements:
			return NCXText(text_elements[0])
		return None

	@property
	def text(self) -> str:
		"""Get the text content."""
		text_elem = self.text_element
		return text_elem.text if text_elem else ''

	@text.setter
	def text(self, value: str) -> None:
		"""Set the text content."""
		text_elem = self.text_element
		if text_elem:
			text_elem.text = value
		else:
			# Create text element if it doesn't exist
			text_element = etree.SubElement(
				self.element, '{http://www.daisy.org/z3986/2005/ncx/}text'
			)
			text_element.text = value


class NCXNavPoint(NCXElement):
	"""Represents a navPoint element in the navigation hierarchy."""

	@property
	def class_attr(self) -> Optional[str]:
		"""Get the class attribute."""
		return self.element.get('class')

	@class_attr.setter
	def class_attr(self, value: str) -> None:
		"""Set the class attribute."""
		self.element.set('class', value)

	@property
	def play_order(self) -> Optional[int]:
		"""Get the playOrder attribute."""
		play_order = self.element.get('playOrder')
		return int(play_order) if play_order else None

	@play_order.setter
	def play_order(self, value: int) -> None:
		"""Set the playOrder attribute."""
		self.element.set('playOrder', str(value))

	@property
	def nav_label(self) -> Optional[NCXNavLabel]:
		"""Get the navLabel child element."""
		nav_labels = self.element.xpath(
			'./ncx:navLabel', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if nav_labels:
			return NCXNavLabel(nav_labels[0])
		return None

	@property
	def content(self) -> Optional[NCXContent]:
		"""Get the content child element."""
		content_elements = self.element.xpath(
			'./ncx:content', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if content_elements:
			return NCXContent(content_elements[0])
		return None

	@property
	def nav_points(self) -> List['NCXNavPoint']:
		"""Get child navPoint elements."""
		nav_point_elements = self.element.xpath(
			'./ncx:navPoint', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return [NCXNavPoint(point) for point in nav_point_elements]

	def add_nav_point(
		self,
		id: str,
		label_text: str,
		src: str,
		class_attr: Optional[str] = None,
		play_order: Optional[int] = None,
	) -> 'NCXNavPoint':
		"""Add a child navPoint element."""
		nav_point_element = etree.SubElement(
			self.element, '{http://www.daisy.org/z3986/2005/ncx/}navPoint'
		)
		nav_point = NCXNavPoint(nav_point_element)
		nav_point.id = id

		if class_attr:
			nav_point.class_attr = class_attr
		if play_order is not None:
			nav_point.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(
			nav_point_element, '{http://www.daisy.org/z3986/2005/ncx/}navLabel'
		)
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(
			nav_point_element, '{http://www.daisy.org/z3986/2005/ncx/}content'
		)
		content = NCXContent(content_element)
		content.src = src

		return nav_point

	@property
	def label_text(self) -> str:
		"""Get the text of the navLabel."""
		nav_label = self.nav_label
		return nav_label.text if nav_label else ''

	@property
	def content_src(self) -> str:
		"""Get the src of the content element."""
		content = self.content
		return content.src if content else ''


class NCXNavMap(NCXElement):
	"""Represents the navMap element."""

	@property
	def nav_points(self) -> List[NCXNavPoint]:
		"""Get all direct child navPoint elements."""
		nav_point_elements = self.element.xpath(
			'./ncx:navPoint', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return [NCXNavPoint(point) for point in nav_point_elements]

	def add_nav_point(
		self,
		id: str,
		label_text: str,
		src: str,
		class_attr: Optional[str] = None,
		play_order: Optional[int] = None,
	) -> NCXNavPoint:
		"""Add a navPoint element."""
		nav_point_element = etree.SubElement(
			self.element, '{http://www.daisy.org/z3986/2005/ncx/}navPoint'
		)
		nav_point = NCXNavPoint(nav_point_element)
		nav_point.id = id

		if class_attr:
			nav_point.class_attr = class_attr
		if play_order is not None:
			nav_point.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(
			nav_point_element, '{http://www.daisy.org/z3986/2005/ncx/}navLabel'
		)
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(
			nav_point_element, '{http://www.daisy.org/z3986/2005/ncx/}content'
		)
		content = NCXContent(content_element)
		content.src = src

		return nav_point

	def get_all_nav_points(self) -> List[NCXNavPoint]:
		"""Get all navPoint elements recursively."""
		nav_point_elements = self.element.xpath(
			'.//ncx:navPoint', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return [NCXNavPoint(point) for point in nav_point_elements]


class NCXPageTarget(NCXElement):
	"""Represents a pageTarget element."""

	@property
	def type_attr(self) -> Optional[str]:
		"""Get the type attribute."""
		return self.element.get('type')

	@type_attr.setter
	def type_attr(self, value: str) -> None:
		"""Set the type attribute."""
		self.element.set('type', value)

	@property
	def value(self) -> Optional[str]:
		"""Get the value attribute."""
		return self.element.get('value')

	@value.setter
	def value(self, value: str) -> None:
		"""Set the value attribute."""
		self.element.set('value', value)

	@property
	def play_order(self) -> Optional[int]:
		"""Get the playOrder attribute."""
		play_order = self.element.get('playOrder')
		return int(play_order) if play_order else None

	@play_order.setter
	def play_order(self, value: int) -> None:
		"""Set the playOrder attribute."""
		self.element.set('playOrder', str(value))

	@property
	def nav_label(self) -> Optional[NCXNavLabel]:
		"""Get the navLabel child element."""
		nav_labels = self.element.xpath(
			'./ncx:navLabel', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if nav_labels:
			return NCXNavLabel(nav_labels[0])
		return None

	@property
	def content(self) -> Optional[NCXContent]:
		"""Get the content child element."""
		content_elements = self.element.xpath(
			'./ncx:content', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if content_elements:
			return NCXContent(content_elements[0])
		return None

	@property
	def label_text(self) -> str:
		"""Get the text of the navLabel."""
		nav_label = self.nav_label
		return nav_label.text if nav_label else ''

	@property
	def content_src(self) -> str:
		"""Get the src of the content element."""
		content = self.content
		return content.src if content else ''


class NCXPageList(NCXElement):
	"""Represents the pageList element."""

	@property
	def page_targets(self) -> List[NCXPageTarget]:
		"""Get all pageTarget elements."""
		page_target_elements = self.element.xpath(
			'./ncx:pageTarget', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return [NCXPageTarget(target) for target in page_target_elements]

	def add_page_target(
		self,
		id: str,
		type_attr: str,
		value: str,
		label_text: str,
		src: str,
		play_order: Optional[int] = None,
	) -> NCXPageTarget:
		"""Add a pageTarget element."""
		page_target_element = etree.SubElement(
			self.element, '{http://www.daisy.org/z3986/2005/ncx/}pageTarget'
		)
		page_target = NCXPageTarget(page_target_element)
		page_target.id = id
		page_target.type_attr = type_attr
		page_target.value = value

		if play_order is not None:
			page_target.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(
			page_target_element, '{http://www.daisy.org/z3986/2005/ncx/}navLabel'
		)
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(
			page_target_element, '{http://www.daisy.org/z3986/2005/ncx/}content'
		)
		content = NCXContent(content_element)
		content.src = src

		return page_target


class NCXNavTarget(NCXElement):
	"""Represents a navTarget element."""

	@property
	def value(self) -> Optional[str]:
		"""Get the value attribute."""
		return self.element.get('value')

	@value.setter
	def value(self, value: str) -> None:
		"""Set the value attribute."""
		self.element.set('value', value)

	@property
	def class_attr(self) -> Optional[str]:
		"""Get the class attribute."""
		return self.element.get('class')

	@class_attr.setter
	def class_attr(self, value: str) -> None:
		"""Set the class attribute."""
		self.element.set('class', value)

	@property
	def play_order(self) -> Optional[int]:
		"""Get the playOrder attribute."""
		play_order = self.element.get('playOrder')
		return int(play_order) if play_order else None

	@play_order.setter
	def play_order(self, value: int) -> None:
		"""Set the playOrder attribute."""
		self.element.set('playOrder', str(value))

	@property
	def nav_label(self) -> Optional[NCXNavLabel]:
		"""Get the navLabel child element."""
		nav_labels = self.element.xpath(
			'./ncx:navLabel', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if nav_labels:
			return NCXNavLabel(nav_labels[0])
		return None

	@property
	def content(self) -> Optional[NCXContent]:
		"""Get the content child element."""
		content_elements = self.element.xpath(
			'./ncx:content', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if content_elements:
			return NCXContent(content_elements[0])
		return None


class NCXNavList(NCXElement):
	"""Represents the navList element."""

	@property
	def nav_label(self) -> Optional[NCXNavLabel]:
		"""Get the navLabel child element."""
		nav_labels = self.element.xpath(
			'./ncx:navLabel', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if nav_labels:
			return NCXNavLabel(nav_labels[0])
		return None

	@property
	def nav_targets(self) -> List[NCXNavTarget]:
		"""Get all navTarget elements."""
		nav_target_elements = self.element.xpath(
			'./ncx:navTarget', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return [NCXNavTarget(target) for target in nav_target_elements]

	def add_nav_target(
		self, id: str, label_text: str, src: str, play_order: Optional[int] = None
	) -> NCXNavTarget:
		"""Add a navTarget element."""
		nav_target_element = etree.SubElement(
			self.element, '{http://www.daisy.org/z3986/2005/ncx/}navTarget'
		)
		nav_target = NCXNavTarget(nav_target_element)
		nav_target.id = id

		if play_order is not None:
			nav_target.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(
			nav_target_element, '{http://www.daisy.org/z3986/2005/ncx/}navLabel'
		)
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(
			nav_target_element, '{http://www.daisy.org/z3986/2005/ncx/}content'
		)
		content = NCXContent(content_element)
		content.src = src

		return nav_target

	@property
	def label_text(self) -> str:
		"""Get the text of the navLabel."""
		nav_label = self.nav_label
		return nav_label.text if nav_label else ''


class NCXDocument(NCXElement):
	"""Represents the root ncx element."""

	@property
	def nav_map(self) -> Optional[NCXNavMap]:
		"""Get the navMap element."""
		nav_map_elements = self.element.xpath(
			'./ncx:navMap', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if nav_map_elements:
			return NCXNavMap(nav_map_elements[0])
		return None

	@property
	def page_list(self) -> Optional[NCXPageList]:
		"""Get the pageList element."""
		page_list_elements = self.element.xpath(
			'./ncx:pageList', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if page_list_elements:
			return NCXPageList(page_list_elements[0])
		return None

	@property
	def nav_lists(self) -> List[NCXNavList]:
		"""Get all navList elements."""
		nav_list_elements = self.element.xpath(
			'./ncx:navList', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return [NCXNavList(nav_list) for nav_list in nav_list_elements]

	@property
	def title(self) -> str:
		"""Get the document title text."""
		title_elements = self.element.xpath(
			'.//ncx:docTitle/ncx:text', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return title_elements[0].text if title_elements else ''

	@property
	def author(self) -> str:
		"""Get the document author text."""
		author_elements = self.element.xpath(
			'.//ncx:docAuthor/ncx:text', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return author_elements[0].text if author_elements else ''

	def get_uid(self) -> Optional[str]:
		"""Get the dtb:uid meta content."""
		uid_elements = self.element.xpath(
			'.//ncx:meta[@name="dtb:uid"]/@content',
			namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'},
		)
		return uid_elements[0] if uid_elements else None

	def get_depth(self) -> Optional[int]:
		"""Get the dtb:depth meta content."""
		depth_elements = self.element.xpath(
			'.//ncx:meta[@name="dtb:depth"]/@content',
			namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'},
		)
		return int(depth_elements[0]) if depth_elements else None

	def get_total_page_count(self) -> Optional[int]:
		"""Get the dtb:totalPageCount meta content."""
		count_elements = self.element.xpath(
			'.//ncx:meta[@name="dtb:totalPageCount"]/@content',
			namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'},
		)
		return int(count_elements[0]) if count_elements else None

	def get_max_page_number(self) -> Optional[int]:
		"""Get the dtb:maxPageNumber meta content."""
		max_elements = self.element.xpath(
			'.//ncx:meta[@name="dtb:maxPageNumber"]/@content',
			namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'},
		)
		return int(max_elements[0]) if max_elements else None
