import re
from argparse import *
from tinydb import TinyDB, Query


def parse_args():
    parser = ArgumentParser(
        prog='Form Template Search',
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
    if re.match(r'^([0-9]{2}.[0-9]{2}.[0-9]{4})|([0-9]{4}-[0-9]{2}-[0-9]{2})$', value):
        return True
    return False


def value_is_phone(value: str) -> bool:
    if re.match(r'^\+7 [0-9]{3} [0-9]{3} [0-9]{2} [0-9]{2}$', value):
        return True
    return False


def value_is_email(value: str) -> bool:
    if re.match(r'^[a-zA-Z_0-9-]+@[a-zA-Z_0-9.-]+$', value):
        return True
    return False


def parse_fields(fields: dict) -> set:
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


if __name__ == "__main__":
    args, fields = parse_args()
    if args.command == 'get_tpl':
        fields = parse_fields(fields)

        db = TinyDB('db.json')
        Form = Query()
        res = db.search(Form.name != '')
        for form in res:
            db_fields = set(
                [f'{k}: {v}' for k, v in form.items() if k != 'name'])
            if db_fields.issubset(fields):
                print(form['name'])
                break
        else:
            print('{')
            print(*[f'  {x}' for x in fields], sep='\n')
            print('}')
    else:
        print('Неизвестная команда. Доступные команды [\'get_tpl\']')
