from django.contrib import admin
from .models import Room, Slot, Routine, Notification

class SlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'is_available', 'date')
    search_fields = ('day', 'start_time', 'end_time', 'date')
    list_filter = ('day', 'is_available')

admin.site.register(Room)
admin.site.register(Slot, SlotAdmin)
admin.site.register(Routine)

