from django import forms
from .models import Donor

class DonorForm(forms.ModelForm):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'aria-label': 'Name',
        })
    )
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'aria-label': 'Blood Group',
        })
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your address',
            'aria-label': 'Address',
        })
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
            'aria-label': 'Phone Number',
        })
    )
    last_donated_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'aria-label': 'Last Donated Date',
        })
    )

    class Meta:
        model = Donor
        fields = ['name', 'blood_group', 'address', 'phone_number', 'last_donated_date']

class NotifyForm(forms.Form):
    patient_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter patient name',
            'aria-label': 'Patient Name',
        })
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter contact number',
            'aria-label': 'Contact Number',
        })
    )
    reason_for_blood = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter reason for blood',
            'aria-label': 'Reason for Blood',
            'rows': 3,
        })
    )
    patient_situation = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe the patient situation',
            'aria-label': 'Patient Situation',
            'rows': 3,
        })
    )