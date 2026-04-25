"""Context processors for the CRM."""

from django.conf import settings


def crm_settings(request):
    """Inject CRM branding settings into every template context."""
    return {
        'CRM_COMPANY_NAME': getattr(settings, 'CRM_COMPANY_NAME', 'Selentra CRM'),
        'CRM_COMPANY_LOGO': getattr(settings, 'CRM_COMPANY_LOGO', ''),
        'CRM_PRIMARY_COLOR': getattr(settings, 'CRM_PRIMARY_COLOR', '#0d6efd'),
        'CRM_SUPPORT_EMAIL': getattr(settings, 'CRM_SUPPORT_EMAIL', 'support@example.com'),
    }
