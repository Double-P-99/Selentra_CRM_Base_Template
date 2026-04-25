# Selentra CRM Base Template

A reusable Django-based CRM (Customer Relationship Management) base template that can be quickly adapted for different clients. Built with Django 4.2+, Django REST Framework, Bootstrap 5, and Bootstrap Icons.

---

## ✨ Features

| Module | Capabilities |
|--------|-------------|
| **Dashboard** | KPI cards, upcoming activities, recent deals & contacts |
| **Contacts** | Full CRUD, status tracking (Lead → Customer), lead source, tags, notes |
| **Companies** | Company profiles, linked contacts & deals, notes |
| **Deals** | Pipeline management, Kanban board view, weighted value, probability |
| **Activities** | Tasks, calls, meetings, emails – with due dates, priority, overdue alerts |
| **REST API** | Full DRF API for all modules with filtering, search, pagination |
| **Admin** | Django admin with customised interfaces for all models |
| **Auth** | Login/logout, user profiles, roles, teams |
| **Branding** | Client name, logo, primary colour and support email via `.env` |

---

## 🏗 Project Structure

```
Selentra_CRM_Base_Template/
├── apps/
│   ├── core/               # Abstract base models, mixins, context processors
│   │   └── management/commands/seed_demo_data.py
│   ├── accounts/           # Custom User model, Teams, roles
│   ├── contacts/           # Contacts, Companies, Tags, Notes
│   ├── deals/              # Deals, Pipelines, Stages
│   ├── activities/         # Tasks, Calls, Meetings, Emails
│   ├── dashboard/          # Dashboard KPIs and summary views
│   └── api/                # Django REST Framework API (v1)
├── config/
│   ├── settings/
│   │   ├── base.py         # Shared settings
│   │   ├── development.py  # SQLite, console email, debug toolbar
│   │   └── production.py   # PostgreSQL, Redis, security headers
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/              # Django templates (Bootstrap 5)
├── static/
│   ├── css/crm.css         # Custom CRM stylesheet
│   ├── js/crm.js           # Sidebar toggle, alerts, helpers
│   └── vendor/             # Local Bootstrap 5 + Icons (offline-ready)
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── nginx/nginx.conf        # Production nginx configuration
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── .env.example
└── README.md
```

---

## 🚀 Quick Start (Development)

### 1. Clone & set up environment

```bash
git clone <repo-url>
cd Selentra_CRM_Base_Template
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements/development.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set at minimum:
#   SECRET_KEY=your-secret-key
#   CRM_COMPANY_NAME=My Client Name
```

### 3. Run migrations and seed demo data

```bash
python manage.py migrate
python manage.py seed_demo_data     # Creates demo users, contacts, deals, activities
```

### 4. Start the development server

```bash
python manage.py runserver
```

Open **http://localhost:8000** and log in with:
- **Admin:** `admin` / `admin123`
- **Sales:** `sarah.smith` / `demo123`

---

## 🐳 Docker (Production)

```bash
cp .env.example .env
# Edit .env with production values, set DJANGO_SETTINGS_MODULE=config.settings.production

docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

The application will be available at **http://localhost:80**.

---

## 🔧 Customising for a New Client

All branding is controlled via environment variables — no code changes needed:

```env
# .env
CRM_COMPANY_NAME=Acme Corp CRM
CRM_COMPANY_LOGO=/media/logos/acme.png
CRM_PRIMARY_COLOR=#e84040
CRM_SUPPORT_EMAIL=soporte@acme.com
TIME_ZONE=America/Mexico_City
```

For deeper customisation:
- **Override CSS variables** in `static/css/crm.css` (`:root` block)
- **Add client apps** as new Django apps in `apps/`
- **Extend models** by subclassing the abstract base models in `apps/core/models.py`

---

## 🌐 REST API

The API is available at `/api/v1/` and uses token or session authentication.

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/contacts/` | List contacts (filterable by status, assigned_to) |
| `GET /api/v1/companies/` | List companies |
| `GET /api/v1/deals/` | List deals |
| `POST /api/v1/deals/{id}/move_stage/` | Move deal to a new stage |
| `GET /api/v1/pipelines/` | List pipelines with stages |
| `GET /api/v1/activities/` | List activities |
| `POST /api/v1/activities/{id}/complete/` | Mark activity as completed |

Get an auth token:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
     -d "username=admin&password=admin123"
```

---

## 👤 User Roles

| Role | Permissions |
|------|-------------|
| `admin` | Full access + Django admin |
| `manager` | View all records, manage team |
| `sales` | Own records, create/edit |
| `support` | View contacts, log activities |
| `readonly` | View only |

---

## 🧩 Core Abstract Models

All CRM models extend from `apps/core/models.py`:

```python
class BaseModel(UUIDModel, TimeStampedModel):
    """UUID primary key + created_at/updated_at + is_active soft-delete."""
    ...
```

This gives every record:
- **UUID primary key** (URL-safe, no sequential ID leakage)
- **Automatic timestamps** (`created_at`, `updated_at`)
- **Soft delete** via `is_active` flag

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 4.2+ |
| API | Django REST Framework 3.14+ |
| Database (dev) | SQLite |
| Database (prod) | PostgreSQL 16 |
| Cache (prod) | Redis 7 |
| Frontend | Bootstrap 5.3, Bootstrap Icons 1.11 |
| Forms | django-crispy-forms + crispy-bootstrap5 |
| Config | python-decouple |
| Server | Gunicorn + Nginx |
| Containers | Docker + docker-compose |

---

## 📝 License

This project is provided as a reusable base template. Customise freely for each client engagement.
