from django.db import models
from routine.models import Routine
# Create your models here.
class ClassConductRecord(models.Model):
    STATUS_CHOICES = [
        ('conducted', 'Conducted'),
        ('rescheduled', 'Rescheduled'),
        ('missed', 'Missed'),
    ]

    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('routine', 'date')  # Only one record per routine per date

    def __str__(self):
        return f"{self.routine.course.code} on {self.date} - {self.status}"
