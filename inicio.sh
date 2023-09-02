#!/bin/bash

# Eliminar migraciones
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
echo "Migraciones eliminadas"

# Eliminar archivos .pyc y carpetas __pycache__
find . -type f -name "*.pyc" -delete -o -type d -name "__pycache__" -delete
echo "Archivos .pyc y carpetas __pycache__ eliminados"
