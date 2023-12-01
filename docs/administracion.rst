Administracion App
==================

En la aplicacion de administracion se contemplan las siguientes funcionalidades:

- **Creacion, edicion y borrado de categorias**:  Se pueden crear categorias de dos tipos, moderada y no moderada. La manera mas sencilla es la no moderada, en donde la publicacion a ser publicada no necesita de aprobacion de parte de otros usuarios para ser publicada. Cada categoria tiene un campo descripcion y un color asignado al azar. Tambien se pueden destacar una categoria como favorito

- **Gestion de usuarios**: Se pueden crear usuarios, editarlos y borrarlos.

- **Gestion de roles**: Se pueden crear roles, editarlos, asignarlos y borrarlos. Es importante destacar que un rol es un conjunto de permisos

- **Gestion de permisos**: Se pueden crear permisos, editarlos, asignarlos y borrarlos. Es importante destacar que un rol es un conjunto de permisos

A continuacion, se detalla una explicacion mas tecnica de los modelos y las vistas utilizadas en la aplicacion

Models
------

.. automodule:: administracion.models
   :members:
   :show-inheritance:

Vistas
------

.. automodule:: administracion.views
   :members:
   :show-inheritance:


