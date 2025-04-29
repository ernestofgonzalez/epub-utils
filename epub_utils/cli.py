import click

import epub_utils


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
    doc = epub_utils.Document(path)