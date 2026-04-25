from django.db.models import Sum, Count, Q

from apps.crm_core.models import Opportunity, Invoice
from apps.crm_core.services.reports_service import CRMReportsService


class ClientCustomReports(CRMReportsService):
    """Client-specific report extensions."""

    @staticmethod
    def revenue_vs_goal(*, year: int, month: int):
        from apps.crm_core.models import SalesGoal
        goals = SalesGoal.objects.filter(year=year, month=month).select_related("executive")
        invoiced = Invoice.objects.filter(
            issued_date__year=year,
            issued_date__month=month,
            status__in=["issued", "paid"],
        ).values("executive__id").annotate(total=Sum("total"))

        invoiced_map = {row["executive__id"]: row["total"] for row in invoiced}

        result = []
        for goal in goals:
            achieved = invoiced_map.get(goal.executive_id, 0) or 0
            result.append({
                "executive": str(goal.executive),
                "goal_amount": goal.goal_amount,
                "achieved": achieved,
                "percentage": round((float(achieved) / float(goal.goal_amount)) * 100, 2) if goal.goal_amount else 0,
            })

        return result
