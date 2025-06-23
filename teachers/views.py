from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import ClassSchedule, Reschedule, Teacher
from .forms import RescheduleForm, TeacherForm
from routine.models import Routine
from datetime import date

@login_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    today=date.today()
    schedules = ClassSchedule.objects.filter(teacher=teacher,date__gte=today).exclude(status='cancelled').order_by('date', 'start_time')
    return render(request, 'teachers/teacher_dashboard.html', {
        'teacher': teacher,
        'schedules': schedules,
    })

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    today=date.today()
    schedules = ClassSchedule.objects.filter(teacher=teacher,date__gte=today).exclude(status='cancelled').order_by('date', 'start_time')

    if request.method == "POST":
        action = request.POST.get("action")
        schedule_id = request.POST.get("schedule_id")

        if action == "cancel" and schedule_id:
            schedule = get_object_or_404(ClassSchedule, pk=schedule_id)

            # Delete related Reschedule objects (optional, cascade will handle anyway)
            Reschedule.objects.filter(class_schedule=schedule).delete()

            # Delete the class schedule itself
            # schedule.delete()
            # 1️⃣ Cancel original class
            schedule.status = 'cancelled'
            schedule.save()

            messages.success(request, "Class and its reschedule(s) canceled successfully.")
            return redirect('teacher_detail', teacher_id=teacher.id)

        elif action == "extra_class":
            # TODO: Implement extra class creation or redirect logic here
            messages.info(request, "Extra Class functionality not implemented yet.")
            return redirect('teacher_detail', teacher_id=teacher.id)

    context = {
        "teacher": teacher,
        "schedules": schedules,
    }
    return render(request, "teachers/teacher_detail.html", context)


# teachers/views.py
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ClassSchedule, Reschedule
from .forms import RescheduleForm
from routine.models import Slot, Room
from courses.models import Course
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import RescheduleForm
from .models import ClassSchedule, Reschedule
from routine.models import Room,Slot


# def reschedule_class(request, schedule_id):
#     class_schedule = get_object_or_404(ClassSchedule, id=schedule_id)
#     existing_reschedule = Reschedule.objects.filter(class_schedule=class_schedule).first()

#     if request.method == "POST":
#         form = RescheduleForm(request.POST, instance=existing_reschedule, class_schedule=class_schedule)

#         date_str = request.POST.get('reschedule_date')
#         is_online_str = request.POST.get('is_online')
#         is_online = (is_online_str == 'True') if is_online_str is not None else None

#         if date_str and is_online is not None:
#             date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
#             form.fields['selected_slot'].choices = get_available_slots(class_schedule, date_obj, is_online)
#         else:
#             form.fields['selected_slot'].choices = []

#         if form.is_valid():
#             reschedule = form.save(commit=False)
#             reschedule.class_schedule = class_schedule
#             original_date = class_schedule.date

#             selected_slot = form.cleaned_data.get('selected_slot')
#             parts = selected_slot.strip().split()

#             try:
#                 time_range = parts[1]
#                 start_str, end_str = time_range.split('-')
#                 start_time = datetime.strptime(start_str, '%H:%M').time()
#                 end_time = datetime.strptime(end_str, '%H:%M').time()

#                 if reschedule.is_online:
#                     room = None
#                     class_type = 'online'
#                 else:
#                     room_number = parts[0]
#                     room = Room.objects.get(number=room_number)
#                     class_type = 'offline'

#                 # Assign values to reschedule instance
#                 reschedule.new_start_time = start_time
#                 reschedule.new_end_time = end_time
#                 reschedule.room = room if room else None

#             except Exception as e:
#                 messages.error(request, f"Error parsing slot: {e}")
#                 return render(request, 'teachers/reschedule_class.html', {
#                     'form': form,
#                     'class_schedule': class_schedule,
#                 })

#             # Cancel original class
#             class_schedule.status = 'cancelled'
#             class_schedule.save()

