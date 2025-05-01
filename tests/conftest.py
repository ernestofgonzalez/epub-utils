import pytest



@pytest.fixture
def doc_path():
    path = str("tests/assets/roads.epub")
    return path
