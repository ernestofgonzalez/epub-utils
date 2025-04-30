import pytest



@pytest.fixture
def doc_path(tmpdir):
    path = str(tmpdir / "example1.epub")
    return path
