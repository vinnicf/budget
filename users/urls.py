from django.urls import path, include
from .views import signup, PricingView, UserCreateView, LoginAPIView, payment_view

app_name = 'users'
urlpatterns = [

    path('signup/', signup, name='signup'),
    path('planos/', PricingView.as_view(), name='pricing'),
    path('payment/<int:user_id>/', payment_view, name='payment'),
    path('signupmodal/', UserCreateView.as_view(), name='signupmodal'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),

]
