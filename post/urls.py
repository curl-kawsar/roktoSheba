# Step 5: Add a URL pattern for the post list view in post/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
]