"""
Management command to seed demo data for the CRM.
Usage: python manage.py seed_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with demo data for development/testing.'

    def handle(self, *args, **options):
        from apps.accounts.models import Team
        from apps.contacts.models import Company, Contact, Tag
        from apps.deals.models import Pipeline, Stage, Deal
        from apps.activities.models import Activity

        self.stdout.write(self.style.NOTICE('Seeding demo data...'))

        # Create admin user
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com', 'role': 'admin',
                'is_staff': True, 'is_superuser': True,
                'first_name': 'Admin', 'last_name': 'User'
            }
        )
        admin.set_password('admin123')
        admin.save()

        # Sales users
        sales1, _ = User.objects.get_or_create(
            username='sarah.smith',
            defaults={'email': 'sarah@example.com', 'role': 'sales',
                      'first_name': 'Sarah', 'last_name': 'Smith'}
        )
        sales1.set_password('demo123')
        sales1.save()

        sales2, _ = User.objects.get_or_create(
            username='john.doe',
            defaults={'email': 'john@example.com', 'role': 'sales',
                      'first_name': 'John', 'last_name': 'Doe'}
        )
        sales2.set_password('demo123')
        sales2.save()

        # Team
        team, _ = Team.objects.get_or_create(name='Sales Team', defaults={'manager': admin})
        for u in [sales1, sales2]:
            u.team = team
            u.save()

        # Tags
        tag_data = [('VIP', '#dc3545'), ('Partner', '#0d6efd'), ('Prospect', '#ffc107'), ('New', '#198754')]
        tags = [Tag.objects.get_or_create(name=n, defaults={'color': c})[0] for n, c in tag_data]

        # Companies
        companies_spec = [
            ('Acme Corporation', 'technology', '201-500', 'New York', 'USA'),
            ('Global Finance Ltd', 'finance', '501-1000', 'London', 'UK'),
            ('HealthFirst Inc', 'healthcare', '51-200', 'Chicago', 'USA'),
            ('TechStartup SAS', 'technology', '1-10', 'Mexico City', 'Mexico'),
            ('Retail World SA', 'retail', '11-50', 'Buenos Aires', 'Argentina'),
        ]
        companies = []
        for name, industry, size, city, country in companies_spec:
            c, _ = Company.objects.get_or_create(
                name=name,
                defaults={'industry': industry, 'size': size, 'city': city, 'country': country,
                          'assigned_to': random.choice([sales1, sales2])}
            )
            companies.append(c)

        # Contacts
        contacts_spec = [
            ('Alice', 'Johnson', 'alice@acme.com', 'customer', 'CTO'),
            ('Bob', 'Williams', 'bob@globalfinance.com', 'prospect', 'CFO'),
            ('Carol', 'Martinez', 'carol@healthfirst.com', 'lead', 'Operations Manager'),
            ('David', 'Chen', 'david@techstartup.mx', 'customer', 'CEO'),
            ('Eva', 'Lopez', 'eva@retailworld.com', 'prospect', 'Marketing Director'),
            ('Frank', 'Brown', 'frank@example.com', 'lead', 'Sales Manager'),
            ('Grace', 'Lee', 'grace@example.com', 'lead', 'Product Manager'),
        ]
        contacts = []
        for i, (fn, ln, email, status, title) in enumerate(contacts_spec):
            c, _ = Contact.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': fn, 'last_name': ln, 'status': status, 'job_title': title,
                    'company': companies[i % len(companies)],
                    'lead_source': random.choice(['website', 'referral', 'social_media', 'cold_call']),
                    'assigned_to': random.choice([sales1, sales2]),
                }
            )
            contacts.append(c)

        # Pipeline & Stages
        pipeline, _ = Pipeline.objects.get_or_create(
            name='Sales Pipeline', defaults={'is_default': True}
        )
        stages_spec = [
            ('Lead', 0, 10, False, False),
            ('Qualified', 1, 25, False, False),
            ('Proposal', 2, 50, False, False),
            ('Negotiation', 3, 75, False, False),
            ('Won', 4, 100, True, False),
            ('Lost', 5, 0, False, True),
        ]
        stages = {}
        for name, order, prob, is_won, is_lost in stages_spec:
            s, _ = Stage.objects.get_or_create(
                pipeline=pipeline, name=name,
                defaults={'order': order, 'probability': prob, 'is_won': is_won, 'is_lost': is_lost}
            )
            stages[name] = s

        # Deals
        deals_spec = [
            ('Acme ERP Implementation', 50000, 'Negotiation'),
            ('Global Finance Analytics Platform', 120000, 'Proposal'),
            ('HealthFirst Patient Portal', 35000, 'Qualified'),
            ('TechStartup CRM License', 8000, 'Won'),
            ('Retail World POS Integration', 22000, 'Lead'),
            ('Enterprise Cloud Migration', 75000, 'Negotiation'),
        ]
        for i, (title, value, stage_name) in enumerate(deals_spec):
            stage = stages[stage_name]
            Deal.objects.get_or_create(
                title=title,
                defaults={
                    'pipeline': pipeline, 'stage': stage, 'value': value,
                    'probability': stage.probability,
                    'contact': contacts[i % len(contacts)],
                    'company': companies[i % len(companies)],
                    'expected_close_date': (timezone.now() + timedelta(days=random.randint(7, 90))).date(),
                    'assigned_to': random.choice([sales1, sales2]),
                }
            )

        # Activities
        activities_spec = [
            ('call', 'Follow-up call with Alice', 'pending', 'high', timezone.now() + timedelta(days=1)),
            ('meeting', 'Product demo with Bob Williams', 'pending', 'high', timezone.now() + timedelta(days=2)),
            ('email', 'Send proposal to Carol Martinez', 'in_progress', 'medium', timezone.now() + timedelta(days=3)),
            ('task', 'Prepare contract for TechStartup', 'completed', 'high', timezone.now() - timedelta(days=1)),
            ('call', 'Quarterly review with Eva Lopez', 'pending', 'low', timezone.now() + timedelta(days=7)),
            ('task', 'Update CRM data for Q4 targets', 'pending', 'medium', timezone.now() - timedelta(days=2)),
        ]
        for i, (atype, title, status, priority, due) in enumerate(activities_spec):
            Activity.objects.get_or_create(
                title=title,
                defaults={
                    'type': atype, 'status': status, 'priority': priority, 'due_date': due,
                    'contact': contacts[i % len(contacts)],
                    'assigned_to': random.choice([sales1, sales2]),
                    'created_by': admin,
                }
            )

        self.stdout.write(self.style.SUCCESS(
            '\nDemo data seeded!\n'
            '  Admin:  admin / admin123\n'
            '  Sales:  sarah.smith / demo123\n'
            '  Sales:  john.doe / demo123\n'
        ))
