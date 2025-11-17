#!/bin/bash
MSG=${1:-'auto_migration'}
docker-compose run --rm backend bash -lc "alembic revision --autogenerate -m \"$MSG\" && alembic upgrade head"
