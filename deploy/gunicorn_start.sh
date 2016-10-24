#!/bin/bash

NAME="{{ project_name }}"                                  # Name of the application
DJANGODIR=/home/ubuntu/{{ project_name }}                  # Django project directory
SOCKFILE=/home/ubuntu/{{ project_name }}/run/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                        # the user to run as
GROUP=ubuntu                                     # the group to run as
NUM_WORKERS=5                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE={{ project_name }}.settings.production             # which settings file should Django use
DJANGO_WSGI_MODULE={{ project_name }}.wsgi                     # WSGI module name
CONFIG_FILE=/home/ubuntu/{{ project_name }}/deploy/gunicorn_config.py
echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/ubuntu/.virtualenvs/{{ project_name }}/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export NEW_RELIC_CONFIG_FILE=/home/ubuntu/{{ project_name }}/newrelic.ini

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
#exec ../.virtualenvs/hsorka-ar/bin/newrelic-admin run-program ../.virtualenvs/{{ project_name }}/deploy/gunicorn ${DJANGO_WSGI_MODULE}:application \
exec /home/ubuntu/.virtualenvs/{{ project_name }}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=info \
  --log-file=- \