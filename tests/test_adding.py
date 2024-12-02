import csv

import pytest

from .. import main, settings, sorting


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


def test_check_file(get_file, get_wrong_file):
    main.check_file(get_file)
    with open(get_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
    assert fields == settings.FIELD_NAMES, ('Проверьте, что заголовок csv',
                                            ' файла заполняется корректно')
    with pytest.raises(Exception) as e:
        main.check_file(get_wrong_file)
    assert e, ('Проврьте, что при попытке создать файл с ',
               'неверным расширением вызывается исключение')


def test_create_new_correct_task(get_file):
    test_data = [
        '1', 'test_title', 'test_desc', 'test_cat', '02-12-2024', 'высокий'
    ]
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
    main.TaskManager().create_new_task(test_data, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
        print(reader)
    assert len(reader) == 1, ('Проверьте, что при создании',
                              ' задачи она записывается в файл')
    test_data.append('не выполнено')
    error_msg = 'Проверьте, что при записи задачи она записывается корректно'
    assert list(reader[0].values()) == test_data, error_msg


def test_adding_wrong_date(get_file, capsys):
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
    test_data = [
        1, 'test_title', 'test_desc', 'test_cat', 'wrong_date', 'высокий'
    ]
    try:
        main.TaskManager().create_new_task(test_data, get_file)
    except Exception:
        error_msg = ('Проверьте, что при вводе неверной даты',
                     ' пользователю предлагается ввести ее снова')
        assert capsys.readouterr(), error_msg
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 0, ('Проверьте, что задачи с',
                              ' неверной датой не записываются')


def test_adding_wrong_prio(get_file, capsys):
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
    test_data = [
        1, 'test_title', 'test_desc', 'test_cat', '02-12-2024', 'wrong_prio'
    ]
    try:
        main.TaskManager().create_new_task(test_data, get_file)
    except Exception:
        error_msg = ('Проверьте, что при вводе неверного приоритета',
                     ' пользователю предлагается ввести его снова')
        assert capsys.readouterr(), error_msg
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
    assert is_sorted, 'Проверьте, что сортировка работает правильно'


def test_empty(get_file, capsys):
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
    empty_title = [
        1, '', 'test_desc', 'test_cat', '02-12-2024', 'высокий'
    ]
    try:
        main.TaskManager().create_new_task(empty_title, get_file)
    except Exception:
        error_msg = ('Проверьте, что если название не введено,',
                     ' пользователю предлагается ввести его снова')
        assert capsys.readouterr(), error_msg
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 0, ('Проверьте, что задачи без',
                              ' названия не записываются')
    empty_desc = [
        1, 'test_title', '', 'test_cat', '02-12-2024', 'высокий'
    ]
    try:
        main.TaskManager().create_new_task(empty_desc, get_file)
    except Exception:
        error_msg = ('Проверьте, что если описание не введено,',
                     ' пользователю предлагается ввести его снова')
        assert capsys.readouterr(), error_msg
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 0, ('Проверьте, что задачи без',
                              ' описания не записываются')
    empty_cat = [
        1, 'test_title', 'test_desc', '', '02-12-2024', 'выскоий'
    ]
    try:
        main.TaskManager().create_new_task(empty_cat, get_file)
    except Exception:
        error_msg = ('Проверьте, что если категория не введена,',
                     ' пользователю предлагается ввести ее снова')
        assert capsys.readouterr(), error_msg
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    assert len(reader) == 0, ('Проверьте, что задачи',
                              ' без категории не записываются')


def test_create_multiple_tasks(get_file):
    test_data = [
        ['1', 'test_title1', 'test_desc', 'test_cat', '02-12-2024', 'высокий'],
        ['2', 'test_title2', 'test_desc', 'test_cat', '02-12-2024', 'средний'],
        ['3', 'test_title3', 'test_desc', 'test_cat', '02-12-2024', 'низкий'],
    ]
    with open(get_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, settings.FIELD_NAMES)
        writer.writeheader()
    for item in test_data:
        main.TaskManager().create_new_task(item, get_file)
    with open(get_file, 'r', encoding='utf-8', newline='') as f:
        reader = list(csv.DictReader(f))
    error_msg = ('Проверьте, что при наличии задач',
                 ' в файле новые записываются успешно')
    assert len(reader) == len(test_data), error_msg
