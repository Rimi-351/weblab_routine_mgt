from django.urls import path
from . import views

urlpatterns = [
    path('available-slots/', views.available_slots_view, name='available_slots'),
    path('notifications/', views.notification_list_view, name='notifications'),
    path('today/', views.today_routine_view, name='today_routine'),
    path('list/', views.routine_list_view, name='routine_list'),
    path('create/', views.routine_create_view, name='routine_create'),
    path('add-slot/', views.add_slot_view, name='add_slot'),  # New URL for adding a slot
]
