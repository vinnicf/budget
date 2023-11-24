from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegistrationForm, CustomUserChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = CustomUserChangeForm
    list_display = ['username','id', 'age']
    model = CustomUser

     # Add new fieldsets for custom fields
    fieldsets = UserAdmin.fieldsets + (
        (_('Membership Status'), {'fields': ('is_standard', 'is_premium')}),
    )

     # If you also want to include these fields in the create form:
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Membership Status'), {'fields': ('is_standard', 'is_premium')}),
    )
    
    # Make sure to include your custom fields in list_display if you want them listed in the admin list view
    list_display = ['username', 'email', 'age', 'is_standard', 'is_premium']
    
    # And also in list_filter if you want to be able to filter by these fields
    list_filter = UserAdmin.list_filter + ('is_standard', 'is_premium')

admin.site.register(CustomUser, CustomUserAdmin)
