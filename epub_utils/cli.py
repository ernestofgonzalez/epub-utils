import click

from epub_utils.doc import Document


VERSION = "0.0.0a3"


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(VERSION)
    ctx.exit()


@click.group(
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option(
    '-v', '--version', 
    is_flag=True, 
    callback=print_version,
    expose_value=False, 
    is_eager=True,
    help='Print epub-utils version.'
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
        '-fmt', '--format',
        type=click.Choice(['text', 'xml', 'kv'], case_sensitive=False),
        default=default,
        help=f"Output format, defaults to {default}."
    )


def output_document_part(doc, part_name, format):
    """Helper function to output document parts in the specified format."""
    part = getattr(doc, part_name)
    if format == 'text':
        click.echo(part.to_str())
    elif format == 'xml':
        click.echo(part.to_xml())
    elif format == 'kv':
        if hasattr(part, 'to_kv') and callable(getattr(part, 'to_kv')):
            click.echo(part.to_kv())
        else:
            click.secho('Key-value format not supported for this document part. Falling back to text:\n', fg="yellow")
            click.echo(part.to_str())


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
        if format == 'text':
            click.echo(content.to_str())
        elif format == 'xml':
            click.echo(content.to_xml())
        elif format == 'kv':
            click.secho('Key-value format not supported for content documents. Falling back to text:\n', fg="yellow")
            click.echo(content.to_str())
    except ValueError as e:
        click.secho(str(e), fg="red", err=True)
        ctx.exit(1)
