from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # Import messages module for success notifications
from .models import ClassSchedule, Reschedule, Teacher
from .forms import RescheduleForm, TeacherForm
from routine.models import Routine, Notification
from django.contrib.auth.decorators import login_required
from teachers.models import Teacher, ClassSchedule

@login_required
def teacher_dashboard(request):
    # Get the logged-in user’s Teacher profile
    teacher = Teacher.objects.get(user=request.user)

    # Get upcoming classes for this teacher
    schedules = ClassSchedule.objects.filter(teacher=teacher).order_by('date', 'start_time')

    context = {
        'teacher': teacher,
        'schedules': schedules,
    }
    return render(request, 'teachers/teacher_dashboard.html', context)

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    schedules = ClassSchedule.objects.filter(teacher=teacher)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher, 'schedules': schedules})

def reschedule_class(request, schedule_id):
    class_schedule = get_object_or_404(ClassSchedule, id=schedule_id)

    # Try to get the existing reschedule or create a new one if none exists
    existing_reschedule = Reschedule.objects.filter(class_schedule=class_schedule).first()

    if request.method == 'POST':
        form = RescheduleForm(request.POST, instance=existing_reschedule)
        if form.is_valid():
            rescheduled = form.save(commit=False)
            rescheduled.class_schedule = class_schedule
            rescheduled.save()

            # ➡ Update Routine
            try:
                routine = Routine.objects.get(
                    teacher=class_schedule.teacher,
                    course__title=class_schedule.subject,
                )
                routine.status = 'rescheduled'
                routine.is_cancelled = False
                routine.slot.start_time = rescheduled.new_start_time
                routine.slot.end_time = rescheduled.new_end_time
                routine.save()

                # ➡ Send Notification
                Notification.objects.create(
                    title="Class Rescheduled",
                    message=f"{routine.course.title} class has been rescheduled to {rescheduled.new_start_time}-{rescheduled.new_end_time}.",
                )

            except Routine.DoesNotExist:
                pass

            # Success message and redirect
            messages.success(request, "Class rescheduled successfully.")
            return redirect('teacher_list')
        else:
            # Error message if form is not valid
            messages.error(request, "Failed to reschedule class. Please check the form.")
    else:
        form = RescheduleForm(instance=existing_reschedule)

    return render(request, 'teachers/reschedule_class.html', {'form': form, 'class_schedule': class_schedule})

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            # Generate a random password
            random_password = get_random_string(length=8)
            email = form.cleaned_data['email']
            username = email.split('@')[0]  # You can customize this

            # Create user
            user = User.objects.create_user(username=username, email=email, password=random_password)
            
            # Create teacher
            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()

            # Send email
            send_mail(
                subject='Your Teacher Account Credentials',
                message=f"Dear {teacher.name},\n\nYour account has been created.\n\nLogin Credentials:\nUsername: {username}\nPassword: {random_password}\n\nPlease log in and change your password.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, '✅ Teacher added and credentials sent via email!')
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
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/edit_teacher.html', {'form': form})

def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully.')
        return redirect('teacher_list')
    return render(request, 'teachers/delete_teacher.html', {'teacher': teacher})