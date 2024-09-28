from django.contrib import admin

# Register your models here.
# Step 3: Register the Post model in post/admin.py
from django.contrib import admin
from .models import Post

admin.site.register(Post)