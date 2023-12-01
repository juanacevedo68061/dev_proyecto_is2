Testing
=======

Este documento describe cómo ejecutar tests en nuestro proyecto de Django, dónde encontrar los archivos de test y las prácticas recomendadas para escribir tests.

Ejecución de Tests
------------------

Para ejecutar los tests en Django, utiliza el siguiente comando desde la raíz de tu proyecto:

.. code-block:: bash

    python manage.py test

Django buscará automáticamente en la carpeta `tests` de cada aplicación los archivos que comiencen con `test_`, ejecutando cualquier función que comience con `test_` dentro de cualquier archivo `tests.py` o en módulos dentro de un paquete `tests`.

Ubicación de los Tests
----------------------

Por convención, los tests se colocan en un archivo llamado `tests.py` dentro de la aplicación correspondiente. Alternativamente, para un conjunto de pruebas más extenso, puedes crear un paquete `tests` con múltiples archivos como `test_models.py`, `test_views.py`, etc.

.. note:: Asegúrate de que cada archivo de test dentro del paquete `tests` comience con `test_` para que Django los reconozca y ejecute.

Estructura de un Archivo de Test
--------------------------------

Un archivo de test típico en Django podría tener la siguiente estructura:

.. code-block:: python

    from django.test import TestCase
    from .models import MiModelo

    class MiModeloTest(TestCase):
        def setUp(self):
            # Configuración inicial para tests
            pass

        def test_funcionalidad_x(self):
            # Test para funcionalidad x
            pass

        def test_funcionalidad_y(self):
            # Test para funcionalidad y
            pass

Crear Nuevos Tests
------------------

Para crear un nuevo test:

1. Define una clase que herede de `django.test.TestCase`.
2. Agrega métodos que comiencen con `test_` para cada escenario que desees probar.
3. Utiliza los métodos `assert` proporcionados por `TestCase` para validar la lógica de tu aplicación.

Ejemplo de Test para un Modelo:

.. code-block:: python

    class MiModeloTest(TestCase):
        def test_creacion_mi_modelo(self):
            # Aquí va la lógica para probar la creación de una instancia de MiModelo
            obj = MiMod
