"""
NCX DOM

This module contains classes representing the DOM elements of NCX (Navigation Center eXtended) files.
Based on the DAISY/NISO Standard, Section 8 of ANSI/NISO Z39.86-2005,
Specifications for the Digital Talking Book.
"""

from typing import List, Optional, Union

from lxml import etree


class NCXElement:
	"""Base class for all NCX elements."""

	def __init__(self, element: etree.Element):
		self.element = element
		self.id = element.get('id')

	@property
	def tag(self) -> str:
		"""Return the tag name without namespace."""
		return etree.QName(self.element).localname

	def get_attribute(self, name: str) -> Optional[str]:
		"""Get an attribute value."""
		return self.element.get(name)

	def set_attribute(self, name: str, value: str) -> None:
		"""Set an attribute value."""
		self.element.set(name, value)


class NCXText(NCXElement):
	"""Represents a text element in NCX."""

	@property
	def text(self) -> str:
		"""Get the text content."""
		return self.element.text or ''

	@text.setter
	def text(self, value: str) -> None:
		"""Set the text content."""
		self.element.text = value


class NCXContent(NCXElement):
	"""Represents a content element that points to a resource."""

	@property
	def src(self) -> str:
		"""Get the src attribute."""
		return self.element.get('src', '')

	@src.setter
	def src(self, value: str) -> None:
		"""Set the src attribute."""
		self.element.set('src', value)


class NCXMeta(NCXElement):
	"""Represents a meta element in the NCX head."""

	@property
	def name(self) -> str:
		"""Get the name attribute."""
		return self.element.get('name', '')

	@name.setter
	def name(self, value: str) -> None:
		"""Set the name attribute."""
		self.element.set('name', value)

	@property
	def content(self) -> str:
		"""Get the content attribute."""
		return self.element.get('content', '')

	@content.setter
	def content(self, value: str) -> None:
		"""Set the content attribute."""
		self.element.set('content', value)


class NCXHead(NCXElement):
	"""Represents the head element containing metadata."""

	@property
	def metas(self) -> List[NCXMeta]:
		"""Get all meta elements."""
		meta_elements = self.element.xpath(
			'.//ncx:meta', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		return [NCXMeta(meta) for meta in meta_elements]

	def get_meta(self, name: str) -> Optional[NCXMeta]:
		"""Get a specific meta element by name."""
		for meta in self.metas:
			if meta.name == name:
				return meta
		return None

	def add_meta(self, name: str, content: str) -> NCXMeta:
		"""Add a new meta element."""
		meta_element = etree.SubElement(self.element, 'meta')
		meta = NCXMeta(meta_element)
		meta.name = name
		meta.content = content
		return meta


class NCXDocTitle(NCXElement):
	"""Represents the docTitle element."""

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
			text_element = etree.SubElement(self.element, 'text')
			text_elem = NCXText(text_element)
			text_elem.text = value


class NCXDocAuthor(NCXElement):
	"""Represents the docAuthor element."""

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
			text_element = etree.SubElement(self.element, 'text')
			text_elem = NCXText(text_element)
			text_elem.text = value


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
			text_element = etree.SubElement(self.element, 'text')
			text_elem = NCXText(text_element)
			text_elem.text = value


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
		nav_point_element = etree.SubElement(self.element, 'navPoint')
		nav_point = NCXNavPoint(nav_point_element)
		nav_point.id = id

		if class_attr:
			nav_point.class_attr = class_attr
		if play_order is not None:
			nav_point.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(nav_point_element, 'navLabel')
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(nav_point_element, 'content')
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
		nav_point_element = etree.SubElement(self.element, 'navPoint')
		nav_point = NCXNavPoint(nav_point_element)
		nav_point.id = id

		if class_attr:
			nav_point.class_attr = class_attr
		if play_order is not None:
			nav_point.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(nav_point_element, 'navLabel')
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(nav_point_element, 'content')
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
		page_target_element = etree.SubElement(self.element, 'pageTarget')
		page_target = NCXPageTarget(page_target_element)
		page_target.id = id
		page_target.type_attr = type_attr
		page_target.value = value

		if play_order is not None:
			page_target.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(page_target_element, 'navLabel')
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(page_target_element, 'content')
		content = NCXContent(content_element)
		content.src = src

		return page_target


class NCXNavTarget(NCXElement):
	"""Represents a navTarget element."""

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
		nav_target_element = etree.SubElement(self.element, 'navTarget')
		nav_target = NCXNavTarget(nav_target_element)
		nav_target.id = id

		if play_order is not None:
			nav_target.play_order = play_order

		# Add navLabel
		nav_label_element = etree.SubElement(nav_target_element, 'navLabel')
		nav_label = NCXNavLabel(nav_label_element)
		nav_label.text = label_text

		# Add content
		content_element = etree.SubElement(nav_target_element, 'content')
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
	def version(self) -> str:
		"""Get the version attribute."""
		return self.element.get('version', '')

	@version.setter
	def version(self, value: str) -> None:
		"""Set the version attribute."""
		self.element.set('version', value)

	@property
	def lang(self) -> str:
		"""Get the xml:lang attribute."""
		return self.element.get('{http://www.w3.org/XML/1998/namespace}lang', '')

	@lang.setter
	def lang(self, value: str) -> None:
		"""Set the xml:lang attribute."""
		self.element.set('{http://www.w3.org/XML/1998/namespace}lang', value)

	@property
	def head(self) -> Optional[NCXHead]:
		"""Get the head element."""
		head_elements = self.element.xpath(
			'./ncx:head', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if head_elements:
			return NCXHead(head_elements[0])
		return None

	@property
	def doc_title(self) -> Optional[NCXDocTitle]:
		"""Get the docTitle element."""
		doc_title_elements = self.element.xpath(
			'./ncx:docTitle', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if doc_title_elements:
			return NCXDocTitle(doc_title_elements[0])
		return None

	@property
	def doc_author(self) -> Optional[NCXDocAuthor]:
		"""Get the docAuthor element."""
		doc_author_elements = self.element.xpath(
			'./ncx:docAuthor', namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
		)
		if doc_author_elements:
			return NCXDocAuthor(doc_author_elements[0])
		return None

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
		doc_title = self.doc_title
		return doc_title.text if doc_title else ''

	@property
	def author(self) -> str:
		"""Get the document author text."""
		doc_author = self.doc_author
		return doc_author.text if doc_author else ''

	def get_uid(self) -> Optional[str]:
		"""Get the dtb:uid meta content."""
		head = self.head
		if head:
			uid_meta = head.get_meta('dtb:uid')
			return uid_meta.content if uid_meta else None
		return None

	def get_depth(self) -> Optional[int]:
		"""Get the dtb:depth meta content."""
		head = self.head
		if head:
			depth_meta = head.get_meta('dtb:depth')
			if depth_meta and depth_meta.content:
				try:
					return int(depth_meta.content)
				except ValueError:
					pass
		return None

	def get_total_page_count(self) -> Optional[int]:
		"""Get the dtb:totalPageCount meta content."""
		head = self.head
		if head:
			page_count_meta = head.get_meta('dtb:totalPageCount')
			if page_count_meta and page_count_meta.content:
				try:
					return int(page_count_meta.content)
				except ValueError:
					pass
		return None

	def get_max_page_number(self) -> Optional[int]:
		"""Get the dtb:maxPageNumber meta content."""
		head = self.head
		if head:
			max_page_meta = head.get_meta('dtb:maxPageNumber')
			if max_page_meta and max_page_meta.content:
				try:
					return int(max_page_meta.content)
				except ValueError:
					pass
		return None
