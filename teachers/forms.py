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

        # Validation
        if is_online:
            if room:
                self.add_error('room', 'Room should be empty for online classes.')
            if not online_duration:
                self.add_error('online_duration', 'Online duration is required for online classes.')
        else:
            if online_duration:
                self.add_error('online_duration', 'Online duration should be empty for offline classes.')
            if not room:
                self.add_error('room', 'Room is required for offline classes.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make fields required based on instance data
        is_online = None
        if self.instance and self.instance.pk:
            is_online = self.instance.is_online
        if 'data' in kwargs:
            is_online = kwargs['data'].get('is_online') == 'True'

        if is_online:
            self.fields['online_duration'].required = True
            self.fields['room'].required = False
        else:
            self.fields['online_duration'].required = False
            self.fields['room'].required = True

        self.fields['new_start_time'].required = True
        self.fields['new_end_time'].required = True
