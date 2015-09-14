#!/bin/bash
pushd . >> /dev/null

SUBLOG_DIR=~/bin/sublog
SUBLOG_NAME=sublog

function error_exit {
  log "$1"
  popd >> /dev/null
  exit 1
}

function log {
  echo "=== deploy ==> $1"
}

function check_env {
  if [ -z "${!1}" ]; then
    error_exit "environment variable not set: $1"
  fi
}

cd $SUBLOG_DIR

log "pulling code repo..."
git pull >> /dev/null
if [ $? -ne 0 ]; then
  error_exit "pull from git repository failed!"
fi

check_env "WEB_DIR"

SUBLOG_PID=`screen -list | grep $SUBLOG_NAME | cut -f1 -d'.' | sed 's/\W//g'`
if [ -z $SUBLOG_PID ]; then
  log "no process named [$SUBLOG_NAME] found."
else
  log "shutting down $SUBLOG_NAME process: $SUBLOG_PID"
  kill $SUBLOG_PID >> /dev/null
fi

if [ "$1" == "-f" ]; then
  log "deleting static files in folder [$WEB_DIR/]..."
  cd $WEB_DIR
  ls | grep -v 'ghost' | xargs rm -r >> /dev/null 2>&1
  cd $SUBLOG_DIR
fi

export SECRET_KEY="$(head -n 1 /dev/urandom | tr -dc 'a-zA-Z0-9~!@#$%^&*_-')XXX23ifjcf"
log "generated random key: $SECRET_KEY"

log "collecting static files..."
python manage.py collectstatic --noinput >> /dev/null
if [ $? -ne 0 ]; then
  error_exit "collecting static files failed!"
fi
cp assets/favicons/* $WEB_DIR

log "migrate (if required)..."
python manage.py migrate src > /dev/null
if [ $? -ne 0 ]; then
  error_exit "migration failed!"
fi

log "starting server daemon..."
screen -dmS sublog /usr/bin/python manage.py runserver 0.0.0.0:4444
if [ $? -ne 0 ]; then
  error_exit "starting server failed!"
fi

log "finished successfully."
popd >> /dev/null

exit 0

