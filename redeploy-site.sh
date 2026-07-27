#!/usr/bin/env bash

set -Eeuo pipefail

readonly APP_DIR="/root/benjamin-portfolio-site"
readonly COMPOSE_FILE="docker-compose.prod.yml"

cd "${APP_DIR}"

git fetch origin main
git reset --hard origin/main

docker compose -f "${COMPOSE_FILE}" down
docker compose -f "${COMPOSE_FILE}" up -d --build
