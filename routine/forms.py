# from django import forms
# from .models import Routine

# class RoutineForm(forms.ModelForm):
#     class Meta:
#         model = Routine
#         fields = ['course', 'teacher', 'date', 'time', 'room', 'is_published']
from django import forms
from .models import Routine

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['course', 'teacher', 'room', 'slot', 'batch']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        slot = cleaned_data.get('slot')
        batch = cleaned_data.get('batch')

        if room and slot:
            # Check for room + slot conflict
            room_conflict = Routine.objects.filter(
                room=room,
                slot=slot
            ).exclude(pk=self.instance.pk)

            if room_conflict.exists():
                raise forms.ValidationError(
                    f"Room {room.number} is already booked for slot {slot.day} "
                    f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}."
                )

        if batch and slot:
            # Check for batch + slot conflict
            batch_conflict = Routine.objects.filter(
                batch=batch,
                slot=slot
            ).exclude(pk=self.instance.pk)

            if batch_conflict.exists():
                raise forms.ValidationError(
                    f"Batch {batch} already has a class during slot {slot.day} "
                    f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}."
                )

        return cleaned_data
