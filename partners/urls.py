from django.urls import path
from . import views

urlpatterns = [
    # ... other url patterns
    path('partners/', views.partners, name='partners'),
]