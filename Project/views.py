# !python
# log/views.py
import time
import datetime
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import classroom, labs, requestTable, User, TimeTableEvents
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.shortcuts import redirect
from .forms import EventForm, EventFormf ,TimeTableForm
from django.db.models import Max


# Create your views here.
@login_required(login_url=' accounts/login/')
def home(request):
    name = None
    if request.user.is_authenticated():
        print("hello")
        name = request.user.username

    # notify.send(request.user,recipient=User.objects.get(username='Amit Dhar'), verb='you reached level 10')

    vclassroom = classroom.objects.values('block').order_by('block')
    vlabs = labs.objects.values('block').order_by('block')

    seen = set()
    seen1 = set()

    new_class = []
    new_class1 = []

    for d in vclassroom:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_class.append(d)

    for d in vlabs:
        t = tuple(d.items())
        if t not in seen1:
            seen1.add(t)
            new_class1.append(d)

    return render(request, "home.html", {'classroom': new_class, 'labs': new_class1})


@login_required(login_url="accounts/login/")
def classrooms_h(request, block_name):
    floor = classroom.objects.all().aggregate(Max('floor_number'))
    # print()
    max_floor = floor['floor_number__max']
    print(max_floor)
    i = 0
    lst = []
    while i <= max_floor:
        l = []
        l = classroom.objects.filter(block=block_name, floor_number=i)
        lst.append(l)
        i = i + 1
    print(lst[0])

    return render(request, "classrooms.html", {"rooms": lst, "floor": max_floor})


@login_required(login_url="accounts/login/")
def classrooms(request, block_name):
    classes = classroom.objects.filter(block=block_name)
    return render(request, "classrooms.html", {"rooms": classes})


@login_required(login_url="accounts/login/")
def lab(request, block_name):
    classes = labs.objects.filter(block=block_name)
    return render(request, "labs.html", {"rooms": classes})


@login_required(login_url="accounts/login/")
def roomnumber(request, room_number, block_name):
    name = None
    name_id = None
    user_type = None
    form = None
    if request.user.is_authenticated():
        # print("hello")
        name_id = request.user.username
        temp = User.objects.get(username=name_id)
        f_name = temp.first_name
        l_name = temp.last_name
        user_type = temp.type
        if user_type == "faculty":
            form = EventFormf(initial={'booking_status': '1'})
        elif user_type == "student":
            form = EventForm(initial={'booking_status': '1'})
        # print (f_name+" "+l_name+" "+name_id)
        name = f_name + " " + l_name
    return render(request, "calendar.html", {"number": room_number, "block1": block_name, "form": form,
                                             "name": name, "name_id": name_id, "user_type": user_type})


@login_required(login_url="accounts/login/")
def labnumber(request, room_number, block_name):
    return render(request, "calendar.html", {"number": room_number, "block_name": block_name})


@login_required(login_url="accounts/login/")
def auditorium(request):
    return render(request, "calendar.html", {"number": "Auditorium"})


@login_required(login_url="accounts/login/")
def eventlist(request):
    if request.is_ajax():
        start = (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(request.GET['start']))))
        end = (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(request.GET['end']))))
        room_num = str(request.GET['rm'])
        entries = requestTable.objects.filter(room_number=room_num).filter(startDateTime__range=(start, end)).exclude(booking_status='2').all()
        timeTableEntries = TimeTableEvents.objects.filter(room_number=room_num).order_by('startTime').all()
        bookedEvents = entries.filter(booking_status='1').all()
        unbookedEvents = entries.filter(booking_status='0').all()
        events = []

        for entry in unbookedEvents:
            start = datetime.datetime.strptime(entry.startDateTime, "%Y-%m-%d %H:%M:%S")
            end = datetime.datetime.strptime(entry.endDateTime, "%Y-%m-%d %H:%M:%S")
            flag = 0
            for entry1 in bookedEvents:
                startDate = datetime.datetime.strptime(entry1.startDateTime,"%Y-%m-%d %H:%M:%S")
                endDate = datetime.datetime.strptime(entry1.startDateTime, "%Y-%m-%d %H:%M:%S")
                if start > startDate and end < endDate:
                    flag = 1
                if end > startDate and end < endDate:
                    flag = 1
                if start <= startDate and end >= endDate:
                    flag = 1
            if flag == 0:
                events.append(entry)
            else:
                requestTable.objects.filter(id=entry.id).delete()
        json_list = []
        for entry in timeTableEntries:
            json_entry = {'start': str(entry.startTime), 'end': str(entry.endTime), 'allDay': False,
                          'title': entry.course, 'overlap': False,
                          'dow': [int(entry.dayOfWeek)],
                          'lecturer': entry.lecturer,
                          'room_number': entry.room_number}
            json_list.append(json_entry)


        for entry in events:
            json_entry = {'start': str(entry.startDateTime), 'end': str(entry.endDateTime), 'allDay': False,
                          'title': entry.description, 'overlap': False,
                          'booking_status': entry.booking_status,
                          'sender': entry.sender,
                          'sender_id': entry.sender_id,
                          'room_number': entry.room_number}
            json_list.append(json_entry)

        for entry in bookedEvents:
            json_entry = {'start': str(entry.startDateTime), 'end': str(entry.endDateTime), 'allDay': False,
                          'title': entry.description, 'overlap': False,
                          'booking_status': entry.booking_status,
                          'sender': entry.sender,
                          'sender_id': entry.sender_id,
                          'room_number': entry.room_number}
            json_list.append(json_entry)
        return HttpResponse(json.dumps(json_list, cls=DjangoJSONEncoder), content_type='application/json')


