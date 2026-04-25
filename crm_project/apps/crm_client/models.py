from django.conf import settings
from django.db import models

from crm_core.models import Company, Opportunity


class ClientProfile(models.Model):
    """Client-specific profile extending core functionality."""
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="client_profile",
    )
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_clients",
    )
    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    tier = models.CharField(
        max_length=50,
        choices=[("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold"), ("platinum", "Platinum")],
        default="bronze",
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["company__name"]

    def __str__(self):
        return f"Profile: {self.company.name}"
