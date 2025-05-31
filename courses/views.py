
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Course
# from .forms import CourseForm  # You'll need to create this form
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, logout
# from django.contrib import messages
# from .forms import CustomUserCreationForm
# from teachers.models import Teacher
# from django.contrib.auth.models import User

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import Course
from .forms import CourseForm, CustomUserCreationForm
from teachers.models import Teacher

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')  # Redirect to course list after deleting

    return render(request, 'courses/delete_course.html', {'course': course})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect to course list after editing
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('/')
    else:  # Ensure form is initialized on a GET request
        form = CustomUserCreationForm()
    
    return render(request, 'courses/register.html', {'form': form})
  

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")

            # Check user role
            if user.is_superuser:
                return redirect('/admin-dashboard/')  # or your custom admin dashboard
            else:
                try:
                    teacher = Teacher.objects.get(user=user)
                    return redirect('teacher_dashboard')  # create this named URL
                except Teacher.DoesNotExist:
                    messages.error(request, "User is not assigned a teacher role.")
                    logout(request)
                    return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')
