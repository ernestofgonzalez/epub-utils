import click

from epub_utils.doc import Document

VERSION = '0.1.0a1'


def print_version(ctx, param, value):
	if not value or ctx.resilient_parsing:
		return
	click.echo(VERSION)
	ctx.exit()


@click.group(
	context_settings=dict(help_option_names=['-h', '--help']),
)
@click.option(
	'-v',
	'--version',
	is_flag=True,
	callback=print_version,
	expose_value=False,
	is_eager=True,
	help='Print epub-utils version.',
)
@click.argument(
	'path',
	type=click.Path(exists=True, file_okay=True),
	required=True,
)
@click.pass_context
def main(ctx, path):
	ctx.ensure_object(dict)
	ctx.obj['path'] = path


def format_option(default='xml'):
	"""Reusable decorator for the format option."""
	return click.option(
		'-fmt',
		'--format',
		type=click.Choice(['raw', 'xml', 'plain', 'kv'], case_sensitive=False),
		default=default,
		help=f'Output format, defaults to {default}.',
	)


def pretty_print_option():
	"""Reusable decorator for the pretty-print option."""
	return click.option(
		'-pp',
		'--pretty-print',
		is_flag=True,
		default=False,
		help='Pretty-print XML output (only applies to str and xml format).',
	)


def output_document_part(doc, part_name, format, pretty_print=False):
	"""Helper function to output document parts in the specified format."""
	part = getattr(doc, part_name)
	if format == 'raw':
		click.echo(part.to_str(pretty_print=pretty_print))
	elif format == 'xml':
		click.echo(part.to_xml(pretty_print=pretty_print))
	elif format == 'kv':
		if hasattr(part, 'to_kv') and callable(getattr(part, 'to_kv')):
			click.echo(part.to_kv())
		else:
			click.secho(
				'Key-value format not supported for this document part. Falling back to raw:\n',
				fg='yellow',
			)
			click.echo(part.to_str())


def format_file_size(size_bytes: int) -> str:
	"""Format file size in human-readable format."""
	if size_bytes == 0:
		return '0 B'

	size_names = ['B', 'KB', 'MB', 'GB']
	i = 0
	size = float(size_bytes)

	while size >= 1024.0 and i < len(size_names) - 1:
		size /= 1024.0
		i += 1

	if i == 0:
		return f'{int(size)} {size_names[i]}'
	else:
		return f'{size:.1f} {size_names[i]}'


def format_files_table(files_info: list) -> str:
	"""Format file information as a table."""
	if not files_info:
		return 'No files found in EPUB archive.'

	# Calculate column widths
	max_path_width = max(len(file_info['path']) for file_info in files_info)
	max_size_width = max(len(format_file_size(file_info['size'])) for file_info in files_info)
	max_compressed_width = max(
		len(format_file_size(file_info['compressed_size'])) for file_info in files_info
	)

	# Ensure minimum widths for headers
	path_width = max(max_path_width, len('Path'))
	size_width = max(max_size_width, len('Size'))
	compressed_width = max(max_compressed_width, len('Compressed'))
	modified_width = len('Modified')  # Fixed width for date/time

	# Create header
	header = f'{"Path":<{path_width}} | {"Size":>{size_width}} | {"Compressed":>{compressed_width}} | {"Modified":<{modified_width}}'
	separator = '-' * len(header)

	# Create rows
	rows = []
	for file_info in files_info:
		path = file_info['path'][:path_width]  # Truncate if too long
		size = format_file_size(file_info['size'])
		compressed = format_file_size(file_info['compressed_size'])
		modified = file_info['modified']

		row = f'{path:<{path_width}} | {size:>{size_width}} | {compressed:>{compressed_width}} | {modified:<{modified_width}}'
		rows.append(row)

	# Combine all parts
	result = [header, separator] + rows
	return '\n'.join(result)


@main.command()
@format_option()
@pretty_print_option()
@click.pass_context
def container(ctx, format, pretty_print):
	"""Outputs the container information of the EPUB file."""
	doc = Document(ctx.obj['path'])
	output_document_part(doc, 'container', format, pretty_print)


@main.command()
@format_option()
@pretty_print_option()
@click.pass_context
def package(ctx, format, pretty_print):
	"""Outputs the package information of the EPUB file."""
	doc = Document(ctx.obj['path'])
	output_document_part(doc, 'package', format, pretty_print)


