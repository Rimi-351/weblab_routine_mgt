#<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Slot, Routine, Room, Notification
from .utils import get_today_routines
from courses.models import Course
from teachers.models import Teacher
from django.utils import timezone
from collections import defaultdict
from collections import OrderedDict
from itertools import groupby


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


# def routine_home_view(request):
#     return render(request, 'routine/routine_home.html')


def available_slots_view(request):
    from collections import OrderedDict

    days_of_week = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    rooms = Room.objects.all()

    # Unique time ranges
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
            matching_slots = Slot.objects.filter(day=day, start_time=time_range['start_time'], end_time=time_range['end_time'])

            available_rooms = set(rooms)
            for slot in matching_slots:
                booked_rooms = Routine.objects.filter(slot=slot, status='scheduled').values_list('room', flat=True)
                available_rooms -= set(Room.objects.filter(id__in=booked_rooms))

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


def notification_list_view(request):
    notifications = Notification.objects.all().order_by('-created_at')[:10]
    return render(request, 'routine/notifications.html', {
        'notifications': notifications,
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
        existing_routine = Routine.objects.filter(room=room, slot=slot, status='scheduled').exists()
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
            status='scheduled',
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

from datetime import datetime, timedelta, time
from .models import Slot

from django.shortcuts import render
from collections import OrderedDict
from datetime import time
from .models import Routine

def routine_homepage(request):
    return render(request, 'routine/routine_homepage.html')

from collections import OrderedDict
from datetime import time

def render_routine_page(request, batch, template_name='routine/routine_list2.html'):
    routines = Routine.objects.select_related('course', 'teacher', 'room', 'slot').filter(batch=batch)

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Fixed 80-minute slots only
    time_ranges = [
        (time(9, 0),  time(10, 20)),
        (time(10, 25), time(11, 45)),
        (time(11, 50), time(13, 10)),
        (time(14, 0),  time(15, 20)),
        (time(15, 25), time(16, 45)),
    ]

    def time_to_minutes(t):
        return t.hour * 60 + t.minute

    routine_map = OrderedDict()

    for day in days:
        row = []
        skip_slots = 0

        for idx, (slot_start, slot_end) in enumerate(time_ranges):
            if skip_slots > 0:
                skip_slots -= 1
                continue

            # Find routine starting exactly at this slot
            routine = next((r for r in routines if r.slot.day == day and r.slot.start_time == slot_start and r.slot.end_time == slot_end), None)

            if routine is None:
                # Maybe routine starts here but spans multiple slots, or no routine at all
                routine = next((r for r in routines if r.slot.day == day and r.slot.start_time == slot_start), None)

            if routine:
                start_min = time_to_minutes(routine.slot.start_time)
                end_min = time_to_minutes(routine.slot.end_time)

                # Count how many slots this routine covers
                colspan = 1
                for next_idx in range(idx + 1, len(time_ranges)):
                    next_start, next_end = time_ranges[next_idx]
                    next_start_min = time_to_minutes(next_start)
                    next_end_min = time_to_minutes(next_end)

                    # Check if next slot fully fits inside routine time
                    if next_start_min >= start_min and next_end_min <= end_min:
                        colspan += 1
                    else:
                        break

                skip_slots = colspan - 1
                row.append((routine, colspan))
            else:
                row.append((None, 1))

        routine_map[day] = row

    routine_map_items = list(routine_map.items())

    return render(request, template_name, {
        'batch': batch,
        'days': days,
        'time_ranges': time_ranges,
        'routine_map_items': routine_map_items,
    })

# def render_routine_page(request, batch, template_name='routine/routine_list2.html'):
#     routines = Routine.objects.select_related('course', 'teacher', 'room', 'slot').filter(batch=batch)

#     days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#     time_ranges = [
#         (time(9, 0),  time(10, 20)),
#         (time(10, 25), time(11, 45)),
#         (time(10, 25), time(13, 10)),
#         (time(11, 50), time(13, 10)),
#         (time(14, 0),  time(15, 20)),
#         (time(14, 0),  time(16, 45)),
#         (time(15, 25), time(16, 45)),
#     ]

#     routine_map = OrderedDict()
#     for day in days:
#         row = []
#         for start, end in time_ranges:
#             routine = next((r for r in routines if r.slot.day == day and r.slot.start_time == start and r.slot.end_time == end), None)
#             row.append(routine)
#         routine_map[day] = row

#     # Convert dict to list of tuples for template-friendly iteration
#     routine_map_items = list(routine_map.items())

#     return render(request, template_name, {
#         'batch': batch,
#         'days': days,
#         'time_ranges': time_ranges,
#         'routine_map_items': routine_map_items,  # pass list of tuples instead of dict
#     })


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

# def generate_slots_for_weekdays(request):
#     days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     start = time(9, 0)
#     end = time(17, 0)
#     lunch_start = time(13, 10)
#     lunch_end = time(14, 0)
#     duration = timedelta(minutes=80)

#     for day in days:
#         current = datetime.combine(datetime.today(), start)
#         end_datetime = datetime.combine(datetime.today(), end)

#         while current.time() < end and (current + duration).time() <= end:
#             start_time = current.time()
#             end_time = (current + duration).time()

#             # Skip lunch time
#             if end_time <= lunch_start or start_time >= lunch_end:
#                 # Create if not exists
#                 Slot.objects.get_or_create(
#                     day=day,
#                     start_time=start_time,
#                     end_time=end_time,
#                     defaults={'is_available': True}
#                 )
#             current += duration

#     return HttpResponse("Slots generated successfully for Monday to Friday.")

# def render_routine_page(request, batch, template_name='routine/routine_list2.html'):
#     routines = Routine.objects.select_related('course', 'teacher', 'room', 'slot').filter(batch=batch)

#     days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
#     time_ranges = [
#         (time(9, 0), time(10, 20)),
#         (time(10, 25), time(11, 45)),
#         (time(11, 50), time(13, 10)),
#         (time(14, 0), time(15, 20)),
#         (time(15, 25), time(16, 45)),
#     ]

#     routine_map = OrderedDict()
#     for day in days:
#         row = []
#         for start, end in time_ranges:
#             routine = next((r for r in routines if r.slot.day == day and r.slot.start_time == start and r.slot.end_time == end), None)
#             row.append(routine)
#         routine_map[day] = row

#     return render(request, template_name, {
#         'batch': batch,
#         'days': days,
#         'time_ranges': time_ranges,
#         'routine_map': routine_map,
#     })