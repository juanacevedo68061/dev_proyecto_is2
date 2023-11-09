#!/bin/sh

# Detener y eliminar todos los contenedores en ejecución
if [ "$(docker ps -q)" ]; then
    docker stop $(docker ps -q)
    docker rm -f $(docker ps -a -q)
else
    echo "No hay contenedores en ejecución para detener o eliminar."
fi

# Eliminar todas las imágenes de Docker
if [ "$(docker images -q)" ]; then
    docker rmi $(docker images -q)
else
    echo "No hay imágenes de Docker para eliminar."
fi

# Eliminar todos los volúmenes Docker
if [ "$(docker volume ls -q)" ]; then
    docker volume prune --force
else
    echo "No hay volúmenes de Docker para eliminar."
fi

# Eliminar todas las redes Docker de manera forzada
if [ "$(docker network ls -q)" ]; then
    docker network prune --force
else
    echo "No hay redes de Docker para eliminar."
fi
