## Getting started

1. `sudo docker-compose run web django-admin startproject dgtodo .` to build image
2. `docker compose up -d` to build containers
3. `docker exec -it django-graphene-todo_web_1 python manage.py migrate` to run database migrations

To access container, run `docker exec -it CONTAINER_ID sh`
Run `docker-compose build` whenever a new dependency is added
