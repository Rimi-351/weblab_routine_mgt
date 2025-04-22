from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    semester = models.CharField(max_length=20)
    total_classes = models.PositiveIntegerField(default=0, help_text="Total number of classes to conduct")

    def __str__(self):
        return f"{self.code} - {self.name}"
