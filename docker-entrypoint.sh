#!/bin/sh
set -e

# Apply pending migrations before serving. Set SKIP_MIGRATIONS=1 to opt out,
# e.g. when several replicas start at the same time.
if [ "${SKIP_MIGRATIONS:-0}" != "1" ]; then
    python manage.py migrate --noinput
fi

exec "$@"
