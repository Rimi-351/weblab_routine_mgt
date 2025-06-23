from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from courses.models import Course
from teachers.models import Teacher 
from django.utils import timezone
from datetime import date, timedelta
from django.apps import apps

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.number


class Vacation(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.reason or 'Holiday'} ({self.start_date} to {self.end_date})"


class Slot(models.Model):
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time}"

    def get_slot_details(self):
        time_range = f"{self.start_time} - {self.end_time}"
        return f"{self.day} {time_range} on {self.date.strftime('%d %b %Y')}" if self.date else f"{self.day} {time_range} (TBA)"


class Routine(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    batch = models.CharField(max_length=10, default='3-2')

    def __str__(self):
        return f"{self.course.code} - {self.course.title} by {self.teacher.name} in {self.room.number} on {self.slot}"



# class Notification(models.Model):
#     title = models.CharField(max_length=255)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# @receiver(pre_save, sender=Routine)
# def routine_status_change(sender, instance, **kwargs):
#     if instance.pk:
#         previous = Routine.objects.get(pk=instance.pk)
#         if previous.status != instance.status:
#             if instance.status == 'cancelled':
#                 Notification.objects.create(
#                     title="Class Cancelled",
#                     message=f"The class {instance.course.title} has been cancelled."
#                 )
#             elif instance.status == 'rescheduled':
#                 Notification.objects.create(
#                     title="Class Rescheduled",
#                     message=f"The class {instance.course.title} has been rescheduled."
#                 )
