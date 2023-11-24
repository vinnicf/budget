from django.urls import path
from .views import signup, PricingView, UserCreateView, LoginAPIView

app_name = 'users'
urlpatterns = [

    path('signup/', signup, name='signup'),
    path('planos/', PricingView.as_view(), name='pricing'),
    path('signupmodal/', UserCreateView.as_view(), name='signupmodal'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),


]
