from django import forms
from donors.models import Donor

class SearchForm(forms.Form):
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

    blood_group = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, required=True)
    location = forms.CharField(required=False)  # Change to CharField

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update({'list': 'location-list'})
        self.fields['location'].choices = self.get_location_choices()

    def get_location_choices(self):
        address = Donor.objects.values_list('address', flat=True).distinct()
        location_choices = [(address, address) for address in address]
        return location_choices