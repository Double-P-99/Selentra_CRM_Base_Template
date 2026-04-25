"""URL patterns for contacts."""

from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    # Contacts
    path('', views.ContactListView.as_view(), name='contact_list'),
    path('new/', views.ContactCreateView.as_view(), name='contact_create'),
    path('<uuid:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('<uuid:pk>/edit/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('<uuid:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    # Companies
    path('companies/', views.CompanyListView.as_view(), name='company_list'),
    path('companies/new/', views.CompanyCreateView.as_view(), name='company_create'),
    path('companies/<uuid:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('companies/<uuid:pk>/edit/', views.CompanyUpdateView.as_view(), name='company_update'),
]
