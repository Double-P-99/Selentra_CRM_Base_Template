"""Activity models: tasks, calls, meetings, emails."""

from django.db import models
from django.urls import reverse
from apps.core.models import BaseModel


class Activity(BaseModel):
    """A CRM activity (task, call, meeting, email)."""

    TYPE_CHOICES = [
        ('task', 'Task'),
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='task')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    contact = models.ForeignKey(
        'contacts.Contact', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='activities'
    )
    company = models.ForeignKey(
        'contacts.Company', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='activities'
    )
    deal = models.ForeignKey(
        'deals.Deal', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='activities'
    )
    assigned_to = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='activities'
    )
    created_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_activities'
    )

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return f'[{self.get_type_display()}] {self.title}'

    def get_absolute_url(self):
        return reverse('activities:activity_detail', kwargs={'pk': self.pk})

    def mark_completed(self):
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at', 'updated_at'])

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.due_date and self.due_date < timezone.now() and self.status not in ('completed', 'cancelled')
