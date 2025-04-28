import pytest
from click.testing import CliRunner
from epub_utils import cli


@pytest.mark.parametrize(
    "options",
    (
        ["-h"],
        ["--help"],
    ),
)
def test_help(options):
    result = CliRunner().invoke(cli.main, options)
    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")
    assert "-h, --help" in result.output
