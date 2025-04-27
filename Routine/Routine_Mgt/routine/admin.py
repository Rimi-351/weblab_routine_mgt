from django.contrib import admin

# Register your models here.
from .models import Routine, Room, Slot

admin.site.register(Routine)
admin.site.register(Slot)
admin.site.register(Room)