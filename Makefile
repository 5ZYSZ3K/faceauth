build:
	docker build -t faceauth .
up:
	docker compose up -d
bootstrap: down removevolumes
	docker compose run --rm backend bootstrap
	make up
down:
	docker compose down --remove-orphans
removevolumes: down
	docker volume rm `docker volume ls -f name=faceauth -q|grep -v "pycharm"`
bash:
	docker compose exec backend bash
bash_root:
	docker compose exec -u root backend bash

