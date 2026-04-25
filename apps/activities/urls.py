"""URL patterns for activities."""

from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.ActivityListView.as_view(), name='activity_list'),
    path('new/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('<uuid:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('<uuid:pk>/edit/', views.ActivityUpdateView.as_view(), name='activity_update'),
    path('<uuid:pk>/complete/', views.complete_activity, name='activity_complete'),
]
