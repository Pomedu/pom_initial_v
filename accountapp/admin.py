from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name','email','phone_number', 'role', 'is_admin')
    list_filter = ('is_admin', 'role')
    fieldsets = (
        (None,{'fields':('name','email','password')}),
        ("Personal info",{'fields':('role','phone_number')}),
        ("Permissions",{'fields':('is_admin',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','email', 'role','phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','name','phone_number')
    ordering = ('name',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
