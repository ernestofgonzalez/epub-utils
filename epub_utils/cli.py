import click

from epub_utils.doc import Document

VERSION = '0.0.0a4'


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


def output_document_part(doc, part_name, format):
	"""Helper function to output document parts in the specified format."""
	part = getattr(doc, part_name)
	if format == 'raw':
		click.echo(part.to_str())
	elif format == 'xml':
		click.echo(part.to_xml())
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
@click.pass_context
def container(ctx, format):
	"""Outputs the container information of the EPUB file."""
	doc = Document(ctx.obj['path'])
	output_document_part(doc, 'container', format)


@main.command()
@format_option()
@click.pass_context
def package(ctx, format):
	"""Outputs the package information of the EPUB file."""
	doc = Document(ctx.obj['path'])
	output_document_part(doc, 'package', format)


@main.command()
@format_option()
@click.pass_context
def toc(ctx, format):
	"""Outputs the Table of Contents (TOC) of the EPUB file."""
	doc = Document(ctx.obj['path'])
	output_document_part(doc, 'toc', format)


@main.command()
@format_option()
@click.pass_context
def metadata(ctx, format):
	"""Outputs the metadata information from the package file."""
	doc = Document(ctx.obj['path'])
	package = doc.package
	output_document_part(package, 'metadata', format)


@main.command()
@format_option()
@click.pass_context
def manifest(ctx, format):
	"""Outputs the manifest information from the package file."""
	doc = Document(ctx.obj['path'])
	package = doc.package
	output_document_part(package, 'manifest', format)


@main.command()
@format_option()
@click.pass_context
def spine(ctx, format):
	"""Outputs the spine information from the package file."""
	doc = Document(ctx.obj['path'])
	package = doc.package
	output_document_part(package, 'spine', format)


@main.command()
@click.argument('item_id', required=True)
@format_option()
@click.pass_context
def content(ctx, item_id, format):
	"""Outputs the content of a document by its manifest item ID."""
	doc = Document(ctx.obj['path'])

	try:
		content = doc.find_content_by_id(item_id)
		if format == 'raw':
			click.echo(content.to_str())
		elif format == 'xml':
			click.echo(content.to_xml())
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
@click.option(
	'-fmt',
	'--format',
	type=click.Choice(['table', 'raw'], case_sensitive=False),
	default='table',
	help='Output format, defaults to table.',
)
@click.pass_context
def files(ctx, format):
	"""List all files in the EPUB archive with their metadata."""
	doc = Document(ctx.obj['path'])
	files_info = doc.get_files_info()

	if format == 'table':
		click.echo(format_files_table(files_info))
	elif format == 'raw':
		for file_info in files_info:
			click.echo(f'{file_info["path"]}')
	else:
		click.echo(format_files_table(files_info))
