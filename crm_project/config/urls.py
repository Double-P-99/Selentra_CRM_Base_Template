from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from ninja.security import django_auth

from crm_core.api.routers import (
    companies_router,
    contacts_router,
    pipelines_router,
    opportunities_router,
    activities_router,
    visits_router,
    reports_router,
)

api = NinjaAPI(title="Selentra CRM API", version="1.0.0", auth=django_auth)

api.add_router("/companies/", companies_router)
api.add_router("/contacts/", contacts_router)
api.add_router("/pipelines/", pipelines_router)
api.add_router("/opportunities/", opportunities_router)
api.add_router("/activities/", activities_router)
api.add_router("/visits/", visits_router)
api.add_router("/reports/", reports_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("", include("apps.crm_client.urls", namespace="crm_client")),
]
