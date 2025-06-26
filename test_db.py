from tinydb import TinyDB, Query
from config import *

db = TinyDB(DB_NAME)
db.drop_tables()

Form = Query()
db.insert_multiple([
    {
        "name": "Данные пользователя",
        "login": "email",
        "tel": "phone"
    },
    {
        "name": "Форма заказа",
        "customer": "text",
        "order_id": "text",
        "дата_заказа": "date",
        "contact": "phone"
    },
    {
        "name": "Проба",
        "f_name1": "email",
        "f_name2": "date"
    }
])

res = db.search(Form.name != '')
print(*res, sep='\n')
