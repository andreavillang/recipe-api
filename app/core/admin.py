from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']

    # This is basically telling Django to generate the fields for us. 
    # I've added tons of indentation for you to understand the parameters.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', )}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important dates'),
            {
                'fields': ('last_login',)
            }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)
# we dont need to add UserAdmin since this 
# Tag doesnt need any special settings coming from the admin.
admin.site.register(models.Tag)