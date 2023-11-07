#!/bin/sh

# Detener y eliminar todos los contenedores en ejecución
docker stop $(docker ps -q)
docker rm -f $(docker ps -a -q)

# Eliminar todas las imágenes de Docker
docker rmi $(docker images -q)

# Eliminar todos los volúmenes Docker
docker volume prune --force

# Eliminar todas las redes Docker de manera forzada
docker network prune --force
