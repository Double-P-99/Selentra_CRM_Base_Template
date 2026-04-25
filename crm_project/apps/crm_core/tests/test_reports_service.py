from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.crm_core.models import Company, Pipeline, PipelineStage, Opportunity
from apps.crm_core.services.reports_service import CRMReportsService

User = get_user_model()


class ReportsServiceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="exec1", password="pass")
        self.company = Company.objects.create(name="ACME Corp")
        self.pipeline = Pipeline.objects.create(name="Main Pipeline")
        self.stage_open = PipelineStage.objects.create(
            pipeline=self.pipeline,
            name="Prospect",
            order=1,
            stage_type=PipelineStage.StageType.OPEN,
        )
        self.stage_won = PipelineStage.objects.create(
            pipeline=self.pipeline,
            name="Won",
            order=2,
            stage_type=PipelineStage.StageType.WON,
        )
        self.stage_lost = PipelineStage.objects.create(
            pipeline=self.pipeline,
            name="Lost",
            order=3,
            stage_type=PipelineStage.StageType.LOST,
        )

    def _create_opp(self, status, amount=1000):
        return Opportunity.objects.create(
            title=f"Opp {status}",
            company=self.company,
            pipeline=self.pipeline,
            stage=self.stage_open,
            owner=self.user,
            amount=amount,
            status=status,
        )

    def test_closing_percentage_by_executive(self):
        self._create_opp(Opportunity.Status.WON)
        self._create_opp(Opportunity.Status.WON)
        self._create_opp(Opportunity.Status.LOST)
        result = CRMReportsService.closing_percentage_by_executive()
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row["won_total"], 2)
        self.assertEqual(row["closed_total"], 3)
        self.assertAlmostEqual(row["closing_percentage"], 66.67, places=1)
