import click

from epub_utils.doc import Document
from epub_utils.highlighters import highlight_xml

VERSION = "0.0.0a1"


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
        help=f"Output format (default: {default})"
    )


@main.command()
@format_option()
@click.pass_context
def container(ctx, format):
    """Outputs the container information of the EPUB file."""
    path = ctx.obj['path']
    doc = Document(path)
    if format == 'text':
        click.echo(doc.container)
    elif format == 'xml':
        click.echo(highlight_xml(doc.container.xml_content))


@main.command()
@format_option()
@click.pass_context
def package(ctx, format):
    """Outputs the package information of the EPUB file."""
    path = ctx.obj['path']
    doc = Document(path)
    if format == 'text':
        click.echo(doc.package.xml_content)
    elif format == 'xml':
        click.echo(highlight_xml(doc.package.xml_content))


@main.command()
@click.pass_context
def toc(ctx):
    """Outputs the Table of Contents (TOC) of the EPUB file."""
    path = ctx.obj['path']
    doc = Document(path)
    click.echo(doc.toc)
