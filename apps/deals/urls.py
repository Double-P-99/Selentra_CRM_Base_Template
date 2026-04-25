"""URL patterns for deals."""

from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.DealListView.as_view(), name='deal_list'),
    path('pipeline/', views.DealPipelineView.as_view(), name='deal_pipeline'),
    path('new/', views.DealCreateView.as_view(), name='deal_create'),
    path('<uuid:pk>/', views.DealDetailView.as_view(), name='deal_detail'),
    path('<uuid:pk>/edit/', views.DealUpdateView.as_view(), name='deal_update'),
    path('<uuid:pk>/delete/', views.DealDeleteView.as_view(), name='deal_delete'),
]
