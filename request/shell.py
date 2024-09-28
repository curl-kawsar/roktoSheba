from .models import BloodRequest
from django.db.models import F

# Replace 'yourapp' with the actual name of your app
BloodRequest.objects.filter(requester_name__isnull=True).update(requester_name=F('requester__username'))
