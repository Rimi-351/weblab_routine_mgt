# teachers/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),  # List all teachers
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add/', views.add_teacher, name='add_teacher'),
    path('update/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('delete/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    path('<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),  # Teacher details
    path('reschedule/<int:schedule_id>/', views.reschedule_class, name='reschedule_class'),  # Reschedule a class
]
