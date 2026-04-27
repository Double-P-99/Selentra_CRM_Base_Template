import django
import pytest
from django.conf import settings


def pytest_configure():
    if not settings.configured:
        settings.configure(
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.contenttypes",
                "django.contrib.auth",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django_filters",
                "crm_core",
            ],
            AUTH_USER_MODEL="auth.User",
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
            ROOT_URLCONF="crm_core.test_urls",
            USE_TZ=True,
            SECRET_KEY="test-secret-key",
            MIDDLEWARE=[
                "django.contrib.sessions.middleware.SessionMiddleware",
                "django.contrib.auth.middleware.AuthenticationMiddleware",
                "django.contrib.messages.middleware.MessageMiddleware",
            ],
            TEMPLATES=[
                {
                    "BACKEND": "django.template.backends.django.DjangoTemplates",
                    "DIRS": [],
                    "APP_DIRS": False,
                    "OPTIONS": {
                        "context_processors": [
                            "django.template.context_processors.request",
                            "django.contrib.auth.context_processors.auth",
                            "django.contrib.messages.context_processors.messages",
                        ],
                        "loaders": [
                            (
                                "django.template.loaders.locmem.Loader",
                                {
                                    "crm_core/company_list.html": "{{ companies }}",
                                    "crm_core/company_detail.html": "{{ company }}",
                                    "crm_core/company_form.html": "{{ form }}",
                                    "crm_core/company_confirm_delete.html": "{{ object }}",
                                    "crm_core/contact_list.html": "{{ contacts }}",
                                    "crm_core/contact_detail.html": "{{ contact }}",
                                    "crm_core/contact_form.html": "{{ form }}",
                                    "crm_core/contact_confirm_delete.html": "{{ object }}",
                                    "crm_core/opportunity_list.html": "{{ opportunities }}",
                                    "crm_core/opportunity_detail.html": "{{ opportunity }}",
                                    "crm_core/opportunity_form.html": "{{ form }}",
                                    "crm_core/opportunity_confirm_delete.html": "{{ object }}",
                                    "crm_core/activity_list.html": "{{ activities }}",
                                    "crm_core/activity_form.html": "{{ form }}",
                                    "crm_core/activity_confirm_delete.html": "{{ object }}",
                                    "crm_core/pipeline_list.html": "{{ pipelines }}",
                                    "crm_core/pipeline_form.html": "{{ form }}",
                                    "crm_core/pipeline_confirm_delete.html": "{{ object }}",
                                    "crm_core/pipelinestage_list.html": "{{ pipeline_stages }}",
                                    "crm_core/pipelinestage_form.html": "{{ form }}",
                                    "crm_core/pipelinestage_confirm_delete.html": "{{ object }}",
                                    "crm_core/visit_list.html": "{{ visits }}",
                                    "crm_core/visit_form.html": "{{ form }}",
                                    "crm_core/visit_confirm_delete.html": "{{ object }}",
                                },
                            )
                        ],
                    },
                }
            ],
            SESSION_ENGINE="django.contrib.sessions.backends.db",
            MESSAGE_STORAGE="django.contrib.messages.storage.cookie.CookieStorage",
            LOGIN_URL="/admin/login/",
        )


@pytest.fixture
def user(db):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def client_logged_in(client, user):
    client.login(username="testuser", password="testpass123")
    return client


@pytest.fixture
def pipeline(db):
    from crm_core.models import Pipeline

    return Pipeline.objects.create(name="Test Pipeline")


@pytest.fixture
def pipeline_stage(db, pipeline):
    from crm_core.models import PipelineStage

    return PipelineStage.objects.create(
        pipeline=pipeline,
        name="Prospecting",
        order=1,
        stage_type=PipelineStage.StageType.OPEN,
        probability=10,
    )


@pytest.fixture
def company(db, user):
    from crm_core.models import Company

    return Company.objects.create(name="ACME Corp", owner=user)


@pytest.fixture
def contact(db, company):
    from crm_core.models import Contact

    return Contact.objects.create(
        company=company, first_name="Jane", last_name="Doe"
    )


@pytest.fixture
def opportunity(db, company, pipeline, pipeline_stage, user):
    from crm_core.models import Opportunity

    return Opportunity.objects.create(
        title="Big Deal",
        company=company,
        pipeline=pipeline,
        stage=pipeline_stage,
        owner=user,
    )


@pytest.fixture
def activity(db, user):
    from crm_core.models import Activity

    return Activity.objects.create(
        assigned_to=user,
        activity_type=Activity.ActivityType.CALL,
        subject="Follow up",
    )


@pytest.fixture
def visit(db, company, user):
    from django.utils import timezone

    from crm_core.models import Visit

    return Visit.objects.create(
        company=company,
        executive=user,
        visit_date=timezone.now(),
        purpose="Demo",
    )
