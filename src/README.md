Run backend instructions:<p>
Make sure docker is running and make sure you are in `src` folder
```
docker ps
```

CREATE empty files/folders for frontend build
```
mkdir frontend_build/ && touch frontend_build/index.html
mkdir frontend_build/static
```

Build only needed once or when I make changes and you repull on git
```
docker-compose build
```
Run container for image (these two steps below can be done with Docker desktop. Just run the image
with option 8000 as port!)
```
docker-compose up -d
```
Check its running
```
docker ps
```

Create superuser for login for now (and django admin access)
```
docker exec -it moodtracker_api python3 manage.py createsuperuser
```

Migrate database (if db changes):
```
docker exec -it moodtracker_api poetry run python3 /app/manage.py migrate
```

Static files (if you want to view django admin)
```
docker exec -it moodtracker_api poetry run python3 /app/manage.py collectstatic --noinput
```

If you are rebuilding
```
docker stop moodtracker_api
docker rm moodtracker_api
.. build cmd
.. run cmd
```

API runs on localhost:8000, database for now is temporary so destroyed on container shutdown
