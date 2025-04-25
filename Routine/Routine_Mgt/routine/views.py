from django.shortcuts import render
from .models import Slot, Routine, Room, Notification
from .utils import get_available_slots_for_day
from django.http import HttpResponse

def routine_home_view(request):
    return HttpResponse(
        "<h1>Welcome to the Routine App</h1>"
        "<p><a href='/routine/available-slots/'>Available Slots</a> | "
        "<a href='/routine/notifications/'>Notifications</a></p>"
    )

def available_slots_view(request):
    selected_day = request.GET.get('day', 'Monday')
    available_slots = get_available_slots_for_day(selected_day)
    rooms = Room.objects.all()
    return render(request, 'routine/available_slots.html', {
        'available_slots': available_slots,
        'day': selected_day,
        'rooms': rooms
    })

def notification_list_view(request):
    notifications = Notification.objects.all().order_by('-created_at')[:10]
    return render(request, 'routine/notifications.html', {
        'notifications': notifications
    })
