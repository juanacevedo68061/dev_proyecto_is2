from django.db import models

class Vistas(models.Model):
    aplicacion = models.CharField(max_length=255)
    vista = models.TextField(default='')

    def __str__(self):
        return f"{self.aplicacion} - {self.vista}"

    @classmethod
    def obtener(cls, nombre_aplicacion):
        try:
            registro = cls.objects.get(aplicacion=nombre_aplicacion)
            # Dividir la cadena de vistas por comas y eliminar espacios en blanco
            nombres_vistas = [nombre.strip() for nombre in registro.vista.split(',')]
            return nombres_vistas
        except cls.DoesNotExist:
            return []
    
    class Media(models.Model):
        file = models.FileField(upload_to='media/')