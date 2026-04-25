from django.contrib import admin

from crm_core.models import (
    Activity,
    Company,
    Contact,
    Invoice,
    Opportunity,
    OpportunityStageHistory,
    Pipeline,
    PipelineStage,
    SalesGoal,
    Visit,
)


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "owner", "phone", "email", "is_active")
    list_filter = ("industry", "is_active", "owner")
    search_fields = ("name", "legal_name", "tax_id", "email", "phone")
    inlines = [ContactInline]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company", "position", "email", "phone", "is_primary")
    list_filter = ("is_primary", "is_active")
    search_fields = ("first_name", "last_name", "email", "company__name")


class PipelineStageInline(admin.TabularInline):
    model = PipelineStage
    extra = 0


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    inlines = [PipelineStageInline]


@admin.register(PipelineStage)
class PipelineStageAdmin(admin.ModelAdmin):
    list_display = ("name", "pipeline", "order", "stage_type", "probability", "is_active")
    list_filter = ("pipeline", "stage_type", "is_active")
    search_fields = ("name",)


class OpportunityStageHistoryInline(admin.TabularInline):
    model = OpportunityStageHistory
    extra = 0
    readonly_fields = ("entered_at", "exited_at", "duration_seconds")


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "owner", "stage", "status", "amount", "expected_close_date", "created_at")
    list_filter = ("status", "pipeline", "stage", "owner", "expected_close_date")
    search_fields = ("title", "company__name", "contact__first_name", "contact__last_name")
    date_hierarchy = "created_at"
    inlines = [OpportunityStageHistoryInline]


@admin.register(OpportunityStageHistory)
class OpportunityStageHistoryAdmin(admin.ModelAdmin):
    list_display = ("opportunity", "from_stage", "to_stage", "changed_by", "entered_at", "exited_at", "duration_seconds")
    list_filter = ("to_stage", "changed_by")
    search_fields = ("opportunity__title",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("subject", "activity_type", "status", "assigned_to", "company", "opportunity", "due_at")
    list_filter = ("activity_type", "status", "assigned_to", "due_at")
    search_fields = ("subject", "description", "company__name", "opportunity__title")
    date_hierarchy = "due_at"


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("company", "opportunity", "executive", "visit_date", "purpose")
    list_filter = ("executive", "visit_date")
    search_fields = ("company__name", "purpose", "result")
    date_hierarchy = "visit_date"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "company", "executive", "issued_date", "total", "status")
    list_filter = ("status", "executive", "issued_date")
    search_fields = ("invoice_number", "company__name")
    date_hierarchy = "issued_date"


@admin.register(SalesGoal)
class SalesGoalAdmin(admin.ModelAdmin):
    list_display = ("executive", "month", "year", "goal_amount")
    list_filter = ("executive", "year", "month")
