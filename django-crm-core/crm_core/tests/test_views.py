"""
Basic view tests for the crm_core UI layer.

Each model's views are tested for:
- List: HTTP 200 (authenticated), HTTP 302 to login (unauthenticated)
- Create GET: HTTP 200
- Create POST valid: HTTP 302 (redirect to list)
- Update GET: HTTP 200
- Delete POST: HTTP 302
"""

import pytest
from django.urls import reverse


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestCompanyViews:
    def test_list_authenticated(self, client_logged_in):
        url = reverse("crm_core:company_list")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_list_unauthenticated(self, client):
        url = reverse("crm_core:company_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_create_get(self, client_logged_in):
        url = reverse("crm_core:company_create")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged_in):
        url = reverse("crm_core:company_create")
        response = client_logged_in.post(url, {"name": "New Corp", "country": "Mexico"})
        assert response.status_code == 302

    def test_update_get(self, client_logged_in, company):
        url = reverse("crm_core:company_update", kwargs={"pk": company.pk})
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_delete_post(self, client_logged_in, company):
        url = reverse("crm_core:company_delete", kwargs={"pk": company.pk})
        response = client_logged_in.post(url)
        assert response.status_code == 302


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestContactViews:
    def test_list_authenticated(self, client_logged_in):
        url = reverse("crm_core:contact_list")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_list_unauthenticated(self, client):
        url = reverse("crm_core:contact_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_create_get(self, client_logged_in):
        url = reverse("crm_core:contact_create")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged_in, company):
        url = reverse("crm_core:contact_create")
        response = client_logged_in.post(
            url,
            {"company": company.pk, "first_name": "John", "last_name": "Smith"},
        )
        assert response.status_code == 302

    def test_update_get(self, client_logged_in, contact):
        url = reverse("crm_core:contact_update", kwargs={"pk": contact.pk})
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_delete_post(self, client_logged_in, contact):
        url = reverse("crm_core:contact_delete", kwargs={"pk": contact.pk})
        response = client_logged_in.post(url)
        assert response.status_code == 302


# ---------------------------------------------------------------------------
# Opportunity
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestOpportunityViews:
    def test_list_authenticated(self, client_logged_in):
        url = reverse("crm_core:opportunity_list")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_list_unauthenticated(self, client):
        url = reverse("crm_core:opportunity_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_create_get(self, client_logged_in):
        url = reverse("crm_core:opportunity_create")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged_in, company, pipeline, pipeline_stage, user):
        url = reverse("crm_core:opportunity_create")
        response = client_logged_in.post(
            url,
            {
                "title": "New Opportunity",
                "company": company.pk,
                "pipeline": pipeline.pk,
                "stage": pipeline_stage.pk,
                "owner": user.pk,
                "amount": "1000.00",
                "status": "open",
            },
        )
        assert response.status_code == 302

    def test_update_get(self, client_logged_in, opportunity):
        url = reverse("crm_core:opportunity_update", kwargs={"pk": opportunity.pk})
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_delete_post(self, client_logged_in, opportunity):
        url = reverse("crm_core:opportunity_delete", kwargs={"pk": opportunity.pk})
        response = client_logged_in.post(url)
        assert response.status_code == 302


# ---------------------------------------------------------------------------
# Activity
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestActivityViews:
    def test_list_authenticated(self, client_logged_in):
        url = reverse("crm_core:activity_list")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_list_unauthenticated(self, client):
        url = reverse("crm_core:activity_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_create_get(self, client_logged_in):
        url = reverse("crm_core:activity_create")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged_in, user):
        url = reverse("crm_core:activity_create")
        response = client_logged_in.post(
            url,
            {
                "assigned_to": user.pk,
                "activity_type": "call",
                "status": "pending",
                "subject": "Test Call",
            },
        )
        assert response.status_code == 302

    def test_update_get(self, client_logged_in, activity):
        url = reverse("crm_core:activity_update", kwargs={"pk": activity.pk})
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_delete_post(self, client_logged_in, activity):
        url = reverse("crm_core:activity_delete", kwargs={"pk": activity.pk})
        response = client_logged_in.post(url)
        assert response.status_code == 302


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestPipelineViews:
    def test_list_authenticated(self, client_logged_in):
        url = reverse("crm_core:pipeline_list")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_list_unauthenticated(self, client):
        url = reverse("crm_core:pipeline_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_create_get(self, client_logged_in):
        url = reverse("crm_core:pipeline_create")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged_in):
        url = reverse("crm_core:pipeline_create")
        response = client_logged_in.post(url, {"name": "Sales Pipeline"})
        assert response.status_code == 302

    def test_update_get(self, client_logged_in, pipeline):
        url = reverse("crm_core:pipeline_update", kwargs={"pk": pipeline.pk})
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_delete_post(self, client_logged_in, pipeline):
        url = reverse("crm_core:pipeline_delete", kwargs={"pk": pipeline.pk})
        response = client_logged_in.post(url)
        assert response.status_code == 302


# ---------------------------------------------------------------------------
# PipelineStage
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestPipelineStageViews:
    def test_list_authenticated(self, client_logged_in):
        url = reverse("crm_core:pipelinestage_list")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_list_unauthenticated(self, client):
        url = reverse("crm_core:pipelinestage_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_create_get(self, client_logged_in):
        url = reverse("crm_core:pipelinestage_create")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged_in, pipeline):
        url = reverse("crm_core:pipelinestage_create")
        response = client_logged_in.post(
            url,
            {
                "pipeline": pipeline.pk,
                "name": "Qualification",
                "order": 2,
                "stage_type": "open",
                "probability": "20.00",
            },
        )
        assert response.status_code == 302

    def test_update_get(self, client_logged_in, pipeline_stage):
        url = reverse("crm_core:pipelinestage_update", kwargs={"pk": pipeline_stage.pk})
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_delete_post(self, client_logged_in, pipeline_stage):
        url = reverse("crm_core:pipelinestage_delete", kwargs={"pk": pipeline_stage.pk})
        response = client_logged_in.post(url)
        assert response.status_code == 302


# ---------------------------------------------------------------------------
# Visit
# ---------------------------------------------------------------------------

@pytest.mark.django_db
class TestVisitViews:
    def test_list_authenticated(self, client_logged_in):
        url = reverse("crm_core:visit_list")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_list_unauthenticated(self, client):
        url = reverse("crm_core:visit_list")
        response = client.get(url)
        assert response.status_code == 302

    def test_create_get(self, client_logged_in):
        url = reverse("crm_core:visit_create")
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_create_post_valid(self, client_logged_in, company, user):
        url = reverse("crm_core:visit_create")
        response = client_logged_in.post(
            url,
            {
                "company": company.pk,
                "executive": user.pk,
                "visit_date": "2024-06-01T10:00",
                "purpose": "Product demo",
            },
        )
        assert response.status_code == 302

    def test_update_get(self, client_logged_in, visit):
        url = reverse("crm_core:visit_update", kwargs={"pk": visit.pk})
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_delete_post(self, client_logged_in, visit):
        url = reverse("crm_core:visit_delete", kwargs={"pk": visit.pk})
        response = client_logged_in.post(url)
        assert response.status_code == 302
