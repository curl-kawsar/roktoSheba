from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=255, required=False)
    blood_group = forms.ChoiceField(choices=Profile.BLOOD_GROUP_CHOICES, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'address', 'blood_group', 'phone_number', 'password1', 'password2']
        error_messages = {
            'username': {
                'required': 'Username is Required',
                'max_length': '',
            },
            'password1': {
                'required': 'Password is Required',
                'min_length': '',
            },
            'password2': {
                'required': 'Password Confirmation is Required',
                'password_mismatch': 'Passwords do not match',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': '',
                'invalid': '',
            }


from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'blood_group', 'phone_number']