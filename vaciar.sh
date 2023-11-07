#!/bin/sh

docker-compose down
docker rmi $(docker images)
docker volume rm $(docker volume ls -q)
docker network prune --force