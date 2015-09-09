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

cd $SUBLOG_DIR

# check env variable set: $WEB_DIR
if [ -z "$WEB_DIR" ]; then
  error_exit "environment variable not set: WEB_DIR"
fi

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
  rm -r $WEB_DIR/*
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

