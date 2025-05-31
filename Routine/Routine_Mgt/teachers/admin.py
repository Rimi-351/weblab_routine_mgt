from django.contrib import admin
from .models import Teacher, Reschedule, ClassSchedule
from .forms import RescheduleForm

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'designation', 'department']
    search_fields = ['name', 'email', 'department']

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['subject', 'teacher', 'date', 'start_time', 'end_time']
    list_filter = ['date', 'teacher']
    search_fields = ['subject', 'teacher__name']

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
