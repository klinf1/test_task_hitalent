# Тестовое задание: Менеджер задач
Консольное приложение, позволяющее записывать, читать, изменять и удалять данные о различных задачах пользователя.
Приложение позволяет:
* читать все задачи
* искать задачу по id, статусу выполнения, категории и ключевым словам
* удалять задачи по id
* удалять все задачи из категории
* отмечать задачу как выполненную
* изменять данные задачи
## Установка
1. Сделайте форк репозитория
> 'https://github.com/klinf1/test_task_hitalent/fork'
2. Клонируйте репозиторий на компьютер
> git clone git@github.com:*your github id*/test_task_hitalent.git (*название папки, если хотите чтобы ее название не совпадало с названием репозитория*)
3. Перейдите в папку с проектом
> cd *путь к папке*/test_task_hitalent
4. Создайте и запустите виртуальное окружение
> python -m venv venv
>
> sourse venv/Scripts/activate
5. Установите зависимости
> pip install -r requirements.txt
6. Запустите приложение
> python -m main

## Тестирование
Перед тестированием проверьте, что у вас запущено виртуальное окружение и перейдите в корневую папку проекта!
Для тестирования введите
> pytest -vv
