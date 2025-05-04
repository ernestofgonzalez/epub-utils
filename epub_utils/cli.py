import click

from epub_utils.doc import Document


VERSION = "0.0.0a2"


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


@main.command()
@format_option()
@click.pass_context
def container(ctx, format):
    """Outputs the container information of the EPUB file."""
    path = ctx.obj['path']
    doc = Document(path)
    if format == 'text':
        click.echo(doc.container.tostring())
    elif format == 'xml':
        click.echo(doc.container.toxml())


@main.command()
@format_option()
@click.pass_context
def package(ctx, format):
    """Outputs the package information of the EPUB file."""
    path = ctx.obj['path']
    doc = Document(path)
    if format == 'text':
        click.echo(doc.package.tostring())
    elif format == 'xml':
        click.echo(doc.package.toxml())


@main.command()
@click.pass_context
def toc(ctx):
    """Outputs the Table of Contents (TOC) of the EPUB file."""
    path = ctx.obj['path']
    doc = Document(path)
    click.echo(doc.toc)
