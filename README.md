# Lab2DBXml
NonSQL databases, second lab

## Завдання
    Встановити сервер redis.
    Розробити модуль кешування на основі пакету redis-py.
    Підготувати тестові дані (50-100тис. документів MongoDB).
    Реалізувати збереження результатів пошуку в базі даних redis (створити кеш).
    Реалізувати функцію отримання результатів пошуку з кешу, у випадку, коли основна база даних не оновлювалась до створення кешу

### Реалізація

#### Пошук
```
rows = []
        start = datetime.now()
        data = red.hget('employees', request['name'])
        end = datetime.now() - start
        if data:
            print 'loaded from cache'
            print end
            return pickle.loads(data)
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        employees = db.employee_info
        start = datetime.now()
        result = employees.find({'name': re.compile(request['name'], re.IGNORECASE)})
        end = datetime.now() - start
        print 'loaded from mongodb'
        print end
        for employee in result:
            rows.append(employee)
        red.hset('employees', request['name'], pickle.dumps(rows))
        return rows
```

#### Вставка 
```
        employees.insert_one(inserteed_employee)
        hash_data = red.hgetall('employees')
        if hash_data:
            for key in hash_data.keys():
                if key == inserted_employee['name']:
                    red.hdel('employees', key)
```

В redis результати пошуку користувачів по імені. Ключем є ім’я користувавача, значенням - результат вибірки з mongodb. Ключ видаляється з redis, якщо при додаванні нового юзера в mongodb, в redis вже зберігаєтсья такий ключ (ключ в redis - ім’я юзера).
Спочатку пошук відбувається в redis. Якщо пошук в redis не дав результату, відбувається пошук в mongodb. Потім результат пошуку записується в redis і тільки після цього повертає юзеру результати пошуку.


  
