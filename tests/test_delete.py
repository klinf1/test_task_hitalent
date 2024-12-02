import csv

from .. import main
from .. import settings


def test_delete_id(get_file):
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
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
        for row in old_data:
            writer.writerow(row)
    params = {'id': int(old_data[0].get('id'))}
    main.TaskManager().delete_tasks(old_data, params, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    error_msg = 'Проверьте, что удаление задания по id работает'
    assert len(reader) == (len(old_data) - 1), error_msg
    error_msg = ('Проверьте, что при удалении задания по id ',
                 'удаляется только выбранное задание')
    assert reader[0] == old_data[1], error_msg


def test_delete_empty_id(get_file):
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
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
        for row in old_data:
            writer.writerow(row)
    params = {'id': 5}
    main.TaskManager().delete_tasks(old_data, params, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    error_msg = ('Проверьте, что при удалении задания по id, ',
                 'если указано несуществующее id, то файл не изменяется')
    assert reader == old_data, error_msg


def test_delete_cat(get_file):
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
            'category': 'test_cat2',
            'date': '02-12-2024',
            'prio': 'низкий',
            'status': 'не выполнено'
        },
        {
            'id': '23',
            'title': 'test_title',
            'description': 'test_desc',
            'category': 'test_cat2',
            'date': '02-12-2024',
            'prio': 'низкий',
            'status': 'не выполнено'
        }
    ]
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
        for row in old_data:
            writer.writerow(row)
    params = {'category': 'test_cat2'}
    main.TaskManager().delete_tasks(old_data, params, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    error_msg = ('Проверьте, что при удалении категории удаляются ',
                 'все задачи из этой категории')
    assert len(reader) == 1, error_msg
    error_msg = 'Проверьте, что при удалении категории удаляются нужные задачи'
    assert reader[0] == old_data[0], error_msg


def test_delete_empty_cat(get_file):
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
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
        for row in old_data:
            writer.writerow(row)
    params = {'category': 'empty'}
    main.TaskManager().delete_tasks(old_data, params, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    error_msg = ('Проверьте, что при удалении задания по категории, ',
                 'если указана несуществующая категория, ',
                 'то файл не изменяется')
    assert reader == old_data, error_msg
