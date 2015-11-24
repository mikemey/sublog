#!/bin/bash

H_PID=`ps -ax | grep -e "\ssublog" | sed 's/\s*\([0-9]*\).*/\1/'`
if [ -z $H_PID ]; then
  echo "process not found."
else
  echo "shutdown process: [$H_PID]"
  kill $H_PID >> /dev/null
fi

. deploy/sublog_variables.sh

export SECRET_KEY="`date | md5sum`"
screen -dmS sublog /usr/bin/python manage.py runserver 0.0.0.0:4444
