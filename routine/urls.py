from django.urls import path
from . import views

urlpatterns = [
    path('', views.routine_home_view, name='routine_home'),  # Home page for the routine system
    path('available-slots/', views.available_slots_view, name='available_slots'),  # View available slots
    path('notifications/', views.notification_list_view, name='notifications'),  # List of recent notifications
    path('today/', views.today_routine_view, name='today_routine'),  # Today's routine
    path('list/', views.routine_list_view, name='routine_list'),  # List all routines
    path('create/', views.routine_create_view, name='routine_create'),  # Create a new routine
    path('add-slot/', views.add_slot_view, name='add_slot'),  # New URL for adding a slot
]
