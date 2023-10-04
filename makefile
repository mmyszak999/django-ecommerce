build:
		docker compose build

up:		
		docker compose up

up-detatched:
		docker compose up -d

down:
		docker compose down

migrations:
		docker compose exec backend bash -c "python3 manage.py makemigrations && python3 manage.py migrate"

superuser:
		docker compose exec backend bash -c "python3 manage.py createsuperuser"

test:
		docker compose exec backend bash -c "python manage.py test"

backend-bash:
		docker-compose exec backend bash

black:
		docker compose exec backend bash -c "black ."