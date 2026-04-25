"""API URL patterns."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register('contacts', views.ContactViewSet, basename='contact')
router.register('companies', views.CompanyViewSet, basename='company')
router.register('deals', views.DealViewSet, basename='deal')
router.register('pipelines', views.PipelineViewSet, basename='pipeline')
router.register('activities', views.ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
