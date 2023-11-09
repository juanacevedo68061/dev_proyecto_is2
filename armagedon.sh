#!/bin/sh

# Detener y eliminar todos los contenedores en ejecución
docker stop $(docker ps -q) >/dev/null 2>&1
docker rm -f $(docker ps -a -q) >/dev/null 2>&1

# Eliminar todas las imágenes de Docker
docker rmi -f $(docker images -q) >/dev/null 2>&1

# Eliminar todos los volúmenes Docker
docker volume prune --force >/dev/null 2>&1

# Eliminar todas las redes Docker de manera forzada
docker network prune --force >/dev/null 2>&1

echo "Entorno Docker limpiado exitosamente."
