from django.urls import path
from .views import SignUpView, UserCreateView

app_name = 'users'
urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('signupmodal/', UserCreateView.as_view(), name='signupmodal'),


]
