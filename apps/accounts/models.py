"""User and team models for the CRM."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class User(AbstractUser):
    """Extended User model for CRM."""

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Sales Manager'),
        ('sales', 'Sales Representative'),
        ('support', 'Support Agent'),
        ('readonly', 'Read Only'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales')
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='members'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_manager(self):
        return self.role in ('admin', 'manager') or self.is_superuser


class Team(TimeStampedModel):
    """Sales/support team grouping."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='managed_teams', limit_choices_to={'role__in': ['admin', 'manager']}
    )

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['name']

    def __str__(self):
        return self.name