@login_required(login_url="accounts/login/")
def notifications(request):
    type = None
    name = None
    id = None
    rows = None

    if request.user.is_authenticated():
        type = request.user.type
        id = request.user.username
        name = request.user.first_name + " " + request.user.last_name

    if type == 'faculty':
        print("not fac " + id)
        rows = requestTable.objects.filter(granter=id, booking_status='0').exclude(booking_status='2')
        rows1 = requestTable.objects.filter(granter=id, booking_status='1')
        print("row " + str(rows.count()))
        print(rows1)
    elif type == 'student':
        print("not stu")
        rows = requestTable.objects.filter(sender_id=id)

    return render(request, "notifications.html", {'rows': rows, 'user_type': type, 'name': name})


@login_required(login_url="accounts/login/")
def nothandler(request, pk, status):
    if request.method == "POST":
        row = requestTable.objects.get(id=pk)
        print(status)
        if status == '1':
            row.booking_status = '1'
            row.save()
        else:
            row.booking_status = '2'
            row.save()

    return redirect('notifications')


@login_required(login_url="accounts/login/")
def saveEvents(request):
    form = None
    if request.user.is_authenticated():
        type = request.user.type
        if type == "faculty":
            print("faculty")
            form = EventFormf(request.POST)
            if form.is_valid():
                temp = form.save(commit=False)
                temp.booking_status = '1'
                temp.save()
            else:
                return HttpResponse(form.errors)
        elif type == "student":
            print("student")
            form = EventForm(request.POST)
            if form.is_valid():
                temp = form.save(commit=False)
                temp.booking_status = '0'
                form.save()
        else:
            return HttpResponse(form.errors)

    return HttpResponse("Sucess")


def viewEvents(request, pk):
    entry = requestTable.objects.get(id=pk)
    date = entry.startDateTime
    return render(request, 'eventView.html', {'rowId': pk, 'eventStartDate': date})


@login_required(login_url='accounts/login/')
def getEvents(request):
    if request.is_ajax():
        entry = requestTable.objects.get(id=request.GET['id'])
        json_list = []
        json_entry = {'start': str(entry.startDateTime), 'end': str(entry.endDateTime), 'allDay': False,
                      'title': entry.description, 'overlap': False,
                      'booking_status': entry.booking_status,
                      'room_number': entry.room_number}
        json_list.append(json_entry)
        print(json_entry)
        return HttpResponse(json.dumps(json_list, cls=DjangoJSONEncoder), content_type='application/json')

@login_required(login_url="accounts/login/")
def get_schedule(request, room_number):
    form = TimeTableForm
    return render(request, 'timetable_calendar.html', {'room': room_number, 'form': form})


@login_required(login_url="accounts/login/")
def saveTimeTableEvents(request):
    form = TimeTableForm(request.POST)

    if form.is_valid():
        form.save()
    else:
        return HttpResponse(form.errors)

    return HttpResponse("Sucess")



@login_required(login_url="accounts/login/")
def timeTableEvents(request):
    if request.is_ajax():
        room_num = str(request.GET['rm'])
        print(room_num)
        entries = TimeTableEvents.objects.filter(room_number=room_num).order_by('startTime').all()
        json_list = []
        print(entries)
        for entry in entries:
            print(entry)
            json_entry = {'start': str(entry.startTime), 'end': str(entry.endTime), 'allDay': False,
                          'title': entry.course, 'overlap': False,
                          'dow': [int(entry.dayOfWeek)],
                          'lecturer': entry.lecturer,
                          'room_number': entry.room_number}
            json_list.append(json_entry)
        return HttpResponse(json.dumps(json_list, cls=DjangoJSONEncoder), content_type='application/json')


def get_rooms(request):
    classes = classroom.objects.all().order_by('room_number')
    return render(request, "classes.html", {"rooms": classes})


def testingLogin(request):
    return render(request,'testLogin.html')