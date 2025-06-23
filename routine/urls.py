from django.urls import path
from . import views


urlpatterns = [
    path('available-slots/', views.available_slots_view, name='available_slots'),
    #path('notifications/', views.notification_list_view, name='notifications'),
    path('today/', views.today_routine_view, name='today_routine'),
    #path('list/', views.routine_list_view, name='routine_list'),
    #path('create/', views.routine_create_view, name='routine_create'),
    path('add-slot/', views.add_slot_view, name='add_slot'),  # New URL for adding a slot

    path('', views.routine_homepage, name='routine_homepage'),
    path('1-2/', views.routine_1_2, name='routine_1_2'),
    path('2-1/', views.routine_2_1, name='routine_2_1'),
    path('3-1/', views.routine_3_1, name='routine_3_1'),
    path('3-2/', views.routine_3_2, name='routine_3_2'),
    path('4-2/', views.routine_4_2, name='routine_4_2'),
    path('routine/online/<str:batch>/<str:day>/<str:date_str>/', views.routine_online_classes, name='routine_online_classes'),
    #path('<str:batch>/<str:day>/online/', views.routine_online_classes, name='routine_online_classes'),


]
