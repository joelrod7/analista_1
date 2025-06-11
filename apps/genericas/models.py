from django.db import models
import os
from uuid import uuid4

# Create your models here.
def path_and_rename(instance, filename):
    upload_to = 'adjuntos/genericas'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Generica(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Valores_generica(models.Model):
    generica = models.ForeignKey('Generica', on_delete=models.PROTECT, related_name='genericas_relacion')
    codigo = models.CharField(max_length=50, blank=True, null=True)
    archivo = models.FileField(upload_to=path_and_rename, blank=True, null=True)
    nombre = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    valora = models.TextField(blank=True, null=True)
    valorb = models.TextField(blank=True, null=True)
    valorc = models.TextField(blank=True, null=True)
    valord = models.TextField(blank=True, null=True)
    valore = models.TextField(blank=True, null=True)
    valorf = models.TextField(blank=True, null=True)
    valorg = models.TextField(blank=True, null=True)
    valorh = models.TextField(blank=True, null=True)
    valori = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, null=True)
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT,  related_name='elimina_generica', null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)

    def __str__(self):
        return self.nombre


class Permiso(models.Model):
    principal = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='permiso_pricipal')
    secundario = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='permiso_secundario')
    valora = models.CharField(max_length=500, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_add_permiso')
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_del_permiso', null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)

    def __str__(self):
      return self.principal.nombre
