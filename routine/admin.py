from django.contrib import admin
from .models import Room, Slot, Routine, Vacation
from django.contrib import messages
from django.shortcuts import redirect

# Admin for Room
admin.site.register(Room)

# Admin for Slot
class SlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'is_available', 'date')
    search_fields = ('day', 'start_time', 'end_time', 'date')
    list_filter = ('day', 'is_available')

admin.site.register(Slot, SlotAdmin)

# Admin for Vacation
@admin.register(Vacation)
class VacationAdmin(admin.ModelAdmin):
    list_display = ('reason', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('reason',)

# Admin for Routine
from .forms import RoutineForm  # ✅ import the form

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    form = RoutineForm  # ✅ assign the form here

    list_display = ('course_code', 'course_title', 'teacher', 'room', 'slot', 'batch')
    search_fields = (
        'course__title',
        'course__code',
        'teacher__name',
        'room__number',
        'slot__day',
        'batch',
    )
    list_filter = ('batch', 'slot__day', 'room', 'teacher', 'course')

    def course_title(self, obj):
        return obj.course.title

    def course_code(self, obj):
        return obj.course.code

