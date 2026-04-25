"""Deal / Pipeline models for the CRM."""

from django.db import models
from django.urls import reverse
from apps.core.models import BaseModel


class Pipeline(models.Model):
    """A sales pipeline with stages."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            Pipeline.objects.exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class Stage(models.Model):
    """A stage within a pipeline."""

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    probability = models.PositiveIntegerField(default=0, help_text='Win probability (%)')
    is_won = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)

    class Meta:
        ordering = ['pipeline', 'order']
        unique_together = ['pipeline', 'name']

    def __str__(self):
        return f'{self.pipeline.name} → {self.name}'


class Deal(BaseModel):
    """A deal/opportunity in the CRM pipeline."""

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('MXN', 'Mexican Peso'),
        ('BRL', 'Brazilian Real'),
        ('ARS', 'Argentine Peso'),
        ('COP', 'Colombian Peso'),
    ]

    title = models.CharField(max_length=200)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.PROTECT, related_name='deals')
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name='deals')
    contact = models.ForeignKey(
        'contacts.Contact', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='deals'
    )
    company = models.ForeignKey(
        'contacts.Company', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='deals'
    )
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    probability = models.PositiveIntegerField(default=0, help_text='Win probability (%)')
    expected_close_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='deals'
    )

    class Meta:
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('deals:deal_detail', kwargs={'pk': self.pk})

    @property
    def weighted_value(self):
        return self.value * self.probability / 100
