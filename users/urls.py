from django.urls import path, include
from .views import signup, PricingView, UserCreateView, LoginAPIView, payment_view, thank_you, CustomEmailConfirmView, thank_you_email, email_already_confirmed, password_reset_confirm 

app_name = 'users'
urlpatterns = [

    path('signup/', signup, name='signup'),
    path('planos/', PricingView.as_view(), name='pricing'),
    path('payment/<int:user_id>/', payment_view, name='payment'),
    path('signupmodal/', UserCreateView.as_view(), name='signupmodal'),
    path('obrigado/', thank_you, name='thank_you'),
    path('accounts/confirm-email/<key>/', CustomEmailConfirmView.as_view(), name="account_confirm_email"),
    path('obrigado-again/', thank_you_email, name='thank_you_email'),
    path('recuperar-senha/<uid>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
]
