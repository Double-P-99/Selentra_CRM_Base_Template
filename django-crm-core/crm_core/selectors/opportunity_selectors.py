from crm_core.models import Opportunity


def get_opportunity_by_id(opportunity_id: int) -> Opportunity:
    return Opportunity.objects.select_related(
        "company", "contact", "pipeline", "stage", "owner"
    ).get(pk=opportunity_id)


def list_opportunities(*, owner_id=None, status=None, pipeline_id=None):
    qs = Opportunity.objects.select_related(
        "company", "contact", "pipeline", "stage", "owner"
    )
    if owner_id:
        qs = qs.filter(owner_id=owner_id)
    if status:
        qs = qs.filter(status=status)
    if pipeline_id:
        qs = qs.filter(pipeline_id=pipeline_id)
    return qs
