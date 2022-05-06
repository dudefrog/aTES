install: install_deps migrate

install_deps:
	poetry install

dev:
	poetry run python manage.py runserver 5000

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

admin:
	poetry run python manage.py createsuperuser --username admin --email admin@admin.com
