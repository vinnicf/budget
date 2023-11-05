import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import ReactAppView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('compositions.urls')),
    path('api/', include('compositions.apiurls')),  # DRF endpoints
    path('app/', ReactAppView.as_view(), name='react_app'),
    path('usuario/', include ('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('app/assets/', document_root=os.path.join(settings.BASE_DIR, 'app/assets'))