#             # Create new class
#             new_class = ClassSchedule.objects.create(
#                 course=class_schedule.course,
#                 teacher=class_schedule.teacher,
#                 room=room,
#                 date=reschedule.reschedule_date,
#                 original_date=original_date,
#                 start_time=start_time,
#                 end_time=end_time,
#                 semester=class_schedule.semester,
#                 status='rescheduled',
#                 class_type=class_type
#             )

#             reschedule.class_schedule = new_class
#             reschedule.save()

#             messages.success(request, "Class rescheduled successfully.")
#             return redirect('teacher_upcoming_classes', teacher_id=new_class.teacher.id)

#         else:
#             messages.error(request, "Please fix the errors below.")

#     else:
#         form = RescheduleForm(instance=existing_reschedule, class_schedule=class_schedule)
#         form.fields['selected_slot'].choices = []

#     return render(request, 'teachers/reschedule_class.html', {
#         'form': form,
#         'class_schedule': class_schedule,
#     })

from datetime import datetime, time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import ClassSchedule, Reschedule
from routine.models import Room
from .forms import RescheduleForm

# def reschedule_class(request, schedule_id):
#     class_schedule = get_object_or_404(ClassSchedule, id=schedule_id)
#     existing_reschedule = Reschedule.objects.filter(class_schedule=class_schedule).first()

#     if request.method == "POST":
#         form = RescheduleForm(request.POST, instance=existing_reschedule, class_schedule=class_schedule)

#         # Dynamically set available slots choices based on posted date and online status
#         date_str = request.POST.get('reschedule_date')
#         is_online_str = request.POST.get('is_online')
#         is_online = (is_online_str == 'True') if is_online_str is not None else None

#         if date_str and is_online is not None:
#             try:
#                 date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
#             except ValueError:
#                 messages.error(request, "Invalid date format")
#                 date_obj = None
            
#             if date_obj:
#                 form.fields['selected_slot'].choices = get_available_slots(class_schedule, date_obj, is_online)
#             else:
#                 form.fields['selected_slot'].choices = []
#         else:
#             form.fields['selected_slot'].choices = []

#         if form.is_valid():
#             reschedule = form.save(commit=False)
#             original_date = class_schedule.date

#             selected_slot = form.cleaned_data.get('selected_slot')
#             if not selected_slot:
#                 messages.error(request, "Please select a valid time slot.")
#                 return render(request, 'teachers/reschedule_class.html', {
#                     'form': form,
#                     'class_schedule': class_schedule,
#                 })

#             parts = selected_slot.strip().split(' ', 1)
#             try:
#                 if reschedule.is_online:
#                     # Online slot format: "Online HH:MM-HH:MM"
#                     time_range = parts[1]
#                     start_str, end_str = time_range.split('-')
#                     start_time = datetime.strptime(start_str, '%H:%M').time()
#                     end_time = datetime.strptime(end_str, '%H:%M').time()
#                     room = None
#                     class_type = 'online'
#                 else:
#                     # Offline slot format: "RoomNumber HH:MM-HH:MM"
#                     room_number = parts[0]
#                     time_range = parts[1]
#                     start_str, end_str = time_range.split('-')
#                     start_time = datetime.strptime(start_str, '%H:%M').time()
#                     end_time = datetime.strptime(end_str, '%H:%M').time()
#                     room = Room.objects.get(number=room_number)
#                     class_type = 'offline'
#             except Exception as e:
#                 messages.error(request, f"Error parsing selected slot: {e}")
#                 return render(request, 'teachers/reschedule_class.html', {
#                     'form': form,
#                     'class_schedule': class_schedule,
#                 })
            
            

#             # Cancel the original class schedule
#             class_schedule.status = 'cancelled'
#             class_schedule.save()

#             # Create the new rescheduled class schedule
#             new_class_schedule = ClassSchedule.objects.create(
#                 course=class_schedule.course,
#                 teacher=class_schedule.teacher,
#                 room=room,
#                 date=reschedule.reschedule_date,
#                 original_date=original_date,
#                 start_time=start_time,
#                 end_time=end_time,
#                 semester=class_schedule.semester,
#                 status='rescheduled',
#                 class_type=class_type
#             )

