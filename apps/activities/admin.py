"""Admin for activities."""

from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'status', 'priority', 'due_date', 'assigned_to']
    list_filter = ['type', 'status', 'priority', 'is_active']
    search_fields = ['title', 'description']
    raw_id_fields = ['contact', 'company', 'deal', 'assigned_to', 'created_by']
    date_hierarchy = 'due_date'
