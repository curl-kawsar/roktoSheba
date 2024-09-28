from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BloodRequest
from .forms import BloodRequestForm, BloodRequestStatusForm
from django.http import HttpResponseForbidden

def blood_request_list(request):
    requests = BloodRequest.objects.all()
    return render(request, 'blood_request_list.html', {'requests': requests})

@login_required
def blood_request_create(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            return redirect('blood_request_list')
    else:
        form = BloodRequestForm()
    return render(request, 'blood_request_form.html', {'form': form})

@login_required
def blood_request_update_status(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    
    if blood_request.requester != request.user:
        return render(request, 'blood_request_list.html', {
            'error_message': "You are not allowed to edit this request.",
            'requests': BloodRequest.objects.all()
        })
    
    if blood_request.status == 'Fulfilled':
        return render(request, 'blood_request_list.html', {
            'error_message': "You cannot edit a request that has already been fulfilled.",
            'requests': BloodRequest.objects.all()  # Pass the list of requests to the template
        })
    
    if request.method == 'POST':
        form = BloodRequestStatusForm(request.POST, instance=blood_request)
        if form.is_valid():
            blood_request.update_status(form.cleaned_data['status'])
            return redirect('blood_request_list')
    else:
        form = BloodRequestStatusForm(instance=blood_request)
    
    return render(request, 'blood_request_update_status.html', {'form': form})

@login_required
def blood_request_delete(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)

    if blood_request.requester != request.user:
        return render(request, 'blood_request_list.html', {
            'error_message': "You are not allowed to delete this request.",
            'requests': BloodRequest.objects.all()  # Pass the list of requests to the template
        })
    
    if request.method == 'POST':
        blood_request.delete()
        return redirect('blood_request_list')
    
    return render(request, 'blood_request_confirm_delete.html', {'blood_request': blood_request})

from django.shortcuts import render
from .models import BloodRequest

def recent_receiver_list(request):
    recent_receivers = BloodRequest.objects.filter(status='Fulfilled').order_by('-fulfilled_date')
    return render(request, 'recent_receiver_list.html', {'recent_receivers': recent_receivers})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BloodRequest
from donors.models import Donor, Notification
from users.models import User 

@login_required
def requester_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    donors = Donor.objects.filter(created_by=user)
    blood_requests = BloodRequest.objects.filter(
        requester=user
    ).exclude(status='Fulfilled') 
    
    pending_request = Notification.objects.filter(requester=user, is_accepted=False, is_declined=False).first()
    
    return render(request, 'donors/requester_profile.html', {
        'user': user, 
        'blood_requests': blood_requests, 
        'donors': donors,
        'pending_request': pending_request
    })