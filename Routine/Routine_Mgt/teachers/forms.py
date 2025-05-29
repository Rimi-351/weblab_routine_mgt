from django import forms
from .models import Reschedule
from django.core.exceptions import ValidationError

class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Reschedule
        fields = [
            'reschedule_date',
            'is_online',
            'online_duration',
            'offline_duration',  # add this field in your model too!
            'room',
            'new_start_time',
            'new_end_time',
        ]

        widgets = {
            'reschedule_date': forms.DateInput(attrs={'type': 'date'}),
            'is_online': forms.RadioSelect(choices=[(True, 'Online'), (False, 'Offline')]),
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

        # Check start/end times
        if new_start_time and new_end_time:
            if new_start_time >= new_end_time:
                raise ValidationError("End time must be later than start time.")

        # If offline, room must be filled
        if is_online is False and not room:
            raise ValidationError("Please enter the room number for offline classes.")

        return cleaned_data
