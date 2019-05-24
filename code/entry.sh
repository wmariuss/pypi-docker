#!/usr/bin/env bash

set -e

echo Creating config file...
python make_config.py

echo Start...
if [ "$ENV" == "prod" ]; then
  uwsgi --ini-paste-logged server.ini
else
  pserve server.ini
fi

echo Bye!
