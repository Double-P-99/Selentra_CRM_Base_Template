# django-crm-core

Reusable Django CRM package. Provides models, services, selectors and API routers (django-ninja).

## Installation

```bash
# Local development (editable)
pip install -e ./django-crm-core

# From GitHub
pip install git+https://github.com/YOUR_ORG/django-crm-core.git
```

## Setup

```python
# settings.py
INSTALLED_APPS = [
    ...
    "crm_core",
]
```

```bash
python manage.py migrate
python manage.py seed_crm      # optional: load sample data
```

## What's included

| Module | Contents |
|---|---|
| `crm_core.models` | Company, Contact, Pipeline, PipelineStage, Opportunity, Activity, Visit, Invoice, SalesGoal |
| `crm_core.services` | OpportunityService, CRMReportsService |
| `crm_core.selectors` | opportunity_selectors, reports_selectors |
| `crm_core.api.routers` | companies, contacts, pipelines, opportunities, activities, visits, reports |
| `crm_core.management.commands.seed_crm` | Seed command for sample data |

## Usage in client projects

```python
# myapp/models.py
from crm_core.models import Company

class ClientProfile(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    ...
```

```python
# config/urls.py
from ninja import NinjaAPI
from crm_core.api.routers import companies_router, opportunities_router

api = NinjaAPI()
api.add_router("/companies/", companies_router)
api.add_router("/opportunities/", opportunities_router)
```