#             # Link reschedule record to new class schedule
#             reschedule.class_schedule = new_class_schedule
#             reschedule.new_start_time = start_time
#             reschedule.new_end_time = end_time
#             reschedule.room = room.number if room else None
#             reschedule.save()

#             messages.success(request, "Class rescheduled successfully.")
#             return redirect('teacher_upcoming_classes', teacher_id=new_class_schedule.teacher.id)
#         else:
#             messages.error(request, "Please fix the errors below.")
#     else:
#         form = RescheduleForm(instance=existing_reschedule, class_schedule=class_schedule)
#         form.fields['selected_slot'].choices = []

#     return render(request, 'teachers/reschedule_class.html', {
#         'form': form,
#         'class_schedule': class_schedule,
#     })

from django.utils.timezone import now, make_aware
def reschedule_class(request, schedule_id):
    class_schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    existing_reschedule = Reschedule.objects.filter(class_schedule=class_schedule).first()

    if request.method == "POST":
        form = RescheduleForm(request.POST, instance=existing_reschedule, class_schedule=class_schedule)

        # Dynamically set available slots choices based on posted date and online status
        date_str = request.POST.get('reschedule_date')
        is_online_str = request.POST.get('is_online')
        is_online = (is_online_str == 'True') if is_online_str is not None else None

        if date_str and is_online is not None:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format")
                date_obj = None

            if date_obj:
                form.fields['selected_slot'].choices = get_available_slots(class_schedule, date_obj, is_online)
            else:
                form.fields['selected_slot'].choices = []
        else:
            form.fields['selected_slot'].choices = []

        if form.is_valid():
            reschedule = form.save(commit=False)
            original_date = class_schedule.date

            selected_slot = form.cleaned_data.get('selected_slot')
            if not selected_slot:
                messages.error(request, "Please select a valid time slot.")
                return render(request, 'teachers/reschedule_class.html', {
                    'form': form,
                    'class_schedule': class_schedule,
                })

            parts = selected_slot.strip().split(' ', 1)
            try:
                if reschedule.is_online:
                    # Online slot format: "Online HH:MM-HH:MM"
                    time_range = parts[1]
                    start_str, end_str = time_range.split('-')
                    start_time = datetime.strptime(start_str, '%H:%M').time()
                    end_time = datetime.strptime(end_str, '%H:%M').time()
                    room = None
                    class_type = 'online'
                else:
                    # Offline slot format: "RoomNumber HH:MM-HH:MM"
                    room_number = parts[0]
                    time_range = parts[1]
                    start_str, end_str = time_range.split('-')
                    start_time = datetime.strptime(start_str, '%H:%M').time()
                    end_time = datetime.strptime(end_str, '%H:%M').time()
                    room = Room.objects.get(number=room_number)
                    class_type = 'offline'
            except Exception as e:
                messages.error(request, f"Error parsing selected slot: {e}")
                return render(request, 'teachers/reschedule_class.html', {
                    'form': form,
                    'class_schedule': class_schedule,
                })

            # ✳️ 24-Hour Reschedule Restriction
            try:
                original_datetime = datetime.combine(class_schedule.date, class_schedule.start_time)
                if not original_datetime.tzinfo:
                    original_datetime = make_aware(original_datetime)

                if now() > original_datetime - timedelta(hours=24):
                    messages.error(request, "Rescheduling is only allowed at least 24 hours before the class.")
                    return render(request, 'teachers/reschedule_class.html', {
                        'form': form,
                        'class_schedule': class_schedule,
                    })
            except Exception as e:
                messages.error(request, f"Error checking 24-hour restriction: {e}")
                return render(request, 'teachers/reschedule_class.html', {
                    'form': form,
                    'class_schedule': class_schedule,
                })

            # Cancel the original class schedule
            class_schedule.status = 'cancelled'
            class_schedule.save()

            # Create the new rescheduled class schedule
            new_class_schedule = ClassSchedule.objects.create(
                course=class_schedule.course,
                teacher=class_schedule.teacher,
                room=room,
                date=reschedule.reschedule_date,
                original_date=original_date,
                start_time=start_time,
                end_time=end_time,
                semester=class_schedule.semester,
                status='rescheduled',
                class_type=class_type
            )

            # Link reschedule record to new class schedule
            reschedule.class_schedule = new_class_schedule
            reschedule.new_start_time = start_time
            reschedule.new_end_time = end_time
            reschedule.room = room.number if room else None
            reschedule.save()

            messages.success(request, "Class rescheduled successfully.")
            return redirect('teacher_upcoming_classes', teacher_id=new_class_schedule.teacher.id)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RescheduleForm(instance=existing_reschedule, class_schedule=class_schedule)
        form.fields['selected_slot'].choices = []

    return render(request, 'teachers/reschedule_class.html', {
        'form': form,
        'class_schedule': class_schedule,
    })

