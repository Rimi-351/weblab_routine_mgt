from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
# from routine.views import routine_list_view
# from courses.views import user_logout
# from monitor.views import admin_dashboard, mark_class_status
from routine import views 
urlpatterns = [
    # path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    # path('mark-class-status/', mark_class_status, name='mark_class_status'),
]
