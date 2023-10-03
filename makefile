build:
		docker compose build

up:		
		docker compose up

up-detatched:
		docker compose up -d

down:
		docker compose down

migrations:
		docker compose exec app_backend bash -c "python3 manage.py makemigrations api && python3 manage.py migrate"

superuser:
		docker compose exec app_backend bash -c "python3 manage.py createsuperuser"

test:
		docker compose exec app_backend bash -c "python manage.py test"

backend-bash:
		docker-compose exec app_backend bash

black:
		docker compose exec app_backend bash -c "black ."