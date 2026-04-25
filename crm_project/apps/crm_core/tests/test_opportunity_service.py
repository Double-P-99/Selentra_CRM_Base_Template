from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.crm_core.models import (
    Company, Pipeline, PipelineStage, Opportunity, OpportunityStageHistory
)
from apps.crm_core.services.opportunity_service import OpportunityService

User = get_user_model()


class OpportunityServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.company = Company.objects.create(name="Test Co")
        self.pipeline = Pipeline.objects.create(name="Sales Pipeline")
        self.stage_open = PipelineStage.objects.create(
            pipeline=self.pipeline,
            name="Prospecting",
            order=1,
            stage_type=PipelineStage.StageType.OPEN,
        )
        self.stage_won = PipelineStage.objects.create(
            pipeline=self.pipeline,
            name="Closed Won",
            order=2,
            stage_type=PipelineStage.StageType.WON,
        )
        self.stage_lost = PipelineStage.objects.create(
            pipeline=self.pipeline,
            name="Closed Lost",
            order=3,
            stage_type=PipelineStage.StageType.LOST,
        )

    def _make_opportunity_data(self):
        return {
            "title": "Test Opportunity",
            "company_id": self.company.id,
            "pipeline_id": self.pipeline.id,
            "stage_id": self.stage_open.id,
            "owner_id": self.user.id,
            "amount": 1000,
        }

    def test_create_opportunity_creates_stage_history(self):
        opp = OpportunityService.create_opportunity(data=self._make_opportunity_data(), user=self.user)
        self.assertEqual(OpportunityStageHistory.objects.filter(opportunity=opp).count(), 1)
        history = OpportunityStageHistory.objects.get(opportunity=opp)
        self.assertEqual(history.notes, "Initial stage")

    def test_move_stage_closes_previous_history(self):
        opp = OpportunityService.create_opportunity(data=self._make_opportunity_data(), user=self.user)
        OpportunityService.move_stage(opportunity=opp, to_stage=self.stage_won, user=self.user)
        first_history = OpportunityStageHistory.objects.filter(opportunity=opp).order_by("entered_at").first()
        self.assertIsNotNone(first_history.exited_at)

    def test_move_stage_to_won(self):
        opp = OpportunityService.create_opportunity(data=self._make_opportunity_data(), user=self.user)
        opp = OpportunityService.move_stage(opportunity=opp, to_stage=self.stage_won, user=self.user)
        self.assertEqual(opp.status, Opportunity.Status.WON)
        self.assertIsNotNone(opp.closed_at)

    def test_move_stage_to_lost(self):
        opp = OpportunityService.create_opportunity(data=self._make_opportunity_data(), user=self.user)
        opp = OpportunityService.move_stage(opportunity=opp, to_stage=self.stage_lost, user=self.user)
        self.assertEqual(opp.status, Opportunity.Status.LOST)
        self.assertIsNotNone(opp.closed_at)

    def test_move_same_stage_no_change(self):
        opp = OpportunityService.create_opportunity(data=self._make_opportunity_data(), user=self.user)
        OpportunityService.move_stage(opportunity=opp, to_stage=self.stage_open, user=self.user)
        self.assertEqual(OpportunityStageHistory.objects.filter(opportunity=opp).count(), 1)
