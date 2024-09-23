# Background Process

## Requirement
- Celery
- Celery Beat
- Redis, ensure that the server has it running and configured for 127.0.0.1:6379


## Installing
- Activate the virtual environment for this project
- `pip install -r requirements.txt` this will install celery related packages (if not installed yet)

## Setup
- Run `./manage.py migrate`, this will migrate requirements for celery beat


## Running
- **Development** (to see any issues): `celery -A bgsos worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler`
- **Production** (running in the backgroud): `celery -A bgsos worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach`
