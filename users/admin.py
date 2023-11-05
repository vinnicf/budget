from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username','id', 'age']
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
