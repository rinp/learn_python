#/bin/bash
COMPOSE_PROJECT_NAME="$(basename "$PWD")_test"
docker-compose -f docker-compose-test.yml up --build -d
docker-compose -f docker-compose-test.yml exec web uv run pytest --cov=app
#docker-compose -f docker-compose-test.yml down -v
