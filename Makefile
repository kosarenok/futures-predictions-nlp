.PHONY: down up logs clean build start

# Stop containers
down:
	docker-compose down

# Clean old images and cache
clean:
	docker builder prune -f

# Build new image
build:
	docker-compose build --no-cache

# Start containers
start:
	docker-compose up -d

# Full rebuild and start (combines clean, build, start)
up: down clean build start

logs:
	docker-compose logs -f

pre_commit:
	pre-commit run --all-files

help:
	@echo "Available commands:"
	@echo "  make down  - Stop containers"
	@echo "  make up    - Full rebuild and restart"
	@echo "  make logs  - View container logs"
	@echo "  make pre_commit - Run pre-commit"
