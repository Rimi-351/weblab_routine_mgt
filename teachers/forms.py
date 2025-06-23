from django import forms
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from .models import Reschedule, Teacher

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


class ScheduleGenerationForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class RescheduleForm(forms.ModelForm):
    is_online = forms.TypedChoiceField(
        choices=[(True, 'Online'), (False, 'Offline')],
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect
    )

    selected_slot = forms.ChoiceField(
        choices=[],  # filled dynamically
        required=False,
        label="Select Stot"
    )

    class Meta:
        model = Reschedule
        fields = ['reschedule_date', 'is_online', 'selected_slot']
        widgets = {
            'reschedule_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.class_schedule = kwargs.pop('class_schedule', None)
        super().__init__(*args, **kwargs)
        self.fields['selected_slot'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        is_online = cleaned_data.get('is_online')
        reschedule_date = cleaned_data.get('reschedule_date')
        selected_slot = cleaned_data.get('selected_slot')

        if not reschedule_date:
            raise forms.ValidationError("Please select a reschedule date.")

        # Friday=4, Saturday=5
        weekday = reschedule_date.weekday()

        if weekday in [4, 5] and not is_online:
            raise forms.ValidationError("Offline classes are NOT allowed on Friday or Saturday.")

        if not selected_slot:
            if is_online:
                raise forms.ValidationError("Online class requires selecting a slot.")
            else:
                raise forms.ValidationError("Offline class requires selecting a slot.")
        # if is_online:
        #     if not selected_slot:
        #         raise forms.ValidationError("Online class requires selecting a slot.")
        # else:
        #     if weekday in [4, 5]:
        #         raise forms.ValidationError("Offline classes are NOT allowed on Friday or Saturday.")

        #     if not cleaned_data.get('selected_slot'):
        #         raise forms.ValidationError("Offline class requires selecting a slot.")

        return cleaned_data