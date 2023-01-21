InfluxDB bootstrap
==================

Instructions from here: https://github.com/docker-library/docs/blob/master/influxdb/README.md

When running from docker or even with docker-compose, first create volumes and then
bootstrap the influxdb:

```
docker volume create influxdb-data
docker volume create influxdb-config
docker volume ls

docker run -d -p 8086:8086 \
      --mount source=influxdb-data,target=/var/lib/influxdb2 \
      --mount source=influxdb-config,target=/etc/influxdb2 \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
      -e DOCKER_INFLUXDB_INIT_PASSWORD=somethingsecret \
      -e DOCKER_INFLUXDB_INIT_ORG=Household \
      -e DOCKER_INFLUXDB_INIT_BUCKET=Energy \
      influxdb:latest

```

However, when running in portainer (stack) then the volumes are mounted
with the stack name prefix: <stackname>_<volumename>
So it's easier to just define the boostrap environment variables in a .env
file that can be loaded just for the initial startup of the stack.



