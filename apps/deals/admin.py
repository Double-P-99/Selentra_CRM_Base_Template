"""Admin for deals."""

from django.contrib import admin
from .models import Pipeline, Stage, Deal


class StageInline(admin.TabularInline):
    model = Stage
    extra = 1


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_default', 'order']
    inlines = [StageInline]


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'pipeline', 'order', 'probability', 'is_won', 'is_lost']
    list_filter = ['pipeline']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'stage', 'value', 'currency', 'probability', 'assigned_to', 'created_at']
    list_filter = ['pipeline', 'stage', 'currency', 'is_active']
    search_fields = ['title', 'contact__first_name', 'company__name']
    raw_id_fields = ['contact', 'company', 'assigned_to']
