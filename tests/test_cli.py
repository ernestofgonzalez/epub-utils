import pytest
from click.testing import CliRunner

from epub_utils import cli


@pytest.mark.parametrize(
	'options',
	(
		['-h'],
		['--help'],
	),
)
def test_help(options):
	result = CliRunner().invoke(cli.main, options)
	assert result.exit_code == 0
	assert result.output.startswith('Usage: ')
	assert '-h, --help' in result.output


@pytest.mark.parametrize(
	'options',
	(
		['-v'],
		['--version'],
	),
)
def test_version(options):
	result = CliRunner().invoke(cli.main, options)
	assert result.exit_code == 0
	assert result.output.strip() == cli.VERSION


def test_files_command_with_file_path_xhtml_xml(doc_path):
	"""Test the files command with XHTML file path in XML format."""
	result = CliRunner().invoke(
		cli.main, [str(doc_path), 'files', 'GoogleDoc/Roads.xhtml', '--format', 'xml']
	)
	assert result.exit_code == 0
	assert len(result.output) > 0


def test_files_command_with_file_path_missing_file(doc_path):
	"""Test the files command with missing file path."""
	result = CliRunner().invoke(cli.main, [str(doc_path), 'files', 'nonexistent/file.xhtml'])
	assert result.exit_code == 1
	assert 'Missing' in result.output


def test_files_command_without_file_path_table(doc_path):
	"""Test the files command without file path (list files) in table format."""
	result = CliRunner().invoke(cli.main, [str(doc_path), 'files', '--format', 'table'])
	assert result.exit_code == 0
	assert len(result.output) > 0
	assert 'Path' in result.output
	assert 'Size' in result.output


def test_files_command_without_file_path_raw(doc_path):
	"""Test the files command without file path (list files) in raw format."""
	result = CliRunner().invoke(cli.main, [str(doc_path), 'files', '--format', 'raw'])
	assert result.exit_code == 0
	assert len(result.output) > 0
	assert 'GoogleDoc/Roads.xhtml' in result.output


def test_toc_command_default(doc_path):
	"""Test the toc command with default behavior (auto-detect)."""
	result = CliRunner().invoke(cli.main, [str(doc_path), 'toc'])
	assert result.exit_code == 0
	assert len(result.output) > 0


def test_toc_command_nav_flag(doc_path):
	"""Test the toc command with --nav flag."""
	result = CliRunner().invoke(cli.main, [str(doc_path), 'toc', '--nav'])
	assert result.exit_code == 0
	assert len(result.output) > 0


def test_toc_command_mutually_exclusive_flags(doc_path):
	"""Test that --ncx and --nav flags are mutually exclusive."""
	result = CliRunner().invoke(cli.main, [str(doc_path), 'toc', '--ncx', '--nav'])
	assert result.exit_code == 1
	assert '--ncx and --nav flags cannot be used together' in result.output
