from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F, Q, Sum
from django.db.models.functions import ExtractMonth, ExtractYear

from crm_core.models import Invoice, Opportunity, OpportunityStageHistory


class CRMReportsService:
    @staticmethod
    def won_lost_report(*, start_date=None, end_date=None):
        qs = Opportunity.objects.all()
        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)
        return qs.values("owner__id", "owner__username").annotate(
            total=Count("id"),
            won=Count("id", filter=Q(status=Opportunity.Status.WON)),
            lost=Count("id", filter=Q(status=Opportunity.Status.LOST)),
            open=Count("id", filter=Q(status=Opportunity.Status.OPEN)),
            won_amount=Sum("amount", filter=Q(status=Opportunity.Status.WON)),
        ).order_by("owner__username")

    @staticmethod
    def closing_percentage_by_executive(*, start_date=None, end_date=None):
        qs = Opportunity.objects.exclude(status=Opportunity.Status.OPEN)
        if start_date:
            qs = qs.filter(created_at__date__gte=start_date)
        if end_date:
            qs = qs.filter(created_at__date__lte=end_date)
        rows = qs.values("owner__id", "owner__username").annotate(
            closed_total=Count("id"),
            won_total=Count("id", filter=Q(status=Opportunity.Status.WON)),
        )
        result = []
        for row in rows:
            closed_total = row["closed_total"] or 0
            won_total = row["won_total"] or 0
            row["closing_percentage"] = round((won_total / closed_total) * 100, 2) if closed_total else 0
            result.append(row)
        return result

    @staticmethod
    def pipeline_value_by_executive():
        return Opportunity.objects.filter(
            status=Opportunity.Status.OPEN
        ).values(
            "owner__id",
            "owner__username",
            "stage__name",
        ).annotate(
            opportunities=Count("id"),
            pipeline_value=Sum("amount"),
        ).order_by("owner__username", "stage__order")

    @staticmethod
    def monthly_invoicing_by_executive(*, year=None):
        qs = Invoice.objects.filter(status__in=[Invoice.Status.ISSUED, Invoice.Status.PAID])
        if year:
            qs = qs.filter(issued_date__year=year)
        return qs.annotate(
            year=ExtractYear("issued_date"),
            month=ExtractMonth("issued_date"),
        ).values(
            "executive__id",
            "executive__username",
            "year",
            "month",
        ).annotate(
            total_invoiced=Sum("total"),
            invoices=Count("id"),
        ).order_by("year", "month", "executive__username")

    @staticmethod
    def average_time_per_stage():
        duration = ExpressionWrapper(
            F("exited_at") - F("entered_at"),
            output_field=DurationField(),
        )
        return OpportunityStageHistory.objects.filter(
            exited_at__isnull=False
        ).values(
            "to_stage__id",
            "to_stage__name",
        ).annotate(
            avg_duration=Avg(duration),
            movements=Count("id"),
        ).order_by("to_stage__order")
