from django.contrib import admin
from .models import Teacher, Reschedule, ClassSchedule
from .forms import RescheduleForm
from django.utils.safestring import mark_safe
from routine.models import Routine, Notification

@admin.register(Reschedule)
class RescheduleAdmin(admin.ModelAdmin):
    form = RescheduleForm
    list_display = ['class_schedule', 'reschedule_date', 'is_online', 'new_start_time', 'new_end_time']

    fieldsets = (
        (None, {
            'fields': ('class_schedule', 'reschedule_date', 'is_online')
        }),
        ('Online Class Details', {
            'fields': ('online_duration',),
            'classes': ('collapse',)
        }),
        ('Offline Class Details', {
            'fields': ('offline_duration', 'room',),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('new_start_time', 'new_end_time'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['room'].help_text = mark_safe(
            '<a href="http://127.0.0.1:8000/routine/available-slots/" target="_blank" style="color: green;">Check Available Slots</a>'
        )
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # After saving Reschedule, update the related ClassSchedule
        class_schedule = obj.class_schedule
        class_schedule.date = obj.reschedule_date
        if obj.new_start_time:
            class_schedule.start_time = obj.new_start_time
        if obj.new_end_time:
            class_schedule.end_time = obj.new_end_time
        class_schedule.save()

        # Update Routine if exists
        try:
            routine = Routine.objects.get(
                teacher=class_schedule.teacher,
                course__title=class_schedule.subject,
            )
            routine.status = 'rescheduled'
            routine.is_cancelled = False
            routine.slot.start_time = obj.new_start_time or routine.slot.start_time
            routine.slot.end_time = obj.new_end_time or routine.slot.end_time
            routine.save()

            Notification.objects.create(
                title="Class Rescheduled",
                message=f"{routine.course.title} class has been rescheduled to {obj.new_start_time} - {obj.new_end_time}.",
            )
        except Routine.DoesNotExist:
            pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'designation', 'department']
    search_fields = ['name', 'email', 'department']


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['subject', 'teacher', 'date', 'start_time', 'end_time']
    list_filter = ['date', 'teacher']
    search_fields = ['subject', 'teacher__name']
