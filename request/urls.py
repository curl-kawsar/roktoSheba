from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.blood_request_list, name='blood_request_list'),
    path('requests/new/', views.blood_request_create, name='blood_request_create'),
    path('delete/<int:pk>/', views.blood_request_delete, name='blood_request_delete'),
    path('requests/<int:pk>/edit/', views.blood_request_update_status, name='blood_request_update_status'),
    path('requester/<int:user_id>/', views.requester_profile, name='requester_profile'),
    path('recent-receivers/', views.recent_receiver_list, name='recent_receiver_list'),  # Add this line
]