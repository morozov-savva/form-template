import re
from argparse import *
from tinydb import TinyDB, Query
from config import *


def parse_args():
    '''Начальный разбор аргументов командной строки.

    Выделяем позиционный аргумент с командой (get_tpl),
    а все остальные аргументы в формате --name=value сохраняем 
    в отдельный словарь'''

    parser = ArgumentParser(
        prog='app.py',
        description='Возвращает имя шаблона формы, если она была найдена'
    )

    parser.add_argument('command', help='Команда', default='get_tpl')

    # Получаем известные и неизвестные аргументы
    args, unknown_args = parser.parse_known_args()

    # Обрабатываем неизвестные аргументы в формате --key value
    extra_args = {}
    key = None
    for item in unknown_args:
        if item.startswith('--'):
            arg = item.lstrip('--')
            if '=' in arg:
                key, value = arg.split('=')
                extra_args[key] = value
        elif not (key is None):
            extra_args[key] += ' ' + item

    return args, extra_args


def value_is_date(value: str) -> bool:
    '''Проверка, что значение является корректной датой'''

    if re.match(r'^([0-9]{2}.[0-9]{2}.[0-9]{4})|([0-9]{4}-[0-9]{2}-[0-9]{2})$', value):
        return True
    return False


def value_is_phone(value: str) -> bool:
    '''Проверка, что значение является корректным номером телефона'''

    if re.match(r'^\+7 [0-9]{3} [0-9]{3} [0-9]{2} [0-9]{2}$', value):
        return True
    return False


def value_is_email(value: str) -> bool:
    '''Проверка, что значение является корректным адресом электронной почты'''

    if re.match(r'^[a-zA-Z_0-9-]+@[a-zA-Z_0-9.-]+$', value):
        return True
    return False


def parse_fields(fields: dict) -> set:
    '''Распознавание типа каждого поля из входных аргументов'''

    res = set()
    for key, value in fields.items():
        if value_is_date(value):
            res.add(f'{key}: date')
        elif value_is_phone(value):
            res.add(f'{key}: phone')
        elif value_is_email(value):
            res.add(f'{key}: email')
        else:
            res.add(f'{key}: text')
    return res


def get_db_forms() -> list:
    '''Загрузка всех форм из БД'''

    db = TinyDB(DB_NAME)
    Form = Query()
    return db.search(Form.name != '')


def search_db_form(fields):
    '''Поиск формы из БД, соответвующей набору входных аргументов'''

    #  Получаем список всех форм из БД
    db_forms = get_db_forms()
    
    # Для каждой формы
    for form in db_forms:
        # Создаём множество названий полей с типом 
        # в формате '<name>: <type>'
        db_fields = set(
            [f'{k}: {v}' for k, v in form.items() if k != 'name'])
        
        # Если множество полей текущей формы из БД
        # является подмножеством полей формы из входных аргументов,
        # то форма найдена, возвращаем её имя
        if db_fields.issubset(fields):
            return form['name']

    # Форма не найдена, возвращаем пустую строку
    return ''


def print_fields(fields: list):
    '''Печать полей формы с типами из входных аргументов'''
    print('{')
    print(*sorted([f'  {x}' for x in fields]), sep=',\n')
    print('}')


if __name__ == "__main__":
    # Разбираем входные аргументы 
    args, fields = parse_args()

    # Если указана команда поиска шаблона формы 
    if args.command == 'get_tpl':
        # Распознаём типы данных, переданных во входных параметрах
        fields = parse_fields(fields)

        # Ищем подходящую форму
        form_name = search_db_form(fields)

        # Если форма найдена, то выводим её название
        if form_name:
            print(form_name)
        else:
            # Иначе выводим поля формы с типами из входных аргументов
            print_fields(fields)

    else:
        print('Неизвестная команда. Доступные команды [\'get_tpl\']')
