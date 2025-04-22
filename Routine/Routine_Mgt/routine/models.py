
from django.db import models
from courses.models import Course
from teachers.models import Teacher

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.number

class Slot(models.Model):
    day = models.CharField(max_length=10)  # e.g., 'Monday', 'Tuesday'
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.day} {self.start_time}-{self.end_time}"

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
    is_online = models.BooleanField(default=False)  # True if the class is online
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    is_cancelled = models.BooleanField(default=False)  # For cancellations
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically record when the routine was added

    def __str__(self):
        return f"{self.course.name} by {self.teacher.name} in {self.room.number} on {self.slot}"
    def save(self, *args, **kwargs):
        # If a routine is cancelled, mark the slot as available
        if self.status == 'cancelled':
            self.slot.is_available = True  # Assuming 'is_available' exists on Slot model
            self.slot.save()

        super().save(*args, **kwargs)