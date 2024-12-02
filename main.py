import csv
import os

from datetime import datetime

from settings import FIELD_NAMES, RU_TO_ENG, FILE_NAME
from exceptions import FileError
from sorting import sort_tasks


class AskUser():
    '''
    Класс, работающий с пользовательским вводом.

    Если введенные данные не соответствуют указанным
    типам значений, то пользоватю будет выведено сообщение об ошибке
    и предложено ввести значение снова.

    Методы:
        get_title
        get_description
        get_category
        get_date
        get_prio
        get_categories_to_update
        get_title_update
        get_description_update
        get_category_update
        get_date_update
        get_prio_update.
    '''

    title = 'Название\n'
    description = 'Краткое описание\n'
    category = 'Название категории, к которой она относится \n'
    date = 'Дату, к которой её нужно выполнить в формате DD-MM-YYYY\n'
    prio = 'Приоритет: низкий, средний или высокий\n'
    categories_to_update = ('Введите названия полей, которые',
                            ' вы бы хотели изменить через проблел')
    title_update = 'Введите новое название\n'
    description_update = 'Введите новое описание\n'
    category_update = 'Введите новую категорию\n'
    date_update = 'Введите новую дату в формате DD-MM-YYYY\n'
    prio_update = 'Введите новый приоритет - низкий, средний или высокий\n'

    def get_title(self) -> str:
        '''
        Выводит запрос на ввод названия и возвращает введенную строку.

        Если полученный ввод - пустая строка, то выводит сообщение об ошибке
        и предложение ввести название заново.
        '''

        title = input(self.title)
        validated = False
        while validated is False:
            if title != '':
                validated = True
            else:
                print('У задания должно быть название!')
                print('Введите название')
                title = input()
        return title

    def get_description(self) -> str:
        '''
        Выводит запрос на ввод описания и возвращает введенную строку.

        Если полученный ввод - пустая строка, то выводит сообщение об ошибке
        и предложение ввести описание заново.
        '''

        description = input(self.description)
        validated = False
        while validated is False:
            if description != '':
                validated = True
            else:
                print('У задания должно быть описание!')
                print('Введите описание')
                description = input()
        return description

    def get_category(self) -> str:
        '''
        Выводит запрос на ввод категории и возвращает введенную строку.

        Если полученный ввод - пустая строка, то выводит сообщение об ошибке
        и предложение ввести категорию заново.
        '''

        cat = input(self.category)
        validated = False
        while validated is False:
            if cat != '':
                validated = True
            else:
                print('У задания должна быть категория!')
                print('Введите категорию')
                cat = input()
        return cat

    def get_date(self) -> str:
        '''
        Выводит запрос на ввод даты и возвращает введенную строку.

        Если дата не соответствует формату DD-MM-YYYY, то выводит сообщение об
        ошибке и предложение ввести дату заново.
        '''

        validated = False
        date = input(self.date)
        while validated is False:
            try:
                datetime.strptime(date, '%d-%m-%Y').strftime(
                    '%d-%m-%Y'
                )
                validated = True
            except Exception:
                print('Срок выполнения указан неверно!')
                print('Укажите дату, к которой задачу нужно выполнить ',
                      'в формате DD-MM-YYYY')
                date = input()
        return date

    def get_prio(self) -> str:
        '''
        Выводит запрос на ввод приоритета и возвращает введенную строку.

        Если полученный ввод не соответствует заданным значениям,
        то выводит сообщение об ошибке
        и предложение ввести приоритет заново.
        '''

        prio = input(self.prio)
        validated = False
        while validated is False:
            if prio in ['низкий', 'средний', 'высокий']:
                validated = True
            else:
                print('Приоритет может быть низким средним или высоким!')
                print('Введите приоритет')
                prio = input()
        return prio

    def get_categories_to_update(self) -> str:
        '''Выводит запрос на ввод категорий для обновления и
        возвращает введенную строку.
        '''

        print(''.join(i for i in self.categories_to_update))
        return input()

    def get_title_update(self) -> str:
        '''
        Выводит запрос на ввод названия и возвращает введенную строку.

        Если полученный ввод - пустая строка, то выводит сообщение об ошибке
        и предложение ввести название заново.
        '''

        title = input(self.title_update)
        validated = False
        while validated is False:
            if title != '':
                validated = True
            else:
                print('У задания должно быть название!')
                print('Введите название')
                title = input()
        return title

    def get_description_update(self) -> str:
        '''
        Выводит запрос на ввод описания и возвращает введенную строку.

        Если полученный ввод - пустая строка, то выводит сообщение об ошибке
        и предложение ввести описание заново.
        '''

        description = input(self.description_update)
        validated = False
        while validated is False:
            if description != '':
                validated = True
            else:
                print('У задания должно быть описание!')
                print('Введите описание')
                description = input()
        return description

    def get_category_update(self) -> str:
        '''
        Выводит запрос на ввод категории и возвращает введенную строку.

        Если полученный ввод - пустая строка, то выводит сообщение об ошибке
        и предложение ввести категорию заново.
        '''

        cat = input(self.category_update)
        validated = False
        while validated is False:
            if cat != '':
                validated = True
            else:
                print('У задания должна быть категория!')
                print('Введите категорию')
                cat = input()
        return cat

    def get_date_update(self) -> str:
        '''
        Выводит запрос на ввод даты и возвращает введенную строку.

        Если дата не соответствует формату DD-MM-YYYY, то выводит сообщение об
        ошибке и предложение ввести дату заново.
        '''

        validated = False
        date = input(self.date)
        while validated is False:
            try:
                datetime.strptime(date, '%d-%m-%Y').strftime(
                    '%d-%m-%Y'
                )
                validated = True
            except ValueError:
                print('Срок выполнения указан неверно!')
                print('Укажите дату, к которой задачу нужно выполнить ',
                      'в формате DD-MM-YYYY')
                date = input()
        return date

    def get_prio_update(self) -> str:
        '''
        Выводит запрос на ввод приоритета и возвращает введенную строку.

        Если полученный ввод не соответствует заданным значениям,
        то выводит сообщение об ошибке
        и предложение ввести приоритет заново.
        '''

        prio = input(self.prio_update)
        validated = False
        while validated is False:
            if prio in ['низкий', 'средний', 'высокий']:
                validated = True
            else:
                print('Приоритет может быть низким средним или высоким!')
                print('Введите приоритет')
                prio = input()
        return prio

    def input_edited_task(self) -> dict:
        '''
        Получает от пользователя данные, которые нужно обновить в задании.

        Возвращает:
            Данные, представленные в виде словаря, в котором
            ключи - названия полей в файле с данными, а
            значения - введенные пользователем данные.

            Если пользователь вводит название поля, которого
            нет в файле данных, то данное поле не записывается в словарь, а
            пользователю выводится сообщение об этом.
        '''
        params = {}
        categories = self.get_categories_to_update().lower().split()
        for item in categories:
            if item in RU_TO_ENG.keys():
                if item == 'название':
                    params[RU_TO_ENG[item]] = self.get_title_update()
                if item == 'описание':
                    params[RU_TO_ENG[item]] = self.get_description_update()
                if item == 'категория':
                    params[RU_TO_ENG[item]] = self.get_category_update()
                if item == 'срок':
                    params[RU_TO_ENG[item]] = self.get_date_update()
                if item == 'приоритет':
                    params[RU_TO_ENG[item]] = self.get_prio_update()
            else:
                print(f'Такого поля "{item}" не существует, ',
                      'перехожу к следующему')
        return params

    def input_id(self) -> int:
        '''
        Получает от пользователя id задачи.

        Возвращает:
            id, введенное пользователем.

            Если пользователь вводит что-либо, кроме целого числа,
            то выводится сообщение об ошибке и предложение ввести
            корректые данные.
        '''

        id = input('Введите id\n')
        validated = False
        while validated is False:
            try:
                id = int(id)
                validated = True
            except ValueError:
                print('id должно быть целым числом!')
                id = input('Введите id\n')
        return id


