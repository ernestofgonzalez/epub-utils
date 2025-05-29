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
		if isinstance(xml_content, str):
			xml_content = xml_content.encode('utf-8')
		root = etree.fromstring(xml_content)
		xml_content = etree.tostring(root, pretty_print=True, encoding='unicode')
	except etree.ParseError:
		return xml_content
