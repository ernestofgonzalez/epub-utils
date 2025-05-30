try:
	from lxml import etree
except ImportError:
	import xml.etree.ElementTree as etree

from epub_utils.exceptions import ParseError
from epub_utils.printers import XMLPrinter


class Metadata:
	"""
	Represents the metadata section of an EPUB package document.
	Handles Dublin Core (DC) and Dublin Core Terms (DCTERMS) metadata elements.
	"""

	DC_NAMESPACE = 'http://purl.org/dc/elements/1.1/'
	DCTERMS_NAMESPACE = 'http://purl.org/dc/terms/'
	REQUIRED_FIELDS = ['identifier', 'title', 'creator']

	NSMAP = {'dc': DC_NAMESPACE, 'dcterms': DCTERMS_NAMESPACE}

	def __init__(self, xml_content: str):
		self.xml_content = xml_content
		self.fields = {}

		self._parse(xml_content)

		self._printer = XMLPrinter(self)

	def _parse(self, xml_content: str) -> None:
		try:
			if isinstance(xml_content, str):
				xml_content = xml_content.encode('utf-8')
			root = etree.fromstring(xml_content)

			for ns_prefix, ns_uri in self.NSMAP.items():
				for element in root.findall(f'.//{{{ns_uri}}}*'):
					name = element.tag.split('}')[-1]
					text = element.text.strip() if element.text else None
					if text:
						self._add_field(name, text)

			for meta in root.findall('.//meta[@property]'):
				prop = meta.get('property', '')
				if prop.startswith('dcterms:'):
					name = prop.split(':')[1]
					text = meta.text.strip() if meta.text else None
					if text:
						self._add_field(name, text)

			self._validate()

		except etree.ParseError as e:
			raise ParseError(f'Error parsing metadata element: {e}')

	def _add_field(self, name: str, value: str) -> None:
		if name in self.fields:
			if isinstance(self.fields[name], list):
				self.fields[name].append(value)
			else:
				self.fields[name] = [self.fields[name], value]
		else:
			self.fields[name] = value

	def _validate(self, raise_exception=False) -> None:
		"""
		Validate all required fields and raise ValueError if validation fails.
		"""
		errors = {}

		for field in self.REQUIRED_FIELDS:
			try:
				self._validate_field(field)
			except ValueError as e:
				errors[field] = str(e)

		if errors and raise_exception:
			error_messages = [f'{field}: {msg}' for field, msg in errors.items()]
			# TODO: save validation errors for check functionality
			raise ValueError(f'Invalid metadata element: {", ".join(error_messages)}')

	def _validate_field(self, field_name: str) -> None:
		"""
		Validate an individual field.

		Args:
		    field_name: Name of the field to validate

		Raises:
		    ValueError: If the field validation fails
		"""
		value = self.fields.get(field_name)
		if value is None or (isinstance(value, str) and not value.strip()):
			raise ValueError('This field is required')

	def __str__(self) -> str:
		return self.xml_content

	def to_str(self, *args, **kwargs) -> str:
		return self._printer.to_str(*args, **kwargs)

	def to_xml(self, *args, **kwargs) -> str:
		return self._printer.to_xml(*args, **kwargs)

	def _get_text(self, root: etree.Element, xpath: str) -> str:
		element = root.find(xpath)
		return element.text.strip() if element is not None and element.text else None

	def __getattr__(self, name: str) -> str:
		return self.fields.get(name)

	def to_kv(self) -> str:
		if not self.fields:
			return ''

		max_key_length = max(len(k) for k in self.fields.keys())

		lines = [f'{k.rjust(max_key_length)}: {str(v)}' for k, v in self.fields.items()]

		return '\n'.join(lines)
