run:
	docker compose up --build
re:
	docker compose down
	+make run
dev:
	docker compose up --build --watch
redev:
	docker compose down
	+make dev
rebuild:
	docker compose down
	docker compose up --build --force-recreate
prune:
	docker system prune -a
	docker volume prune -a
createsuperuser:
	docker compose run back python /app/manage.py createsuperuser