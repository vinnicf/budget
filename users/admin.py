from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, AdminRegistrationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _





class CustomUserAdmin(UserAdmin):
    add_form = AdminRegistrationForm
    form = CustomUserChangeForm
    list_display = ['id', 'age']
    model = CustomUser

     # Add new fieldsets for custom fields
    fieldsets = UserAdmin.fieldsets + (
        (_('Membership Status'), {'fields': ('is_standard', 'is_premium')}),
    )

     # If you also want to include these fields in the create form:
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Membership Status'), {'fields': ('is_standard', 'is_premium')}),
    )
    
    # Custom fields in list_display for them to be listed in the admin list view
    list_display = [ 'username', 'email', 'age', 'is_standard', 'is_premium']
    
    # Filter by these fields
    list_filter = UserAdmin.list_filter + ('is_standard', 'is_premium')

admin.site.register(CustomUser, CustomUserAdmin)