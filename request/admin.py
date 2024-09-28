from django.contrib import admin
from .models import BloodRequest, RecentDonor, RecentReceiver

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'contact_number', 'blood_group', 'status', 'request_date')

class RecentDonorAdmin(admin.ModelAdmin):
    list_display = ('donor', 'blood_group', 'donation_date')

class RecentReceiverAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'blood_group', 'received_date')

admin.site.register(BloodRequest, BloodRequestAdmin)
admin.site.register(RecentDonor, RecentDonorAdmin)
admin.site.register(RecentReceiver, RecentReceiverAdmin)