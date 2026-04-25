"""API ViewSets."""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.contacts.models import Contact, Company
from apps.deals.models import Deal, Pipeline
from apps.activities.models import Activity
from .serializers import (
    ContactSerializer, CompanySerializer, DealSerializer,
    PipelineSerializer, ActivitySerializer,
)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.filter(is_active=True).select_related('company', 'assigned_to')
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'lead_source', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'company__name']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    ordering = ['-created_at']


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['industry', 'size', 'assigned_to']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.filter(is_active=True).select_related(
        'pipeline', 'stage', 'contact', 'company', 'assigned_to'
    )
    serializer_class = DealSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pipeline', 'stage', 'assigned_to', 'currency']
    search_fields = ['title', 'contact__first_name', 'company__name']
    ordering_fields = ['created_at', 'value', 'expected_close_date']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def move_stage(self, request, pk=None):
        """Move a deal to a different stage."""
        deal = self.get_object()
        stage_id = request.data.get('stage_id')
        try:
            from apps.deals.models import Stage
            stage = Stage.objects.get(pk=stage_id, pipeline=deal.pipeline)
            deal.stage = stage
            deal.probability = stage.probability
            deal.save(update_fields=['stage', 'probability', 'updated_at'])
            return Response(self.get_serializer(deal).data)
        except Stage.DoesNotExist:
            return Response({'error': 'Stage not found'}, status=status.HTTP_400_BAD_REQUEST)


class PipelineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pipeline.objects.prefetch_related('stages')
    serializer_class = PipelineSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.filter(is_active=True).select_related(
        'contact', 'company', 'deal', 'assigned_to'
    )
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status', 'priority', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']
    ordering = ['due_date']

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark an activity as completed."""
        activity = self.get_object()
        activity.mark_completed()
        return Response(self.get_serializer(activity).data)
