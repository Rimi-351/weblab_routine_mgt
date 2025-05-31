#<<<<<<< HEAD
"""
URL configuration for Routine_Mgt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from routine.views import routine_list_view
from courses.views import user_logout
from monitor.views import admin_dashboard
from routine import views  # ✅ Added this import

urlpatterns = [
    path('', views.routine_homepage, name='routine_homepage'),

    # path('', routine_list_view, name='routine_list'),
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('routine/', include('routine.urls')),
    path('teachers/', include('teachers.urls')), 
    path('logout/', user_logout, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    #path('generate-slots/', views.create_weekday_class_slots, name='generate_slots'),  # ✅ Adjusted view name
]