def get_available_slots(class_schedule, date, is_online):
    from routine.models import Slot, Room
    from teachers.models import ClassSchedule

    weekday = date.weekday()
    teacher = class_schedule.teacher
    semester = class_schedule.semester

    available = []

    if is_online:
        if weekday in [4, 5]:
            valid_slots = Slot.objects.filter(start_time__gte='09:00', end_time__lte='23:10').distinct()
        else:
            valid_slots = Slot.objects.filter(start_time__gte='19:00', end_time__lte='23:10').distinct()

        seen = set()
        for slot in valid_slots:
            key = (slot.start_time, slot.end_time)
            if key in seen:
                continue
            seen.add(key)

            if ClassSchedule.objects.filter(
                teacher=teacher, date=date,
                start_time__lt=slot.end_time, end_time__gt=slot.start_time,
                status__in=['pending', 'conducted', 'rescheduled']
            ).exists():
                continue

            if ClassSchedule.objects.filter(
                semester=semester, date=date,
                start_time__lt=slot.end_time, end_time__gt=slot.start_time,
                status__in=['pending', 'conducted', 'rescheduled']
            ).exists():
                continue

            value = f"Online {slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}"
            label = f"Online {slot.start_time.strftime('%I:%M %p')}–{slot.end_time.strftime('%I:%M %p')}"
            available.append((value, label))

    else:
        if weekday in [4, 5]:
            return []

        
        seen = set()
         # Define time range bounds
        from datetime import time
        start_limit = time(9, 0)
        end_limit = time(17, 0)
        
        for room in Room.objects.all():
            for slot in Slot.objects.filter(start_time__gte=start_limit, end_time__lte=end_limit):
            # for slot in Slot.objects.all():
                key = (room.number, slot.start_time, slot.end_time)
                if key in seen:
                    continue

                if ClassSchedule.objects.filter(
                    teacher=teacher, date=date,
                    start_time__lt=slot.end_time, end_time__gt=slot.start_time,
                    status__in=['pending', 'conducted', 'rescheduled']
                ).exists():
                    continue

                if ClassSchedule.objects.filter(
                    semester=semester, date=date,
                    start_time__lt=slot.end_time, end_time__gt=slot.start_time,
                    status__in=['pending', 'conducted', 'rescheduled']
                ).exists():
                    continue

                if ClassSchedule.objects.filter(
                    room=room, date=date,
                    start_time__lt=slot.end_time, end_time__gt=slot.start_time,
                    status__in=['pending', 'conducted', 'rescheduled']
                ).exists():
                    continue

                seen.add(key)
                value = f"{room.number} {slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}"
                label = f"Room {room.number} {slot.start_time.strftime('%I:%M %p')}–{slot.end_time.strftime('%I:%M %p')}"
                available.append((value, label))

    return available


from django.http import JsonResponse
from datetime import datetime

