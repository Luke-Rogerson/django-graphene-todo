## Getting started

1. `sudo docker-compose run web django-admin startproject dgtodo .` to build image
2. `docker compose up -d` to build containers

To access container, run `docker exec -it CONTAINER_ID sh`  
Run `docker-compose build` whenever a new dependency is added

### Add a new app

1. `python manage.py APPNAME`

### Database migrations

`python manage.py makemigrations`  
`python manage.py migrate`

### Access shell

`python manage.py shell`

```python
from todos.models import todo

```
