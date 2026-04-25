from django.urls import path
from apps.crm_client import views

app_name = "crm_client"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("companies/", views.company_list, name="company_list"),
    path("companies/<int:pk>/", views.company_detail, name="company_detail"),
    path("opportunities/", views.opportunity_list, name="opportunity_list"),
    path("opportunities/<int:pk>/", views.opportunity_detail, name="opportunity_detail"),
    path("activities/", views.activity_list, name="activity_list"),
    path("reports/", views.reports, name="reports"),
]
