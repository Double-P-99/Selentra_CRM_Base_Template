"""Admin configuration for accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'team', 'is_active']
    list_filter = ['role', 'team', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('CRM Info', {'fields': ('role', 'team', 'phone', 'bio', 'avatar')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('CRM Info', {'fields': ('role', 'team', 'phone')}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'created_at']
    search_fields = ['name']
