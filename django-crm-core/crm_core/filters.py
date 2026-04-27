import django_filters
from django.utils.translation import gettext_lazy as _

from crm_core.models import Activity, Company, Contact, Opportunity, Pipeline, Visit


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Nombre"))
    industry = django_filters.CharFilter(lookup_expr="icontains", label=_("Industria"))

    class Meta:
        model = Company
        fields = ["name", "industry", "owner", "is_active"]


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        lookup_expr="icontains", label=_("Nombre")
    )
    last_name = django_filters.CharFilter(
        lookup_expr="icontains", label=_("Apellido")
    )

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "company", "is_primary"]


class OpportunityFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", label=_("Título"))
    expected_close_date = django_filters.DateFromToRangeFilter(
        label=_("Fecha estimada de cierre")
    )

    class Meta:
        model = Opportunity
        fields = ["title", "status", "pipeline", "owner", "expected_close_date"]


class ActivityFilter(django_filters.FilterSet):
    subject = django_filters.CharFilter(lookup_expr="icontains", label=_("Asunto"))

    class Meta:
        model = Activity
        fields = ["subject", "status", "activity_type", "assigned_to"]


class PipelineFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label=_("Nombre"))

    class Meta:
        model = Pipeline
        fields = ["name", "is_active"]


class VisitFilter(django_filters.FilterSet):
    class Meta:
        model = Visit
        fields = ["company", "executive"]
