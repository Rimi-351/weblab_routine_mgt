from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=100, default="CSE")

    def __str__(self):
        return self.name

class ClassSchedule(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject} - {self.date} from {self.start_time} to {self.end_time}"

class Reschedule(models.Model):
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    reschedule_date = models.DateField()
    is_online = models.BooleanField(default=False)
    online_duration = models.IntegerField(null=True, blank=True)
    offline_duration = models.IntegerField(null=True, blank=True)  # Keep this field
    room = models.CharField(max_length=100, null=True, blank=True)
    new_start_time = models.TimeField(null=True, blank=True)
    new_end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Reschedule for {self.class_schedule.subject} on {self.reschedule_date}"
