# niyo_tms

Niyo Task Management system

Overview

The Task Management System is a web application built with Django, Django REST Framework (DRF), Redis, Celery, PostgreSQL, and Django Channels. It allows users to manage projects, sprints, and tasks with real-time updates using WebSockets. The application uses JWT for authentication.


Features

Projects: Create and manage projects, assign members, and track project details.

Sprints: Define sprints within projects, with start and end dates.

Tasks: Create tasks within sprints, assign them to project members, and track their status.

Real-time updates: Receive real-time updates for task changes using WebSockets.

User Authentication: Secure access to the application with JWT-based authentication.


Technologies Used:

Backend: Django, Django REST Framework, Django Channels

Database: PostgreSQL

Task Queue: Celery with Redis as a message broker

Real-time: Django Channels with Redis

Containerization: Docker and Docker Compose


# Setup and Installation

Prerequisites
Docker and Docker Compose

# Installation Steps

# Clone the Repository

git clone https://github.com/ulaitorcodes/niyo_tms.git
cd niyo_tms


POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

JWT_SECRET_KEY=your_jwt_secret_key


# Environment Variables

Create a .env file in the project root with the following variables:
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

JWT_SECRET_KEY=your_jwt_secret_key


# Build and Start Docker Containers

docker-compose -f docker-compose.local.yml build
docker-compose -f docker-compose.local.yml up


# Export Docker Compose File for Future Commands

export COMPOSE_FILE=docker-compose.local.yml

# Execute Management Commands
As with any shell command that we wish to run in our container, this is done using the docker compose -f docker-compose.local.yml run --rm command:

$ docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

$ docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser