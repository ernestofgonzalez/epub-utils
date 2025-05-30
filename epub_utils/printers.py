try:
	from lxml import etree
except ImportError:
	import xml.etree.ElementTree as etree

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import XmlLexer


def highlight_xml(xml_content: str) -> str:
	return highlight(xml_content, XmlLexer(), TerminalFormatter())


def pretty_print_xml(xml_content: str) -> str:
	try:
		original_content = xml_content
		if isinstance(xml_content, str):
			xml_content_bytes = xml_content.encode('utf-8')
		else:
			xml_content_bytes = xml_content
			original_content = (
				xml_content.decode('utf-8') if isinstance(xml_content, bytes) else xml_content
			)

		xml_declaration = ''
		doctype_declaration = ''

		if original_content.strip().startswith('<?xml'):
			xml_decl_end = original_content.find('?>') + 2
			xml_declaration = original_content[:xml_decl_end]

		doctype_start = original_content.find('<!DOCTYPE')
		if doctype_start != -1:
			doctype_end = original_content.find('>', doctype_start) + 1
			doctype_declaration = original_content[doctype_start:doctype_end]

		parser = etree.XMLParser(remove_blank_text=True)
		root = etree.fromstring(xml_content_bytes, parser)
		pretty_xml = etree.tostring(root, pretty_print=True, encoding='unicode')

		result = ''
		if xml_declaration:
			result += xml_declaration + '\n'
		if doctype_declaration:
			result += doctype_declaration + '\n'
		result += pretty_xml

		return result
	except etree.ParseError:
		return original_content if isinstance(original_content, str) else xml_content


def print_to_str(xml_content: bool, pretty_print: bool) -> str:
	if pretty_print:
		xml_content = pretty_print_xml(xml_content)

	return xml_content


def print_to_xml(xml_content: str, pretty_print: bool, highlight_syntax: bool) -> str:
	if pretty_print:
		xml_content = pretty_print_xml(xml_content)

	if highlight_syntax:
		xml_content = highlight_xml(xml_content)

	return xml_content


class XMLPrinter:
	"""Handles XML printing operations for objects with xml_content."""

	def __init__(self, xml_content_provider):
		"""
		Initialize the XMLPrinter with an object that provides xml_content.

		Args:
			xml_content_provider: Object that has an xml_content attribute
		"""
		self._xml_content_provider = xml_content_provider

	def to_str(self, pretty_print: bool = False) -> str:
		"""
		Get string representation of the XML content.

		Args:
			pretty_print: Whether to format the XML with proper indentation

		Returns:
			String representation of the XML content
		"""
		return print_to_str(self._xml_content_provider.xml_content, pretty_print)

	def to_xml(self, pretty_print: bool = False, highlight_syntax: bool = True) -> str:
		"""
		Get formatted XML representation with optional syntax highlighting.

		Args:
			pretty_print: Whether to format the XML with proper indentation
			highlight_syntax: Whether to apply syntax highlighting

		Returns:
			Formatted XML string with optional syntax highlighting
		"""
		return print_to_xml(self._xml_content_provider.xml_content, pretty_print, highlight_syntax)
