import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from crm_core.models import (
    Activity,
    Company,
    Contact,
    Opportunity,
    Pipeline,
    PipelineStage,
)

User = get_user_model()

INDUSTRIES = ["Technology", "Finance", "Healthcare", "Manufacturing", "Retail", "Education"]
CITIES = ["Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Querétaro"]


class Command(BaseCommand):
    help = "Seed the database with sample CRM data for development/testing."

    def add_arguments(self, parser):
        parser.add_argument("--companies", type=int, default=10)
        parser.add_argument("--opportunities", type=int, default=20)

    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stderr.write("No superuser found. Run createsuperuser first.")
            return

        # Pipeline
        pipeline, _ = Pipeline.objects.get_or_create(name="Sales Pipeline")
        stages_data = [
            ("Prospecto", "open", 0, 10),
            ("Calificado", "open", 1, 25),
            ("Propuesta", "open", 2, 50),
            ("Negociación", "open", 3, 75),
            ("Ganado", "won", 4, 100),
            ("Perdido", "lost", 5, 0),
        ]
        stages = []
        for name, stage_type, order, prob in stages_data:
            stage, _ = PipelineStage.objects.get_or_create(
                pipeline=pipeline,
                name=name,
                defaults={"stage_type": stage_type, "order": order, "probability": Decimal(str(prob))},
            )
            stages.append(stage)

        open_stages = [s for s in stages if s.stage_type == "open"]

        # Companies + Contacts
        companies = []
        for i in range(options["companies"]):
            company, _ = Company.objects.get_or_create(
                name=f"Empresa Demo {i + 1}",
                defaults={
                    "industry": random.choice(INDUSTRIES),
                    "city": random.choice(CITIES),
                    "country": "Mexico",
                    "email": f"contacto@empresa{i + 1}.com",
                    "owner": user,
                },
            )
            companies.append(company)
            Contact.objects.get_or_create(
                company=company,
                first_name=f"Contacto{i + 1}",
                defaults={
                    "last_name": "Demo",
                    "position": "Director General",
                    "email": f"director@empresa{i + 1}.com",
                    "is_primary": True,
                },
            )

        # Opportunities
        for i in range(options["opportunities"]):
            company = random.choice(companies)
            stage = random.choice(open_stages)
            Opportunity.objects.get_or_create(
                title=f"Oportunidad Demo {i + 1}",
                defaults={
                    "company": company,
                    "pipeline": pipeline,
                    "stage": stage,
                    "owner": user,
                    "amount": Decimal(str(random.randint(10000, 500000))),
                    "status": "open",
                    "description": "Oportunidad generada por seed_crm.",
                },
            )

        # Activities
        opportunities = list(Opportunity.objects.filter(status="open")[:5])
        types = ["call", "email", "meeting", "task"]
        for opp in opportunities:
            Activity.objects.get_or_create(
                opportunity=opp,
                subject=f"Seguimiento a {opp.title}",
                defaults={
                    "activity_type": random.choice(types),
                    "assigned_to": user,
                    "status": "pending",
                    "due_at": timezone.now() + timezone.timedelta(days=random.randint(1, 14)),
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete: {len(companies)} companies, {options['opportunities']} opportunities, {len(opportunities)} activities."
        ))
