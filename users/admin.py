from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('permissions', 'folder')}),
admin.site.register(CustomUser, UserAdmin)
