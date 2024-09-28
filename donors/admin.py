from django.contrib import admin
from .models import Donor, Notification

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'last_donated_date', 'next_estimated_donating_date', 'created_by')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('requester', 'message', 'is_accepted', 'is_declined', 'donor')
    list_filter = ('is_accepted', 'is_declined')
    search_fields = ('requester__username', 'message', 'donor__name')
    