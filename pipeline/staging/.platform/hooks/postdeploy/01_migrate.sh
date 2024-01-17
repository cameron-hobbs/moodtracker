#! /bin/bash
if [[ "$EB_IS_COMMAND_LEADER" == "true" ]]; then
  docker exec `docker ps --no-trunc -q | head -n 1` python3 /app/manage.py migrate
fi

