from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
# from django.apps import apps

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=100, default="CSE")

    def __str__(self):
        return self.name

from django.db import models
from courses.models import Course
from teachers.models import Teacher

class ClassSchedule(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('conducted', 'Conducted'),
        ('missed', 'Missed'),
        ('rescheduled', 'Rescheduled'),
        ('cancelled', 'Cancelled'),
    ]

    class_type_choices = [
        ('offline', 'Offline'),
        ('online', 'Online'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey('routine.Room', on_delete=models.CASCADE, default=1,null=True)
    date = models.DateField()  # actual scheduled date (rescheduled date if rescheduled)
    original_date = models.DateField(null=True, blank=True)  # original planned date
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.CharField(max_length=10, default='3-2')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    class_type = models.CharField(max_length=10, choices=class_type_choices, default='offline')

    def __str__(self):
        return f"{self.course.code} on {self.date} ({self.status}) [{self.class_type}]"

    

class Reschedule(models.Model):
    
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    reschedule_date = models.DateField()
    is_online = models.BooleanField(default=False)
    online_duration = models.IntegerField(null=True, blank=True)
    offline_duration = models.IntegerField(null=True, blank=True)
    room = models.CharField(max_length=100, null=True, blank=True)
    new_start_time = models.TimeField(null=True, blank=True)
    new_end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Reschedule for {self.class_schedule.course} on {self.reschedule_date}"

    