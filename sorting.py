def merge(left: list[dict], right: list[dict]):
    '''
    Функция для слияния двух сортированных списков задач и
    формирования общего сортированного списка словарей задач.

    Аргументы:
        left(list[dict]), right(list[dict]): подсписки задач

    Возвращает:
        list[dict]: сортированный объединенный список словарей задач
    '''

    if len(left) == 0:
        return right
    if len(right) == 0:
        return left
    result = []
    index_left = index_right = 0
    while len(result) < (len(left) + len(right)):
        if int(left[index_left].get('id')) <= int(right[index_right].get(
            'id'
        )):
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1
        if index_right == len(right):
            result += left[index_left:]
            break
        if index_left == len(left):
            result += right[index_right:]
            break
    return result


def insertion_sort(data: list[dict], left: int, right: int) -> list[dict]:
    '''
    Функция для сортировки заданной части списка вставкой.

    Аргументы:
        data(list[dict]): cписок словарей задач
        left, right(int): индексы, в рамках которых необходимо
        сортировать список

    Возвращает:
        list[dict]: отсортированный по id в указанных
        рамках список словарей задач
    '''

    for i in range(left + 1, right + 1):
        key = data[i]
        j = i - 1
        while j >= left and int(data[j].get('id')) > int(key.get('id')):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data
