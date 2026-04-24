from typing import List, Optional

from django.shortcuts import get_object_or_404
from ninja import Router

from apps.crm_core.models import (
    Activity,
    Company,
    Contact,
    Invoice,
    Opportunity,
    Pipeline,
    PipelineStage,
    Visit,
)
from apps.crm_core.api.schemas import (
    ActivityIn,
    ActivityOut,
    CompanyIn,
    CompanyOut,
    ContactIn,
    ContactOut,
    InvoiceIn,
    InvoiceOut,
    OpportunityIn,
    OpportunityMoveStageIn,
    OpportunityOut,
    PipelineIn,
    PipelineOut,
    PipelineStageIn,
    PipelineStageOut,
    VisitIn,
    VisitOut,
)
from apps.crm_core.selectors.opportunity_selectors import get_opportunity_by_id, list_opportunities
from apps.crm_core.selectors.reports_selectors import (
    get_average_time_per_stage,
    get_closing_percentage,
    get_monthly_invoicing,
    get_pipeline_value,
    get_won_lost_report,
)
from apps.crm_core.services.opportunity_service import OpportunityService

companies_router = Router(tags=["Companies"])
contacts_router = Router(tags=["Contacts"])
pipelines_router = Router(tags=["Pipelines"])
opportunities_router = Router(tags=["Opportunities"])
activities_router = Router(tags=["Activities"])
visits_router = Router(tags=["Visits"])
reports_router = Router(tags=["Reports"])


# --- Companies ---

@companies_router.get("/", response=List[CompanyOut])
def list_companies(request, is_active: Optional[bool] = None):
    qs = Company.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return list(qs)


@companies_router.get("/{company_id}/", response=CompanyOut)
def get_company(request, company_id: int):
    return get_object_or_404(Company, pk=company_id)


@companies_router.post("/", response=CompanyOut)
def create_company(request, data: CompanyIn):
    company = Company.objects.create(**data.dict())
    return company


@companies_router.put("/{company_id}/", response=CompanyOut)
def update_company(request, company_id: int, data: CompanyIn):
    company = get_object_or_404(Company, pk=company_id)
    for attr, value in data.dict().items():
        setattr(company, attr, value)
    company.save()
    return company


@companies_router.delete("/{company_id}/")
def delete_company(request, company_id: int):
    company = get_object_or_404(Company, pk=company_id)
    company.delete()
    return {"success": True}


# --- Contacts ---

@contacts_router.get("/", response=List[ContactOut])
def list_contacts(request, company_id: Optional[int] = None):
    qs = Contact.objects.all()
    if company_id:
        qs = qs.filter(company_id=company_id)
    return list(qs)


@contacts_router.get("/{contact_id}/", response=ContactOut)
def get_contact(request, contact_id: int):
    return get_object_or_404(Contact, pk=contact_id)


@contacts_router.post("/", response=ContactOut)
def create_contact(request, data: ContactIn):
    contact = Contact.objects.create(**data.dict())
    return contact


@contacts_router.put("/{contact_id}/", response=ContactOut)
def update_contact(request, contact_id: int, data: ContactIn):
    contact = get_object_or_404(Contact, pk=contact_id)
    for attr, value in data.dict().items():
        setattr(contact, attr, value)
    contact.save()
    return contact


# --- Pipelines ---

@pipelines_router.get("/", response=List[PipelineOut])
def list_pipelines(request):
    return list(Pipeline.objects.all())


@pipelines_router.get("/{pipeline_id}/", response=PipelineOut)
def get_pipeline(request, pipeline_id: int):
    return get_object_or_404(Pipeline, pk=pipeline_id)


@pipelines_router.post("/", response=PipelineOut)
def create_pipeline(request, data: PipelineIn):
    pipeline = Pipeline.objects.create(**data.dict())
    return pipeline


# --- Opportunities ---

@opportunities_router.get("/", response=List[OpportunityOut])
def list_opps(request, owner_id: Optional[int] = None, status: Optional[str] = None, pipeline_id: Optional[int] = None):
    return list(list_opportunities(owner_id=owner_id, status=status, pipeline_id=pipeline_id))


@opportunities_router.get("/{opportunity_id}/", response=OpportunityOut)
def get_opp(request, opportunity_id: int):
    return get_opportunity_by_id(opportunity_id)


@opportunities_router.post("/", response=OpportunityOut)
def create_opp(request, data: OpportunityIn):
    # Use a dummy user (request.auth) - for now use first available user
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.first()
    return OpportunityService.create_opportunity(data=data.dict(), user=user)


@opportunities_router.post("/{opportunity_id}/move_stage/", response=OpportunityOut)
def move_stage(request, opportunity_id: int, data: OpportunityMoveStageIn):
    opportunity = get_opportunity_by_id(opportunity_id)
    to_stage = get_object_or_404(PipelineStage, pk=data.to_stage_id)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.first()
    return OpportunityService.move_stage(opportunity=opportunity, to_stage=to_stage, user=user, notes=data.notes)


# --- Activities ---

@activities_router.get("/", response=List[ActivityOut])
def list_activities(request, assigned_to_id: Optional[int] = None):
    qs = Activity.objects.all()
    if assigned_to_id:
        qs = qs.filter(assigned_to_id=assigned_to_id)
    return list(qs)


@activities_router.get("/{activity_id}/", response=ActivityOut)
def get_activity(request, activity_id: int):
    return get_object_or_404(Activity, pk=activity_id)


@activities_router.post("/", response=ActivityOut)
def create_activity(request, data: ActivityIn):
    activity = Activity.objects.create(**data.dict())
    return activity


# --- Visits ---

@visits_router.get("/", response=List[VisitOut])
def list_visits(request, executive_id: Optional[int] = None):
    qs = Visit.objects.all()
    if executive_id:
        qs = qs.filter(executive_id=executive_id)
    return list(qs)


@visits_router.get("/{visit_id}/", response=VisitOut)
def get_visit(request, visit_id: int):
    return get_object_or_404(Visit, pk=visit_id)


@visits_router.post("/", response=VisitOut)
def create_visit(request, data: VisitIn):
    visit = Visit.objects.create(**data.dict())
    return visit


# --- Reports ---

@reports_router.get("/won-lost/")
def won_lost(request, start_date: Optional[str] = None, end_date: Optional[str] = None):
    return list(get_won_lost_report(start_date=start_date, end_date=end_date))


@reports_router.get("/closing-percentage/")
def closing_percentage(request, start_date: Optional[str] = None, end_date: Optional[str] = None):
    return get_closing_percentage(start_date=start_date, end_date=end_date)


@reports_router.get("/pipeline-value/")
def pipeline_value(request):
    return list(get_pipeline_value())


@reports_router.get("/monthly-invoicing/")
def monthly_invoicing(request, year: Optional[int] = None):
    return list(get_monthly_invoicing(year=year))


@reports_router.get("/average-time-per-stage/")
def average_time_per_stage(request):
    return list(get_average_time_per_stage())
