from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from ninja import Schema


# Company schemas
class CompanyIn(Schema):
    name: str
    legal_name: str = ""
    tax_id: str = ""
    industry: str = ""
    website: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    country: str = "Mexico"
    owner_id: Optional[int] = None


class CompanyOut(Schema):
    id: int
    name: str
    legal_name: str
    tax_id: str
    industry: str
    website: str
    phone: str
    email: str
    address: str
    city: str
    state: str
    country: str
    owner_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime


# Contact schemas
class ContactIn(Schema):
    company_id: int
    first_name: str
    last_name: str = ""
    position: str = ""
    email: str = ""
    phone: str = ""
    mobile: str = ""
    notes: str = ""
    is_primary: bool = False


class ContactOut(Schema):
    id: int
    company_id: int
    first_name: str
    last_name: str
    position: str
    email: str
    phone: str
    mobile: str
    notes: str
    is_primary: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


# Pipeline schemas
class PipelineIn(Schema):
    name: str
    description: str = ""


class PipelineOut(Schema):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# PipelineStage schemas
class PipelineStageIn(Schema):
    pipeline_id: int
    name: str
    order: int = 0
    stage_type: str = "open"
    probability: Decimal = Decimal("0")


class PipelineStageOut(Schema):
    id: int
    pipeline_id: int
    name: str
    order: int
    stage_type: str
    probability: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime


# Opportunity schemas
class OpportunityIn(Schema):
    title: str
    company_id: int
    contact_id: Optional[int] = None
    pipeline_id: int
    stage_id: int
    owner_id: int
    amount: Decimal = Decimal("0")
    expected_close_date: Optional[date] = None
    description: str = ""
    lost_reason: str = ""


class OpportunityOut(Schema):
    id: int
    title: str
    company_id: int
    contact_id: Optional[int]
    pipeline_id: int
    stage_id: int
    owner_id: int
    amount: Decimal
    expected_close_date: Optional[date]
    closed_at: Optional[datetime]
    status: str
    description: str
    lost_reason: str
    created_at: datetime
    updated_at: datetime


class OpportunityMoveStageIn(Schema):
    to_stage_id: int
    notes: str = ""


# Activity schemas
class ActivityIn(Schema):
    opportunity_id: Optional[int] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    assigned_to_id: int
    activity_type: str
    subject: str
    description: str = ""
    due_at: Optional[datetime] = None


class ActivityOut(Schema):
    id: int
    opportunity_id: Optional[int]
    company_id: Optional[int]
    contact_id: Optional[int]
    assigned_to_id: int
    activity_type: str
    status: str
    subject: str
    description: str
    due_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


# Visit schemas
class VisitIn(Schema):
    opportunity_id: Optional[int] = None
    company_id: int
    contact_id: Optional[int] = None
    executive_id: int
    visit_date: datetime
    purpose: str
    result: str = ""
    next_steps: str = ""


class VisitOut(Schema):
    id: int
    opportunity_id: Optional[int]
    company_id: int
    contact_id: Optional[int]
    executive_id: int
    visit_date: datetime
    purpose: str
    result: str
    next_steps: str
    created_at: datetime
    updated_at: datetime


# Invoice schemas
class InvoiceIn(Schema):
    opportunity_id: Optional[int] = None
    company_id: int
    executive_id: int
    invoice_number: str
    issued_date: date
    due_date: Optional[date] = None
    subtotal: Decimal = Decimal("0")
    tax: Decimal = Decimal("0")
    total: Decimal
    status: str = "issued"


class InvoiceOut(Schema):
    id: int
    opportunity_id: Optional[int]
    company_id: int
    executive_id: int
    invoice_number: str
    issued_date: date
    due_date: Optional[date]
    paid_date: Optional[date]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
