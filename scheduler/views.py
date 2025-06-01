# scheduler/views.py
from django.shortcuts import render
from .models import ScheduleEntry, AcademicWeek
from .utils import get_current_academic_week, is_class_week
from datetime import datetime, date

# View to display the daily schedule
def daily_schedule(request):
    today = datetime.today().strftime('%a')  # e.g., "Sun"
    entries = ScheduleEntry.objects.filter(day=today).order_by('start_time')
    return render(request, 'scheduler/daily_schedule.html', {'entries': entries})

# Function to get the current academic week (from AcademicWeek model)
def get_current_academic_week():
    today = date.today()
    return AcademicWeek.objects.filter(start_date__lte=today, end_date__gte=today).first()

# Home view (Make sure to create home.html template)
def home(request):
    return render(request, 'scheduler/home.html')

# View to display the current academic week
def current_week_view(request):
    current_week = get_current_academic_week()
    return render(request, 'scheduler/current_week.html', {'week': current_week})

# Dashboard view (Displays current week and today's schedule)
def dashboard_view(request):
    # Get the current academic week (you may need to adjust this part based on your logic)
    current_week = get_current_academic_week()

    # Get today's day (e.g., 'Mon', 'Tue', etc.)
    today_day = datetime.today().strftime('%a')  # 'Mon', 'Tue', etc.

    # Query ScheduleEntry for today's classes (filter by 'day' field)
    today_schedule = ScheduleEntry.objects.filter(day=today_day)

    # Render the dashboard template with the current week and today's schedule
    return render(request, 'scheduler/dashboard.html', {
        'current_week': current_week,
        'today_schedule': today_schedule
    })
