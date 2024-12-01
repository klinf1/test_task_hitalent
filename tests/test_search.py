from .. import main


def test_search_id():
    test_data = [
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
        }
    ]
    found = main.TaskManager().search_id(test_data, 1)
    error_msg = 'Проверьте что поиск по id работает правильно'
    assert found == test_data[0], error_msg
    found = main.TaskManager().search_id(test_data, 5)
    error_msg = ('Проверьте, что при попытке найти задачу,',
                 ' id которой нет в файле возвращается сообщение об ошибке')
    assert type(found) is str, error_msg
    found = main.TaskManager().search_id([], 1)
    error_msg = ('Проверьте, что при попытке поиска в пустом файле,',
                 ' возвращается сообщение об ошибке')
    assert type(found) is str, error_msg


def test_search_params():
    test_data = [
        {
            'id': '1',
            'title': 'test_title',
            'description': '999',
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
            'id': '9',
            'title': 'test_title',
            'description': 'Выполнено',
            'category': 'test_cat1',
            'date': '02-12-2024',
            'prio': 'низкий',
            'status': 'не выполнено'
        },
        {
            'id': '10',
            'title': 'test_cat2',
            'description': 'test_desc',
            'category': 'test_cat1',
            'date': '02-12-2024',
            'prio': 'низкий',
            'status': 'выполнено'
        }
    ]
    found = main.TaskManager().search_params(
        test_data, {'category': 'test_cat2'}
    )
    error_msg = 'Проверьте, что поиск по категории работает правильно'
    assert len(found) == 1, error_msg
    assert found[0] == test_data[1], error_msg
    found = main.TaskManager().search_params(
        test_data, {'status': 'выполнено'}
    )
    error_msg = 'Проверьте, что поиск по статусу работает правильно'
    assert len(found) == 1, error_msg
    assert found[0] == test_data[-1], error_msg
    found = main.TaskManager().search_params(
        test_data, {'keyword': '9'}
    )
    error_msg = 'Проверьте, что поиск по ключевым словам не затрагивает id'
    assert len(found) == 1, error_msg
    error_msg = 'Проверьте, что поиск по ключевым словам работает правильно'
    assert found[0] == test_data[0], error_msg
