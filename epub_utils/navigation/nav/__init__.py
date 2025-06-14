import re
from typing import List, Optional

from lxml import etree

from epub_utils.exceptions import ParseError
from epub_utils.navigation.base import Navigation, NavigationItem
from epub_utils.printers import XMLPrinter

from .dom import NavDocument, NavListItem


class EPUBNavDocNavigation(Navigation):
	"""EPUB 3 Navigation Document implementation."""

	MEDIA_TYPES = ['application/xhtml+xml']

	def __init__(
		self, xml_content: str, media_type: str = 'application/xhtml+xml', href: str = None
	) -> None:
		self.xml_content = xml_content

		self._tree = None

		self.xmlns = None
		self.lang = None

		if media_type not in self.MEDIA_TYPES:
			raise ValueError(f'Invalid media type for navigation document: {media_type}')
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
			self.lang = root.get('{http://www.w3.org/XML/1998/namespace}lang', '')

		except etree.ParseError as e:
			raise ParseError(f'Error parsing navigation document: {e}')

	@property
	def tree(self):
		"""Lazily parse and cache the XHTML tree."""
		if self._tree is None:
			self._parse(self.xml_content)
		return self._tree

	@property
	def inner_text(self) -> str:
		tree = self.tree

		body_elements = tree.xpath(
			'//*[local-name()="body"]', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
		)

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
		nav_doc = NavDocument(self.tree)
		toc_nav = nav_doc.toc_nav
		if not toc_nav:
			return []

		ordered_list = toc_nav.ordered_list
		if not ordered_list:
			return []

		return self._convert_list_items_recursive(ordered_list.list_items, level=0)

	def get_page_list(self) -> List[NavigationItem]:
		"""Get page list/breaks as normalized items."""
		nav_doc = NavDocument(self.tree)
		page_list_nav = nav_doc.page_list_nav
		if not page_list_nav:
			return []

		ordered_list = page_list_nav.ordered_list
		if not ordered_list:
			return []

		return self._convert_list_items_to_pages(ordered_list.list_items)

	def get_landmarks(self) -> List[NavigationItem]:
		"""Get landmarks/guide references as normalized items."""
		nav_doc = NavDocument(self.tree)
		landmarks_nav = nav_doc.landmarks_nav
		if not landmarks_nav:
			return []

		ordered_list = landmarks_nav.ordered_list
		if not ordered_list:
			return []

		return self._convert_list_items_to_landmarks(ordered_list.list_items)

	# === Editing Interface ===

	def add_toc_item(self, item: NavigationItem, after_id: Optional[str] = None) -> None:
		"""Add item to table of contents."""
		nav_doc = NavDocument(self.tree)
		toc_nav = nav_doc.toc_nav

		if not toc_nav:
			# Create TOC nav if it doesn't exist
			toc_nav = nav_doc.add_nav_section('toc')
			toc_nav.add_heading(1, 'Table of Contents')
			ordered_list = toc_nav.add_ordered_list()
		else:
			ordered_list = toc_nav.ordered_list
			if not ordered_list:
				ordered_list = toc_nav.add_ordered_list()

		# Create new list item
		new_li = ordered_list.add_list_item()
		if item.id:
			new_li.id = item.id

		# Add anchor or span based on whether target is provided
		if item.target:
			anchor = new_li.add_anchor(item.target, item.label)
			if item.item_type:
				anchor.epub_type = item.item_type
		else:
			span = new_li.add_span(item.label)
			if item.id:
				span.id = item.id

		# TODO: Handle after_id positioning and children

	def remove_toc_item(self, item_id: str) -> bool:
		"""Remove item from table of contents by ID."""
		nav_doc = NavDocument(self.tree)
		toc_nav = nav_doc.toc_nav
		if not toc_nav:
			return False

		# Find and remove the list item with the given ID
		items_to_remove = self.tree.xpath(
			f'.//xhtml:li[@id="{item_id}"]',
			namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'},
		)

		# Also check for anchors with the ID
		if not items_to_remove:
			items_to_remove = self.tree.xpath(
				f'.//xhtml:a[@id="{item_id}"]',
				namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'},
			)
			# Remove the parent li element if found
			items_to_remove = [
				item.getparent() for item in items_to_remove if item.getparent() is not None
			]

		if items_to_remove:
			for item in items_to_remove:
				if item.getparent() is not None:
					item.getparent().remove(item)
			return True

		return False

	def update_toc_item(self, item_id: str, **kwargs) -> bool:
		"""Update existing TOC item properties."""
		nav_doc = NavDocument(self.tree)
		toc_nav = nav_doc.toc_nav
		if not toc_nav:
			return False

		# Find the item by ID (could be on li or a element)
		target_items = self.tree.xpath(
			f'.//xhtml:li[@id="{item_id}"] | .//xhtml:a[@id="{item_id}"]',
			namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'},
		)

		if not target_items:
			return False

		target_element = target_items[0]

		# If we found an anchor, work with it; if we found a li, find its anchor
		if target_element.tag.endswith('}a'):
			anchor_element = target_element
			li_element = target_element.getparent()
		else:
			li_element = target_element
			anchors = li_element.xpath(
				'./xhtml:a', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
			)
			anchor_element = anchors[0] if anchors else None

		# Update properties
		if 'label' in kwargs and anchor_element is not None:
			anchor_element.text = kwargs['label']
		elif 'label' in kwargs:
			# Handle span elements or create anchor
			spans = li_element.xpath(
				'./xhtml:span', namespaces={'xhtml': 'http://www.w3.org/1999/xhtml'}
			)
			if spans:
				spans[0].text = kwargs['label']

		if 'target' in kwargs and anchor_element is not None:
			anchor_element.set('href', kwargs['target'])

		if 'item_type' in kwargs and anchor_element is not None:
			anchor_element.set('{http://www.idpf.org/2007/ops}type', kwargs['item_type'])

		return True

	def reorder_toc_items(self, new_order: List[str]) -> None:
		"""Reorder TOC items by list of IDs."""
		# This is a complex operation that would require rebuilding the list structure
		# For now, we'll implement a basic version that moves items around
		nav_doc = NavDocument(self.tree)
		toc_nav = nav_doc.toc_nav
		if not toc_nav:
			return

		ordered_list = toc_nav.ordered_list
		if not ordered_list:
			return

		# Collect all items with their IDs
		items_map = {}
		for li_item in ordered_list.list_items:
			if li_item.id:
				items_map[li_item.id] = li_item.element
			elif li_item.anchor and li_item.anchor.id:
				items_map[li_item.anchor.id] = li_item.element

		# Reorder by removing and re-adding in new order
		for item_id in new_order:
			if item_id in items_map:
				element = items_map[item_id]
				parent = element.getparent()
				if parent is not None:
					parent.remove(element)
					parent.append(element)

	# === Helper Methods ===

	def _convert_list_items_recursive(
		self, list_items: List[NavListItem], level: int = 0
	) -> List[NavigationItem]:
		"""Convert navigation list items to NavigationItems recursively."""
		items = []

		for i, list_item in enumerate(list_items):
			anchor = list_item.anchor
			span = list_item.span

			if anchor:
				item = NavigationItem(
					id=anchor.id or list_item.id or '',
					label=anchor.text,
					target=anchor.href or '',
					order=i + 1,
					level=level,
					item_type=anchor.epub_type,
				)
			elif span:
				item = NavigationItem(
					id=span.id or list_item.id or '',
					label=span.element.text or '',
					target='',
					order=i + 1,
					level=level,
					item_type=None,
				)
			else:
				# Fallback for items without anchor or span
				continue

			# Convert nested items
			nested_list = list_item.nested_list
			if nested_list:
				item.children = self._convert_list_items_recursive(
					nested_list.list_items, level + 1
				)

			items.append(item)

		return items

	def _convert_list_items_to_pages(self, list_items: List[NavListItem]) -> List[NavigationItem]:
		"""Convert navigation list items to page NavigationItems."""
		items = []

		for i, list_item in enumerate(list_items):
			anchor = list_item.anchor
			if not anchor:
				continue

			item = NavigationItem(
				id=anchor.id or list_item.id or '',
				label=anchor.text,
				target=anchor.href or '',
				order=i + 1,
				level=0,
				item_type=anchor.epub_type or 'page',
			)
			items.append(item)

		return items

	def _convert_list_items_to_landmarks(
		self, list_items: List[NavListItem]
	) -> List[NavigationItem]:
		"""Convert navigation list items to landmark NavigationItems."""
		items = []

		for i, list_item in enumerate(list_items):
			anchor = list_item.anchor
			if not anchor:
				continue

			item = NavigationItem(
				id=anchor.id or list_item.id or '',
				label=anchor.text,
				target=anchor.href or '',
				order=i + 1,
				level=0,
				item_type=anchor.epub_type or 'landmark',
			)
			items.append(item)

		return items
