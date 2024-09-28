from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib import messages
from .models import Donor, Notification
from request.models import BloodRequest
from users.models import User
from django.views.decorators.http import require_POST
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from .forms import DonorForm, NotifyForm
from django.http import Http404
from django.utils import timezone


def send_sms(phone_number, message):
    url = "http://bulksmsbd.net/api/smsapi?api_key=XAAPz7cGWvHami0JHN67&type=text&number=Receiver&senderid=8809617614175&message=TestSM"  # Replace with the actual BulkSMS API endpoint
    payload = {
        "to": phone_number,
        "message": message,
        "api_key": "XAAPz7cGWvami0JHN67",
        "sender": "8809617614175"
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200


def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donor_list.html', {'donors': donors})


@login_required
def donor_create(request):
    if Donor.objects.filter(created_by=request.user).exists():
        messages.error(request, "You have already created a donor.")
        return redirect('donor_list')
    
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.created_by = request.user
            donor.save()
            messages.success(request, "Donor created successfully.")
            return redirect('donor_list')
    else:
        form = DonorForm()
    return render(request, 'donor_form.html', {'form': form})

@login_required
def donor_update(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    
    if request.user != donor.created_by:
        return render(request, 'donor_list.html', {
            'error_message': "You are not allowed to edit this donor."
        })
    
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, "Donor information updated successfully.")
            return redirect('donor_list')
        else:
            return render(request, 'donor_list.html', {
                'error_message': "Please correct the errors below."
            })
    
    form = DonorForm(instance=donor)
    return render(request, 'donor_form.html', {'form': form})

@login_required
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    
    if request.user != donor.created_by:
        return render(request, 'donor_list.html', {
            'error_message': "You are not allowed to delete this donor."
        })
    
    if request.method == 'POST':
        donor.delete()
        messages.success(request, "Donor deleted successfully.")
        return redirect('donor_list')
    
    return render(request, 'donor_confirm_delete.html', {'donor': donor})

def notify_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)

    if request.method == 'POST':
        form = NotifyForm(request.POST)
        if form.is_valid():
            patient_name = form.cleaned_data['patient_name']
            contact_number = form.cleaned_data['contact_number']
            reason_for_blood = form.cleaned_data['reason_for_blood']
            patient_situation = form.cleaned_data['patient_situation']

            sms_message = (
                f"Patient Name: {patient_name}\n"
                f"Contact Number: {contact_number}\n"
                f"Reason for Blood: {reason_for_blood}\n"
                f"Patient Situation: {patient_situation}"
            )
            
            if send_sms(donor.phone_number, sms_message):
                return redirect('donor_list')
            else:
                return HttpResponse("Failed to send SMS. Please try again later.", status=500)
    else:
        form = NotifyForm()
    
    return render(request, 'notify_form.html', {'form': form, 'donor': donor})

@login_required
def donor_select(request, pk):
    donor = get_object_or_404(Donor, pk=pk)

    if Notification.objects.filter(requester=request.user, is_accepted=False, is_declined=False).exists():
        messages.error(request, "You already have a pending request.")
        return redirect('donor_list')
    
    Notification.objects.create(
        donor=donor,
        requester=request.user,
        message=f"{request.user.username} has requested your donation."
    )
    
    messages.success(request, "Donor selected successfully.")
    return redirect('donor_list')

@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        donor__created_by=request.user
    ) | Notification.objects.filter(
        requester=request.user
    )
    notifications_count = notifications.filter(is_accepted=False, is_declined=False).count()
    return render(request, 'donors/notifications.html', {
        'notifications': notifications,
        'notifications_count': notifications_count
    })
@login_required
@require_POST
def notification_accept(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    
    if notification.donor.created_by != request.user:
        raise Http404

    if Notification.objects.filter(donor=notification.donor, is_accepted=True).exists():
        messages.error(request, "You have already accepted a request.")
        return redirect('notifications')
    
    donor = notification.donor

    if not donor.is_eligible_to_donate():
        messages.error(request, "Donor is not eligible to donate at this time.")
        return redirect('notifications')
    
    donor.last_donated_date = timezone.now().date()
    donor.save()
    
    notification.is_accepted = True
    notification.save()

    blood_request = get_object_or_404(BloodRequest, requester=notification.requester)
    contact_number = blood_request.contact_number
    
    api_url = "http://bulksmsbd.net/api/smsapi?api_key=XAAPz7cGWvHami0JHN67&type=text&number=Receiver&senderid=8809617614175&message=TestSM"
    api_key = "XAAPz7cGWvHami0JHN67"
    sender_id = "8809617614175"
    message = f"{donor.name} has accepted your donation request. His Blood Group is {donor.blood_group}. His contact number is {donor.phone_number}."
    params = {
        'api_key': api_key,
        'type': 'text',
        'number': contact_number,
        'senderid': sender_id,
        'message': message
    }
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        messages.success(request, "Donation request accepted and SMS sent.")
    else:
        messages.error(request, "Donation request accepted but failed to send SMS.")
    
    return redirect('notifications')

@login_required
@require_POST
def notification_decline(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    
    if notification.donor.created_by != request.user:
        raise Http404
    
    notification.is_declined = True
    notification.save()
    
    blood_request = get_object_or_404(BloodRequest, requester=notification.requester)
    contact_number = blood_request.contact_number
    api_url = "http://bulksmsbd.net/api/smsapi?api_key=XAAPz7cGWvHami0JHN67&type=text&number=Receiver&senderid=8809617614175&message=TestSM"
    api_key = "XAAPz7cGWvHami0JHN67"
    sender_id = "8809617614175"
    message = f"{notification.donor.name} has declined your donation request."
    params = {
        'api_key': api_key,
        'type': 'text',
        'number': contact_number,
        'senderid': sender_id,
        'message': message
    }
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        messages.success(request, "Donation request declined and SMS sent.")
    else:
        messages.error(request, "Donation request declined but failed to send SMS.")
    
    return redirect('notifications')