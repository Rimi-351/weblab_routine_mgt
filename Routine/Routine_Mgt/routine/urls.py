from django.urls import path
from .views import available_slots_view, notification_list_view, routine_home_view

urlpatterns = [
    path('', routine_home_view, name='routine_home'),  # this line!
    path('available-slots/', available_slots_view, name='available_slots'),
    path('notifications/', notification_list_view, name='notifications'),
]
