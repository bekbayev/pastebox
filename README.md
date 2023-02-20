# Pastebox
[![CI](https://github.com/bekbayev/pastebox/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/bekbayev/pastebox/actions/workflows/main.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Django](https://img.shields.io/badge/Django-3.2-success?style=flat&logo=Django)](https://docs.djangoproject.com/en/3.2/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.1-success?style=flat&logo=PostgreSQL)](https://www.postgresql.org/docs/14/index.html)
[![NGINX](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX)](https://nginx.org/)
[![Gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=Gunicorn)](https://gunicorn.org/)
[![RabbitMQ](https://img.shields.io/badge/-RabbitMQ-464646?style=flat&logo=RabbitMQ)](https://www.rabbitmq.com/)
[![Celery](https://img.shields.io/badge/-Celery-464646?style=flat&logo=Celery)](https://docs.celeryproject.org/en/stable/)

Pastebox is a website where you can store any text online for easy sharing.
The Website is mostly used programmers to store snippets of source code or
configuration information, but anyone can insert any text, choose the
expiration date and syntax highlighting. The idea for the project was
[Pastebin.com](https://pastebin.com/).

![pastebox_example_1](https://user-images.githubusercontent.com/121730304/220012614-ae52d07f-d1b8-49f2-8bb0-ed0def8d4b26.png)
![pastebox_example_2](https://user-images.githubusercontent.com/121730304/220012672-11940b66-dfa4-4e76-8e4e-9bf0109a6eb5.png)

## Technologies
### Back-end

- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [Celery](https://github.com/celery/celery)
- [NGINX](https://nginx.org/ru/)
- [Docker](https://www.docker.com/)

### Front-end

- [Bootstrap](https://getbootstrap.com/)

## Features
A few of the things you can do with Pastebox:

- Paste or type any text and save it to get the link and share it
- Specify syntax highlighting for a specific programming language
- Select the expiration time after which the text will be deleted
- Create an account and all saved texts will be linked to the account
- Edit and delete texts in the account

## How To Use
### Prerequisites
To start the website, you'll need the installed on your computer:
- [git](https://git-scm.com/)
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/#install-compose)

### 1. Clone the repo
```
git clone https://github.com/bekbayev/pastebox.git
```

### 2. Create a `.env` file
Inside the repo, create a file `.env` and fill it with the data: 
```
DEBUG=False
DJANGO_SECRET_KEY=<your_secret_key>
ALLOWED_HOSTS=<public_ip>, <website_domain>, <www.website_domain>

DB_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_PASSWORD=<password>
```
replace the values inside the angle brackets with your values without angle
brackets

### 3. Edit the `nginx/pastebox.conf` file
In the `nginx` directory, edit the file `pastebox.conf` by replacing it with
your own values

Example:
```
upstream app {
    server django:8000;
}
server {
    listen 80;
    server_name localhost <public_ip> <website_domain> <www.website_domain>;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /home/app/web/staticfiles/;
    }
}
```

### 4. Run the website
Inside the repo, run the command
(for Linux you may need to add `sudo` before the command):
```
docker compose up -d --build
```
It will take some time to start up

### 5. Create a super user
After the website is up and running, run the command:
```
docker exec -it pastebox-django-1 bash -c "python manage.py createsuperuser"
```
fill out the details

---

After that, you can go to the administration site `/admin/` and manage it.

*Note*: By default registration does not require mail confirmation,
but you can configure this behavior in `src/config/settings.py` file,
there are links to configure it in the comments.
