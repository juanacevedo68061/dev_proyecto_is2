# Proyecto CMS

Este repositorio contiene el código fuente y la documentación para el proyecto CMS.

## Flujo de Trabajo y Contribución

Nuestro equipo sigue un flujo de trabajo colaborativo para desarrollar y mantener este proyecto. Aquí está el proceso que seguimos:

### Creación de Nuevas Funcionalidades o Cambios

1. Asegúrate de estar en la rama principal (main) y obten los últimos cambios:
'''
git checkout main
git pull origin main
'''
2. Crea una nueva rama de características para la funcionalidad o cambio:

'git checkout -b funcionalidad/NombreDescriptivo'

3. Realiza tus cambios en la rama de características, agrega y confirma:
'''
git add .
git commit -m "Agregar FuncionalidadXYZ: Descripción breve de los cambios"
'''
4. (Opcional) Mantén tu rama de características actualizada con los cambios de la rama principal:

'git pull origin main'

5. (Opcional) Resuelve conflictos si es necesario y confirma los cambios resultantes.

6. Crea un Pull Request (PR) en GitHub desde tu rama de características hacia la rama principal.
- Describe tus cambios y proporciona información relevante en el PR.

7. Los miembros del equipo revisarán y comentarán el PR.
- Realiza ajustes si es necesario.

8. Una vez aprobado, un miembro con permisos fusionará el PR en la rama principal.

9. Elimina la rama de características después de la fusión:

'git branch -d funcionalidad/NombreDescriptivo'

### Presentaciones y Colaboración

Durante el desarrollo, presentamos avances al profesor. Para ello:
- Mostramos el historial de ramas eliminadas para demostrar el progreso.
- Explicamos los cambios en las ramas de características y cómo se integran en la rama principal.
- Resaltamos la documentación, los comentarios de código y las pruebas realizadas.

## Contacto

Si tienes preguntas o necesitas ayuda, puedes contactar a [juan.acevedo68061@fpuna.edu.py].

¡Gracias por contribuir al proyecto CMS!
