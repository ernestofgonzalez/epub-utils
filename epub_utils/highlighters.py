from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import XmlLexer


def highlight_xml(xml_content: str) -> str:
	return highlight(xml_content, XmlLexer(), TerminalFormatter())
