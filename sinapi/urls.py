import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from users.views import CustomEmailConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('compositions.urls')),
    path('api/', include('compositions.apiurls')),  # DRF endpoints
    path('budget/', include('orcamentos.urls')),
    path('app/', views.ReactAppView.as_view(), name='react_app'),
    path('accounts/confirm-email/<key>/', CustomEmailConfirmView.as_view(), name="account_confirm_email"),
    path('accounts/', include('allauth.urls')),
    path('usuario/', include ('users.urls')),
    path('politica-de-privacidade/', views.privacy_policy, name='privacy_policy'),
    path('termos-de-uso/', views.terms_and_conditions, name='terms_and_conditions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('app/assets/', document_root=os.path.join(settings.BASE_DIR, 'app/assets'))