import builtins
import csv
from unittest import mock

import pytest

from .. import main, sorting
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
    assert fields == FIELD_NAMES, ('Проверьте, что заголовок csv',
                                   ' файла заполняется корректно')


def test_create_new_correct_task(get_file):
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
    assert len(reader) == 1, ('Проверьте, что при создании',
                              ' задачи она записывается в файл')
    assert reader[0] == TEST_DATA[0], ('Проверьте, что при записи ',
                                       'задачи она записывается корректно')


def test_adding_wrong_date(get_file, capsys):
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, FIELD_NAMES)
        writer.writeheader()
    test_data = [
        1, 'test_title', 'test_desc', 'test_cat', 'wrong_date', 'высокий'
    ]
    try:
        main.TaskManager().create_new_task(test_data, get_file)
    except Exception:
        assert capsys.readouterr(), ('Проверьте, что при вводе неверной даты',
                                     ' пользователю предлагается',
                                     ' ввести дату снова')
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 0, ('Проверьте, что задачи с',
                              ' неверной датой не записываются')


def test_adding_wrong_prio(get_file, capsys):
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, FIELD_NAMES)
        writer.writeheader()
    test_data = [
        1, 'test_title', 'test_desc', 'test_cat', '02-12-2024', 'wrong_prio'
    ]
    try:
        main.TaskManager().create_new_task(test_data, get_file)
    except Exception:
        assert capsys.readouterr(), ('Проверьте, что при вводе неверного ',
                                     'приоритета пользователю предлагается',
                                     ' ввести его снова')
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 0, ('Проверьте, что задачи с',
                              ' неверным приоритетом не записываются')


def test_get_id():
    id = main.get_id(TEST_DATA)
    assert id == 2, ('Проверьте, что при получении нового id ',
                     'новое значение на 1 больше предыдущего')
    id_testing = [
        {
            'id': '2',
            'title': 'test_title',
            'description': 'test_desc',
            'category': 'test_cat1',
            'date': '02-12-2024',
            'prio': 'низкий',
            'status': 'не выполнено'
        },
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
    id = main.get_id(id_testing)
    assert id == 3, ('Проверьте, что при ошибке в записи файлов ',
                     'новое значение id на 1 больше наибольшего')


def test_sorting():
    sort_testing = [
        {'id': '2'}, {'id': '1'}, {'id': '124987327'},
        {'id': '21'}, {'id': '123'}
    ]
    sorted = sorting.sort_tasks(sort_testing)
    id_list = []
    for item in sorted:
        id_list.append(int(item.get('id')))
    is_sorted = all(
        id_list[i] <= id_list[i + 1] for i in range(len(id_list) - 1)
    )
    assert is_sorted is True, 'Проверьте, что сортировка работает правильно'
