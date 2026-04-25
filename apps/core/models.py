"""Core abstract models for the CRM."""

import uuid
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base model with UUID primary key."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    """Base model combining UUID pk, timestamps, and soft-delete."""

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
