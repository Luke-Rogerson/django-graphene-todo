FROM python:3.9-alpine

# Run in unbuffered mode (recommended when running in container environments)
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# install psycopg2 dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

#  don't user root
RUN adduser -D user
USER user