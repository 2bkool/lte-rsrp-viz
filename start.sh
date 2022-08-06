#!/bin/bash


PID_FILE=lte-rsrp-viz.pid
APP_ROOT=/data/lte-rsrp-viz


echo "Starting lte-rsrp-viz..."
sleep 2

if [ ! -f $PID_FILE ]; then
    ~/.pyenv/versions/lte-rsrp-viz/bin/python -V
    ~/.pyenv/versions/lte-rsrp-viz/bin/python $APP_ROOT/runserver.py >> /dev/null & echo $! > $PID_FILE
fi

