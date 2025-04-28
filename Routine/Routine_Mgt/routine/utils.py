from .models import Slot, Routine
from datetime import datetime

def get_available_slots_for_day(day):
    booked_slots = Routine.objects.filter(slot__day=day).values_list('slot_id', flat=True)
    return Slot.objects.filter(day=day).exclude(id__in=booked_slots)

def is_slot_conflict(slot, room):
    return Routine.objects.filter(slot=slot, room=room, status__in=['scheduled', 'rescheduled']).exists()


def get_today_routines():
    today_day = datetime.today().strftime('%A')
    return Routine.objects.filter(
        slot__day=today_day,
        is_cancelled=False
    ).order_by('slot__start_time')