from django.urls import include, path

urlpatterns = [
    path("crm/", include("crm_core.urls", namespace="crm_core")),
]
