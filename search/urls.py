# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_results, name='search_results'),
    path('send_confirmation_sms/<int:donor_id>/', views.send_confirmation_sms, name='send_confirmation_sms'),

]