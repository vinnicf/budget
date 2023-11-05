from django.urls import path
from .views import SignUpView, UserCreateView, LoginAPIView

app_name = 'users'
urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('signupmodal/', UserCreateView.as_view(), name='signupmodal'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),


]
