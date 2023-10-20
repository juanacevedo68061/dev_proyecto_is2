from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from cms.models import Vistas
from django.db import models, connection
class Rol(models.Model):
    """
    Modelo que representa los roles en el sistema.

    Atributos:
        nombre (CharField): El nombre del rol (Autor, Editor, Publicador, Administrador).
        permisos (ManyToManyField): Los permisos asignados a este rol.

    Métodos:
        __str__(): Devuelve una representación en cadena del rol.
        save(): Método personalizado para guardar el rol y asignar permisos correspondientes.

    """
    table_exists = 'cms_vistas' in connection.introspection.table_names()
    nombres_de_vistas=''
    if table_exists:
        nombres_de_vistas = Vistas.obtener('administracion')

    ROLES = [
        ('autor', 'Autor'),
        ('editor', 'Editor'),
        ('publicador', 'Publicador'),
        ('administrador', 'Administrador'),
    ]

    @classmethod
    def agregar_rol(cls, nombre, display):
        cls.ROLES.append((nombre, display))

    PERMISOS = {
        'autor': [
            'crear_publicacion',
            'editar_publicacion_autor',
            # Agrega aquí los permisos correspondientes al rol "autor"
        ],
        'editor': [
            'editar_publicacion_editor',
            'rechazar_editor',
            # Agrega aquí los permisos correspondientes al rol "editor"
        ],
        'publicador': [
            'publicar_no_moderada',
            'rechazar_publicador',
            'mostar_para_publicador',
            # Agrega aquí los permisos correspondientes al rol "publicador"
        ],
        'administrador': nombres_de_vistas,
    }
    #print(PERMISOS['administrador'])

    nombre = models.CharField(max_length=20, choices=ROLES)
    permisos = models.ManyToManyField('auth.Permission', blank=True)

    def __str__(self):
        return self.get_nombre_display()

    def save(self, *args, **kwargs):
        super(Rol, self).save(*args, **kwargs)
        # Después de guardar el rol, asigna los permisos correspondientes si existen en el diccionario
        if self.nombre in self.PERMISOS:
            permisos = self.PERMISOS[self.nombre]
            for permiso_codename in permisos:
                # Obtener el objeto ContentType para el modelo deseado (reemplaza 'TuModelo' por el modelo real)
                content_type = ContentType.objects.get_for_model(Rol)
                
                # Verificar si el permiso ya existe o crearlo si no existe
                permiso, created = Permission.objects.get_or_create(
                    codename=permiso_codename,
                    content_type=content_type,
                    defaults={'name': f'Permiso {permiso_codename}'}
                )

                # Agregar el permiso al rol
                self.permisos.add(permiso)
