from django.db import models

# Create your models here.
from teachers.models import Teacher  # import Teacher model

class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    semester = models.CharField(max_length=20)
    total_classes = models.PositiveIntegerField(default=0, help_text="Total number of classes to conduct")
    teachers = models.ManyToManyField(Teacher, related_name='courses')

    def __str__(self):
       return f"{self.id}: {self.code} - {self.title}"

