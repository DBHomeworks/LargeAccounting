from django.shortcuts import render
from .class_db import MyDataDase
from django.http import HttpResponseRedirect


from .forms import IdForm

db = MyDataDase()

def showallinfo(request):
    emp = db.ShowAllInfo()
    return render(request, 'DB_LAB2/ShowAllInfo.html', {'emp': emp})

def accounting(request):
    emp = db.Accounting()
    emps = db.ShowAllInfo()
    if request.method == 'POST':
        info = db.GetVisitingById(request.POST['visit_id'])
        return render(request, 'DB_LAB2/Accounting.html', {'emp' : emp, 'emps': emps, 'info': info})
    return render(request, 'DB_LAB2/Accounting.html', {'emp' : emp, 'emps' : emps})

def addvisiting(request):
    if request.method == "POST":
        if request.POST["employee_id"] != "" and request.POST["date"] != "":
            db.AddVisiting(request.POST)
        return HttpResponseRedirect('/Accounting')

def deletevisiting(request):
    if request.method == 'POST':
        db.DeleteVisiting(request.POST)
    return HttpResponseRedirect('/Accounting')

def datesearch(request):
    if request.method == 'POST':
        emp = db.DateSearch(request.POST)
        return render(request, 'DB_LAB2/ShowAllInfo.html', {'emp' : emp})
    else:
        return HttpResponseRedirect('/ShowAllInfo')

def exactlysearch(request):
    if request.method == 'POST':
        emp = db.ExactlySearch(request.POST)
        return render(request, 'DB_LAB2/ShowAllInfo.html', {'emp' : emp})
    else:
        return HttpResponseRedirect('/ShowAllInfo')

def booleanmodesearch(request):
    if request.method == 'POST':
        emp = db.BooleanModeSearch(request.POST)
        return render(request, 'DB_LAB2/ShowAllInfo.html', {'emp' : emp})
    else:
        return HttpResponseRedirect('/ShowAllInfo')

def editvisiting(request):
    if request.method == 'POST':
        db.EditVisit(request.POST)
        return HttpResponseRedirect('/Accounting')

def companiessalary(request):
    info = db.Aggregate()
    return render(request, 'DB_LAB2/companies_salary.html', {'info': info})

def employeesinterests(request):
    info = db.GetInterests()
    return render(request, 'DB_LAB2/employees_interests.html', {'info': info})

def employeesfamily(request):
    info = db.EmployeesFamily()
    return render(request, 'DB_LAB2/familyposition.html', {'info': info})


def add_employee(request):
    db.insertEmployee(request.POST['name'])
    emp = db.ShowAllInfo()
    return HttpResponseRedirect('/')