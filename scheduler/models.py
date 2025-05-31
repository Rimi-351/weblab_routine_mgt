from django.db import models

# Teacher model
# models.py
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name  # This ensures that the name is returned, not 'Teacher object (1)'

# # admin.py
from django.contrib import admin
from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']  # Display name and email in the admin interface

# admin.site.register(Teacher, TeacherAdmin)

# Batch model (e.g., "2-2", "M.Sc.-2")
class Batch(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Course model
class Course(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Room model (e.g., virtual or physical rooms)
class Room(models.Model):
    name = models.CharField(max_length=50)
    is_virtual = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# ScheduleEntry model (for actual class schedules)
class ScheduleEntry(models.Model):
    DAY_CHOICES = [
        ("Sun", "Sunday"),
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat", "Saturday"),
    ]
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    is_rescheduled = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)  # Added date field

    class Meta:
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.course.title} - {self.batch.name} ({self.day} {self.start_time}-{self.end_time})"

# AcademicWeek model (for tracking academic weeks)
class AcademicWeek(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    label = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.label}: {self.start_date} to {self.end_date}"

# StaticRoutine model (for static routine data)
class StaticRoutine(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=ScheduleEntry.DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.batch.name} - {self.course.title} ({self.day} {self.start_time}-{self.end_time})"

# AcademicCalendar model (for academic events)
class AcademicCalendar(models.Model):
    date = models.DateField()
    event_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.event_name} on {self.date}"
