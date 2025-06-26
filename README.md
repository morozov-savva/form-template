# Учебная практика 2П. Практическое задание

## Настройка запуска

Клонируйте репозиторий командой и пререйдите в папку проекта

```bash
git clone https://github.com/morozov-savva/form-template.git
cd form-template
```

Тестовая база данных располагается в файле `db.json`. 

Имя тестовой базы данных можно поменять в файле `config.py` в константе `DB_NAME`.

Для пересоздания и изменения содержимого тестовой базы данных можно внести правки и запустить скрипт `test_db.py`:

```bash
python test_db.py
```

## Тестирование

Для запуска тетирования корректности работы следует запустить скрипт `test.py`:

```bash
python test.py
```

При успешном запуске будут выведены все выполненные команды запуска с `OK` вначале:

```bash
OK: python app.py get_tpl --customer=John Smith --дата_заказа=27.05.2025
OK: python app.py get_tpl --f_name1=aaa@bbb.ru --f_name2=27.05.2025
OK: python app.py get_tpl --login=vasya --f_name1=aaa@bbb.ru --f_name2=27.05.2025
OK: python app.py get_tpl --f_name1=aaa@bbb.ru
OK: python app.py get_tpl --login=vasya --f_name2=27.05.2025
OK: python app.py get_tpl --f_name1=27.05.2025 --f_name2=+7 903 123 45 78
OK: python app.py get_tpl --f_name1=vasya@pukin.ru --f_name2=27.05.2025
OK: python app.py get_tpl --tumba=27.05.2025 --yumba=+7 903 123 45 78
```

## Запуск

Для запуска скрипта приложения `app.py` используйте название команды `get_tpl` после которой будет идти перечисление входных параметров в формате `--<имя>=<значение>`, например:

```bash
python app.py get_tpl --login=vasya --user_email=aaa@bbb.ru --date_birth=27.05.2015
```