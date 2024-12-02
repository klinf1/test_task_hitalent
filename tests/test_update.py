import builtins
import csv
import pytest

from unittest import mock

from .. import main
from ..settings import FIELD_NAMES


def test_get_updated_task():
    test_task = {
        'id': '1',
        'title': 'test_title',
        'description': 'test_desc',
        'category': 'test_cat1',
        'date': '02-12-2024',
        'prio': 'низкий',
        'status': 'не выполнено'
    }
    test_params = {'title': 'new_title'}
    edited_task = main.TaskManager().get_updated_task(test_task, test_params)
    assert edited_task.get('title') == test_params.get('title')


def test_update_tasks(get_file):
    old_data = [
        {
            'id': '1',
            'title': 'test_title',
            'description': 'test_desc',
            'category': 'test_cat1',
            'date': '02-12-2024',
            'prio': 'низкий',
            'status': 'не выполнено'
        },
        {
            'id': '2',
            'title': 'test_title',
            'description': 'test_desc',
            'category': 'test_cat1',
            'date': '02-12-2024',
            'prio': 'низкий',
            'status': 'не выполнено'
        }
    ]
    new_task = {
        'id': 1,
        'title': 'new_title',
        'description': 'test_desc',
        'category': 'test_cat1',
        'date': '02-12-2024',
        'prio': 'низкий',
        'status': 'не выполнено'
    }
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, FIELD_NAMES)
        writer.writeheader()
        for row in old_data:
            writer.writerow(row)
    main.TaskManager().update_tasks(old_data, new_task, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    new_task['id'] = str(new_task['id'])
    error_msg = 'Проверьте, что update_task действительно изменяет задание'
    assert reader[0] == new_task, error_msg
    error_msg = 'Проверьте, что update_task изменяет только выбранное задание'
    assert reader[1] == old_data[1], error_msg


def test_Input_updating_to_wrong_date():
    with mock.patch.object(
        builtins, 'input', lambda _: '123'
    ), pytest.raises(Exception):
        main.AskUser().get_date_update()


def test_inputing_updating_to_wrong_prio():
    with mock.patch.object(
        builtins, 'input', lambda _: 'wrong_prio'
    ), pytest.raises(Exception):
        main.AskUser().get_prio_update()


def test_update_to_empty():
    with mock.patch.object(
        builtins, 'input', lambda _: ''
    ), pytest.raises(Exception):
        main.AskUser().get_title_update()
        main.AskUser().get_category_update()
        main.AskUser().get_description_update()
