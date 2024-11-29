import csv
import os


class Task():
    '''
    Класс для объектов Task

    Атрибуты:
    id
        уникально для каждого объекта
    title: str
        название задания
    description: str
        краткое описание задания
    category: str
        категория задания
    due_date: str
        дата, к которой нужно выполнить задание
    prio: str
        приоритетность задания, может быть низким, средним, высоким
    status: str
        статус выполнения задания

    Methods:
    write_csv(): записывает информацию об объекте задания в файл
    data.csv в текущей директории
    '''

    def __init__(self,
                 id,
                 title: str,
                 description: str,
                 category: str,
                 due_date: str,
                 prio: str,
                 status: str):
        '''
        Атрибуты:
        id
            уникально для каждого объекта
        title: str
            название задания
        description: str
            краткое описание задания
        category: str
            категория задания
        due_date: str
            дата, к которой нужно выполнить задание
        prio: str
            приоритетность задания, может быть низким, средним, высоким
        status: str
            статус выполнения задания
        '''
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.prio = prio
        self.status = status

    @property
    def prio(self):
        return self._prio

    @prio.setter
    def prio(self, prio):
        if prio not in ['низкий', 'средний', 'высокий']:
            raise ValueError(
                'Приоритет задачи может быть только низким, средним и высоким!'
            )
        self._prio = prio

    def write_csv(self) -> None:
        '''Writes the current task to a data.csv file
           in the current directory
        '''

        to_write = {}
        for attr, value in self.__dict__.items():
            to_write[attr] = value
        with open('data.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=to_write.keys())
            writer.writerow(to_write)


def read_all() -> list[dict]:
    '''
    Считывает данные из файла data.csv в текущей папке.
    Возвращает:
       list[dict] со всеми строками из файла
    '''

    with open('data.csv', 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


def create_new_task() -> list:
    '''
    Получает данные для создания новой задачи от пользователя.

    Возвращает:
        список для формирования новой задачи.
    '''

    print('Для создания новой задачи укажите следующие данные:')
    title = input('Название ')
    description = input('Краткое описание ')
    category = input('Название категории, к которой она относится ')
    due_date = input('Дату, к которой её нужно выполнить ')
    prio = input('Приоритет: низкий, средний или высокий ')
    status = input('Текущий статус выполнения ')
    return [title, description, category, due_date, prio, status]


def get_id(data: list) -> int:
    '''
    Генерирует новое уникальное id для задачи, основываясь на предыдущем
    наибольшем id.

    Аргументы:
        data(list): список всех текущих задач.

    Возвращает:
        новое уникальное id(int).
    '''

    if len(data) == 0:
        new_id = 1
    else:
        prev_id = data[-1].get('id')
        new_id = int(prev_id) + 1
    return new_id


def search_id(data: list[dict], id: int, low: int, high: int) -> list:
    '''
    Осуществляет бинарный поиск по сортированному списку задач
    для поиска задачи с заданным id.

    Аргументы:
        data(list[dict]): список, состоящий из словарей всех текущих задач
        id(int): id задачи, которую необходимо найти
        low(int): наименьший индекс поискового интервала
        high(int): наибольший индекс поискового интервала

    Вовращает:
        Список [True, задача с искомым id] либо [False],
        если задача не найдена
    '''

    if low <= high:
        mid = (low + high) // 2
        if int(data[mid].get('id')) == id:
            return [True, data[mid]]
        elif int(data[mid].get('id')) < id:
            return search_id(data, id, mid + 1, high)
        else:
            return search_id(data, id, low, mid - 1)
    return [False]


def search_params(data: list[dict], params: dict):
    '''
    Функция для поиска по параметрам.

    Аргументы:
        data(list[dict]): список, состоящий из словарей всех текущих задач
        params(dict): словарь, содержащий возможные варианты поиска

    Возможности поиска:
        По категории: ключ словаря 'category'
        По статусу выполнения: ключ словаря 'status'
        По ключевым словам: ключ словаря 'keyword'

    Возвращает набор задач, соответствующих поисковому запросу
    '''

    result = []
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
            for item in row.values():
                if item == params.get('keyword'):
                    result.append(row)
    return set(result)


def delete_by_id(data: list[dict], id: int, field_names: list) -> None:
    '''
    Перезаписывает data.csv без задачи с указанным id.

    Аргументы:
        data(list[dict]): список со словарями с информацией о всех задачах
        id(int): id задачи, которую необходимо удалить
        field_names(list): список параметров задачи
    '''

    with open('data.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for row in data:
            if int(row.get('id')) != id:
                writer.writerow(row)


def main():
    fieldnames = ['id',
                  'title',
                  'description',
                  'category',
                  'due_date',
                  'prio',
                  'status']
    if not os.path.isfile('data.csv'):
        with open('data.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()


if __name__ == "__main__":
    main()
