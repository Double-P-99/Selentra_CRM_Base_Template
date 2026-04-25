"""Dashboard views."""

from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count, Sum, Q
from datetime import timedelta
from apps.core.mixins import CRMLoginRequiredMixin
from apps.contacts.models import Contact, Company
from apps.deals.models import Deal
from apps.activities.models import Activity


class DashboardView(CRMLoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        seven_days = now + timedelta(days=7)

        ctx['total_contacts'] = Contact.objects.filter(is_active=True).count()
        ctx['total_companies'] = Company.objects.filter(is_active=True).count()
        ctx['total_deals'] = Deal.objects.filter(is_active=True).count()
        ctx['total_deal_value'] = Deal.objects.filter(
            is_active=True
        ).aggregate(total=Sum('value'))['total'] or 0

        ctx['new_contacts_month'] = Contact.objects.filter(
            is_active=True, created_at__gte=thirty_days_ago
        ).count()

        ctx['pending_activities'] = Activity.objects.filter(
            is_active=True, status__in=['pending', 'in_progress']
        ).count()

        ctx['overdue_activities'] = Activity.objects.filter(
            is_active=True,
            due_date__lt=now,
            status__in=['pending', 'in_progress']
        ).count()

        ctx['upcoming_activities'] = Activity.objects.filter(
            is_active=True,
            due_date__gte=now,
            due_date__lte=seven_days,
            status__in=['pending', 'in_progress']
        ).select_related('contact', 'deal', 'assigned_to').order_by('due_date')[:5]

        ctx['recent_deals'] = Deal.objects.filter(
            is_active=True
        ).select_related('stage', 'contact', 'company').order_by('-created_at')[:5]

        ctx['recent_contacts'] = Contact.objects.filter(
            is_active=True
        ).select_related('company').order_by('-created_at')[:5]

        ctx['deals_by_stage'] = Deal.objects.filter(
            is_active=True
        ).values('stage__name').annotate(
            count=Count('id'), total_value=Sum('value')
        ).order_by('stage__order')

        return ctx
