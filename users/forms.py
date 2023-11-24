from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from bootstrap_modal_forms.forms import BSModalModelForm


BRAZILIAN_STATES_CHOICES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]


class RegistrationForm(forms.ModelForm):
    full_name = forms.CharField(label='Nome completo', max_length=100)
    email = forms.EmailField(label='Email')
    phone_regex = RegexValidator(regex=r'^\(\d{2}\) \d{4,5}-\d{4}$', message="Phone number must be entered in the format: '(99) 99999-9999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, label='Telefone')  # validators should be a list
    state = forms.ChoiceField(choices=BRAZILIAN_STATES_CHOICES, label='Selecione seu Estado')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')
    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'phone_number', 'state', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserModalForm(BSModalModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