def ajax_get_available_slots(request):
    date_str = request.GET.get('date')
    is_online_str = request.GET.get('is_online')

    if not date_str or is_online_str is None:
        return JsonResponse({'slots': []})

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        is_online = is_online_str.lower() == 'true'
    except:
        return JsonResponse({'slots': []})

    # You need class_schedule object here, but since it's AJAX, pass teacher_id and semester_id via GET
    teacher_id = request.GET.get('teacher_id')
    semester = request.GET.get('semester')

    # Minimal check for required params
    if not teacher_id or not semester:
        return JsonResponse({'slots': []})

    # Get teacher and create dummy class_schedule-like object
    from teachers.models import Teacher
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        return JsonResponse({'slots': []})

    # Create a dummy class_schedule object with teacher and semester for get_available_slots
    class DummySchedule:
        def __init__(self, teacher, semester):
            self.teacher = teacher
            self.semester = semester

    dummy_schedule = DummySchedule(teacher, semester)

    from .views import get_available_slots  # import your existing function
    slots = get_available_slots(dummy_schedule, date_obj, is_online)

    # Format slots as list of dicts for frontend
    slot_list = [{'value': val, 'label': label} for val, label in slots]

    return JsonResponse({'slots': slot_list})




def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = email.split('@')[0]

            # Create associated User
            user = User.objects.create_user(
                username=username,
                email=email,
                password='cse1234'
            )

            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()

            messages.success(
                request,
                f'✅ Teacher "{teacher.name}" added.\nUsername: {username}, Password: cse1234'
            )
            return redirect('teacher_list')
    else:
        form = TeacherForm()

    return render(request, 'teachers/add_teacher.html', {'form': form})

def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Teacher updated successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/edit_teacher.html', {'form': form})

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, '🗑️ Teacher deleted successfully.')
        return redirect('teacher_list')
    return render(request, 'teachers/delete_teacher.html', {'teacher': teacher})
import re

def get_semester_from_subject(subject):
    # Extract the first 3-digit code from the subject string
    match = re.search(r'\b(\d{3})\b', subject)
    if match:
        code = int(match.group(1))
        if 100 <= code <= 149:
            return '1-1'
        elif 150 <= code <= 199:
            return '1-2'
        elif 200 <= code <= 249:
            return '2-1'
        elif 250 <= code <= 299:
            return '2-2'
        elif 300 <= code <= 349:
            return '3-1'
        elif 350 <= code <= 399:
            return '3-2'
        elif 400 <= code <= 449:
            return '4-1'
        elif 450 <= code <= 499:
            return '4-2'
    return 'Unknown'

