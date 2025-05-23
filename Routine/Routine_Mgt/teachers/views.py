from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # Import messages module for success notifications
from .models import ClassSchedule, Reschedule, Teacher
from .forms import RescheduleForm
from routine.models import Routine, Notification

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
