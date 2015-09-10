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
  echo "$1--${1}--${!1}--"
  if [ -z "${!1}" ]; then
    error_exit "environment variable not set: $1"
  fi
}

check_env "WEB_DIR"
check_env "SECRET_KEY"

cd $SUBLOG_DIR

log "pulling code repo..."
git pull >> /dev/null
if [ $? -ne 0 ]; then
  error_exit "pull from git repository failed!"
fi

log "shutting down running server..."
SUBLOG_PID=`screen -list | grep $SUBLOG_NAME | cut -f1 -d'.' | sed 's/\W//g'`
if [ -z $SUBLOG_PID ]; then
  log "no process named [$SUBLOG_NAME] found."
else
  log "shutdown $SUBLOG_NAME process: $SUBLOG_PID"
  kill $SUBLOG_PID >> /dev/null
fi

log "clean up and deploy static files..."
if [ "$1" == "-f" ]; then
  log "deleting files in static files folder [$WEB_DIR/]..."
  cd $WEB_DIR
  ls | grep -v 'ghost' | xargs rm -r
  cd $SUBLOG_DIR
fi

python manage.py collectstatic --noinput >> /dev/null
if [ $? -ne 0 ]; then
  error_exit "collecting static files failed!"
fi
cp assets/favicons/* $WEB_DIR

log "starting server daemon..."
screen -dmS sublog /usr/bin/python manage.py runserver 0.0.0.0:4444

log "finished successfully."
popd >> /dev/null

exit 0

