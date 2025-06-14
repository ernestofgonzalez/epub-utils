"""
Global epub-utils exception classes.

This module defines custom exceptions for the epub-utils library that provide
more descriptive error messages to help users understand what went wrong and
how to fix it.
"""


class EPUBError(Exception):
	"""Base exception for all epub-utils errors."""

	def __init__(self, message: str, suggestions: list = None, file_path: str = None):
		"""
		Initialize the EPUBError.

		Args:
			message: The error message describing what went wrong
			suggestions: Optional list of suggestions for fixing the error
			file_path: Optional path to the file where the error occurred
		"""
		super().__init__(message)
		self.suggestions = suggestions or []
		self.file_path = file_path

	def __str__(self):
		error_parts = [super().__str__()]

		if self.file_path:
			error_parts.append(f'File: {self.file_path}')

		if self.suggestions:
			error_parts.append('Suggestions:')
			for suggestion in self.suggestions:
				error_parts.append(f'  • {suggestion}')

		return '\n'.join(error_parts)


class ParseError(EPUBError, ValueError):
	"""An error when parsing EPUB content due to invalid formatting."""

	def __init__(
		self,
		message: str,
		element_name: str = None,
		line_number: int = None,
		suggestions: list = None,
		file_path: str = None,
	):
		"""
		Initialize the ParseError.

		Args:
			message: The error message
			element_name: The XML element that caused the parsing error
			line_number: The line number where the error occurred
			suggestions: List of suggestions for fixing the error
			file_path: Path to the file with the parsing error
		"""
		if element_name:
			message = f'Error parsing {element_name}: {message}'
		if line_number:
			message = f'{message} (line {line_number})'

		if not suggestions:
			suggestions = [
				'Verify the EPUB file is not corrupted',
				'Check that the XML is well-formed',
				'Ensure all required elements are present',
			]

		super().__init__(message, suggestions, file_path)


class InvalidEPUBError(EPUBError, ValueError):
	"""An error when the EPUB file structure or content is invalid."""

	def __init__(
		self,
		message: str,
		missing_files: list = None,
		suggestions: list = None,
		file_path: str = None,
	):
		"""
		Initialize the InvalidEPUBError.

		Args:
			message: The error message
			missing_files: List of missing required files
			suggestions: List of suggestions for fixing the error
			file_path: Path to the invalid EPUB file
		"""
		if missing_files:
			file_list = ', '.join(missing_files)
			message = f'{message}. Missing required files: {file_list}'

		if not suggestions:
			suggestions = [
				'Verify the file is a valid EPUB archive',
				'Check that all required EPUB files are present',
				'Ensure the EPUB was created with a compliant tool',
			]

		super().__init__(message, suggestions, file_path)


class UnsupportedFormatError(EPUBError, ValueError):
	"""An error when attempting operations not supported for the EPUB version/format."""

	def __init__(
		self,
		message: str,
		epub_version: str = None,
		required_version: str = None,
		suggestions: list = None,
		file_path: str = None,
	):
		"""
		Initialize the UnsupportedFormatError.

		Args:
			message: The error message
			epub_version: The version of the EPUB file
			required_version: The minimum required version for the operation
			suggestions: List of suggestions for fixing the error
			file_path: Path to the EPUB file
		"""
		if epub_version and required_version:
			message = f'{message} (EPUB {epub_version} detected, requires EPUB {required_version})'
		elif epub_version:
			message = f'{message} (EPUB {epub_version} format)'

		if not suggestions:
			suggestions = [
				'Try using an EPUB file with a compatible version',
				'Check the EPUB specification for version requirements',
			]
			if required_version:
				suggestions.insert(0, f'Convert the EPUB to version {required_version} or higher')

		super().__init__(message, suggestions, file_path)


class NotImplementedError(EPUBError):
	"""An error when attempting to use functionality not yet implemented."""

	def __init__(
		self,
		message: str,
		feature_name: str = None,
		suggestions: list = None,
		file_path: str = None,
	):
		"""
		Initialize the NotImplementedError.

		Args:
			message: The error message
			feature_name: Name of the unimplemented feature
			suggestions: List of suggestions for fixing the error
			file_path: Path to the file (if applicable)
		"""
		if feature_name:
			message = f"Feature '{feature_name}' is not yet implemented: {message}"

		if not suggestions:
			suggestions = [
				'Check the documentation for supported features',
				'Consider contributing this feature to the project',
				'Use an alternative approach if available',
			]

		super().__init__(message, suggestions, file_path)


class FileNotFoundError(EPUBError, ValueError):
	"""An error when a required file is not found in the EPUB archive."""

	def __init__(self, file_path: str, epub_path: str = None, suggestions: list = None):
		"""
		Initialize the FileNotFoundError.

		Args:
			file_path: Path to the missing file within the EPUB
			epub_path: Path to the EPUB file
			suggestions: List of suggestions for fixing the error
		"""
		message = f"Missing '{file_path}' in EPUB archive"

		if not suggestions:
			suggestions = [
				'Verify the file path is correct',
				'Check that the EPUB file is complete and not corrupted',
				'Ensure the file was included when the EPUB was created',
			]

		super().__init__(message, suggestions, epub_path)


class ValidationError(EPUBError, ValueError):
	"""An error when EPUB content fails validation."""

	def __init__(
		self,
		message: str,
		validation_errors: list = None,
		suggestions: list = None,
		file_path: str = None,
	):
		"""
		Initialize the ValidationError.

		Args:
			message: The error message
			validation_errors: List of specific validation errors
			suggestions: List of suggestions for fixing the error
			file_path: Path to the file with validation errors
		"""
		if validation_errors:
			error_list = '\n'.join(f'  • {error}' for error in validation_errors)
			message = f'{message}\nValidation errors:\n{error_list}'

		if not suggestions:
			suggestions = [
				'Fix the validation errors listed above',
				'Use an EPUB validator to check for additional issues',
				'Consult the EPUB specification for requirements',
			]

		super().__init__(message, suggestions, file_path)
