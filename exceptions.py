class PrioError(ValueError):
    '''Вызывается при попытке создать задачу с неверным приоритетом'''

    pass


class DateError(ValueError):
    '''Вызывается при попытке создать задачу с неверной датой'''

    pass


class TitleError(ValueError):
    '''Вызывается при попытке создать задачу с неверным названием'''

    pass


class CategoryError(ValueError):
    '''Вызывается при попытке создать задачу с неверной категорией'''

    pass


class DescriptionError(ValueError):
    '''Вызывается при попытке создать задачу с неверным описанием'''

    pass


class StatusError(ValueError):
    '''Вызывается при попытке создать задачу с неверным статусом'''

    pass


class FileError(Exception):
    '''Вызывается при попытке создать файл с неверным расширением'''

    pass