@login_required
def online_rescheduled_classes(request):
    rescheduled_classes = Reschedule.objects.filter(is_online=True).select_related('class_schedule__teacher').order_by('-reschedule_date')

    # Annotate semester info on each reschedule object
    for reschedule in rescheduled_classes:
        subject = reschedule.class_schedule.subject
        reschedule.semester = get_semester_from_subject(subject)

    return render(request, 'teachers/online_rescheduled_list.html', {
        'rescheduled_classes': rescheduled_classes
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q
from .models import Teacher, ClassSchedule
from courses.models import Course

@login_required
def teacher_assigned_courses(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)

    # Debug prints
    print(f"Teacher: {teacher.name}, ID: {teacher.id}")

    course_ids = ClassSchedule.objects.filter(teacher=teacher).values_list('course', flat=True).distinct()
    print(f"Course IDs: {list(course_ids)}")

    courses = Course.objects.filter(id__in=course_ids)
    print(f"Courses found: {[c.code for c in courses]}")

    course_stats = []
    for course in courses:
        classes = ClassSchedule.objects.filter(teacher=teacher, course=course)
        stats = classes.aggregate(
            conducted=Count('id', filter=Q(status='conducted')),
            rescheduled=Count('id', filter=Q(status='rescheduled')),
            missed=Count('id', filter=Q(status='missed')),
            total=Count('id'),
        )
        course_stats.append({
            'code': course.code,
            'title': course.title,
            'semester': course.semester,
            'conducted': stats['conducted'],
            'rescheduled': stats['rescheduled'],
            'missed': stats['missed'],
            'expected': stats['total'],
            'remaining': stats['total'] - (stats['conducted'] + stats['rescheduled'] + stats['missed']),
        })

    return render(request, 'teachers/assigned_courses.html', {
        'teacher': teacher,
        'course_stats': course_stats,
    })


from django.utils.dateparse import parse_date

@login_required
# def teacher_upcoming_classes(request, teacher_id):
#     teacher = get_object_or_404(Teacher, pk=teacher_id)
#     today = timezone.now().date()

#     course_id = request.GET.get('course_id')
#     date_str = request.GET.get('date')
#     filter_date = parse_date(date_str) if date_str else None

#     if request.method == 'POST':
#         action = request.POST.get('action')
#         schedule_id = request.POST.get('schedule_id')
#         if action == 'cancel' and schedule_id:
            
#             schedule = get_object_or_404(ClassSchedule, pk=schedule_id, teacher=teacher)
#             # Delete related Reschedule objects
#             Reschedule.objects.filter(class_schedule=schedule).delete()
#             schedule.status = 'missed'
#             schedule.save()
#             messages.success(request, "Class canceled successfully.")
#             # Redirect to the same URL to avoid POST resubmission
#             return redirect(request.path + '?' + request.META.get('QUERY_STRING', ''))

#     classes = ClassSchedule.objects.filter(
#         teacher=teacher,
#         date__gte=today,
#     ).exclude(status__in=['missed', 'cancelled'])


#     if course_id:
#         classes = classes.filter(course__id=course_id)
#     if filter_date:
#         classes = classes.filter(date=filter_date)

#     classes = classes.order_by('date', 'start_time')

#     assigned_courses = Course.objects.filter(classschedule__teacher=teacher).distinct()

#     context = {
#         'teacher': teacher,
#         'classes': classes,
#         'assigned_courses': assigned_courses,
#         'selected_course_id': course_id,
#         'selected_date': date_str,
#     }
#     return render(request, 'teachers/upcoming_classes.html', context)


def teacher_upcoming_classes(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    today = timezone.now().date()

    course_id = request.GET.get('course_id')
    date_str = request.GET.get('date')
    filter_date = parse_date(date_str) if date_str else None

    if request.method == 'POST':
        action = request.POST.get('action')
        schedule_id = request.POST.get('schedule_id')
        class_schedule = get_object_or_404(ClassSchedule, id=schedule_id)

        if action == 'cancel' and schedule_id:
            # ✳️ 24-Hour Cancel Restriction
            try:
                original_datetime = datetime.combine(class_schedule.date, class_schedule.start_time)
                if not original_datetime.tzinfo:
                    original_datetime = make_aware(original_datetime)

                if now() > original_datetime - timedelta(hours=24):
                    messages.error(request, "Cancellation is only allowed before 24 hours")
                    return redirect(request.path + '?' + request.META.get('QUERY_STRING', ''))
                else:
                    # Proceed with cancellation
                    Reschedule.objects.filter(class_schedule=class_schedule).delete()
                    class_schedule.status = 'missed'
                    class_schedule.save()
                    messages.success(request, "Class marked as missed successfully.")
                    return redirect(request.path + '?' + request.META.get('QUERY_STRING', ''))
            except Exception as e:
                messages.error(request, f"Error checking 24-hour restriction: {e}")

    # Load classes again (fresh, after POST or GET)
    classes = ClassSchedule.objects.filter(
        teacher=teacher,
        date__gte=today,
    ).exclude(status__in=['missed', 'cancelled'])

    if course_id:
        classes = classes.filter(course__id=course_id)
    if filter_date:
        classes = classes.filter(date=filter_date)

    classes = classes.order_by('date', 'start_time')
    assigned_courses = Course.objects.filter(classschedule__teacher=teacher).distinct()

    context = {
        'teacher': teacher,
        'classes': classes,
        'assigned_courses': assigned_courses,
        'selected_course_id': course_id,
        'selected_date': date_str,
    }

    return render(request, 'teachers/upcoming_classes.html', context)
