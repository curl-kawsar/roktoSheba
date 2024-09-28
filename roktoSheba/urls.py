
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('donors/', include('donors.urls')),
    # path('recipients/', include('recipients.urls')),
    # path('inventory/', include('inventory.urls'))e
    path('request/', include('request.urls')),
    path('search/', include('search.urls')),
    path('post/', include('post.urls')),
    path('partner/', include('partners.urls')),
    path('developer/', views.developer, name='developer'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)