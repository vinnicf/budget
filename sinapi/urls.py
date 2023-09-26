from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('compositions/', include('compositions.urls')),
    path('api/', include('compositions.apiurls')),  # DRF endpoints
]
