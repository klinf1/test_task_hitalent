import pytest


@pytest.fixture(scope='session')
def get_file(tmpdir_factory):
    filename = str(tmpdir_factory.mktemp('data').join('data.csv'))
    return filename


@pytest.fixture(scope='session')
def get_wrong_file(tmpdir_factory):
    filename = str(tmpdir_factory.mktemp('data').join('wrong.file'))
    return filename
