from django.shortcuts import render
from django.contrib.auth.models import User
from donors.models import Donor
from request.models import BloodRequest

def home(request):
    total_donors = Donor.objects.count()
    total_users = User.objects.count()
    total_requests = BloodRequest.objects.count()
    recent_requests = BloodRequest.objects.order_by('-request_date')[:5]  # Fetch the 5 most recent requests
    context = {
        'total_donors': total_donors,
        'total_users': total_users,
        'total_requests': total_requests,
        'recent_requests': recent_requests,
    }
    return render(request, 'home.html', context)

def developer(request):
    return render(request, 'developer.html')