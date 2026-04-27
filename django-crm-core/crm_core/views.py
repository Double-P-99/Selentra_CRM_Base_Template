from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from crm_core.filters import (
    ActivityFilter,
    CompanyFilter,
    ContactFilter,
    OpportunityFilter,
    PipelineFilter,
    VisitFilter,
)
from crm_core.forms import (
    ActivityForm,
    CompanyForm,
    ContactForm,
    OpportunityForm,
    PipelineForm,
    PipelineStageForm,
    VisitForm,
)
from crm_core.models import (
    Activity,
    Company,
    Contact,
    Opportunity,
    Pipeline,
    PipelineStage,
    Visit,
)
from crm_core.services.opportunity_service import OpportunityService


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

class CompanyListView(LoginRequiredMixin, FilterView):
    model = Company
    form_class = CompanyForm
    filterset_class = CompanyFilter
    template_name = "crm_core/company_list.html"
    context_object_name = "companies"
    paginate_by = 25


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = "crm_core/company_detail.html"
    context_object_name = "company"


class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "crm_core/company_form.html"
    success_url = reverse_lazy("crm_core:company_list")
    success_message = _("Empresa creada exitosamente.")


class CompanyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "crm_core/company_form.html"
    success_url = reverse_lazy("crm_core:company_list")
    success_message = _("Empresa actualizada exitosamente.")


class CompanyDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Company
    template_name = "crm_core/company_confirm_delete.html"
    success_url = reverse_lazy("crm_core:company_list")
    success_message = _("Empresa eliminada exitosamente.")


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

class ContactListView(LoginRequiredMixin, FilterView):
    model = Contact
    form_class = ContactForm
    filterset_class = ContactFilter
    template_name = "crm_core/contact_list.html"
    context_object_name = "contacts"
    paginate_by = 25


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "crm_core/contact_detail.html"
    context_object_name = "contact"


class ContactCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "crm_core/contact_form.html"
    success_url = reverse_lazy("crm_core:contact_list")
    success_message = _("Contacto creado exitosamente.")


class ContactUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "crm_core/contact_form.html"
    success_url = reverse_lazy("crm_core:contact_list")
    success_message = _("Contacto actualizado exitosamente.")


class ContactDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Contact
    template_name = "crm_core/contact_confirm_delete.html"
    success_url = reverse_lazy("crm_core:contact_list")
    success_message = _("Contacto eliminado exitosamente.")


# ---------------------------------------------------------------------------
# Opportunity
# ---------------------------------------------------------------------------

class OpportunityListView(LoginRequiredMixin, FilterView):
    model = Opportunity
    form_class = OpportunityForm
    filterset_class = OpportunityFilter
    template_name = "crm_core/opportunity_list.html"
    context_object_name = "opportunities"
    paginate_by = 25


class OpportunityDetailView(LoginRequiredMixin, DetailView):
    model = Opportunity
    template_name = "crm_core/opportunity_detail.html"
    context_object_name = "opportunity"


class OpportunityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Opportunity
    form_class = OpportunityForm
    template_name = "crm_core/opportunity_form.html"
    success_url = reverse_lazy("crm_core:opportunity_list")
    success_message = _("Oportunidad creada exitosamente.")

    def form_valid(self, form):
        self.object = OpportunityService.create_opportunity(
            data=form.cleaned_data, user=self.request.user
        )
        return HttpResponseRedirect(self.get_success_url())


class OpportunityUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Opportunity
    form_class = OpportunityForm
    template_name = "crm_core/opportunity_form.html"
    success_url = reverse_lazy("crm_core:opportunity_list")
    success_message = _("Oportunidad actualizada exitosamente.")


class OpportunityDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Opportunity
    template_name = "crm_core/opportunity_confirm_delete.html"
    success_url = reverse_lazy("crm_core:opportunity_list")
    success_message = _("Oportunidad eliminada exitosamente.")


