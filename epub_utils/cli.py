import click
from epub_utils.doc import Document  # Import the Document class from the C extension

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
def main():
    pass

@main.command()
@click.argument(
    'path', 
    type=click.Path(exists=True, file_okay=True),
    required=True,
)
def toc(path):
    """Outputs the Table of Contents (TOC) of the EPUB file."""
    doc = Document(path)  # Instantiate the Document class
    click.echo(doc.get_toc())  # Call the get_toc method and print the result