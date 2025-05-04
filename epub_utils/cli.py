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
        type=click.Choice(['text', 'xml'], case_sensitive=False),
        default=default,
        help=f"Output format, defaults to {default}."
    )


def output_document_part(doc, part_name, format):
    """Helper function to output document parts in the specified format."""
    part = getattr(doc, part_name)
    if format == 'text':
        click.echo(part.tostring())
    elif format == 'xml':
        click.echo(part.toxml())


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
