from django.shortcuts import render, get_object_or_404, redirect
from .models import ClassSchedule, Reschedule,Teacher  # noqa: F401
from .forms import RescheduleForm

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    schedules = ClassSchedule.objects.filter(teacher=teacher)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher, 'schedules': schedules})

def reschedule_class(request, schedule_id):
    class_schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    if request.method == 'POST':
        form = RescheduleForm(request.POST)
        if form.is_valid():
            rescheduled = form.save(commit=False)
            rescheduled.class_schedule = class_schedule
            rescheduled.save()
            return redirect('teacher_list')  # Redirect to teacher list after rescheduling
    else:
        form = RescheduleForm()

    return render(request, 'teachers/reschedule_class.html', {'form': form, 'class_schedule': class_schedule})
