from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Company(TimeStampedModel, ActiveModel):
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, default="Mexico")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_companies",
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["owner"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class Contact(TimeStampedModel, ActiveModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True)
    position = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["first_name", "last_name"]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["email"]),
            models.Index(fields=["is_primary"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Pipeline(TimeStampedModel, ActiveModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PipelineStage(TimeStampedModel, ActiveModel):
    class StageType(models.TextChoices):
        OPEN = "open", "Open"
        WON = "won", "Won"
        LOST = "lost", "Lost"

    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        related_name="stages",
    )
    name = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    stage_type = models.CharField(
        max_length=20,
        choices=StageType.choices,
        default=StageType.OPEN,
    )
    probability = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        ordering = ["pipeline", "order"]
        unique_together = [("pipeline", "name")]
        indexes = [
            models.Index(fields=["pipeline", "order"]),
            models.Index(fields=["stage_type"]),
        ]

    def __str__(self):
        return f"{self.pipeline.name} / {self.name}"


class Opportunity(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        WON = "won", "Won"
        LOST = "lost", "Lost"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="opportunities",
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="opportunities",
    )
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.PROTECT,
        related_name="opportunities",
    )
    stage = models.ForeignKey(
        PipelineStage,
        on_delete=models.PROTECT,
        related_name="opportunities",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="opportunities",
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    expected_close_date = models.DateField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    lost_reason = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["owner"]),
            models.Index(fields=["pipeline", "stage"]),
            models.Index(fields=["status"]),
            models.Index(fields=["expected_close_date"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.title


class OpportunityStageHistory(TimeStampedModel):
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="stage_history",
    )
    from_stage = models.ForeignKey(
        PipelineStage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="history_from",
    )
    to_stage = models.ForeignKey(
        PipelineStage,
        on_delete=models.PROTECT,
        related_name="history_to",
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stage_changes",
    )
    entered_at = models.DateTimeField(default=timezone.now)
    exited_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["opportunity", "entered_at"]
        indexes = [
            models.Index(fields=["opportunity", "entered_at"]),
            models.Index(fields=["to_stage"]),
            models.Index(fields=["changed_by"]),
        ]

    @property
    def duration_seconds(self):
        end = self.exited_at or timezone.now()
        return int((end - self.entered_at).total_seconds())

    def __str__(self):
        return f"{self.opportunity} -> {self.to_stage}"


class Activity(TimeStampedModel):
    class ActivityType(models.TextChoices):
        CALL = "call", "Call"
        EMAIL = "email", "Email"
        MEETING = "meeting", "Meeting"
        TASK = "task", "Task"
        NOTE = "note", "Note"
        WHATSAPP = "whatsapp", "WhatsApp"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        DONE = "done", "Done"
        CANCELLED = "cancelled", "Cancelled"

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True,
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        related_name="activities",
        null=True,
        blank=True,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assigned_activities",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="created_activities",
        null=True,
        blank=True,
    )

    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-due_at", "-created_at"]
        indexes = [
            models.Index(fields=["assigned_to", "status"]),
            models.Index(fields=["activity_type"]),
            models.Index(fields=["due_at"]),
            models.Index(fields=["opportunity"]),
            models.Index(fields=["company"]),
        ]

    def __str__(self):
        return self.subject


class Visit(TimeStampedModel):
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="visits",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="visits",
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        related_name="visits",
        null=True,
        blank=True,
    )
    executive = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="visits",
    )

    visit_date = models.DateTimeField()
    purpose = models.CharField(max_length=255)
    result = models.TextField(blank=True)
    next_steps = models.TextField(blank=True)

    class Meta:
        ordering = ["-visit_date"]
        indexes = [
            models.Index(fields=["executive", "visit_date"]),
            models.Index(fields=["company"]),
            models.Index(fields=["opportunity"]),
        ]

    def __str__(self):
        return f"{self.company} - {self.visit_date:%Y-%m-%d}"


class Invoice(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ISSUED = "issued", "Issued"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.SET_NULL,
        related_name="invoices",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="invoices",
    )
    executive = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    invoice_number = models.CharField(max_length=100, unique=True)
    issued_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2)

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ISSUED)

    class Meta:
        ordering = ["-issued_date"]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["executive", "issued_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["issued_date"]),
        ]

    def __str__(self):
        return self.invoice_number


class SalesGoal(TimeStampedModel):
    executive = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sales_goals",
    )
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    goal_amount = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        unique_together = [("executive", "year", "month")]
        ordering = ["-year", "-month"]
        indexes = [
            models.Index(fields=["executive", "year", "month"]),
        ]

    def __str__(self):
        return f"{self.executive} - {self.month}/{self.year}"
