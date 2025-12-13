from django import forms
from .models import GuestUser

class GuestLoginForm(forms.ModelForm):
    class Meta:
        model = GuestUser
        fields = ['email', 'cookies_accepted']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-transparent text-white border-secondary',
                'placeholder': 'name@example.com'
            }),
            'cookies_accepted': forms.CheckboxInput(attrs={
                'class': 'form-check-input bg-transparent border-secondary'
            }),
        }
