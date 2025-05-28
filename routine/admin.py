from django.contrib import admin
from .models import Batch, Room, ScheduleEntry, Slot, Routine, Notification

# Register simple models except Teacher and Course
admin.site.register([Batch, Room, ScheduleEntry, Routine, Notification])

# Custom admin for Slot
class SlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'is_available', 'date')
    search_fields = ('day', 'start_time', 'end_time', 'date')
    list_filter = ('day', 'is_available')

admin.site.register(Slot, SlotAdmin)
