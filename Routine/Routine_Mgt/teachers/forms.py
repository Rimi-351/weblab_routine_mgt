from django import forms
from .models import Reschedule
from django.core.exceptions import ValidationError

class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Reschedule
        fields = ['new_start_time', 'new_end_time']  # Removed 'reason' from the fields

    # Custom validation to ensure that the end time is later than the start time
    def clean(self):
        cleaned_data = super().clean()
        new_start_time = cleaned_data.get('new_start_time')
        new_end_time = cleaned_data.get('new_end_time')

        if new_start_time and new_end_time:
            if new_start_time >= new_end_time:
                raise ValidationError("End time must be later than start time.")
        
        return cleaned_data
