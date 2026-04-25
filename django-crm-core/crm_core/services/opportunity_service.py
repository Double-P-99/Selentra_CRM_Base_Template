from django.db import transaction
from django.utils import timezone

from crm_core.models import Opportunity, OpportunityStageHistory, PipelineStage


class OpportunityService:
    @staticmethod
    @transaction.atomic
    def create_opportunity(*, data: dict, user):
        opportunity = Opportunity.objects.create(**data)

        OpportunityStageHistory.objects.create(
            opportunity=opportunity,
            from_stage=None,
            to_stage=opportunity.stage,
            changed_by=user,
            entered_at=timezone.now(),
            notes="Initial stage",
        )

        return opportunity

    @staticmethod
    @transaction.atomic
    def move_stage(*, opportunity: Opportunity, to_stage: PipelineStage, user, notes: str = ""):
        if opportunity.stage_id == to_stage.id:
            return opportunity

        current_history = (
            OpportunityStageHistory.objects
            .filter(opportunity=opportunity, exited_at__isnull=True)
            .order_by("-entered_at")
            .first()
        )

        now = timezone.now()

        if current_history:
            current_history.exited_at = now
            current_history.save(update_fields=["exited_at", "updated_at"])

        from_stage = opportunity.stage
        opportunity.stage = to_stage

        if to_stage.stage_type == PipelineStage.StageType.WON:
            opportunity.status = Opportunity.Status.WON
            opportunity.closed_at = now
        elif to_stage.stage_type == PipelineStage.StageType.LOST:
            opportunity.status = Opportunity.Status.LOST
            opportunity.closed_at = now
        else:
            opportunity.status = Opportunity.Status.OPEN
            opportunity.closed_at = None

        opportunity.save(update_fields=["stage", "status", "closed_at", "updated_at"])

        OpportunityStageHistory.objects.create(
            opportunity=opportunity,
            from_stage=from_stage,
            to_stage=to_stage,
            changed_by=user,
            entered_at=now,
            notes=notes,
        )

        return opportunity
