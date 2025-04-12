#!/bin/sh

set -e

echo "INFO: Starting database availability check..."
wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -t 30

echo "INFO: Applying migrations..."
python src/manage.py migrate --noinput
