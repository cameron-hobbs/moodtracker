#! /bin/bash
docker exec `docker ps --no-trunc -q | head -n 1` python3 /app/manage.py collectstatic --no-input
