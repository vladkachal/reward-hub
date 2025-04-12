#!/bin/sh

set -e

echo "INFO: Starting database availability check..."
wait-for-it "$DATABASE_HOST:$DATABASE_PORT" -t 30

echo "INFO: Proceeding with container startup..."
exec "$@"
