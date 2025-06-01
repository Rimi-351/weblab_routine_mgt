# from django.db import models
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from courses.models import Course
# from teachers.models import Teacher, ClassSchedule
# from django.utils import timezone
# from datetime import date, timedelta
# from .models import ClassSchedule, Course, Teacher, Room, Slot 
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from courses.models import Course
from teachers.models import Teacher, ClassSchedule
from django.utils import timezone
from datetime import date, timedelta

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.number

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
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('rescheduled', 'Rescheduled'),
        ('cancelled', 'Cancelled'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    batch = models.CharField(max_length=10, default='3-2')

    def __str__(self):
        return f"{self.course.code} - {self.course.title} by {self.teacher.name} in {self.room.number} on {self.slot}"

    def save(self, *args, **kwargs):
        if self.status == 'cancelled':
            self.slot.is_available = True
            self.slot.save()

        if self.status in ['scheduled', 'rescheduled']:
            day_to_int = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6}

            today = date.today()
            today_weekday = today.weekday()
            class_day = day_to_int.get(self.slot.day)

            if class_day is not None:
                days_ahead = (class_day - today_weekday) % 7
                class_date = today + timedelta(days=days_ahead)

                ClassSchedule.objects.update_or_create(
                    teacher=self.teacher,
                    subject=f"{self.course.code} - {self.course.title}",
                    date=class_date,
                    defaults={
                        'start_time': self.slot.start_time,
                        'end_time': self.slot.end_time,
                    }
                )

        super().save(*args, **kwargs)

   

# class Routine(models.Model):
#     STATUS_CHOICES = [
#         ('scheduled', 'Scheduled'),
#         ('rescheduled', 'Rescheduled'),
#         ('cancelled', 'Cancelled'),
#     ]

#     SEMESTER_CHOICES = [
#     ('1-1', '1st Year 1st Semester'),
#     ('1-2', '1st Year 2nd Semester'),
#     ('2-1', '2nd Year 1st Semester'),
#     ('2-2', '2nd Year 2nd Semester'),
#     ('3-1', '3rd Year 1st Semester'),
#     ('3-2', '3rd Year 2nd Semester'),
#     ('4-1', '4th Year 1st Semester'),
#     ('4-2', '4th Year 2nd Semester'),
# ]
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
#     semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
#     is_online = models.BooleanField(default=False)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
#     is_cancelled = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.course.code} - {self.course.title} by {self.teacher.name} in {self.room.number} on {self.slot}"

#     def save(self, *args, **kwargs):
#         # Mark slot as available if cancelled
#         if self.status == 'cancelled':
#             self.slot.is_available = True
#             self.slot.save()

#         # If scheduled or rescheduled, create/update ClassSchedule
#         if self.status in ['scheduled', 'rescheduled']:
#             day_to_int = {
#                 'Monday': 0, 'Tuesday': 1, 'Wednesday': 2,
#                 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6,
#             }

#             today = date.today()
#             today_weekday = today.weekday()
#             class_day = day_to_int.get(self.slot.day)

#             if class_day is not None:
#                 days_ahead = class_day - today_weekday
#                 if days_ahead < 0:
#                     days_ahead += 7
#                 class_date = today + timedelta(days=days_ahead)

#                 ClassSchedule.objects.update_or_create(
#                     teacher=self.teacher,
#                     subject=f"{self.course.code} - {self.course.title} (Sem {self.semester})",  # ⬅️ Include semester in subject
#                     date=class_date,
#                     defaults={
#                         'start_time': self.slot.start_time,
#                         'end_time': self.slot.end_time,
#                     }
#                 )

#         super().save(*args, **kwargs)

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# SIGNAL to create notification on cancellation
@receiver(pre_save, sender=Routine)
def routine_status_change(sender, instance, **kwargs):
    if instance.pk:  # if it already exists
        previous = Routine.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            if instance.status == 'cancelled':
                Notification.objects.create(
                    title="Class Cancelled",
                    message=f"The class {instance.course.title} has been cancelled."
                )
            elif instance.status == 'rescheduled':
                Notification.objects.create(
                    title="Class Rescheduled",
                    message=f"The class {instance.course.title} has been rescheduled."
                )
