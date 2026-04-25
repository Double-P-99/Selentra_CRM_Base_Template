from django.contrib import admin
from apps.crm_client.models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("company", "account_manager", "tier", "contract_start", "contract_end")
    list_filter = ("tier", "account_manager")
    search_fields = ("company__name",)
