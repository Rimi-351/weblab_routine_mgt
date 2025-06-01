# scheduler/urls.py
from django.urls import path
from . import views  # Assuming you have views

urlpatterns = [
    # Add your URL patterns here
    # Example:
    path('', views.home, name='home'),
    path('current-week/', views.current_week_view, name='current_week'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

]
