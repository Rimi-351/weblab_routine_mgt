# teachers/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),  # List all teachers
    path('<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),  # Teacher details
    path('reschedule/<int:schedule_id>/', views.reschedule_class, name='reschedule_class'),  # Reschedule a class
]
