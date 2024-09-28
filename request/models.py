from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RecentDonor(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3)
    donation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} - {self.blood_group}"

class BloodRequest(models.Model):
    requester_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
        ('Cancelled', 'Cancelled'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=3)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    reason_for_request = models.TextField(default='📛রোগীর নাম: \n💁রোগীর সমস্যা: \n🔴রক্তের গ্রুপ: \n⌚রক্তের প্রয়োজন কারণ: \n🏥রক্তদানের  স্থান : \n📞যোগাযোগ : ')
    fulfilled_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.requester_name} - {self.blood_group} - {self.status} - {self.location}"

    def update_status(self, new_status):
        self.status = new_status
        if new_status == 'Fulfilled':
            self.fulfilled_date = timezone.now()
            RecentDonor.objects.create(donor=self.requester, blood_group=self.blood_group)
        self.save()

class RecentReceiver(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3)
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receiver.username} - {self.blood_group}"
    

