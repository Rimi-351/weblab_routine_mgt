# teachers/admin.py
from django.contrib import admin
from .models import Teacher, ClassSchedule

admin.site.register(Teacher)
admin.site.register(ClassSchedule)
