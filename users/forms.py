from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from bootstrap_modal_forms.forms import BSModalModelForm


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
            }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Usuário'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repita a senha'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserModalForm(BSModalModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
