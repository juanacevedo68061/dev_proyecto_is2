# Proyecto CMS

Este repositorio contiene el código fuente y la documentación para el proyecto CMS.

## Flujo de Trabajo y Contribución

Este repositorio sigue un flujo de trabajo colaborativo para desarrollar nuevas características y mantener el entorno de producción actualizado. El proceso implica las ramas de desarrollo (`development`) y producción (`main`).

## Ramas de Entornos

- **`main` (Producción):** Esta rama contiene el código en producción. Se considera estable y se actualiza únicamente con cambios verificados y probados.
- **`development` (Desarrollo):** Esta rama es donde ocurre el desarrollo activo. Nuevas características y cambios se integran aquí antes de ser fusionados en la rama principal.

## Indicaciones Iniciales

Si aún no has clonado este repositorio, sigue estos pasos:

1. **Clonar el Repositorio:**
   - Abre tu terminal o línea de comandos.
   - Navega al directorio donde deseas clonar el repositorio.
   - Ejecuta el siguiente comando para clonar el repositorio en tu máquina local:
     ```bash
     git clone https://github.com/juanacevedo68061/dev_proyecto_is2.git
     ```

2. **Navegar al Directorio del Repositorio:**
   - Una vez que hayas clonado el repositorio, navega al directorio del repositorio en tu terminal:
     ```bash
     cd dev_proyecto_is2
     ```

## Flujo de Trabajo para Desarrollo

1. **Crear una Nueva Rama de Funcionalidad (Feature):**
   - Asegurate de estar en la rama development
     ```bash
     git checkout development  # Esto te posicionará en la rama development para que al crear la rama feature tambien traiga el contenido de development a la rama
     ``` 
   - Antes de trabajar en una nueva funcionalidad, crea una nueva rama feature utilizando el comando:
     ```bash
     git checkout -b nombre-de-la-rama  # Crea la rama feature y se posiciona en ella
     git pull origin development  # Actualizar la rama feature con los últimos cambios de development
     git push origin nombre-de-la-rama  # Sube la rama feature que solo estaba en local a remoto
     ```

2. **Colaboración en la Rama Feature (Opcional):**
   - Si deseas colaborar en una rama feature que esté en el repositorio remoto, primero verifica si la rama feature ya existe en el repositorio remoto:
     ```bash
     git ls-remote --heads origin nombre-de-la-rama
     ```
   - Si la rama feature existe en el repositorio remoto, puedes posicionarte en la rama y colaborar en ella.
     ```bash
     git checkout nombre-de-la-rama
     ```

3. **Realizar Cambios y Commitear:**
   - Realiza los cambios necesarios en la nueva rama.
   - Prueba tus cambios y asegúrate de que todo funcione correctamente. Luego.
     ```bash
     git add .  # Agregar los cambios al área de preparación
     git commit -m "Descripción concisa de los cambios"  # Confirmar los cambios con un mensaje
     ```

4. **Fusión de la rama feature en `development`:**
   - Cambiate a `development` y actualiza con los últimos cambios del repositorio remoto:
     ```bash
     git checkout development
     git pull origin development
     ```
   - Fusiona tu rama de funcionalidad en `development`:
     ```bash
     git merge --no-ff nombre-de-la-rama -m "Merge de nombre-de-la-rama"  # Fusiona los cambios de la rama feature en la rama development y realiza el commit del merge con mensaje
     git push origin development  # Sube los cambios de la fusión a la rama development en el repositorio remoto
     ```

5. **Eliminar la Rama Feature (Local):**
   - Después de haber fusionado con éxito la rama feature en `development`, puedes eliminar la rama feature si ya no la necesitas en tu repositorio local:
     ```bash
     git branch -d nombre-de-la-rama
     ```

6. **Eliminar la Rama Feature (Remota):**
   - Después de que se haya fusionado en `development`, puedes hacerlo con el siguiente comando:
     ```bash
     git push origin --delete nombre-de-la-rama-feature
     ```


## Flujo de Fusión en `main` (Producción)

Cuando estés listo para fusionar tus cambios en la rama principal (`main`), sigue estos pasos:

1. **Fusión de `development` en `main` (Producción):**
   - Asegúrate de estar en la rama `main`. Si no lo estás, puedes cambiar a esta rama ejecutando el siguiente comando:
     ```bash
     git checkout main
     ```
   - Luego, fusiona los cambios de `development` en `main` con la opción `--no-commit` para preparar la fusión:
     ```bash
     git pull origin main
     git merge --no-commit development
     ```

2. **Exclusión de Archivos Específicos:**
   - Para excluir archivos específicos de la fusión, ejecuta el siguiente comando para traer esos archivos desde `development`:
     ```bash
     git checkout development -- .gitattributes
     ```

3. **Confirmar la Fusión y Realizar el Commit:**
   - Reinicia el encabezado del commit y realiza el commit para registrar la fusión con un mensaje descriptivo:
     ```bash
     git reset HEAD
     git commit -m "Fusión de development en main, excluyendo archivos específicos"
     ```

4. **Subir Cambios a `main` (Producción):**
   - Finalmente, sube los cambios realizados en la rama principal al repositorio remoto:
     ```bash
     git push origin main
     ```


### Presentaciones y Colaboración

Durante el desarrollo, presentamos avances al profesor. Para ello:
   - Mostramos el historial de ramas eliminadas para demostrar el progreso.
   - Explicamos los cambios en las ramas de características y cómo se integran en la rama principal.

## Contacto

Si tienes preguntas o necesitas integrarte al proyecto, puedes contactar a [juan.acevedo68061@fpuna.edu.py].

¡Gracias por contribuir al proyecto CMS!

