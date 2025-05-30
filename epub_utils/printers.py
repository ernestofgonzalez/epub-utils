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
