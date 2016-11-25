from pymongo import MongoClient
import random
from datetime import date
import datetime
import redis
import pickle

red = redis.StrictRedis(host='localhost', port=6379, db=0)


def getLastName():
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

def getFirstName():
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

def getCompany():
    companies = ['Bing', 'Google', 'Yahoo', 'Microsoft', 'Apple', 'Yandex']
    return companies[random.randint(0, len(companies)-1)]

def getPosition():
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

def getDate():
    start_date = datetime.date.today().replace(day=1, month=1).toordinal()
    end_date = datetime.date.today().toordinal()
    # date = datetime.strptime(request['date'], '%Y-%m-%d')
    return  date.fromordinal(random.randint(start_date, end_date))

def getBirthDate():
    start_date = datetime.date.today().replace(day=1, month=1, year=1970).toordinal()
    end_date = datetime.date.today().replace(day=1, month=1, year=1990).toordinal()
    return date.fromordinal(random.randint(start_date, end_date))

def getInterest():
    interests = ['football', 'computers', 'fishing', 'IT', 'women', ' diving',
                 'food', 'reading', 'ping-pong', 'hunting', 'cars', 'poems',
                 'travelling', 'moto', 'bikes', 'hiking', 'singing', 'sport',
                 'videogames', 'shess', 'humor']
    return interests[random.randint(0, len(interests)-1)]

def insertEmployee():
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.attendance_records
    employees = db.employee_info
    id = 60001
    name = 'Lorrie' + ' ' +  getLastName()
    bday = datetime.datetime.strptime(str(getBirthDate()), '%Y-%m-%d')
    family = random.randint(0, 1)
    position = getPosition()
    company = getCompany()
    salary = random.randint(500, 1500)
    start_of_working = datetime.datetime.strptime(str(getBirthDate()), '%Y-%m-%d')
    car = random.randint(0, 1)
    interests = [getInterest(), getInterest(), getInterest()]
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

    employees.insert_one( inserteed_employee )
    hash_data = red.hgetall(name)
    print hash_data
    for key in hash_data.items():
        if key in name:
            print key
            print name
            red.hdel('employees', key)

# insertEmployee()