from django import forms
from .models import BloodRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

# Define blood group choices
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

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['requester_name', 'blood_group', 'contact_number', 'reason_for_request', 'status']
        widgets = {
            'requester_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requester Name'}),
            'blood_group': forms.Select(choices=BLOOD_GROUP_CHOICES, attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'reason_for_request': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reason for Request'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('requester_name', css_class='fas fa-user'),
            Field('blood_group', css_class='fas fa-tint'),
            Field('contact_number', css_class='fas fa-phone'),
            Field('reason_for_request', css_class='fas fa-comment'),
            Field('status', css_class='fas fa-info-circle'),
            Submit('submit', 'Submit', css_class='btn btn-success')
        )

class BloodRequestStatusForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('status', css_class='fas fa-info-circle'),
            Submit('submit', 'Update Status', css_class='btn btn-primary')
        )