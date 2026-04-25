"""Views for activities."""

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from apps.core.mixins import CRMLoginRequiredMixin, SuccessMessageMixin
from .models import Activity
from .forms import ActivityForm


class ActivityListView(CRMLoginRequiredMixin, ListView):
    model = Activity
    template_name = 'activities/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 20

    def get_queryset(self):
        qs = Activity.objects.select_related(
            'contact', 'company', 'deal', 'assigned_to'
        ).filter(is_active=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        type_filter = self.request.GET.get('type')
        if type_filter:
            qs = qs.filter(type=type_filter)
        status_filter = self.request.GET.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['type_choices'] = Activity.TYPE_CHOICES
        ctx['status_choices'] = Activity.STATUS_CHOICES
        ctx['q'] = self.request.GET.get('q', '')
        ctx['type_filter'] = self.request.GET.get('type', '')
        ctx['status_filter'] = self.request.GET.get('status', '')
        ctx['overdue_count'] = Activity.objects.filter(
            is_active=True,
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        ).count()
        return ctx


class ActivityDetailView(CRMLoginRequiredMixin, DetailView):
    model = Activity
    template_name = 'activities/activity_detail.html'
    context_object_name = 'activity'


class ActivityCreateView(CRMLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'
    success_message = 'Activity created successfully.'
    success_url = reverse_lazy('activities:activity_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if not form.instance.assigned_to:
            form.instance.assigned_to = self.request.user
        return super().form_valid(form)


class ActivityUpdateView(CRMLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'
    success_message = 'Activity updated successfully.'
    success_url = reverse_lazy('activities:activity_list')


def complete_activity(request, pk):
    """Mark an activity as completed."""
    from django.shortcuts import get_object_or_404, redirect
    from django.urls import reverse
    activity = get_object_or_404(Activity, pk=pk)
    activity.mark_completed()
    messages.success(request, f'Activity "{activity.title}" marked as completed.')
    return redirect(reverse('activities:activity_list'))
