from django import forms
from .models import Course

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'semester', 'total_classes', 'teachers']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course code'}),
            'semester': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Spring 2025'}),
            'total_classes': forms.NumberInput(attrs={'class': 'form-control'}),
            'teachers': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
