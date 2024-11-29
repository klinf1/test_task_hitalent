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


def read_all():
    with open('data.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


def create_new_task():
    print('Для создания новой задачи укажите следующие данные:')
    title = input('Название ')
    description = input('Краткое описание ')
    category = input('Название категории, к которой она относится ')
    due_date = input('Дату, к которой её нужно выполнить ')
    prio = input('Приоритет: низкий, средний или высокий ')
    status = input('Текущий статус выполнения ')
    return [title, description, category, due_date, prio, status]


def get_id(data):
    if len(data) == 0:
        new_id = 1
    else:
        prev_id = data[-1].get('id')
        new_id = int(prev_id) + 1
    return new_id


def search_id(data, id, low, high):
    if low <= high:
        mid = (low + high) // 2
        if int(data[mid].get('id')) == id:
            return [True, mid]
        elif int(data[mid].get('id')) < id:
            return search_id(data, id, mid + 1, high)
        else:
            return search_id(data, id, low, mid - 1)
    return [False]


def main():
    if not os.path.isfile('data.csv'):
        with open('data.csv', 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['id',
                          'title',
                          'description',
                          'category',
                          'due_date',
                          'prio',
                          'status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    all_tasks = read_all()
    search_result = search_id(all_tasks, 3, 0, len(all_tasks)-1)
    if search_result[0] is True:
        print(all_tasks[search_result[1]])


if __name__ == "__main__":
    main()
