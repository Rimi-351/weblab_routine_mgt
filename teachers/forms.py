from django import forms
from .models import Reschedule
from django.core.exceptions import ValidationError
from .models import Teacher

class RescheduleForm(forms.ModelForm):
    is_online = forms.TypedChoiceField(
        choices=[(True, 'Online'), (False, 'Offline')],
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect
    )

    class Meta:
        model = Reschedule
        fields = [
            'reschedule_date',
            'is_online',
            'online_duration',
            'offline_duration',
            'room',
            'new_start_time',
            'new_end_time',
        ]
        widgets = {
            'reschedule_date': forms.DateInput(attrs={'type': 'date'}),
            'online_duration': forms.NumberInput(attrs={'min': 0}),
            'offline_duration': forms.NumberInput(attrs={'min': 0}),
            'room': forms.TextInput(attrs={'placeholder': 'Enter room number'}),
            'new_start_time': forms.TimeInput(attrs={'type': 'time'}),
            'new_end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_start_time = cleaned_data.get('new_start_time')
        new_end_time = cleaned_data.get('new_end_time')
        is_online = cleaned_data.get('is_online')
        room = cleaned_data.get('room')
        online_duration = cleaned_data.get('online_duration')
        offline_duration = cleaned_data.get('offline_duration')

        if new_start_time and new_end_time:
            if new_start_time >= new_end_time:
                raise ValidationError("End time must be later than start time.")

        if is_online:
            if not online_duration or online_duration <= 0:
                raise ValidationError("Please enter a valid online duration (minutes).")
        else:
            if not room:
                raise ValidationError("Please enter the room number for offline classes.")
            if not offline_duration or offline_duration <= 0:
                raise ValidationError("Please enter a valid offline duration (minutes).")

        return cleaned_data


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'designation', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }