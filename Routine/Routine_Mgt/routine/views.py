from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Slot, Routine, Room, Notification
from .utils import get_available_slots_for_day, get_today_routines
from courses.models import Course
from teachers.models import Teacher
from django.shortcuts import render, redirect
from django.utils import timezone

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


from django.shortcuts import render

def routine_home_view(request):
    return render(request, 'routine/routine_home.html')



def available_slots_view(request):
    # Define the days of the week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Fetch all rooms and slots
    rooms = Room.objects.all()
    slots = Slot.objects.all()

    # Create an empty list to hold the time slots (e.g., 9:00-10:20)
    time_slots = Slot.objects.order_by('start_time').distinct()

    # Dictionary to store availability for each day
    weekly_availability = {}

    for day in days_of_week:
        # Find all slots for the current day
        day_slots = Slot.objects.filter(day=day)
        available_rooms_for_day = []

        for slot in day_slots:
            # Get booked rooms for the current day and time slot
            booked_rooms = Routine.objects.filter(slot=slot, status='scheduled').values_list('room', flat=True)

            # Find rooms that are not booked for this slot
            available_rooms = rooms.exclude(id__in=booked_rooms)

            # Store available rooms for this day and slot
            available_rooms_for_day.append({
                'slot': slot,
                'available_rooms': available_rooms,
            })

        # Store the availability for the day
        weekly_availability[day] = available_rooms_for_day

    # Pass both weekly_availability and time_slots to the template
    return render(request, 'routine/available_slots.html', {
        'weekly_availability': weekly_availability,
        'days_of_week': days_of_week,
        'time_slots': time_slots,
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
    routines = Routine.objects.all().order_by('slot__day', 'slot__start_time')
    return render(request, 'routine/routine_list.html', {
        'routines': routines,
    })

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


