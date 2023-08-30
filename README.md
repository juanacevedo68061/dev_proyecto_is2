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

5. **Crear una Nueva Rama Feature:**
   - Antes de trabajar en una nueva funcionalidad, crea una nueva rama feature utilizando el comando:
     ```bash
     git checkout -b nombre-de-la-rama
     ```

6. **Realizar Cambios y Confirmar:**
   - Realiza los cambios necesarios en la nueva rama:
     ```bash
     git add .  # Agregar los cambios al área de preparación
     git commit -m "Descripción concisa de los cambios"  # Confirmar los cambios con un mensaje
     ```

7. **Fusionar Cambios y Eliminar la Rama Feature:**
   - Si has terminado de trabajar en la funcionalidad, fusiona los cambios en la rama main y realiza un commit para registrar el merge, luego borra la rama feature:
     ```bash
     git checkout main  # Cambia a la rama principal
     git merge --no-ff nombre-de-la-rama -m "Merge de nombre-de-la-rama"  # Fusiona los cambios de la rama feature en la rama main y realiza el commit del merge con mensaje
     git branch -d nombre-de-la-rama  # Borra la rama feature después del merge
     ```

8. **Subir Cambios al Repositorio Remoto:**
   - Sube los cambios realizados en la rama principal al repositorio remoto:
     ```bash
     git push origin main
     ```

### Presentaciones y Colaboración

Durante el desarrollo, presentamos avances al profesor. Para ello:
   - Mostramos el historial de ramas eliminadas para demostrar el progreso.
   - Explicamos los cambios en las ramas de características y cómo se integran en la rama principal.
   - Resaltamos la documentación, los comentarios de código y las pruebas realizadas.

## Contacto

   Si tienes preguntas o necesitas ayuda, puedes contactar a [juan.acevedo68061@fpuna.edu.py].

¡Gracias por contribuir al proyecto CMS!
