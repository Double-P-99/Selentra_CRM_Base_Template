"""Admin for contacts."""

from django.contrib import admin
from .models import Contact, Company, Tag, Note


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'lead_source', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'company__name']
    raw_id_fields = ['company', 'assigned_to']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'size', 'email', 'assigned_to', 'created_at']
    list_filter = ['industry', 'size', 'is_active']
    search_fields = ['name', 'email']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['author', 'contact', 'company', 'created_at']
    list_filter = ['author']
    raw_id_fields = ['contact', 'company', 'author']
