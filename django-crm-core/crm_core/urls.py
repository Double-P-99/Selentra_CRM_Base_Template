from django.urls import path

from crm_core.views import (
    ActivityCreateView,
    ActivityDeleteView,
    ActivityListView,
    ActivityUpdateView,
    CompanyCreateView,
    CompanyDeleteView,
    CompanyDetailView,
    CompanyListView,
    CompanyUpdateView,
    ContactCreateView,
    ContactDeleteView,
    ContactDetailView,
    ContactListView,
    ContactUpdateView,
    OpportunityCreateView,
    OpportunityDeleteView,
    OpportunityDetailView,
    OpportunityListView,
    OpportunityUpdateView,
    PipelineCreateView,
    PipelineDeleteView,
    PipelineListView,
    PipelineStageCreateView,
    PipelineStageDeleteView,
    PipelineStageListView,
    PipelineStageUpdateView,
    PipelineUpdateView,
    VisitCreateView,
    VisitDeleteView,
    VisitListView,
    VisitUpdateView,
)

app_name = "crm_core"

urlpatterns = [
    # Company
    path("empresas/", CompanyListView.as_view(), name="company_list"),
    path("empresas/crear/", CompanyCreateView.as_view(), name="company_create"),
    path("empresas/<int:pk>/", CompanyDetailView.as_view(), name="company_detail"),
    path("empresas/<int:pk>/editar/", CompanyUpdateView.as_view(), name="company_update"),
    path("empresas/<int:pk>/eliminar/", CompanyDeleteView.as_view(), name="company_delete"),

    # Contact
    path("contactos/", ContactListView.as_view(), name="contact_list"),
    path("contactos/crear/", ContactCreateView.as_view(), name="contact_create"),
    path("contactos/<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("contactos/<int:pk>/editar/", ContactUpdateView.as_view(), name="contact_update"),
    path("contactos/<int:pk>/eliminar/", ContactDeleteView.as_view(), name="contact_delete"),

    # Opportunity
    path("oportunidades/", OpportunityListView.as_view(), name="opportunity_list"),
    path("oportunidades/crear/", OpportunityCreateView.as_view(), name="opportunity_create"),
    path("oportunidades/<int:pk>/", OpportunityDetailView.as_view(), name="opportunity_detail"),
    path("oportunidades/<int:pk>/editar/", OpportunityUpdateView.as_view(), name="opportunity_update"),
    path("oportunidades/<int:pk>/eliminar/", OpportunityDeleteView.as_view(), name="opportunity_delete"),

    # Activity
    path("actividades/", ActivityListView.as_view(), name="activity_list"),
    path("actividades/crear/", ActivityCreateView.as_view(), name="activity_create"),
    path("actividades/<int:pk>/editar/", ActivityUpdateView.as_view(), name="activity_update"),
    path("actividades/<int:pk>/eliminar/", ActivityDeleteView.as_view(), name="activity_delete"),

    # Pipeline
    path("pipelines/", PipelineListView.as_view(), name="pipeline_list"),
    path("pipelines/crear/", PipelineCreateView.as_view(), name="pipeline_create"),
    path("pipelines/<int:pk>/editar/", PipelineUpdateView.as_view(), name="pipeline_update"),
    path("pipelines/<int:pk>/eliminar/", PipelineDeleteView.as_view(), name="pipeline_delete"),

    # PipelineStage
    path("etapas/", PipelineStageListView.as_view(), name="pipelinestage_list"),
    path("etapas/crear/", PipelineStageCreateView.as_view(), name="pipelinestage_create"),
    path("etapas/<int:pk>/editar/", PipelineStageUpdateView.as_view(), name="pipelinestage_update"),
    path("etapas/<int:pk>/eliminar/", PipelineStageDeleteView.as_view(), name="pipelinestage_delete"),

    # Visit
    path("visitas/", VisitListView.as_view(), name="visit_list"),
    path("visitas/crear/", VisitCreateView.as_view(), name="visit_create"),
    path("visitas/<int:pk>/editar/", VisitUpdateView.as_view(), name="visit_update"),
    path("visitas/<int:pk>/eliminar/", VisitDeleteView.as_view(), name="visit_delete"),
]
