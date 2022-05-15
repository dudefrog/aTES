install: install_deps migrate

install_deps:
	poetry install

dev:
	poetry run python manage.py runserver 9070

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

admin:
	poetry run python manage.py createsuperuser --username admin --email admin@admin.com

consume:
	poetry run python manage.py consume
