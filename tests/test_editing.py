import builtins
import csv
from unittest import mock

import pytest

from .. import main
from ..constants import FIELD_NAMES


@pytest.fixture(scope='session')
def get_file(tmpdir_factory):
    filename = str(tmpdir_factory.mktemp('data').join('data.csv'))
    return filename


