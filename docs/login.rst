
Login App
=========

La aplicacion `Login` se encarga de gestionar la autenticacion y el registro de usuarios en el sistema CMS. Este documento proporciona una vision detallada del funcionamiento, implementacion y mejores practicas asociadas con esta aplicacion.

En la homepage del CMS, se pueden visualizar contenido para visitantes. Para tener acceso a los contenidos exclusivos para suscriptores, el usuario visitante debe registrarse y autenticarse en el sistema.

Para registrarse, uno debe hacer click en el icono de la esquina superior derecha

.. figure:: /images/loginicon.png
   :align: center

Luego sera redirigido en la pagina de inicio de sesion, a partir de este punto, el registro e inicio de sesion son bastante intuitivos.

.. figure:: /images/login.png
   :align: center
 
.. |nbsp| unicode:: 0xA0
   :trim:

|nbsp|  
 
.. note:: El usuario deberia tener una cuenta de correo electronico valida para poder registrarse en el sistema.
 

.. figure:: /images/registro.png
   :align: center

|nbsp|  

Se recomienda utilizar una contraseña segura, que contenga al menos 8 caracteres, una letra mayuscula, una letra minuscula, un numero y un caracter especial, el sistema probablemente rechazara contrasenas inseguras 

A continuacion, se detalla una explicacion mas tecnica de los modelos y las vistas utilizadas en la aplicacion

Modelos
-------

.. automodule:: login.models
   :members:
   :show-inheritance:

Vistas
------

..   automodule:: login.views
      :members:
      :show-inheritance:

