import click
import json

@click.group(
    context_settings=dict(help_option_names=["-h", "--help"]),
)
def main():
    pass

