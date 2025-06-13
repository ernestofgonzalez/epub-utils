from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class NavigationItem:
	"""Universal navigation item representation."""

	id: str
	label: str
	target: str  # href/src
	order: Optional[int] = None
	level: int = 0
	item_type: Optional[str] = None  # semantic type
	children: List['NavigationItem'] = field(default_factory=list)


class Navigation(ABC):
	"""
	Base class for Navigation Documents.

	Attributes:
	    media_type (str): The MIME type of the content.
	    href (str): The path to the content file within the EPUB.
	"""

	def __init__(self, media_type: str, href: str) -> None:
		self.media_type = media_type
		self.href = href

	# === Core Abstract Methods ===
	@abstractmethod
	def get_toc_items(self) -> List[NavigationItem]:
		"""Get table of contents as normalized items."""
		pass

	@abstractmethod
	def get_page_list(self) -> List[NavigationItem]:
		"""Get page list/breaks as normalized items."""
		pass

	@abstractmethod
	def get_landmarks(self) -> List[NavigationItem]:
		"""Get landmarks/guide references as normalized items."""
		pass

	# === Editing Interface ===
	@abstractmethod
	def add_toc_item(self, item: NavigationItem, after_id: Optional[str] = None) -> None:
		"""Add item to table of contents."""
		pass

	@abstractmethod
	def remove_toc_item(self, item_id: str) -> bool:
		"""Remove item from table of contents by ID."""
		pass

	@abstractmethod
	def update_toc_item(self, item_id: str, **kwargs) -> bool:
		"""Update existing TOC item properties."""
		pass

	@abstractmethod
	def reorder_toc_items(self, new_order: List[str]) -> None:
		"""Reorder TOC items by list of IDs."""
		pass

	# === Query Interface ===
	def find_item_by_id(self, item_id: str) -> Optional[NavigationItem]:
		"""Find navigation item by ID across all collections."""
		for item in self.get_all_items():
			if item.id == item_id:
				return item
		return None

	def find_items_by_target(self, target: str) -> List[NavigationItem]:
		"""Find navigation items by target/href."""
		return [item for item in self.get_all_items() if item.target == target]

	def get_all_items(self) -> List[NavigationItem]:
		"""Get all navigation items from all collections."""
		items = []
		items.extend(self.get_toc_items())
		items.extend(self.get_page_list())
		items.extend(self.get_landmarks())
		return items

	def get_toc_hierarchy(self) -> Dict[str, Any]:
		"""Get TOC as nested dictionary structure."""
		return self._build_hierarchy(self.get_toc_items())

	def _build_hierarchy(self, items: List[NavigationItem]) -> Dict[str, Any]:
		"""Helper to build hierarchical structure."""
		result = {'items': []}

		def add_item_to_hierarchy(item: NavigationItem, parent_dict: Dict[str, Any]):
			item_dict = {
				'id': item.id,
				'label': item.label,
				'target': item.target,
				'order': item.order,
				'level': item.level,
				'type': item.item_type,
				'children': [],
			}

			# Add to parent's items/children list
			if 'items' in parent_dict:
				parent_dict['items'].append(item_dict)
			else:
				parent_dict['children'].append(item_dict)

			# Add children recursively
			for child in item.children:
				add_item_to_hierarchy(child, item_dict)

		for item in items:
			add_item_to_hierarchy(item, result)

		return result

	# === Format-specific Access ===
	@property
	@abstractmethod
	def tree(self):
		"""Get underlying XML/DOM tree for format-specific operations."""
		pass

	# === Output Methods ===
	@abstractmethod
	def to_str(self, *args, **kwargs) -> str:
		pass

	@abstractmethod
	def to_xml(self, *args, **kwargs) -> str:
		pass

	@abstractmethod
	def to_plain(self) -> str:
		pass