# ---------------------------------------------------------------------------
# Activity
# ---------------------------------------------------------------------------

class ActivityListView(LoginRequiredMixin, FilterView):
    model = Activity
    form_class = ActivityForm
    filterset_class = ActivityFilter
    template_name = "crm_core/activity_list.html"
    context_object_name = "activities"
    paginate_by = 25


class ActivityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "crm_core/activity_form.html"
    success_url = reverse_lazy("crm_core:activity_list")
    success_message = _("Actividad creada exitosamente.")


class ActivityUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "crm_core/activity_form.html"
    success_url = reverse_lazy("crm_core:activity_list")
    success_message = _("Actividad actualizada exitosamente.")


class ActivityDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Activity
    template_name = "crm_core/activity_confirm_delete.html"
    success_url = reverse_lazy("crm_core:activity_list")
    success_message = _("Actividad eliminada exitosamente.")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

class PipelineListView(LoginRequiredMixin, FilterView):
    model = Pipeline
    form_class = PipelineForm
    filterset_class = PipelineFilter
    template_name = "crm_core/pipeline_list.html"
    context_object_name = "pipelines"
    paginate_by = 25


class PipelineCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pipeline
    form_class = PipelineForm
    template_name = "crm_core/pipeline_form.html"
    success_url = reverse_lazy("crm_core:pipeline_list")
    success_message = _("Pipeline creado exitosamente.")


class PipelineUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pipeline
    form_class = PipelineForm
    template_name = "crm_core/pipeline_form.html"
    success_url = reverse_lazy("crm_core:pipeline_list")
    success_message = _("Pipeline actualizado exitosamente.")


class PipelineDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Pipeline
    template_name = "crm_core/pipeline_confirm_delete.html"
    success_url = reverse_lazy("crm_core:pipeline_list")
    success_message = _("Pipeline eliminado exitosamente.")


# ---------------------------------------------------------------------------
# PipelineStage
# ---------------------------------------------------------------------------

class PipelineStageListView(LoginRequiredMixin, FilterView):
    model = PipelineStage
    form_class = PipelineStageForm
    filterset_class = PipelineFilter
    template_name = "crm_core/pipelinestage_list.html"
    context_object_name = "pipeline_stages"
    paginate_by = 25


class PipelineStageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PipelineStage
    form_class = PipelineStageForm
    template_name = "crm_core/pipelinestage_form.html"
    success_url = reverse_lazy("crm_core:pipelinestage_list")
    success_message = _("Etapa creada exitosamente.")


class PipelineStageUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PipelineStage
    form_class = PipelineStageForm
    template_name = "crm_core/pipelinestage_form.html"
    success_url = reverse_lazy("crm_core:pipelinestage_list")
    success_message = _("Etapa actualizada exitosamente.")


class PipelineStageDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PipelineStage
    template_name = "crm_core/pipelinestage_confirm_delete.html"
    success_url = reverse_lazy("crm_core:pipelinestage_list")
    success_message = _("Etapa eliminada exitosamente.")


# ---------------------------------------------------------------------------
# Visit
# ---------------------------------------------------------------------------

class VisitListView(LoginRequiredMixin, FilterView):
    model = Visit
    form_class = VisitForm
    filterset_class = VisitFilter
    template_name = "crm_core/visit_list.html"
    context_object_name = "visits"
    paginate_by = 25


class VisitCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Visit
    form_class = VisitForm
    template_name = "crm_core/visit_form.html"
    success_url = reverse_lazy("crm_core:visit_list")
    success_message = _("Visita creada exitosamente.")


class VisitUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Visit
    form_class = VisitForm
    template_name = "crm_core/visit_form.html"
    success_url = reverse_lazy("crm_core:visit_list")
    success_message = _("Visita actualizada exitosamente.")


class VisitDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Visit
    template_name = "crm_core/visit_confirm_delete.html"
    success_url = reverse_lazy("crm_core:visit_list")
    success_message = _("Visita eliminada exitosamente.")
