from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from crm_core.models import Activity, Company, Opportunity, Pipeline


@login_required
def dashboard(request):
    today = timezone.now().date()
    user = request.user

    open_opportunities = Opportunity.objects.filter(status="open")
    my_opportunities = open_opportunities.filter(owner=user)

    pending_activities_qs = Activity.objects.filter(
        assigned_to=user,
        status="pending",
    ).select_related("company", "opportunity")

    overdue_activities = pending_activities_qs.filter(due_at__date__lt=today)
    pending_activities = pending_activities_qs[:10]

    pipeline_summary = (
        open_opportunities
        .values("stage__name", "pipeline__name")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("stage__order")
    )

    context = {
        "open_count": open_opportunities.count(),
        "my_open_count": my_opportunities.count(),
        "my_open_value": my_opportunities.aggregate(Sum("amount"))["amount__sum"] or 0,
        "pending_activities": pending_activities,
        "overdue_count": overdue_activities.count(),
        "pipeline_summary": pipeline_summary,
    }
    return render(request, "crm_client/dashboard.html", context)


@login_required
def company_list(request):
    q = request.GET.get("q", "")
    companies = Company.objects.filter(is_active=True).order_by("name")
    if q:
        companies = companies.filter(name__icontains=q)
    return render(request, "crm_client/company_list.html", {"companies": companies, "q": q})


@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    opportunities = company.opportunities.select_related("stage", "pipeline", "owner").order_by("-created_at")
    contacts = company.contacts.filter(is_active=True)
    activities = company.activities.select_related("assigned_to").order_by("-created_at")[:20]
    context = {
        "company": company,
        "opportunities": opportunities,
        "contacts": contacts,
        "activities": activities,
    }
    return render(request, "crm_client/company_detail.html", context)


@login_required
def opportunity_list(request):
    status = request.GET.get("status", "open")
    pipeline_id = request.GET.get("pipeline", "")

    opportunities = Opportunity.objects.select_related(
        "company", "stage", "pipeline", "owner"
    ).order_by("-created_at")

    if status:
        opportunities = opportunities.filter(status=status)
    if pipeline_id:
        opportunities = opportunities.filter(pipeline_id=pipeline_id)

    pipelines = Pipeline.objects.filter(is_active=True)
    context = {
        "opportunities": opportunities,
        "pipelines": pipelines,
        "current_status": status,
        "current_pipeline": pipeline_id,
    }
    return render(request, "crm_client/opportunity_list.html", context)


@login_required
def opportunity_detail(request, pk):
    opp = get_object_or_404(
        Opportunity.objects.select_related("company", "contact", "stage", "pipeline", "owner"),
        pk=pk,
    )
    activities = opp.activities.select_related("assigned_to").order_by("-created_at")
    stage_history = opp.stage_history.select_related("from_stage", "to_stage", "changed_by").order_by("entered_at")
    context = {
        "opportunity": opp,
        "activities": activities,
        "stage_history": stage_history,
    }
    return render(request, "crm_client/opportunity_detail.html", context)


@login_required
def activity_list(request):
    status = request.GET.get("status", "pending")
    activities = Activity.objects.filter(
        assigned_to=request.user,
    ).select_related("company", "opportunity", "contact").order_by("due_at")
    if status:
        activities = activities.filter(status=status)
    context = {"activities": activities, "current_status": status}
    return render(request, "crm_client/activity_list.html", context)


@login_required
def kanban(request):
    pipeline_id = request.GET.get("pipeline", "")
    pipelines = Pipeline.objects.filter(is_active=True).prefetch_related("stages")
    pipeline = None

    if pipeline_id:
        pipeline = get_object_or_404(Pipeline, pk=pipeline_id, is_active=True)
    else:
        pipeline = pipelines.first()

    stages = []
    if pipeline:
        for stage in pipeline.stages.filter(is_active=True).order_by("order"):
            stage.open_opportunities = (
                Opportunity.objects.filter(stage=stage, status="open")
                .select_related("company", "owner")
                .order_by("-amount")
            )
            stages.append(stage)

    context = {
        "pipeline": pipeline,
        "pipelines": pipelines,
        "stages": stages,
        "current_pipeline": str(pipeline_id),
    }
    return render(request, "crm_client/kanban.html", context)


@login_required
def reports(request):
    from django.db.models.functions import TruncMonth
    monthly = (
        Opportunity.objects.filter(status="won")
        .annotate(month=TruncMonth("closed_at"))
        .values("month")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("month")
    )
    won_count = Opportunity.objects.filter(status="won").count()
    lost_count = Opportunity.objects.filter(status="lost").count()
    context = {
        "monthly_won": list(monthly),
        "won_count": won_count,
        "lost_count": lost_count,
    }
    return render(request, "crm_client/reports.html", context)
