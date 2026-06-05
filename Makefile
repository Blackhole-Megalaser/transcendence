run: .env
	docker compose up --build
re:
	docker compose down
	+make run
dev: .env
	docker compose up --build --watch
redev:
	docker compose down
	+make dev
rebuild: .env
	clear
	docker compose down
	docker compose up --build --force-recreate
down:
	docker compose down
prune:
	clear
	docker system prune -af
	docker volume prune -af
createsuperuser:
	docker compose run back python /app/manage.py createsuperuser

.env:
	cp .env.example .env
	echo -n 'SECRET_KEY=' >> .env
	tr -dc A-Za-z0-9 </dev/urandom | head -c 64 >> .env
	echo >> .env
