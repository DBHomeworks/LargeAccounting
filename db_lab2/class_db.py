import sys
import MySQLdb as mydb
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from bson.code import Code
import re
import redis
import pickle
import random
from datetime import date

red = redis.StrictRedis(host='localhost', port=6379, db=0)

class MyDataDase:

    def __init__(self):
        red.flushall()

    def ShowAllInfo(self):
        rows = []
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        employees = db.employee_info
        for employee in employees.find().sort('id').limit(50):
            rows.append(employee)
        return rows

    def Accounting(self):
        rows = []
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        visits = db.visiting
        for visit in visits.find():
            employee = client.attendance_records.employee_info.find_one({'_id': ObjectId(visit['employee'])})
            rows.append({'id' : visit['_id'], 'employee' : employee, 'date' : visit['date']})

        return rows

    def GetVisitingById(self, _id):
        rows = []

        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        visits = db.visiting

        for v in visits.find({'_id' : ObjectId(_id)}):
            rows.append({'visit_id' : v['_id'], 'employee' : v['employee'], 'date' : v['date']})

        print rows
        return rows

    def GetEmployeeObjectId(self, id):
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        employees = db.employee_info
        for employee in employees.find():
            if employee['id'] == id:
                inserted_id = employee['_id']
                return inserted_id

    def AddVisiting(self, request):
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        visits = db.visiting

        employee_object_id = self.GetEmployeeObjectId(int(request['employee_id']))

        date = request["date"]
        date = datetime.strptime(date, '%Y-%m-%d')

        visits.insert_one({'date' : date, 'employee' : ObjectId(employee_object_id)})

    def DeleteVisiting(self, request):
        # print request['visit_id']
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        visits = db.visiting
        result = visits.delete_many({"_id" : ObjectId(request['visit_id'])})

    def DateSearch(self ,request):
        con = None
        rows = None

        try:
            con = mydb.connect( self.host, self.db_user_name, self.password, self.db_name);
            cur = con.cursor()
            cur.execute("SELECT EmployeeInfo.employee_id, EmployeeInfo.employee_name, EmployeeInfo.date_of_birthday, EmployeeInfo.family, "
                        "WorkPlace.position, WorkPlace.salary, WorkPlace.comp_auto, WorkPlace.start_of_working, Company.company_name "
                        "FROM EmployeeInfo "
                        "JOIN WorkPlace ON EmployeeInfo.workplace_id=WorkPlace.workplace_id "
                        "JOIN Company ON WorkPlace.company_id=Company.company_id "
                        "WHERE DATE(EmployeeInfo.date_of_birthday) BETWEEN '" + request["from"] + "' AND '" + request["to"] + "';")
            rows = cur.fetchall()

            con.commit()

        except mydb.Error, e:

            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)

        finally:
            if con:
                con.close
            return rows

    def ExactlySearch(self, request):
        rows = []
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        employees = db.employee_info
        for employee in employees.find({"workplace.company" : request['name']}).sort('id'):
            rows.append(employee)
        return rows

    def BooleanModeSearch(self, request):
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

        serializable_data = []
        # for row in rows:
        #     row['_id'] = str(row['_id'])
        #     serializable_data.append(row)
        red.hset('employees', request['name'], pickle.dumps(rows))
        return rows

    def EditVisit(self, request):
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        visits = db.visiting

        date = datetime.strptime(request['date'], '%Y-%m-%d')
        employee_object_id = self.GetEmployeeObjectId(int(request['employee_id']))

        print request['visit_id']
        print date, ' ', type(date)
        print employee_object_id

        visit = {'employee' : ObjectId(employee_object_id), 'date' : date}
        visits.update({'_id' : ObjectId(request['visit_id'])}, {"$set" : visit}, upsert=False)

    def GetCompaniesSalary(self):
        rows = []
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        collection = db.companies_salaries
        for element in collection.find():
            rows.append({'company_name' : element['_id'], 'salary' : element['salary']})
        return rows

    def GetInterests(self):
        rows = []
        client = MongoClient('localhost', 27017)
        db = client.attendance_records

        map = Code("function map() { "
                "for(var i in this.interests) { "
                    "emit(this.interests[i], 1); "
                        "} "
                "}")
        reduce = Code("function reduce(key, values) {"
                    "var sum = 0;for(var i in values) {"
                        "sum += values[i];"
                        "}"
                    "return sum;"
                    "}")

        result = db.employee_info.map_reduce(map, reduce, "interests")

        for element in result.find():
            rows.append({'interest' : element['_id'], 'value' : int(element['value'])})
        return rows

    def EmployeesFamily(self):
        rows = []
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        collection = db.employees_with_family
        for element in collection.find():
            value = "Doesn't have a family"
            if int(element['value']) == 1:
                value = "Has a family"
            rows.append({'name' : element['_id'], 'value' : value})
        return rows

    def Aggregate(self):
        rows = []
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        employees = db.employee_info

        # pipe = [
        #     {'$group': {'company_name': "$workplace.company", 'salary': {'$sum': "$workplace.salary"}}},
        #     {'$sort': {'salary': 1}}
        # ]

        salaries = employees.aggregate([
            {'$group': {'_id': "$workplace.company", 'salary': {'$sum': "$workplace.salary"}}},
            {'$sort': {'salary': 1}}
        ])

        print(salaries)

        for salary in salaries:
            rows.append({'company_name' : salary['_id'], 'salary' : salary['salary']})

        return rows

    def getLastName(self):
        names = []
        names.append('Henriques')
        names.append('Kurth')
        names.append('Glaspie')
        names.append('Kiker')
        names.append('Sandidge')
        names.append('Coto')
        names.append('Cost')
        names.append('Raven')
        names.append('Copeland')
        names.append('Mckinsey')
        names.append('Soller')
        names.append('Vasques')
        names.append('Ehlers')
        names.append('Cobbins')
        names.append('Lovingood')
        names.append('Mcneill')
        names.append('Hoy')
        names.append('Pintor')
        names.append('Dieterich')
        names.append('Bonacci')
        names.append('Lehmkuhl')
        names.append('Simons')
        names.append('Schaub')
        names.append('Marriott')
        names.append('Poynter')
        names.append('Mcnicholas')
        names.append('Fiscus')
        names.append('Lesane')
        return names[random.randint(0, len(names)-1)]

    def getFirstName(self):
        names = []
        names.append('Edna')
        names.append('Deetta')
        names.append('Lauretta')
        names.append('Evangelina')
        names.append('Georgie')
        names.append('Ellyn')
        names.append('Nenita')
        names.append('Ellis')
        names.append('Hisako')
        names.append('Randy')
        names.append('Janell')
        names.append('Kit')
        names.append('Jesusita')
        names.append('Eleanore')
        names.append('Lorie')
        names.append('Kristen')
        names.append('Oliver')
        names.append('Tracey')
        names.append('Treena')
        names.append('Sharron')
        names.append('Melonie')
        names.append('Neil')
        names.append('Felicitas')
        names.append('Vernetta')
        names.append('Bertha')
        names.append('Jerrica')
        names.append('Bernie')
        names.append('Talia')
        names.append('Doria')
        names.append('Violet')
        names.append('Ceola')
        names.append('Eloisa')
        names.append('Lorrie')
        names.append('Chung')
        names.append('Evelin')
        names.append('Marjory')
        names.append('Alysha')
        names.append('Beatris')
        names.append('Ophelia')
        names.append('Tiffani')
        names.append('Monserrate')
        names.append('Stanley')
        names.append('Lekisha')
        names.append('Hosea')
        names.append('Chiquita')
        names.append('Karly')
        names.append('Jeanelle')
        names.append('Nena')
        names.append('Vonnie')
        return names[random.randint(0, len(names)-1)]

    def getCompany(self):
        companies = ['Bing', 'Google', 'Yahoo', 'Microsoft', 'Apple', 'Yandex']
        return companies[random.randint(0, len(companies)-1)]

    def getPosition(self):
        positions = []
        positions.append('security')
        positions.append('boss')
        positions.append('courier')
        positions.append('developer')
        positions.append('developer')
        positions.append('developer')
        positions.append('cleaner')
        positions.append('helper')
        positions.append('intern')
        positions.append('HR')
        positions.append('PM')
        return positions[random.randint(0, len(positions)-1)]

    def getDate(self):
        start_date = date.today().replace(day=1, month=1).toordinal()
        end_date = date.today().toordinal()
        # date = datetime.strptime(request['date'], '%Y-%m-%d')
        return  date.fromordinal(random.randint(start_date, end_date))

    def getBirthDate(self):
        start_date = date.today().replace(day=1, month=1, year=1970).toordinal()
        end_date = date.today().replace(day=1, month=1, year=1990).toordinal()
        return date.fromordinal(random.randint(start_date, end_date))

    def getInterest(self):
        interests = ['football', 'computers', 'fishing', 'IT', 'women', ' diving',
                     'food', 'reading', 'ping-pong', 'hunting', 'cars', 'poems',
                     'travelling', 'moto', 'bikes', 'hiking', 'singing', 'sport',
                     'videogames', 'shess', 'humor']
        return interests[random.randint(0, len(interests)-1)]

    def insertEmployee(self, first_name):
        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.attendance_records
        employees = db.employee_info
        id = 60001
        name = first_name + ' ' + self.getLastName()
        bday = datetime.strptime(str(self.getBirthDate()), '%Y-%m-%d')
        family = random.randint(0, 1)
        position = self.getPosition()
        company = self.getCompany()
        salary = random.randint(500, 1500)
        start_of_working = datetime.strptime(str(self.getDate()), '%Y-%m-%d')
        car = random.randint(0, 1)
        interests = [self.getInterest(), self.getInterest(), self.getInterest()]
        print name
        print bday
        print family
        print position
        print company
        print salary
        print start_of_working
        print car
        print interests
        inserteed_employee = {'id' : id,
             'name' : name,
             'birthday' : bday,
             'family' : family,
             'workplace' : {
            'position' : position,
            'company' : company,
            'salary' : salary,
            'start_of_working' : start_of_working,
            'company_car' : car
        },
             'interests' : interests
             }
        employees.insert_one(inserteed_employee)
        hash_data = red.hgetall('employees')
        print 'lol'
        if hash_data:
            for key in hash_data.keys():
                if key in name:
                    print key
                    print name
                    red.hdel('employees', key)

