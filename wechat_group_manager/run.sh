#!/bin/bash
ps -ef | grep 'runapp.py' | grep -v grep | awk '{print $2}' | xargs kill -9
ps -ef | grep 'api.py' | grep -v grep | awk '{print $2}' | xargs kill -9
server/selenium/run.sh -d
python server/api.py &
./runapp.py &
