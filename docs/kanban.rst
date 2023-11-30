Kanban App
==========

La aplicacion Kanban permite la gestion de publicaciones en un tablero interactivo, donde se pueden crear, editar, eliminar y mover las publicaciones entre las diferentes columnas.

.. figure:: /images/kanban.png
   :align: center

Recordemos que existen distintos estados de contenido, los cuales son:

- **Borrador o rechazado**
- **Edicion o revision y rechazado**
- **A publicar** 
- **Publicado**
- **Inactivo**

Ademas, es importante mencionar que los usuarios pueden tomar uno o mas roles mencionados a continuacion:

- **Autor**
- **Editor**
- **Publicador** 

Teniendo en cuenta eso, un autor puede ver solo sus publicaciones, en cambio, los editores y publicadores pueden ver todas las publicaciones que les toquen en su estado

Modelos
-------

 .. automodule:: kanban.models
    :members:
    :show-inheritance:

Vistas
------

.. automodule:: kanban.views
   :members:
   :show-inheritance:

