run:
	docker compose up --build
re:
	docker compose down
	+make run
dev:
	docker compose up --build
redev:
	docker compose down
	+make dev
createsuperuser:
	docker compose run back python /app/manage.py createsuperuser