from django import forms
from .models import Course

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
     # Make title optional
    title = forms.CharField(required=False)
    # Make teachers optional
    teachers = forms.ModelMultipleChoiceField(
        queryset=Course.teachers.field.related_model.objects.all(),
        required=False
    )
    class Meta:
        model = Course
        fields = ['title', 'code', 'semester', 'total_classes', 'teachers']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course code'}),
            'semester': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3-2'}),
            'total_classes': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'teachers': forms.SelectMultiple(attrs={'class': 'form-control'}),
             'teachers': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'style': 'background-color: white; color: black;',
                'size': '6'
            }),

        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
