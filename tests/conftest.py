import pytest


@pytest.fixture(scope='session')
def get_file(tmpdir_factory):
    filename = str(tmpdir_factory.mktemp('data').join('data.csv'))
    return filename
