import re
from typing import List, Optional

from lxml import etree

from epub_utils.exceptions import ParseError
from epub_utils.navigation.base import Navigation, NavigationItem
from epub_utils.printers import XMLPrinter

from .dom import NCXDocument, NCXNavPoint, NCXNavTarget, NCXPageTarget


class NCXNavigation(Navigation):
	MEDIA_TYPES = ['application/x-dtbncx+xml']

	def __init__(
		self, xml_content: str, media_type: str = 'application/x-dtbncx+xml', href: str = None
	) -> None:
		self.xml_content = xml_content

		self._tree = None

		self.xmlns = None
		self.version = None
		self.lang = None

		if media_type not in self.MEDIA_TYPES:
			raise ValueError(f'Invalid media type for NCX navigation: {media_type}')
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

			root = self._tree

			self.xmlns = root.nsmap.get(None, '') if root.nsmap else ''
			self.version = root.get('version', '')
			self.lang = root.get('{http://www.w3.org/XML/1998/namespace}lang', '')

		except etree.ParseError as e:
			raise ParseError(f'Error parsing Content file: {e}')

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

	# === Navigation Interface Implementation ===

	def get_toc_items(self) -> List[NavigationItem]:
		"""Get table of contents as normalized items."""
		ncx_doc = NCXDocument(self.tree)
		nav_map = ncx_doc.nav_map
		if not nav_map:
			return []

		return self._convert_nav_points_recursive(nav_map.nav_points, level=0)

	def get_page_list(self) -> List[NavigationItem]:
		"""Get page list/breaks as normalized items."""
		ncx_doc = NCXDocument(self.tree)
		page_list = ncx_doc.page_list
		if not page_list:
			return []

		return self._convert_page_targets(page_list.page_targets)

	def get_landmarks(self) -> List[NavigationItem]:
		"""Get landmarks/guide references as normalized items."""
		ncx_doc = NCXDocument(self.tree)
		nav_lists = ncx_doc.nav_lists

		items = []
		for nav_list in nav_lists:
			for nav_target in nav_list.nav_targets:
				items.append(self._convert_nav_target(nav_target))

		return items

	def add_toc_item(self, item: NavigationItem, after_id: Optional[str] = None) -> None:
		"""Add item to table of contents."""
		ncx_doc = NCXDocument(self.tree)
		nav_map = ncx_doc.nav_map
		if not nav_map:
			raise ValueError('No navMap found in NCX document')

		# Find insertion point
		if after_id:
			all_nav_points = nav_map.get_all_nav_points()
			insert_index = None
			for i, nav_point in enumerate(all_nav_points):
				if nav_point.id == after_id:
					insert_index = i + 1
					break

			if insert_index is None:
				raise ValueError(f"Navigation item with ID '{after_id}' not found")

			# For now, append to the end if we can't find the exact position
			# More complex insertion logic would require tree manipulation
			nav_map.add_nav_point(
				item.id, item.label, item.target, class_attr=item.item_type, play_order=item.order
			)
		else:
			# Add to the end
			nav_map.add_nav_point(
				item.id, item.label, item.target, class_attr=item.item_type, play_order=item.order
			)

	def remove_toc_item(self, item_id: str) -> bool:
		"""Remove item from table of contents by ID."""
		ncx_doc = NCXDocument(self.tree)
		nav_map = ncx_doc.nav_map
		if not nav_map:
			return False

		# Find and remove the navPoint
		nav_points = nav_map.element.xpath(
			f'.//ncx:navPoint[@id="{item_id}"]',
			namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'},
		)

		if nav_points:
			nav_points[0].getparent().remove(nav_points[0])
			return True

		return False

	def update_toc_item(self, item_id: str, **kwargs) -> bool:
		"""Update existing TOC item properties."""
		ncx_doc = NCXDocument(self.tree)
		nav_map = ncx_doc.nav_map
		if not nav_map:
			return False

		# Find the navPoint
		nav_points = nav_map.element.xpath(
			f'.//ncx:navPoint[@id="{item_id}"]',
			namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'},
		)

		if not nav_points:
			return False

		nav_point = NCXNavPoint(nav_points[0])

		# Update properties
		if 'label' in kwargs:
			nav_label = nav_point.nav_label
			if nav_label:
				nav_label.text = kwargs['label']

		if 'target' in kwargs:
			content = nav_point.content
			if content:
				content.src = kwargs['target']

		if 'order' in kwargs:
			nav_point.play_order = kwargs['order']

		if 'item_type' in kwargs:
			nav_point.class_attr = kwargs['item_type']

		return True

	def reorder_toc_items(self, new_order: List[str]) -> None:
		"""Reorder TOC items by list of IDs."""
		# This is a complex operation that would require rebuilding the navMap
		# For now, we'll update the playOrder attributes
		ncx_doc = NCXDocument(self.tree)
		nav_map = ncx_doc.nav_map
		if not nav_map:
			return

		for i, item_id in enumerate(new_order):
			nav_points = nav_map.element.xpath(
				f'.//ncx:navPoint[@id="{item_id}"]',
				namespaces={'ncx': 'http://www.daisy.org/z3986/2005/ncx/'},
			)
			if nav_points:
				nav_point = NCXNavPoint(nav_points[0])
				nav_point.play_order = i + 1

	# === Helper Methods ===

	def _convert_nav_points_recursive(
		self, nav_points: List[NCXNavPoint], level: int = 0
	) -> List[NavigationItem]:
		"""Convert NCX navPoints to NavigationItems recursively."""
		items = []

		for nav_point in nav_points:
			item = NavigationItem(
				id=nav_point.id or '',
				label=nav_point.label_text,
				target=nav_point.content_src,
				order=nav_point.play_order,
				level=level,
				item_type=nav_point.class_attr,
			)

			# Convert child nav points
			child_nav_points = nav_point.nav_points
			if child_nav_points:
				item.children = self._convert_nav_points_recursive(child_nav_points, level + 1)

			items.append(item)

		return items

	def _convert_page_targets(self, page_targets: List[NCXPageTarget]) -> List[NavigationItem]:
		"""Convert NCX pageTargets to NavigationItems."""
		items = []

		for page_target in page_targets:
			item = NavigationItem(
				id=page_target.id or '',
				label=page_target.label_text,
				target=page_target.content_src,
				order=page_target.play_order,
				level=0,
				item_type=page_target.type_attr,
			)
			items.append(item)

		return items

	def _convert_nav_target(self, nav_target: NCXNavTarget) -> NavigationItem:
		"""Convert NCX navTarget to NavigationItem."""
		return NavigationItem(
			id=nav_target.id or '',
			label=nav_target.nav_label.text if nav_target.nav_label else '',
			target=nav_target.content.src if nav_target.content else '',
			order=nav_target.play_order,
			level=0,
			item_type=nav_target.class_attr,
		)
