"""API serializers."""

from rest_framework import serializers
from apps.contacts.models import Contact, Company, Tag
from apps.deals.models import Deal, Pipeline, Stage
from apps.activities.models import Activity
from apps.accounts.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'role']

    def get_full_name(self, obj):
        return str(obj)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'industry', 'size', 'website', 'phone', 'email',
            'city', 'country', 'assigned_to', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
            'job_title', 'company', 'company_name', 'status', 'lead_source',
            'city', 'country', 'assigned_to', 'tags', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['id', 'name', 'order', 'probability', 'is_won', 'is_lost']


class PipelineSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Pipeline
        fields = ['id', 'name', 'description', 'is_default', 'stages']


class DealSerializer(serializers.ModelSerializer):
    stage_name = serializers.CharField(source='stage.name', read_only=True)
    contact_name = serializers.SerializerMethodField()
    company_name = serializers.CharField(source='company.name', read_only=True)
    weighted_value = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Deal
        fields = [
            'id', 'title', 'pipeline', 'stage', 'stage_name', 'contact', 'contact_name',
            'company', 'company_name', 'value', 'currency', 'probability', 'weighted_value',
            'expected_close_date', 'assigned_to', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_contact_name(self, obj):
        return str(obj.contact) if obj.contact else None


class ActivitySerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'type', 'title', 'description', 'status', 'priority',
            'due_date', 'completed_at', 'contact', 'company', 'deal',
            'assigned_to', 'created_by', 'is_overdue', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at']
