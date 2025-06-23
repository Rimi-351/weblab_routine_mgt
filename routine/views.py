#<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Slot, Routine, Room
from .utils import get_today_routines
from courses.models import Course
from teachers.models import Teacher
from django.utils import timezone
from collections import defaultdict
from collections import OrderedDict
from itertools import groupby
from teachers.models import ClassSchedule,Reschedule  # Add this at the top of your views.py
from routine.models import Room, Slot       # Assuming these are your models for rooms and slots
from datetime import timedelta
from django.utils import timezone
from .models import Room, Slot
from teachers.models import ClassSchedule  # Make sure to import
from django.shortcuts import render
from collections import defaultdict, OrderedDict
from datetime import datetime, timedelta, time
from django.utils import timezone
from teachers.models import ClassSchedule
from datetime import datetime, timedelta, time
from .models import Slot
from django.shortcuts import render
from collections import OrderedDict
from datetime import time
from .models import Routine
def add_slot_view(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_available = request.POST.get('is_available') == 'on'
        date = request.POST.get('date')

        # Validate the date (if provided)
        if date:
            date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            date = None

        # Create the Slot object
        Slot.objects.create(
            day=day,
            start_time=start_time,
            end_time=end_time,
            is_available=is_available,
            date=date
        )

        return redirect('routine_list')  # Redirect to the routine list or wherever you want to

    return render(request, 'routine/add_slot.html')


def available_slots_view(request):
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    rooms = Room.objects.all()

    # Map days of the week to real dates of current week starting Sunday
    today = timezone.now().date()
    weekday = today.weekday()  # Monday = 0
    # Calculate last Sunday (weekday + 1) mod 7, Sunday = 6 in weekday() system, so adjust:
    sunday = today - timedelta(days=(weekday + 1) % 7)
    date_map = {days_of_week[i]: sunday + timedelta(days=i) for i in range(7)}

    # Get unique time ranges from Slot table (start_time, end_time)
    unique_time_ranges = []
    seen = set()
    for slot in Slot.objects.order_by('start_time', 'end_time'):
        key = (slot.start_time, slot.end_time)
        if key not in seen:
            seen.add(key)
            unique_time_ranges.append({'start_time': slot.start_time, 'end_time': slot.end_time})

    weekly_availability = []

    for day in days_of_week:
        for time_range in unique_time_ranges:
            available_rooms = set(rooms)

            # Query booked rooms by filtering ClassSchedule by date, start_time, end_time, and status
            booked_rooms_ids = ClassSchedule.objects.filter(
                date=date_map[day],
                start_time=time_range['start_time'],
                end_time=time_range['end_time'],
                status__in=['pending', 'conducted', 'rescheduled']
            ).values_list('room_id', flat=True)

            booked_rooms = set(Room.objects.filter(id__in=booked_rooms_ids))

            # Remove booked rooms from available rooms
            available_rooms -= booked_rooms

            weekly_availability.append({
                'day': day,
                'slot': time_range,
                'available_rooms': available_rooms,
            })

    return render(request, 'routine/available_slots.html', {
        'weekly_availability': weekly_availability,
        'days_of_week': days_of_week,
        'time_slots': unique_time_ranges,
    })


def today_routine_view(request):
    today_routine = get_today_routines()
    return render(request, 'routine/today_routine.html', {
        'today_routine': today_routine,
    })


def routine_list_view(request):
    routines = Routine.objects.select_related('course', 'teacher', 'room', 'slot').all()

    # Group slots by unique time ranges
    all_slots = Slot.objects.order_by('start_time', 'end_time')
    unique_time_ranges = []
    seen = set()
    for slot in all_slots:
        key = (slot.start_time, slot.end_time)
        if key not in seen:
            seen.add(key)
            unique_time_ranges.append(key)

    days = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    context = {
        'routines': routines,
        'days': days,
        'time_ranges': unique_time_ranges,  # only unique time slots
    }
    return render(request, 'routine/routine_list.html', context)


def routine_create_view(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        teacher_id = request.POST.get('teacher')
        room_id = request.POST.get('room')
        slot_id = request.POST.get('slot')
        is_online = request.POST.get('is_online') == 'on'

        course = get_object_or_404(Course, id=course_id)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        room = get_object_or_404(Room, id=room_id)
        slot = get_object_or_404(Slot, id=slot_id)

        # Check if the room and slot are already booked
        existing_routine = Routine.objects.filter(room=room, slot=slot,).exists()
        if existing_routine:
            return render(request, 'routine/routine_create.html', {
                'error_message': f"The selected room {room.number} is already booked for {slot.get_slot_date()} at {slot.start_time} - {slot.end_time}. Please choose a different slot or room.",
                'courses': Course.objects.all(),
                'teachers': Teacher.objects.all(),
                'rooms': Room.objects.all(),
                'slots': Slot.objects.filter(is_available=True),
                'selected_course_id': course_id,
                'selected_teacher_id': teacher_id,
                'selected_room_id': room_id,
                'selected_slot_id': slot_id,
            })

        # Create the routine if no conflict
        Routine.objects.create(
            course=course,
            teacher=teacher,
            room=room,
            slot=slot,
            is_online=is_online,
            
        )
        return redirect('routine_list')

    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    rooms = Room.objects.all()
    slots = Slot.objects.filter(is_available=True)
    return render(request, 'routine/routine_create.html', {
        'courses': courses,
        'teachers': teachers,
        'rooms': rooms,
        'slots': slots,
    })


def reschedule_class_view(request, schedule_id):
    routine = get_object_or_404(Routine, id=schedule_id)
    
    if request.method == 'POST':
        is_online = request.POST.get('is_online') == 'on'
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        # Update the routine with new times and status
        routine.is_online = is_online
        routine.slot.start_time = start_time
        routine.slot.end_time = end_time
        routine.status = 'rescheduled'
        routine.save()

        return redirect('routine_list')
    
    return render(request, 'routine/reschedule_class.html', {
        'routine': routine,
    })



def routine_homepage(request):
    return render(request, 'routine/routine_homepage.html')


def render_routine_page(request, batch, template_name='routine/routine_list2.html'):
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Define fixed time ranges
    time_ranges = [
        (time(9, 0),  time(10, 20)),
        (time(10, 25), time(11, 45)),
        (time(11, 50), time(13, 10)),
        (time(14, 0),  time(15, 20)),
        (time(15, 25), time(16, 45)),
    ]

    def time_to_minutes(t):
        return t.hour * 60 + t.minute

    # Calculate current week (Sunday to Saturday)
    
    from django.utils.timezone import localdate
    today = localdate()

    #today = timezone.now().date()
    weekday = today.weekday()  # Monday = 0
    # sunday = today - timedelta(days=weekday + 1) if weekday != 6 else today
    sunday = today - timedelta(days=(today.weekday() + 1) % 7)
    week_dates = [sunday + timedelta(days=i) for i in range(7)]

    date_map = {
        days[i]: week_dates[i]
        for i in range(len(days))
    }

    # Fetch ClassSchedule for the week
    schedules = ClassSchedule.objects.select_related('course', 'teacher', 'room') \
        .filter(semester=batch, date__range=(week_dates[0], week_dates[-1]))

    # Main routine map for displaying grid
    routine_map = OrderedDict()
    for day in days:
        row = []
        skip_slots = 0
        for idx, (slot_start, slot_end) in enumerate(time_ranges):
            if skip_slots > 0:
                skip_slots -= 1
                continue

            # Match the class that starts at this slot and spans into others
            schedule = next((
                s for s in schedules
                if s.date == date_map[day] and
                   s.start_time == slot_start and
                   time_to_minutes(s.end_time) > time_to_minutes(slot_start) and
                   s.status in ['pending', 'conducted','rescheduled']
            ), None)

            if schedule:
                start_min = time_to_minutes(schedule.start_time)
                end_min = time_to_minutes(schedule.end_time)

                colspan = 1
                for next_idx in range(idx + 1, len(time_ranges)):
                    next_start, next_end = time_ranges[next_idx]
                    if time_to_minutes(next_end) <= end_min:
                        colspan += 1
                    else:
                        break

                skip_slots = colspan - 1
                row.append((schedule, colspan))
            else:
                row.append((None, 1))

        routine_map[day] = row

    # Rescheduled classes (for yellow column)
    rescheduled_map = defaultdict(lambda: defaultdict(list))
    for s in schedules.filter(status='rescheduled'):
        d = s.date
        day = d.strftime('%A')
        rescheduled_map[day][d].append(s)

    return render(request, template_name, {
        'batch': batch,
        'days': days,
        'time_ranges': time_ranges,
        'routine_map_items': list(routine_map.items()),
        'rescheduled_map': rescheduled_map,
        'date_map': date_map,
    })



from collections import OrderedDict, defaultdict
from datetime import time, timedelta
from django.shortcuts import render
from django.utils.timezone import localdate
from teachers.models import ClassSchedule

def render_routine_page_2(request, batch, template_name='routine/routine_list2.html'):
    # Python weekday order: Monday=0 ... Sunday=6
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Define fixed time ranges
    time_ranges = [
        (time(9, 0),  time(10, 20)),
        (time(10, 25), time(11, 45)),
        (time(11, 50), time(13, 10)),
        (time(14, 0),  time(15, 20)),
        (time(15, 25), time(16, 45)),
    ]

    def time_to_minutes(t):
        return t.hour * 60 + t.minute

    # Get today's local date
    today = localdate()

    # Get start of next week (next Monday)
    monday = today - timedelta(days=today.weekday()) + timedelta(weeks=1)
    week_dates = [monday + timedelta(days=i) for i in range(7)]

    # Match each Python day name with date
    date_map = {
        days[i]: week_dates[i]
        for i in range(len(days))
    }

    # Filter schedules by semester and next week's date range
    schedules = ClassSchedule.objects.select_related('course', 'teacher', 'room') \
        .filter(semester=batch, date__range=(week_dates[0], week_dates[-1]))

    # Prepare weekly routine map
    routine_map = OrderedDict()
    for day in days:
        row = []
        skip_slots = 0
        for idx, (slot_start, slot_end) in enumerate(time_ranges):
            if skip_slots > 0:
                skip_slots -= 1
                continue

            schedule = next((
                s for s in schedules
                if s.date == date_map[day] and
                   s.start_time == slot_start and
                   time_to_minutes(s.end_time) > time_to_minutes(slot_start) and
                   s.status in ['pending', 'conducted']
            ), None)

            if schedule:
                start_min = time_to_minutes(schedule.start_time)
                end_min = time_to_minutes(schedule.end_time)
                colspan = 1
                for next_idx in range(idx + 1, len(time_ranges)):
                    next_start, next_end = time_ranges[next_idx]
                    if time_to_minutes(next_end) <= end_min:
                        colspan += 1
                    else:
                        break
                skip_slots = colspan - 1
                row.append((schedule, colspan))
            else:
                row.append((None, 1))

        routine_map[day] = row

    # Rescheduled class map
    rescheduled_map = defaultdict(lambda: defaultdict(list))
    for s in schedules.filter(status='rescheduled'):
        d = s.date
        rescheduled_map[d.strftime('%A')][d].append(s)

    return render(request, template_name, {
        'batch': batch,
        'days': days,
        'time_ranges': time_ranges,
        'routine_map_items': list(routine_map.items()),
        'rescheduled_map': rescheduled_map,
        'date_map': date_map,
    })

# Individual pages
def routine_1_2(request):
    return render_routine_page(request, batch='1-2')

def routine_2_1(request):
    return render_routine_page(request, batch='2-1')

def routine_3_1(request):
    return render_routine_page(request, batch='3-1')

def routine_3_2(request):
    return render_routine_page(request, batch='3-2')

def routine_4_2(request):
    return render_routine_page(request, batch='4-2')


# routine a Online class show korar jonno
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from teachers.models import ClassSchedule

# def routine_online_classes(request, batch, day):
#     weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#     today = timezone.now().date()
#     weekday_index = (today.weekday() + 1) % 7
#     start_of_week = today - timedelta(days=weekday_index) 

#     matching_date = None
#     for i in range(7):
#         current_date = start_of_week + timedelta(days=i)
#         if current_date.strftime('%A').lower() == day.lower():
#             matching_date = current_date
#             break

#     classes = ClassSchedule.objects.none()
#     if matching_date:
#         classes = ClassSchedule.objects.filter(
#             semester=batch,
#             date=matching_date,
#             class_type='online'
#         ).select_related('course', 'teacher', 'room')

#     return render(request, 'routine/online_classes.html', {
#         'batch': batch,
#         'day': day,
#         'classes': classes,
#         'date': matching_date
#     })

from datetime import datetime
from django.http import HttpResponseBadRequest
def routine_online_classes(request, batch, day, date_str):
    try:
        matching_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return HttpResponseBadRequest("Invalid date format")

    classes = ClassSchedule.objects.filter(
        semester=batch,
        date=matching_date,
        class_type='online'
    ).select_related('course', 'teacher', 'room')

    return render(request, 'routine/online_classes.html', {
        'batch': batch,
        'day': day,
        'classes': classes,
        'date': matching_date
    })
# def routine_online_classes(request, batch, day, date_str):
#     try:
#         matching_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError:
#         return HttpResponseBadRequest("Invalid date format")

#     classes = ClassSchedule.objects.filter(
#         semester=batch,
#         date=matching_date,
#         class_type='online'
#     ).select_related('course', 'teacher', 'room')

#     return render(request, 'routine/online_classes.html', {
#         'batch': batch,
#         'day': day,
#         'classes': classes,
#         'date': matching_date
#     })