class Task():
    '''
    Класс для объектов Task.

    Переменные:
        id: уникально для каждого объекта.
        title: название задания.
        description: краткое описание задания.
        category: категория задания.
        date: дата, к которой нужно выполнить задание.
        prio: приоритет задания, может быть низким, средним, высоким.
        status: статус выполнения задания. По умолчанию: "не выполнено".

    Валидация:
        (title, description, category) не могут быть пустыми строками.
        prio может принимать значения "низкий", "средний", "высокий".
        date может принимать значения дат в формате DD-MM-YYYY.

    Методы:
        get_dict: формирует словарь с данными об экземпляре.
        write_csv: добавляет информацию об экземпляре в файл.
        update_csv: перезаписывает файл c данными, включая данные экземпляра.
    '''

    def __init__(self,
                 id,
                 title: str,
                 description: str,
                 category: str,
                 date: str,
                 prio: str,
                 status='не выполнено',
                 ):
        '''
        Атрибуты:
            id: уникально для каждого объекта.
            title: название задания.
            description: краткое описание задания.
            category: категория задания.
            date: дата, к которой нужно выполнить задание. Дата должна быть
                в формате DD-MM-YYYY.
            prio: приоритет задания. Приритет должен быть
                низким, средним или высоким.
            status: статус выполнения задания. По умолчанию: "не выполнено".
        '''

        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.date = date
        self.prio = prio
        self.status = status

    def get_dict(self) -> dict:
        '''
        Формирует словарь на основе экземпляра класса Task.

        Возвращает:
            словарь, в котором ключи - названия атрибутов, а
            значения - значения атрибутов текущего экземпляра.
        '''
        to_write = {}
        for attr, value in self.__dict__.items():
            to_write[attr.replace('_', '')] = value
        return to_write

    def write_csv(self, filename: str) -> None:
        '''
        Добавляет данные текущего Task в конец файла данных.

        Атрибуты:
            filename - строка с путем к файлу, в который нужно
            записать данные.
        '''

        to_write = self.get_dict()
        with open(filename, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writerow(to_write)

    def update_csv(self, data: list[dict], filename: str) -> None:
        '''
        Обновляет данные в файле.

        Заменяет строку с id = id текущего экземпляра класса.

        Аргументы:
            data: список словарей со всеми данными.
            filename - строка с путем к файлу, в который нужно
            записать данные.
        '''

        to_write = self.get_dict()
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            for row in data:
                if int(row.get('id')) == self.id:
                    row = to_write
                writer.writerow(row)


class TaskManager():
    '''
    Класс для чтения, удаления, и изменения данных в файле.

    Методы:
        get_id
        search_id
        validate_task
        read_all
        create_new_task
        search_params
        delete_tasks
        update_tasks.
    '''

    def search_id(self, data: list[dict], id: int) -> dict | str:
        '''
        Метод для поиска задачи с указанным id.

        Аргументы:
            data: список словарей всех задач.
            id: id задачи, которую необходимо найти.

        Возвращает:
            словарь с данными искомой задачи или строку с
            данными об ошибке.
        '''

        low = 0
        high = len(data) - 1
        mid = 0
        if len(data) == 0:
            return 'Задачи с таким id не существует'
        while high >= low:
            mid = (high + low) // 2
            if int(data[mid].get('id')) < id:
                low = mid + 1
            elif int(data[mid].get('id')) > id:
                high = mid - 1
            else:
                return data[mid]
        return 'Задачи с таким id не существует'

    def read_all(self, filename: str) -> list[dict]:
        '''
        Считывает данные из указанного файла.

        Аргументы:
            filename: путь к файлу с данными.

        Возвращает:
            Все данные из файла в виде списка со словарями, в которых
            ключи - названия полей, а значения - данные строки.
        '''

        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def create_new_task(self, new_task_data: list, filename: str) -> None:
        '''
        Создает экземпляр Task с введенными данными и вызывает
        Task.write_csv

        Аргументы:
            new_task_data: данные новой задачи.
            filename: строка с путем к файлу, в который нужно
            записать данные.
        '''

        task = Task(*new_task_data)
        task.write_csv(filename)

    def search_params(self, data: list[dict], params: dict) -> list[dict]:
        '''
        Метод для поиска задачи по параметрам.

        Поле для поиска передается в params.
        Может осуществлять поиск по категории (ключ словаря 'category'),
        статусу (ключ словаря 'status') и ключевым
        словам (ключ словаря 'keyword').

        Аргументы:
            data: список словарей всех задач
            params(dict): словарь, содержащий возможные варианты поиска

        Возвращает:
            cписок задач, соответствующих поисковому запросу,
            или список со строкой, описывающей ошибку.
        '''

        result = []
        if len(data) == 0:
            result = ['Сейчас нет активных задач']
        for row in data:
            if 'category' in params.keys() and (
                row.get('category') == params.get('category')
            ):
                result.append(row)
            if 'status' in params.keys() and row.get('status') == params.get(
                'status'
            ):
                result.append(row)
            if 'keyword' in params.keys():
                for item in list(row.values())[1:]:
                    if params.get('keyword') in item.lower() and (
                        row not in result
                    ):
                        result.append(row)
        if result == []:
            result = ['Такой задачи не существует']
        return result

    def delete_tasks(
            self,
            data: list[dict],
            params: dict,
            filename: str
            ) -> None:
        '''
        Перезаписывает файл с данными без задачи с указанными параметрами.

        Поддерживает удаление по id, если в параметрах 'id' = <id задачи,
        которую необходимо удалить>, и по категории, если в параметрах
        'category' = <категория, задачи из которой необходимо удалить>.

        Аргументы:
            data: список словарей всех задач.
            params: словарь, содержащий инструкции по удалению.
            filename: строка с путем к файлу, в который нужно
            записать данные.
        '''

        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            for row in data:
                if 'id' in params.keys() and int(row.get('id')) != params.get(
                    'id'
                ):
                    writer.writerow(row)
                if 'category' in params.keys() and row.get(
                    'category'
                ) != params.get('category'):
                    writer.writerow(row)

    def update_tasks(
            self,
            data: list[dict],
            params: dict,
            filename: str,
            ) -> None:
        '''
        Обновляет данные задачи.

        Аргументы:
            data: список словарей всех задач
            params: обновленные данные задачи
            filename: строка с путем к файлу, в который нужно
            записать данные.
        '''
        new_task = Task(*list(params.values()))
        new_task.update_csv(data, filename)
        print('Задача успешно обновлена')

    def get_updated_task(self, task: dict, params: dict) -> dict:
        '''
        Метод для изменения данных в словаре задачи.

        Аргументы:
            task: словарь с данными задачи.
            params: словарь, в котором ключи - названия полей,
            значения которых необходимо изменить.

        Возвращает:
            словарь с обновленными данными задачи.
        '''

        for key in task.keys():
            if key in params.keys():
                task[key] = params.get(key)
        return task


def check_file(filename: str) -> None:
    '''
    Создает и проверяет файл с данными, указанный в настройках.

    Атрибуты:
        filename: путь к файлу

    Вызывает:
        FileError: если указанный в файл не является
        .csv файлом
    '''

    if os.path.splitext(filename)[1] == '.csv':
        if not os.path.isfile(filename):
            with open(filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, FIELD_NAMES)
                writer.writeheader()
    else:
        error_msg = ('Указанный в настройках файл не является .csv файлом!')
        raise FileError(error_msg)


def get_id(data: list[dict]) -> int:
    '''
    Получает id для новой задачи.

    Полученное id на 1 больше id последней записанной задачи.
    Если задача с таким id уже существует или новое полученное id
    не является наибольшим, то сортирует файл с данными
    по возрастанию id, и получает новое id на 1 больше наибольшего.

    Аргументы:
        data: список словарей всех задач

    Возвращает:
        id: число на 1 больше наибольшего id из задач, переданных
        в data
    '''
    if len(data) == 0:
        id = 1
    else:
        id = int(data[-1].get('id')) + 1
        existing_ids = []
        for i in range(0, (len(data))):
            existing_ids.append(int(data[i].get('id')))
        if id <= max(existing_ids):
            data = sort_tasks(data)
            print(f'отсоритрованные данные {data}')
        id = int(data[-1].get('id')) + 1
    return id


def main():
    check_file(FILE_NAME)
    print('Добро пожаловать в менеджер задач!')
    while True:
        data = TaskManager().read_all(FILE_NAME)
        print('Что бы вы хотели сделать? Доступнные варианты: ',
              'Создать, Просмотреть все, Найти по категории, '
              'Найти по статусу, Найти по ключевым словам, ',
              'Найти по id, Изменить, Отметить выполнение',
              'Удалить по id, Удалить категорию ')
        todo = input().lower()
        if todo == 'создать':
            id = get_id(data)
            print('Для создания новой задачи укажите следующие данные:')
            title = AskUser().get_title()
            description = AskUser().get_description()
            category = AskUser().get_category()
            date = AskUser().get_date()
            prio = AskUser().get_prio()
            new_task_data = [id, title, description, category, date, prio,]
            print(new_task_data)
            TaskManager().create_new_task(new_task_data, FILE_NAME)
        elif todo == 'просмотреть все':
            if data == []:
                print('Сейчас нет активных задач')
            for row in data:
                print(row)
        elif todo == 'найти по категории':
            category = input('Введите категорию\n')
            params = {'category': category}
            for item in TaskManager().search_params(data, params):
                print(item)
        elif todo == 'найти по статусу':
            status = input('Введите статус: выполнено или не выполнено\n')
            params = {'status': status.lower()}
            for item in TaskManager().search_params(data, params):
                print(item)
        elif todo == 'найти по ключевым словам':
            keyword = input('Введите ваш запрос\n')
            params = {'keyword': keyword}
            for item in TaskManager().search_params(data, params):
                print(item)
        elif todo == 'найти по id':
            id = AskUser().input_id()
            print(TaskManager().search_id(data, id))
        elif todo == 'изменить':
            id = AskUser().input_id()
            task = TaskManager().search_id(data, id)
            if type(task) is str:
                print(task)
            else:
                print('Доступные для изменения поля: название, '
                      'описание, категория, срок, приоритет')
                params = AskUser().input_edited_task()
                task = TaskManager().get_updated_task(task, params)
                TaskManager().update_tasks(data, task, FILE_NAME)
        elif todo == 'отметить выполнение':
            id = AskUser().input_id()
            task = TaskManager().search_id(data, id)
            if type(task) is str:
                print(task)
            else:
                params = {'status': 'выполнено'}
                task = TaskManager().get_updated_task(task, params)
                TaskManager().update_tasks(data, task, FILE_NAME)
        elif todo == 'удалить по id':
            params = {'id': AskUser().input_id()}
            existing_ids = []
            for item in data:
                existing_ids.append(item.get('id'))
            if params.get('id') in existing_ids:
                TaskManager().delete_tasks(data, params, FILE_NAME)
            else:
                print('Задач с такой категорией нет')
        elif todo == 'удалить категорию':
            print('Введите категорию. Все задачи',
                  ' из этой категории будут удалены')
            params = {'category': input()}
            existing_categories = []
            for item in data:
                existing_categories.append(item.get('category'))
            if params.get('category') in existing_categories:
                TaskManager().delete_tasks(data, params, FILE_NAME)
            else:
                print('Задач с такой категорией нет')
        else:
            print('К сожалению, менеджер не может понять эту комманду')


if __name__ == "__main__":
    main()
