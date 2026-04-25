"""Contact and Company models for the CRM."""

from django.db import models
from django.urls import reverse
from apps.core.models import BaseModel


class Company(BaseModel):
    """A company or organization."""

    INDUSTRY_CHOICES = [
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('real_estate', 'Real Estate'),
        ('consulting', 'Consulting'),
        ('other', 'Other'),
    ]

    SIZE_CHOICES = [
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1000+', '1000+ employees'),
    ]

    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, blank=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    assigned_to = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='companies'
    )

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contacts:company_detail', kwargs={'pk': self.pk})


class Contact(BaseModel):
    """An individual contact/lead."""

    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('customer', 'Customer'),
        ('churned', 'Churned'),
    ]

    LEAD_SOURCE_CHOICES = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('email_campaign', 'Email Campaign'),
        ('cold_call', 'Cold Call'),
        ('event', 'Event'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='contacts'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    lead_source = models.CharField(max_length=30, choices=LEAD_SOURCE_CHOICES, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='contact_avatars/', blank=True, null=True)
    assigned_to = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='contacts'
    )
    tags = models.ManyToManyField('Tag', blank=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('contacts:contact_detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Tag(models.Model):
    """Tags for categorizing contacts."""

    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#6c757d')  # hex color

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Note(BaseModel):
    """Notes attached to contacts or companies."""

    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True, blank=True, related_name='notes'
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True, related_name='notes'
    )
    author = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, related_name='notes'
    )
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Note by {self.author} on {self.created_at.date()}'
