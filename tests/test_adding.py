import builtins
import csv
from unittest import mock

import pytest

from .. import main
from ..constants import FIELD_NAMES


TEST_DATA = [
    {
        'id': '1',
        'title': 'test_title',
        'description': 'test_desc',
        'category': 'test_cat1',
        'date': '02-12-2024',
        'prio': 'низкий',
        'status': 'не выполнено'
    }
]


@pytest.fixture(scope='session')
def get_file(tmpdir_factory):
    filename = str(tmpdir_factory.mktemp('data').join('data.csv'))
    return filename


def test_headers(get_file):
    main.check_headers(get_file)
    with open(get_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
    assert fields == FIELD_NAMES


def test_create_new_task(get_file):
    with mock.patch.object(
        builtins, 'input', lambda _: TEST_DATA[0].get('title')
    ):
        mocked_title = main.AskUser().get_title()
    with mock.patch.object(
        builtins, 'input', lambda _: TEST_DATA[0].get('description')
    ):
        mocked_desc = main.AskUser().get_description()
    with mock.patch.object(
        builtins, 'input', lambda _: TEST_DATA[0].get('category')
    ):
        mocked_cat = main.AskUser().get_category()
    with mock.patch.object(
        builtins, 'input', lambda _: TEST_DATA[0].get('date')
    ):
        mocked_date = main.AskUser().get_date()
    with mock.patch.object(
        builtins, 'input', lambda _: TEST_DATA[0].get('prio')
    ):
        mocked_prio = main.AskUser().get_prio()
    test_task_data = [
        1, mocked_title, mocked_desc, mocked_cat, mocked_date, mocked_prio
    ]
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, FIELD_NAMES)
        writer.writeheader()
    main.TaskManager().create_new_task(test_task_data, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 1
    assert reader[0].get('id') == '1'
    assert reader[0] == TEST_DATA[0]
