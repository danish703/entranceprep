from django.contrib.auth.forms import UserCreationForm
from django import forms
class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove password validation suggestions
        self.fields['username'].help_text=None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None