import csv
import os

from datetime import datetime

from constants import FIELD_NAMES, RU_TO_ENG
from exceptions import (CategoryError, DateError, DescriptionError,
                        PrioError, TitleError)


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
            data.csv в текущей директории
        update_csv(data(list[dict])): перезаписывает файл data.csv с
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
            status(str): статус выполнения задания
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
        '''Добавляет данные текущего Task в конец файла data.csv'''

        to_write = self.get_dict()
        with open('data.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writerow(to_write)

    def update_csv(self, data: list[dict]) -> None:
        '''Перезаписывает файл data.csv с данными обновленного Task

        Аргументы:
            data(list[dict]): список словарей со всеми ранее
                записанными задачами
        '''

        to_write = self.get_dict()
        with open('data.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            for row in data:
                if int(row.get('id')) == self.id:
                    row = to_write
                writer.writerow(row)


def read_all() -> list[dict]:
    '''
    Считывает данные из файла data.csv в текущей папке.
    Возвращает:
       list[dict] со всеми строками из файла
    '''

    with open('data.csv', 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


def get_id() -> int:
    '''
    Генерирует новое уникальное id для задачи, основываясь на предыдущем
    наибольшем id.

    Аргументы:
        data(list): список всех текущих задач.

    Возвращает:
        новое уникальное id(int).
    '''

    data = read_all()
    if len(data) == 0:
        new_id = 1
    else:
        prev_id = data[-1].get('id')
        new_id = int(prev_id) + 1
    return new_id


def validate_task(params: dict) -> Task:
    '''
    Функция для проверки введенных пользователем данных
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
            params['description'] = input('Введите краткое описание задачи\n')
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
            print('Укажите название категории, к которой относится задача\n')
            params['category'] = input()
    return task


def create_new_task(id: int) -> list:
    '''
    Получает данные для создания новой задачи от пользователя,
    создает экземпляр класса Task и добавляет новую задачу в конец
    data.csv.
    '''

    print('Для создания новой задачи укажите следующие данные:')
    title = input('Название ')
    description = input('Краткое описание ')
    category = input('Название категории, к которой она относится ')
    date = input(
        'Дату, к которой её нужно выполнить в формате DD-MM-YYYY '
    )
    prio = input('Приоритет: низкий, средний или высокий ')
    data = [id, title, description, category, date, prio,]
    params = {}
    for i in range(0, len(data)):
        params[FIELD_NAMES[i]] = data[i]
    task = validate_task(params)
    task.write_csv()
    print(f'Задача с id {id} создана успешно')


def search_id(data: list[dict], id: int) -> list:
    '''
    Осуществляет бинарный поиск по сортированному списку задач
    для поиска задачи с заданным id.

    Аргументы:
        data(list[dict]): список, состоящий из словарей всех текущих задач
        id(int): id задачи, которую необходимо найти

    Вовращает:
        задачу с искомым id либо строку с описанием ошибки,
        если задача не найдена
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


def search_params(data: list[dict], params: dict) -> list:
    '''
    Функция для поиска по параметрам.

    Аргументы:
        data(list[dict]): список, состоящий из словарей всех текущих задач
        params(dict): словарь, содержащий возможные варианты поиска

    Возможности поиска:
        По категории: ключ словаря 'category'
        По статусу выполнения: ключ словаря 'status'
        По ключевым словам: ключ словаря 'keyword'

    Возвращает cписок задач, соответствующих поисковому запросу,
    или список со строкой, описывающей ошибку.
    '''

    result = []
    if len(data) == 0:
        result = ['Сейчас нет активных задач']
    for row in data:
        if 'category' in params.keys() and row.get('category') == params.get(
            'category'
        ):
            result.append(row)
        if 'status' in params.keys() and row.get('status') == params.get(
            'status'
        ):
            result.append(row)
        if 'keyword' in params.keys():
            for item in list(row.values())[1:]:
                if params.get('keyword') in item.lower() and row not in result:
                    result.append(row)
    if result == []:
        result = ['Такой задачи не существует']
    return result


def delete_tasks(data: list[dict], params: dict) -> None:
    '''
    Перезаписывает data.csv без задачи с указанными id или категорией.

    Аргументы:
        data(list[dict]): список со словарями с информацией о всех задачах
        params(dict): словарь, содержащий инструкции по удалению

    Параметры:
        id: удаляет задачу с указанным id
        category: удаляет все задачи в этой категории
    '''

    with open('data.csv', 'w', encoding='utf-8', newline='') as file:
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


def update_tasks(id: int, data: list[dict], setcomplete: bool = False) -> None:
    '''Функция для обновления данных о задаче. Получает
    старую задачу с указанным id, формирует новую задачу и
    записывает ее в data.csv

    Аргументы:
        id(int): id задачи, которую необходимо обновить
        data(list[dict]): список словарей с данными о всех задачах
        setcomplete(bool, default - False): если передано True,
            функция обновит статус задачи на "выполнено"
    '''

    old_task = search_id(data, id)
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
        new_task = validate_task(old_task)
        new_task.update_csv(data)
        print('Задача успешно обновлена\n',
              f'{search_id(data, id, 0, len(data))}')


def input_id() -> int:
    '''
    Функция для получения корректного значения id
    из пользовательского ввода.

    Возвращаяет:
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
        with open('data.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, FIELD_NAMES)
            writer.writeheader()
    print('Добро пожаловать в менеджер задач!')
    while True:
        data = read_all()
        print('Что бы вы хотели сделать? Доступнные варианты: ',
              'Создать, Просмотреть все, Найти по категории, '
              'Найти по статусу, Найти по ключевым словам, ',
              'Найти по id, Изменить, Отметить выполнение',
              'Удалить по id, Удалить категорию ')
        todo = input().lower()
        if todo == 'создать':
            create_new_task(get_id())
        elif todo == 'просмотреть все':
            if data == []:
                print('Сейчас нет активных задач')
            for row in data:
                print(row)
        elif todo == 'найти по категории':
            category = input('Введите категорию\n')
            params = {'category': category}
            for item in search_params(data, params):
                print(item)
        elif todo == 'найти по статусу':
            status = input('Введите статус: выполнено или не выполнено\n')
            params = {'status': status.lower()}
            for item in search_params(data, params):
                print(item)
        elif todo == 'найти по ключевым словам':
            keyword = input('Введите ваш запрос\n')
            params = {'keyword': keyword}
            for item in search_params(data, params):
                print(item)
        elif todo == 'найти по id':
            id = input_id()
            print(search_id(data, id))
        elif todo == 'изменить':
            id = input_id()
            update_tasks(id, data)
        elif todo == 'отметить выполнение':
            id = input_id()
            update_tasks(id, data, True)
        elif todo == 'удалить по id':
            id = input_id()
            delete_tasks(data, {'id': id})
        elif todo == 'удалить категорию':
            print('Введите категорию. Все задачи',
                  ' из этой категории будут удалены')
            category = input()
            delete_tasks(data, {'category': category})
        else:
            print('К сожалению, менеджер не может понять эту комманду')


if __name__ == "__main__":
    main()
