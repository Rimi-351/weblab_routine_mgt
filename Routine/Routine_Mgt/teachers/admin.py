from django.contrib import admin
from .models import Teacher, Reschedule
from .forms import RescheduleForm

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
            'fields': ('room',),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('new_start_time', 'new_end_time'),
        }),
    )

admin.site.register(Teacher)
admin.site.register(Reschedule, RescheduleAdmin)
