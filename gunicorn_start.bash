#!/bin/bash
NAME="cactus"                                  # Name of the application
DJANGODIR=/var/www/cactus             # Django project directory
USER=it-cfa                                        # the user to run as
GROUP=it-cfa                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=cactus.settings.prod             # which settings file should Django use
DJANGO_WSGI_MODULE=cactus.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh

# Activate the virtual environment
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
workon cactus

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ~/Envs/cactus/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=127.0.0.1:8000
  --log-level=debug \
  --log-file=-