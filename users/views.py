from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, UserModalForm
from .models import CustomUser
from bootstrap_modal_forms.generic import BSModalCreateView

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

class UserCreateView(BSModalCreateView):
    template_name = 'modalform.html'
    form_class = UserModalForm
    success_message = 'Sucesso. User Criado'
    success_url = reverse_lazy('home')
