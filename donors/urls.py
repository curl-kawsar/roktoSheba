from django.urls import path
from . import views

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('new/', views.donor_create, name='donor_create'),
    path('edit/<int:pk>/', views.donor_update, name='donor_update'),
    path('delete/<int:pk>/', views.donor_delete, name='donor_delete'),
    path('notify/<int:pk>/', views.notify_donor, name='notify_donor'),
    path('select/<int:pk>/', views.donor_select, name='donor_select'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/accept/<int:pk>/', views.notification_accept, name='notification_accept'),
    path('notifications/decline/<int:pk>/', views.notification_decline, name='notification_decline'),

]