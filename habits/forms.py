from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Habit


# CustomUserCreationForm adds a required email field and removes help text
# for username and password fields in the default UserCreationForm.

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # Remove help text for each field
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }


# Custom email validation
def clean_email(self):
    email = self.cleaned_data.get('email')
    
    # Check if the email is already in use
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError('This email address is already registered.')
    
    return email


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description'] 