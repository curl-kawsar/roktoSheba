from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
from request.models import BloodRequest
from django.utils import timezone

class Donor(models.Model):
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

    name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Assuming user with ID 1 exists
    last_donated_date = models.DateField(null=True, blank=True)
    next_estimated_donating_date = models.DateField(null=True, blank=True)
    notifications = models.ManyToManyField('Notification', blank=True, related_name='donor_notifications_set')
    
    def is_eligible_to_donate(self):
        if self.last_donated_date:
            next_eligible_date = self.last_donated_date + relativedelta(months=4)
            return next_eligible_date <= timezone.now().date()
        return True  # If no last donated date, assume eligible
    
    
    def save(self, *args, **kwargs):
        # Calculate the next estimated donating date if the last donated date is provided
        if self.last_donated_date:
            self.next_estimated_donating_date = self.last_donated_date + relativedelta(months=4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

class Notification(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donor_notifications')
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.donor.name} from {self.requester.username}"