@main.command()
@format_option()
@pretty_print_option()
@click.option(
	'--ncx',
	is_flag=True,
	default=False,
	help='Force retrieval of NCX file (EPUB 2 navigation control file).',
)
@click.option(
	'--nav',
	is_flag=True,
	default=False,
	help='Force retrieval of Navigation Document (EPUB 3 navigation file).',
)
@click.pass_context
def toc(ctx, format, pretty_print, ncx, nav):
	"""Outputs the Table of Contents (TOC) of the EPUB file."""
	doc = Document(ctx.obj['path'])

	if ncx and nav:
		click.secho('Error: --ncx and --nav flags cannot be used together.', fg='red', err=True)
		ctx.exit(1)

	if ncx:
		part = 'ncx'
		if doc.ncx is None:
			click.secho(
				'Error: This document does not include a Navigation Control eXtended (NCX).',
				fg='red',
				err=True,
			)
			ctx.exit(1)
	elif nav:
		part = 'nav'
		if doc.nav is None:
			click.secho(
				'Error: This document does not include an EPUB Navigation Document.',
				fg='red',
				err=True,
			)
			ctx.exit(1)
	else:
		part = 'toc'

	output_document_part(doc, part, format, pretty_print)


@main.command()
@format_option()
@pretty_print_option()
@click.pass_context
def metadata(ctx, format, pretty_print):
	"""Outputs the metadata information from the package file."""
	doc = Document(ctx.obj['path'])
	package = doc.package
	output_document_part(package, 'metadata', format, pretty_print)


@main.command()
@format_option()
@pretty_print_option()
@click.pass_context
def manifest(ctx, format, pretty_print):
	"""Outputs the manifest information from the package file."""
	doc = Document(ctx.obj['path'])
	package = doc.package
	output_document_part(package, 'manifest', format, pretty_print)


@main.command()
@format_option()
@pretty_print_option()
@click.pass_context
def spine(ctx, format, pretty_print):
	"""Outputs the spine information from the package file."""
	doc = Document(ctx.obj['path'])
	package = doc.package
	output_document_part(package, 'spine', format, pretty_print)


@main.command()
@click.argument('item_id', required=True)
@format_option()
@pretty_print_option()
@click.pass_context
def content(ctx, item_id, format, pretty_print):
	"""Outputs the content of a document by its manifest item ID."""
	doc = Document(ctx.obj['path'])

	try:
		content = doc.find_content_by_id(item_id)
		if format == 'raw':
			click.echo(content.to_str())
		elif format == 'xml':
			if hasattr(content, 'to_xml'):
				click.echo(content.to_xml(pretty_print=pretty_print))
			else:
				click.echo(content.to_str())
		elif format == 'plain':
			click.echo(content.to_plain())
		elif format == 'kv':
			click.secho(
				'Key-value format not supported for content documents. Falling back to raw:\n',
				fg='yellow',
			)
			click.echo(content.to_str())
	except ValueError as e:
		click.secho(str(e), fg='red', err=True)
		ctx.exit(1)


@main.command()
@click.argument('file_path', required=False)
@click.option(
	'-fmt',
	'--format',
	type=click.Choice(['table', 'raw', 'xml', 'plain', 'kv'], case_sensitive=False),
	default=None,
	help='Output format. For file listing: table, raw. For file content: raw, xml, plain, kv. Defaults to table for listing, xml for file content.',
)
@pretty_print_option()
@click.pass_context
def files(ctx, file_path, format, pretty_print):
	"""List all files in the EPUB archive with their metadata, or output content of a specific file."""
	doc = Document(ctx.obj['path'])

	# Set dynamic default based on whether file_path is provided
	if format is None:
		format = 'xml' if file_path else 'table'

	if file_path:
		# Display content of specific file
		try:
			content = doc.get_file_by_path(file_path)

			# Handle XHTMLContent objects
			if hasattr(content, 'to_str'):
				if format == 'raw':
					click.echo(content.to_str())
				elif format == 'xml':
					if hasattr(content, 'to_xml'):
						click.echo(content.to_xml(pretty_print=pretty_print))
					else:
						click.echo(content.to_str())
				elif format == 'plain':
					if hasattr(content, 'to_plain'):
						click.echo(content.to_plain())
					else:
						click.echo(content.to_str())
				elif format == 'kv':
					click.secho(
						'Key-value format not supported for file content. Falling back to raw:\n',
						fg='yellow',
					)
					click.echo(content.to_str())
				elif format == 'table':
					# For file content, table format doesn't make sense, fall back to raw
					click.secho(
						'Table format not supported for file content. Falling back to raw:\n',
						fg='yellow',
					)
					click.echo(content.to_str())
			else:
				# Handle raw string content (non-XHTML files)
				click.echo(content)
		except ValueError as e:
			click.secho(str(e), fg='red', err=True)
			ctx.exit(1)
	else:
		# List all files (existing behavior)
		files_info = doc.get_files_info()

		if format == 'table':
			click.echo(format_files_table(files_info))
		elif format == 'raw':
			for file_info in files_info:
				click.echo(f'{file_info["path"]}')
		else:
			# For file listing, only table and raw make sense
			if format in ['xml', 'plain', 'kv']:
				click.secho(
					f'{format.title()} format not supported for file listing. Using table format:\n',
					fg='yellow',
				)
			click.echo(format_files_table(files_info))
