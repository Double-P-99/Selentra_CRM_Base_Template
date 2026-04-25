"""Views for deals."""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum
from apps.core.mixins import CRMLoginRequiredMixin, SuccessMessageMixin
from .models import Deal, Pipeline, Stage
from .forms import DealForm


class DealListView(CRMLoginRequiredMixin, ListView):
    model = Deal
    template_name = 'deals/deal_list.html'
    context_object_name = 'deals'
    paginate_by = 20

    def get_queryset(self):
        qs = Deal.objects.select_related('stage', 'pipeline', 'contact', 'company', 'assigned_to')
        qs = qs.filter(is_active=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(contact__first_name__icontains=q) |
                Q(company__name__icontains=q)
            )
        pipeline = self.request.GET.get('pipeline')
        if pipeline:
            qs = qs.filter(pipeline_id=pipeline)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pipelines'] = Pipeline.objects.all()
        ctx['q'] = self.request.GET.get('q', '')
        ctx['pipeline_filter'] = self.request.GET.get('pipeline', '')
        ctx['total_value'] = Deal.objects.filter(is_active=True).aggregate(
            total=Sum('value'))['total'] or 0
        return ctx


class DealPipelineView(CRMLoginRequiredMixin, ListView):
    """Kanban-style pipeline view."""

    model = Deal
    template_name = 'deals/deal_pipeline.html'
    context_object_name = 'deals'

    def get_queryset(self):
        return Deal.objects.select_related(
            'stage', 'contact', 'company', 'assigned_to'
        ).filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pipeline_id = self.request.GET.get('pipeline')
        try:
            if pipeline_id:
                pipeline = Pipeline.objects.get(pk=pipeline_id)
            else:
                pipeline = Pipeline.objects.filter(is_default=True).first() or Pipeline.objects.first()
        except Pipeline.DoesNotExist:
            pipeline = None

        if pipeline:
            stages = pipeline.stages.prefetch_related('deals')
            ctx['pipeline'] = pipeline
            ctx['stages'] = stages
            ctx['stage_deals'] = {
                stage.id: stage.deals.filter(is_active=True).select_related(
                    'contact', 'company', 'assigned_to'
                ) for stage in stages
            }
        ctx['pipelines'] = Pipeline.objects.all()
        return ctx


class DealDetailView(CRMLoginRequiredMixin, DetailView):
    model = Deal
    template_name = 'deals/deal_detail.html'
    context_object_name = 'deal'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['activities'] = self.object.activities.select_related('assigned_to').all()
        return ctx


class DealCreateView(CRMLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'deals/deal_form.html'
    success_message = 'Deal created successfully.'

    def form_valid(self, form):
        if not form.instance.assigned_to:
            form.instance.assigned_to = self.request.user
        # Sync probability from stage
        if form.instance.stage:
            form.instance.probability = form.instance.stage.probability
        return super().form_valid(form)


class DealUpdateView(CRMLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Deal
    form_class = DealForm
    template_name = 'deals/deal_form.html'
    success_message = 'Deal updated successfully.'


class DealDeleteView(CRMLoginRequiredMixin, DeleteView):
    model = Deal
    template_name = 'deals/deal_confirm_delete.html'
    success_url = reverse_lazy('deals:deal_list')

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        messages.success(self.request, 'Deal deleted.')
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.success_url)
