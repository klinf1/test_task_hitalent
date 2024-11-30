import csv
import os

from datetime import datetime

from constants import FIELD_NAMES, RU_TO_ENG, FILE_NAME
from exceptions import (CategoryError, DateError, DescriptionError,
                        PrioError, TitleError)
from sorting import sort_tasks


class Task():
    '''
    Класс для объектов Task

    Атрибуты:
        id: уникально для каждого объекта
        title(str): название задания
        description(str): краткое описание задания
        category(str): категория задания
        date(str): дата, к которой нужно выполнить задание
        prio(str): приоритет задания, может быть низким, средним, высоким
        status(str): статус выполнения задания. По умолчанию: "не выполнено"

    Валидация:
        (title, description, category) не могут быть пустыми строками
        prio может принимать значения "низкий", "средний", "высокий"
        date может принимать значения дат в формате DD-MM-YYYY

    Методы:
        write_csv(): добавляет информацию об объекте Task в файл
            FILE_NAME в текущей директории
        update_csv(data(list[dict])): перезаписывает файл FILE_NAME с
            данными об объекте Task
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
            id: уникально для каждого объекта
            title(str): название задания
            description(str): краткое описание задания
            category(str): категория задания
            date(str): дата, к которой нужно выполнить задание
            prio(str): приоритет задания, может быть низким, средним, высоким
            status(str): статус выполнения задания.
                По умолчанию: "не выполнено"
        '''
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.date = date
        self.prio = prio
        self.status = status

    @property
    def prio(self):
        return self._prio

    @prio.setter
    def prio(self, prio):
        if prio not in ['низкий', 'средний', 'высокий']:
            raise PrioError(
                'Приоритет может быть только низким, средним или высоким'
            )
        self._prio = prio

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if title == '':
            raise TitleError('У задания должно быть название!')
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if description == '':
            raise DescriptionError('У задания должно быть описание!')
        self._description = description

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if category == '':
            raise CategoryError('У задания должна быть категория!')
        self._category = category

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        try:
            datetime.strptime(date, '%d-%m-%Y').strftime(
                '%d-%m-%Y'
            )
        except ValueError:
            raise DateError('Срок выполнения указан неверно!')
        self._date = date

    def get_dict(self) -> dict:
        '''Формирует словарь на основе экземпляра класса Task.'''

        to_write = {}
        for attr, value in self.__dict__.items():
            to_write[attr.replace('_', '')] = value
        return to_write

    def write_csv(self) -> None:
        '''Добавляет данные текущего Task в конец файла FILE_NAME'''

        to_write = self.get_dict()
        with open(FILE_NAME, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writerow(to_write)

    def update_csv(self, data: list[dict]) -> None:
        '''Перезаписывает файл FILE_NAME с данными обновленного Task

        Аргументы:
            data(list[dict]): список словарей со всеми ранее
                записанными задачами
        '''

        to_write = self.get_dict()
        with open(FILE_NAME, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            for row in data:
                if int(row.get('id')) == self.id:
                    row = to_write
                writer.writerow(row)


class TaskManager():
    '''
    Класс для чтения, удаления, и изменения данный в FILENAME

    Методы:
        get_id(data: list[dict]): получает новый уникальный номер id(int)
        search_id(data: list[dict], id(int)): находит задачу с указанным id
        validate_task(params[dict]): проверяет правильность
            введенных пользователем данных
        read_all(): считывает все данные из FILENAME
        create_new_task(data: list[dict]): получает данные для создания
            новой задачи
        search_params(data: list[dict], params: dict): осуществляет поиск по
            параметрам по всем задачам
        delete_tasks(data: list[dict], params: dict): Перезаписывает FILE_NAME
            без задачи с указанными id или категорией.
        update_tasks(data: list[dict], id: int, setcomplete: bool = False):
            обновляет данные о задаче с id=id
    '''

    def get_id(self, data: list[dict]) -> int:
        '''
        Получает новый уникальный id

        Аргументы:
            data(list[dict]): список словарей всех задач

        Возвращает:
            id(int): новый уникальный id
        '''

        if len(data) == 0:
            new_id = 1
        else:
            prev_id = data[-1].get('id')
            new_id = int(prev_id) + 1
            existing_ids = []
            for i in range(0, len(data) - 1):
                existing_ids.append(data[i].get('id'))
            if new_id in existing_ids:
                data = sort_tasks(data)
                new_id = int(data[-1].get('id')) + 1
        return new_id

    def search_id(self, data: list[dict], id: int) -> dict | str:
        '''
        Метод для поиска задачи с указанным id

        Аргументы:
            data(list[dict]): список словарей всех задач
            id(int): id задачи, которую необходимо найти

        Возвращает:
            словарь с данными искомой задачи или строку с
            данными об ошибке
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

    def validate_task(self, params: dict) -> Task:
        '''
        Метод для проверки введенных пользователем данных
        перед записью новой задачи.
        Если данные были введены неверно, изменяет словарь params,
        получая данные от пользователя.

        Аргументы:
            params(dict): словарь, ключи которого - названия полей,
                а значения - данные о новой задаче.

        Возвращает:
            Экземпляр класса Task с подтвержденными данными.
        '''
        validated = False
        while validated is False:
            try:
                task = Task(*list(params.values()))
                validated = True
            except TitleError as e:
                print(e)
                params['title'] = input('Введите название\n')
            except DescriptionError as e:
                print(e)
                print('Введите краткое описание задачи')
                params['description'] = input()
            except PrioError as e:
                print(e)
                print('Введите приоритет: низкий, средний или высокий')
                params['prio'] = input()
            except DateError as e:
                print(e)
                print('Укажите дату, к которой задачу нужно выполнить ',
                      'в формате DD-MM-YYYY')
                params['date'] = input()
            except CategoryError as e:
                print(e)
                print('Укажите название категории, ',
                      'к которой относится задача\n')
                params['category'] = input()
        return task

    def read_all(self) -> list[dict]:
        '''
        Считывает данные из файла FILE_NAME в текущей папке.

        Возвращает:
            список словарей всех задач
        '''

        with open(FILE_NAME, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def create_new_task(self, data: list[dict]) -> None:
        '''
        Получает данные для создания новой задачи от пользователя,
        создает экземпляр класса Task и добавляет новую задачу в конец
        data.csv.

        Аргументы:
            data(list[dict]): список словарей всех задач
        '''

        id = self.get_id(data)
        print('Для создания новой задачи укажите следующие данные:')
        title = input('Название ')
        description = input('Краткое описание ')
        category = input('Название категории, к которой она относится ')
        date = input(
            'Дату, к которой её нужно выполнить в формате DD-MM-YYYY '
        )
        prio = input('Приоритет: низкий, средний или высокий ')
        new_data = [id, title, description, category, date, prio,]
        params = {}
        for i in range(0, len(new_data)):
            params[FIELD_NAMES[i]] = new_data[i]
        task = self.validate_task(params)
        task.write_csv()
        print(f'Задача с id {id} создана успешно')

    def search_params(self, data: list[dict], params: dict) -> list:
        '''
        Метод для поиска по параметрам.

        Аргументы:
            data(list[dict]): список словарей всех задач
            params(dict): словарь, содержащий возможные варианты поиска

        Возможности поиска:
            По категории: ключ словаря 'category'
            По статусу выполнения: ключ словаря 'status'
            По ключевым словам: ключ словаря 'keyword'

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

    def delete_tasks(self, data: list[dict], params: dict) -> None:
        '''
        Перезаписывает FILE_NAME без задачи с указанными id или категорией.

        Аргументы:
            data(list[dict]): список словарей всех задач
            params(dict): словарь, содержащий инструкции по удалению

        Параметры:
            id: удаляет задачу с указанным id
            category: удаляет все задачи в этой категории
        '''

        with open(FILE_NAME, 'w', encoding='utf-8', newline='') as file:
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
            id: int,
            setcomplete: bool = False
            ) -> None:
        '''
        Метод для обновления данных о задаче. Получает
        старую задачу с указанным id, формирует новую задачу и
        записывает ее в FILE_NAME

        Аргументы:
            id(int): id задачи, которую необходимо обновить
            data(list[dict]): список словарей всех задач
            setcomplete(bool, default - False): если передано True,
                метод обновит статус задачи на "выполнено"
        '''

        old_task = self.search_id(data, id)
        if type(old_task) is str:
            print(old_task)
        else:
            if setcomplete:
                old_task['status'] = 'выполнено'
            else:
                print('Доступные для изменения поля: название, '
                      'описание, категория, срок, приоритет')
                print('Введите названия полей, которые',
                      ' вы бы хотели изменить через проблел')
                categories = input().lower().split()
                for item in categories:
                    if item in RU_TO_ENG.keys():
                        old_task[RU_TO_ENG[item]] = input(f'Введите {item} ')
                    else:
                        print(f'Такого поля "{item}" не существует, ',
                              'перехожу к следующему')
            new_task = self.validate_task(old_task)
            new_task.update_csv(data)
            print('Задача успешно обновлена\n',
                  f'{self.search_id(data, id)}')


def input_id() -> int:
    '''
    Функция для получения корректного значения id
    из пользовательского ввода.

    Возвращает:
        id(int): id задачи, с которой необходимо работать.
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


def main():
    if not os.path.isfile('data.csv'):
        with open(FILE_NAME, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, FIELD_NAMES)
            writer.writeheader()
    print('Добро пожаловать в менеджер задач!')
    while True:
        data = TaskManager().read_all()
        print('Что бы вы хотели сделать? Доступнные варианты: ',
              'Создать, Просмотреть все, Найти по категории, '
              'Найти по статусу, Найти по ключевым словам, ',
              'Найти по id, Изменить, Отметить выполнение',
              'Удалить по id, Удалить категорию ')
        todo = input().lower()
        if todo == 'создать':
            TaskManager().create_new_task(data)
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
            id = input_id()
            print(TaskManager().search_id(data, id))
        elif todo == 'изменить':
            id = input_id()
            TaskManager().update_tasks(data, id)
        elif todo == 'отметить выполнение':
            id = input_id()
            TaskManager().update_tasks(data, id, True)
        elif todo == 'удалить по id':
            params = {}
            params['id'] = input_id()
            TaskManager().delete_tasks(data, params)
        elif todo == 'удалить категорию':
            print('Введите категорию. Все задачи',
                  ' из этой категории будут удалены')
            params = {}
            params['category'] = input()
            TaskManager().delete_tasks(data, params)
        else:
            print('К сожалению, менеджер не может понять эту комманду')


if __name__ == "__main__":
    main()
