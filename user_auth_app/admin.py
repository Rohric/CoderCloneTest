# Admin configuration for the custom User model.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Extends the default UserAdmin to expose birthdate and address fields."""

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Fields', {'fields': ('birthdate', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Fields', {'fields': ('birthdate', 'address')}),
    )
