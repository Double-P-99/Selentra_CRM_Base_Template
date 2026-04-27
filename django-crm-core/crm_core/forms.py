from django import forms
from django.utils.translation import gettext_lazy as _

from crm_core.models import (
    Activity,
    Company,
    Contact,
    Opportunity,
    Pipeline,
    PipelineStage,
    Visit,
)


class CrmBaseModelForm(forms.ModelForm):
    """Base ModelForm that accepts (and discards) an optional ``user`` kwarg.

    Consumer views may inject ``user`` into the form constructor (e.g. to
    pre-populate owner fields or filter querysets). Subclasses that need the
    user should override ``__init__`` and store it before calling super.
    """

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)


class CompanyForm(CrmBaseModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "legal_name",
            "tax_id",
            "industry",
            "website",
            "phone",
            "email",
            "address",
            "city",
            "state",
            "country",
            "owner",
        ]
        labels = {
            "name": _("Nombre"),
            "legal_name": _("Razón social"),
            "tax_id": _("RFC / ID fiscal"),
            "industry": _("Industria"),
            "website": _("Sitio web"),
            "phone": _("Teléfono"),
            "email": _("Correo electrónico"),
            "address": _("Dirección"),
            "city": _("Ciudad"),
            "state": _("Estado"),
            "country": _("País"),
            "owner": _("Responsable"),
        }


class ContactForm(CrmBaseModelForm):
    class Meta:
        model = Contact
        fields = [
            "company",
            "first_name",
            "last_name",
            "position",
            "email",
            "phone",
            "mobile",
            "notes",
            "is_primary",
        ]
        labels = {
            "company": _("Empresa"),
            "first_name": _("Nombre"),
            "last_name": _("Apellido"),
            "position": _("Cargo"),
            "email": _("Correo electrónico"),
            "phone": _("Teléfono"),
            "mobile": _("Celular"),
            "notes": _("Notas"),
            "is_primary": _("Contacto principal"),
        }


class OpportunityForm(CrmBaseModelForm):
    class Meta:
        model = Opportunity
        fields = [
            "title",
            "company",
            "contact",
            "pipeline",
            "stage",
            "owner",
            "amount",
            "expected_close_date",
            "status",
            "lost_reason",
            "description",
        ]
        labels = {
            "title": _("Título"),
            "company": _("Empresa"),
            "contact": _("Contacto"),
            "pipeline": _("Pipeline"),
            "stage": _("Etapa"),
            "owner": _("Responsable"),
            "amount": _("Monto"),
            "expected_close_date": _("Fecha estimada de cierre"),
            "status": _("Estado"),
            "lost_reason": _("Motivo de pérdida"),
            "description": _("Descripción"),
        }
        widgets = {
            "expected_close_date": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }


class ActivityForm(CrmBaseModelForm):
    class Meta:
        model = Activity
        fields = [
            "opportunity",
            "company",
            "contact",
            "assigned_to",
            "created_by",
            "activity_type",
            "status",
            "subject",
            "description",
            "due_at",
            "completed_at",
        ]
        labels = {
            "opportunity": _("Oportunidad"),
            "company": _("Empresa"),
            "contact": _("Contacto"),
            "assigned_to": _("Asignado a"),
            "created_by": _("Creado por"),
            "activity_type": _("Tipo de actividad"),
            "status": _("Estado"),
            "subject": _("Asunto"),
            "description": _("Descripción"),
            "due_at": _("Fecha límite"),
            "completed_at": _("Completada el"),
        }
        widgets = {
            "due_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "completed_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }


class PipelineForm(CrmBaseModelForm):
    class Meta:
        model = Pipeline
        fields = ["name", "description"]
        labels = {
            "name": _("Nombre"),
            "description": _("Descripción"),
        }


class PipelineStageForm(CrmBaseModelForm):
    class Meta:
        model = PipelineStage
        fields = ["pipeline", "name", "order", "stage_type", "probability"]
        labels = {
            "pipeline": _("Pipeline"),
            "name": _("Nombre"),
            "order": _("Orden"),
            "stage_type": _("Tipo de etapa"),
            "probability": _("Probabilidad (%)"),
        }


class VisitForm(CrmBaseModelForm):
    class Meta:
        model = Visit
        fields = [
            "opportunity",
            "company",
            "contact",
            "executive",
            "visit_date",
            "purpose",
            "result",
            "next_steps",
        ]
        labels = {
            "opportunity": _("Oportunidad"),
            "company": _("Empresa"),
            "contact": _("Contacto"),
            "executive": _("Ejecutivo"),
            "visit_date": _("Fecha de visita"),
            "purpose": _("Propósito"),
            "result": _("Resultado"),
            "next_steps": _("Próximos pasos"),
        }
        widgets = {
            "visit_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }
