.PHONY: build up down restart logs shell migrate superuser collectstatic test

# ── Docker ────────────────────────────────────────────────────────────────────
build:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart web

logs:
	docker compose logs -f web

# ── Django ────────────────────────────────────────────────────────────────────
shell:
	docker compose exec web python manage.py shell

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

superuser:
	docker compose exec web python manage.py createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

test:
	docker compose exec web python manage.py test apps

# ── Dev (sin Docker) ──────────────────────────────────────────────────────────
dev:
	cd crm_project && python manage.py runserver

dev-migrate:
	cd crm_project && python manage.py migrate

dev-superuser:
	cd crm_project && python manage.py createsuperuser
