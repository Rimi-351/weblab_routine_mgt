from django.db import models
from courses.models import Course
from teachers.models import Teacher

class DailyClassLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('conducted', 'Conducted'),
        ('missed', 'Missed'),
        ('rescheduled', 'Rescheduled'),
        ('cancelled', 'Cancelled'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.course.code} | {self.date} | {self.start_time} - {self.end_time} | {self.status}"
