from django import forms
from .models import Reschedule

class RescheduleForm(forms.ModelForm):
    class Meta:
        model = Reschedule
        fields = ['is_online', 'online_duration', 'room', 'new_start_time', 'new_end_time']

    def clean(self):
        cleaned_data = super().clean()
        is_online = cleaned_data.get('is_online')
        online_duration = cleaned_data.get('online_duration')
        room = cleaned_data.get('room')

        # Validation: If online is selected, room should be empty
        if is_online and room:
            self.add_error('room', 'Room should be empty for online classes.')

        # Validation: If offline is selected, online_duration should be empty
        if not is_online and online_duration:
            self.add_error('online_duration', 'Online duration should be empty for offline classes.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the fields conditional based on `is_online`
        if self.instance.is_online:
            self.fields['online_duration'].required = True
            self.fields['room'].required = False
            self.fields['new_start_time'].required = True
            self.fields['new_end_time'].required = True
        else:
            self.fields['online_duration'].required = False
            self.fields['room'].required = True
            self.fields['new_start_time'].required = True
            self.fields['new_end_time'].required = True
