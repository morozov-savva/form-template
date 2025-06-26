from tinydb import TinyDB, Query

db = TinyDB('db.json')
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
    }
])
res = db.search(Form.name != '')
print(res)
