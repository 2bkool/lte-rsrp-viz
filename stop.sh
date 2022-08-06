#!/bin/bash

PID_FILE=lte-rsrp-viz.pid

if [ -f $PID_FILE ]; then
    PID=$(cat $PID_FILE)
    sleep 2
    kill $PID
    echo "lte-rsrp-viz stopped."
    rm $PID_FILE
else
    echo "lte-rsrp-viz is not running!"
fi
