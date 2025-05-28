from django import forms
from .models import Routine

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['course', 'teacher', 'room', 'slot', 'is_online', 'status']

    def clean_slot(self):
        # Check if the slot is available
        slot = self.cleaned_data.get('slot')
        if not slot.is_available:
            raise forms.ValidationError("This slot is not available.")
        return slot
