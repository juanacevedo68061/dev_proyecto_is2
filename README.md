# Proyecto CMS

Este repositorio contiene el código fuente y la documentación para el proyecto CMS.

## Flujo de Trabajo y Contribución

Nuestro equipo sigue un flujo de trabajo colaborativo para desarrollar y mantener este proyecto. A continuación, se muestra el proceso que seguimos:

### Paso Inicial: Clonación del Repositorio

1. **Clonar el Repositorio:**
   - Abre tu terminal o línea de comandos.
   - Navega al directorio donde deseas clonar el repositorio.
   - Ejecuta el siguiente comando para clonar el repositorio en tu máquina local:
     ```bash
     git clone https://github.com/juanacevedo68061/dev_proyecto_is2.git
     ```

2. **Ubicarse en el Repositorio:**
   - Una vez que hayas clonado el repositorio, navega al directorio del repositorio en tu terminal:
     ```bash
     cd dev_proyecto_is2
     ```

3. **Cambiar a la Rama Principal:**
   - Es probable que ya estés en la rama principal `main` después de clonar el repositorio. Sin embargo, para estar seguro, puedes ejecutar:
     ```bash
     git checkout main
     ```
     
4. **Actualizar desde la Rama Principal:**
   - Luego, para asegurarte de tener los últimos cambios de la rama principal, ejecuta:
     ```bash
     git pull origin main
     ```
     
### Creación de Nuevas Funcionalidades o Cambios

5. Crea una nueva rama de características para la funcionalidad o cambio:
     ```bash
     git checkout -b funcionalidad/NombreDescriptivo
     ```

6. Realiza tus cambios en la rama de características, agrega y confirma:
     ```bash
     git add .
     git commit -m "Agregar FuncionalidadXYZ: Descripción breve de los cambios"
     ```
7. (Opcional) Mantén tu rama de características actualizada con los cambios de la rama principal:
     ```bash
     git pull origin main
     ```

8. (Opcional) Resuelve conflictos si es necesario y confirma los cambios resultantes.

9. Crea un Pull Request (PR) en GitHub desde tu rama de características hacia la rama principal.
   - Describe tus cambios y proporciona información relevante en el PR.

10. Los miembros del equipo revisarán y comentarán el PR.
   - Realiza ajustes si es necesario.

11. Una vez aprobado, un miembro con permisos fusionará el PR en la rama principal.

12. Elimina la rama de características después de la fusión:
    ```bash
    git branch -d funcionalidad/NombreDescriptivo
    ```

### Presentaciones y Colaboración

Durante el desarrollo, presentamos avances al profesor. Para ello:
   - Mostramos el historial de ramas eliminadas para demostrar el progreso.
   - Explicamos los cambios en las ramas de características y cómo se integran en la rama principal.
   - Resaltamos la documentación, los comentarios de código y las pruebas realizadas.

## Contacto

   Si tienes preguntas o necesitas ayuda, puedes contactar a [juan.acevedo68061@fpuna.edu.py].

¡Gracias por contribuir al proyecto CMS!
