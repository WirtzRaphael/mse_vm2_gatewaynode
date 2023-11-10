#!/bin/bash

# note : more params for setup, use github secrets
# note : volume mount
# fixme : password

# simple start
#docker run \
#              -p 8086:8086 \
#              -v myInfluxVolume:/var/lib/influxdb2 \
#              influxdb:latest
#

# automated setup
docker run -d -p 8086:8086 \
      -v $PWD/data:/var/lib/influxdb2 \
      -v $PWD/config.yml:/etc/influxdb2/config.yml \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME=my-user \
      -e DOCKER_INFLUXDB_INIT_PASSWORD=my-password \
      -e DOCKER_INFLUXDB_INIT_ORG=my-org \
      -e DOCKER_INFLUXDB_INIT_BUCKET=my-bucket \
      influxdb:2.0
