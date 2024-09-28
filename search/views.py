from django.views.decorators.csrf import csrf_protect
from donors.models import Donor
from .forms import SearchForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

@csrf_protect
def send_confirmation_sms(request, donor_id):
    if request.method == "POST":
        api_url = "http://bulksmsbd.net/api/smsapi?api_key=XAAPz7cGWvHami0JHN67&type=text&number=Receiver&senderid=8809617614175&message=TestSM"
        api_key = "XAAPz7cGWvHami0JHN67"
        sender_id = "8809617614175"
        
        donor = Donor.objects.get(id=donor_id)
            
        patient_name = request.POST['patient_name']
        patient_condition = request.POST['patient_condition']
        blood_group = request.POST['blood_group']
        location = request.POST['location']
        number = request.POST['number']
        reason = request.POST['reason']
            
        message = (
            f"📛 রোগীর নাম:: {patient_name}\n"
            f"💁 রোগীর সমস্যা: {patient_condition}\n"
            f"🔴 রক্তের গ্রুপ: {blood_group}\n"
            f"⌚ রক্তের প্রয়োজন কারণ: {reason}\n"
            f"🏥 রক্তদানের  স্থান :  {location}\n"
            f"📞 যোগাযোগ : {number}"
        )

        payload = {
            "api_key": api_key,
            "type": "text",
            "number": donor.phone_number,
            "senderid": sender_id,
            "message": message
        }

        response = requests.post(api_url, data=payload)
        response.raise_for_status()

        return render(request, 'sms_success.html')
    else:
        return HttpResponse("Invalid request method.", status=405)


def search_results(request):
    form = SearchForm(request.GET or None)
    donors = Donor.objects.all()
    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        location = form.cleaned_data.get('location')
        
        if blood_group:
            donors = donors.filter(blood_group__iexact=blood_group)
        if location:
            donors = donors.filter(address__icontains=location)  # Update to filter by address
        
        # Debugging: Print the filters being applied
        print(f"Searching for blood group: {blood_group}, location: {location}")
        print(f"Number of donors found: {donors.count()}")
        for donor in donors:
            print(f"Donor: {donor.name}, Blood Group: {donor.blood_group}, Phone: {donor.phone_number}, Location: {donor.address}")
    
    return render(request, 'search_results.html', {'form': form, 'donors': donors})