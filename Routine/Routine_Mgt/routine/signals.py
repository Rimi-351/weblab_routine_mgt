from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Routine, Notification

@receiver(post_save, sender=Routine)
def notify_routine_change(sender, instance, created, **kwargs):
    if created:
        title = "New Class Scheduled"
        message = f"{instance.course.name} scheduled on {instance.slot.day} at {instance.slot.start_time} in Room {instance.room.number}."
    elif instance.status == 'rescheduled':
        title = "Class Rescheduled"
        message = f"{instance.course.name} has been rescheduled to {instance.slot.day} at {instance.slot.start_time} in Room {instance.room.number}."
    elif instance.status == 'cancelled':
        title = "Class Cancelled"
        message = f"{instance.course.name} class on {instance.slot.day} has been cancelled."

    Notification.objects.create(title=title, message=message)
