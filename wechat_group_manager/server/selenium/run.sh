#!/usr/bin/env bash
DEBUG=""

if [ -n "$1" ] && [ $1 == "-d" ]; then
  DEBUG="-debug"
fi

VERSION="2.46.0"
TMP="/tmp"
TIMEOUT=300000

HUB="hub"
NODE_CHROME="node-chrome$DEBUG"

echo Tearing down Selenium Chrome Node container
docker stop $NODE_CHROME
docker rm $NODE_CHROME

echo Tearing down Selenium Hub container
docker stop $HUB
docker rm $HUB

echo Starting Selenium Hub Container
docker run -d -p 4444:4444 --name $HUB -e GRID_TIMEOUT=$TIMEOUT --restart=always selenium/$HUB:$VERSION
sleep 2

echo Starting Selenium Node Container
if [ $DEBUG == "-debug" ]; then
  docker run -d -p 5900:5900 --link $HUB:hub -v $TMP:/tmp --name $NODE_CHROME --restart=always selenium/$NODE_CHROME:$VERSION
else
  docker run -d --link $HUB:hub -v $TMP:/tmp --name $NODE_CHROME --restart=always selenium/$NODE_CHROME:$VERSION
fi

sleep 2

echo Done
