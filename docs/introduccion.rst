===================
Introducción al CMS
===================

Este documento proporciona una introducción al sistema de gestión de contenido (CMS) desarrollado por el Equipo 6 en el curso de Ingeniería de Software II, utilizando el framework Django.

Sobre Django
------------

Django es un framework de alto nivel para el desarrollo web en Python, que promueve un desarrollo rápido y un diseño limpio y pragmático. Nuestro proyecto aprovecha las capacidades de Django para ofrecer una solución robusta y escalable para la gestión de contenido.

Arquitectura del Sistema
------------------------

El CMS está compuesto por varias aplicaciones integradas, cada una diseñada para cumplir funciones específicas dentro del sistema:

- **Login**: Maneja la autenticación y el acceso de los usuarios.
- **Publicaciones**: Permite a los usuarios crear, editar y gestionar contenido digital.
- **Roles**: Administra los roles de usuario y los permisos asociados a estos.
- **Kanban**: Ofrece una herramienta visual para el seguimiento de tareas y proyectos.
- **Administración**: Proporciona herramientas de configuración y gestión para administradores del sistema.

Estas aplicaciones trabajan de manera conjunta para crear una experiencia de usuario cohesiva y eficiente.

Se utilizan contenedores Docker para facilitar la implementación y el despliegue del sistema. Los contenedores se ejecutan en un servidor web Apache, que se comunica con una base de datos MySQL para almacenar y recuperar datos.

En el entorno de produccion, se utiliza el motor `nginx` para servir los archivos estáticos y el servidor `gunicorn` para ejecutar la aplicación Django.

Para la utilizacion de servicios en la nube, se opto por Google Cloud Platform para el alojamiento de archivos multimedia y Google Analytics para obtener estadisticas de uso.


Características Clave
---------------------

Algunas de las características clave de nuestro CMS incluyen:

- **Interfaz intuitiva**: Diseñada para ser fácil de usar y navegar.
- **Gestión de contenido flexible**: Herramientas potentes para la creación y administración de contenido.
- **Seguridad reforzada**: Implementación de prácticas de seguridad sólidas para proteger la información de los usuarios.
- **Personalización y escalabilidad**: Capacidad para adaptarse y crecer con las necesidades de los usuarios.

Objetivos del Proyecto
----------------------

El principal objetivo de este proyecto es proporcionar un sistema CMS que sea tanto funcional como eficiente, adecuado para una variedad de necesidades de gestión de contenido. Buscamos ofrecer una herramienta que no solo cumpla con los requisitos técnicos, sino que también sea agradable y accesible para los usuarios finales.

Conclusiones
------------

Este documento y los siguientes capítulos proporcionarán detalles detallados sobre cada una de las aplicaciones y características de nuestro CMS. Esperamos que esta documentación sea una guía valiosa para comprender y utilizar nuestro sistema.

