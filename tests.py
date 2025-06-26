from app import *
import codecs
import subprocess


tests = [
    {
        'cmd': 'python app.py get_tpl --customer=John Smith --дата_заказа=27.05.2025',
        'ans': '''{
  customer: text,
  дата_заказа: date
}
'''
    },
    {
        'cmd': 'python app.py get_tpl --f_name1=aaa@bbb.ru --f_name2=27.05.2025',
        'ans': '''Проба'''
    },
    {
        'cmd': 'python app.py get_tpl --login=vasya --f_name1=aaa@bbb.ru --f_name2=27.05.2025',
        'ans': '''Проба'''
    },
    {
        'cmd': 'python app.py get_tpl --f_name1=aaa@bbb.ru',
        'ans': '''{
  f_name1: email
}
'''
    },
    {
        'cmd': 'python app.py get_tpl --login=vasya --f_name2=27.05.2025',
        'ans': '''{
  f_name2: date,
  login: text
}
'''
    },
    {
        'cmd': 'python app.py get_tpl --f_name1=27.05.2025 --f_name2=+7 903 123 45 78',
        'ans': '''{
  f_name1: date,
  f_name2: phone
}
'''
    },
    {
        'cmd': 'python app.py get_tpl --f_name1=vasya@pukin.ru --f_name2=27.05.2025',
        'ans': '''Проба'''
    },
    {
        'cmd': 'python app.py get_tpl --tumba=27.05.2025 --yumba=+7 903 123 45 78',
        'ans': '''{
  tumba: date,
  yumba: phone
}
'''
    },
]

for test in tests:
    cmd, ans = test['cmd'], codecs.encode(test['ans'], 'cp1251')
    ans = ans.replace(b'\r', b'')
    ans = ans.replace(b'\n', b'')

    res = subprocess.check_output(cmd.split())
    res = res.replace(b'\r', b'')
    res = res.replace(b'\n', b'')

    if res == ans:
        print('OK:', cmd)
    else:
        print('FAIL:', cmd)
        print('    Expected:\n', ans)
        print('    Got:\n', res)