from django import forms
from .models import Routine

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['course', 'teacher', 'date', 'time', 'room', 'is_published']
