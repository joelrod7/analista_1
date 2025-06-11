import os
from uuid import uuid4
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, usuario, correo, password=None):
        if usuario is None:
            raise TypeError('Users must have a usuario.')

        if correo is None:
            raise TypeError('Users must have an correo address.')

        user = self.model(usuario=usuario, correo=self.normalize_email(correo))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, usuario, correo, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(usuario, correo, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

# Create your models here.

def path_and_rename(instance, filename):
    upload_to = 'adjuntos/personas'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class Persona(AbstractBaseUser, PermissionsMixin):
    # CAMPOS BASICOS
    login_directorio = models.CharField(choices=[("1", "Si"), ("0", "No")], default="1", max_length=10)
    tipo_identificacion = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='tipo_identificacion', null=True)
    identificacion = models.CharField(max_length=20, unique=True)
    primer_nombre = models.CharField(max_length=200)
    segundo_nombre = models.CharField(max_length=200, blank=True, null=True)
    primer_apellido = models.CharField(max_length=200)
    segundo_apellido = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField(max_length=100, unique=True)
    correo_personal = models.EmailField(max_length=100, null=True, blank=True)
    usuario = models.CharField(max_length=100, unique=True)
    telefono = models.BigIntegerField(null=True)
    indicativo_celular = models.BigIntegerField(null=True, default="57")
    celular = models.BigIntegerField(null=True)
    tipo = models.CharField(choices=[("1", "Interna"), ("2", "Externa")], default="1", max_length=10)
    perfil = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='usuario_perfil', null=True)
    pass_interna = models.CharField(max_length=200, blank=True, null=True)
    activo = models.CharField(choices=[("1", "Si"), ("0", "No")], default="0", max_length=10)
    verificado = models.CharField(choices=[("1", "Si"), ("0", "No")], default="0", max_length=10)
    codigo_verificacion = models.CharField(max_length=20, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('Persona', on_delete=models.PROTECT, related_name='usuario_add_persona', null=True)
    usuario_elimino = models.ForeignKey('Persona', on_delete=models.PROTECT, null=True, related_name='usuario_del_persona')
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    genero = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='genero_persona', blank=True, null=True)
    es_estudiante = models.CharField(choices=[("1", "Si"), ("0", "No")], default="0", max_length=10)

    # CAMPOS PRACTICAS CLINICAS
    fecha_expedicion = models.DateField(null=True)
    lugar_expedicion = models.CharField(
        max_length=100, null=True)  # TB MATRICULAS
    fecha_nacimiento = models.DateField(null=True)  # TB INTERNACIONALIZACION

    # CAMPOS CREDITOS
    estado_civil = models.CharField(max_length=200, blank=True, null=True)
    # TB CONSULTORIO, INTERNACIONALIZACION
    lugar_residencia = models.CharField(max_length=200, blank=True, null=True)
    # TB CONSULTORIO, INTERNACIONALIZACION
    direccion = models.CharField(max_length=500, null=True)

    # CAMPOS CONSULTORIO
    departamento = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='departamento_consultoria', null=True)
    ciudad = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='ciudad_consultoria', null=True)
    comunidad = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='comunidades_consultoria', null=True)
    discapacidad = models.CharField(choices=[("1", "Si"), ("0", "No")], default="0", max_length=10)

    # CAMPOS INTERNACIONALIZACION
    nacionalidad = models.CharField(max_length=200, blank=True, null=True)
    dependencia = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='dependencia_persona', blank=True, null=True)

    # CAMPOS SEMILLEROS
    categoria_investigacion = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='categoria_investigacion_per', null=True)

    # CAMPOS MATRICULAS
    lugar_nacimiento = models.CharField(max_length=200, blank=True, null=True)

    # CAMPOS INSCRIPCIONES POSGRADO
    libreta_militar = models.CharField(max_length=20, blank=True, null=True)

    encuesta_spa = models.CharField(choices=[("1", "Si"), ("0", "No")], default="0", max_length=10)
    # ELIMINADAS
    # reporte_vacuna = models.CharField(choices=[("1", "Si"), ("0", "No")], default="0", max_length=10)
    # sexo = models.CharField(max_length=200, blank=True, null=True) # CAMBIADO EN PRACTICAS por genero
    # ciudad_expedicion = models.CharField(max_length=20, blank=True, null=True) # CAMBIADO EN MATRICCULAS A lugar_expedicion
    # barrio = models.CharField(max_length=500, null=True) # CAMBIADO EN CONSULTORIO A lugar_residencia
    # direccion_residencia = models.CharField(max_length = 200, blank = True, null = True) # CAMBIADO por direccion
    # ubicacion_residencia = models.CharField(max_length = 200, blank = True, null = True) # CAMBIAR por lugar_residencia

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['usuario']
    objects = UserManager()

    def __str__(self):
        return self.correo

    def get_full_name(self):
        return self.correo

    def get_short_name(self):
        return self.correo
        # this methods are require to login super user from admin panel

    def has_perm(self, perm, obj=None):
        return self.is_staff

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_staff

    def get_all_name(self):
        return f"{self.primer_nombre} {self.primer_apellido} {self.segundo_apellido}"


class Generica(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.PROTECT, null=True)
    relacion = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='valor_relacion')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_add_relacion')
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT,  related_name='usuario_del_relacion', null=True)
    tipo = models.CharField(choices=[
        ("1", "Perfiles"),
        ("2", "Rol"),
        ("3", "Programas en Curso"),
        ("4", "Permiso practica - programas"),
        ("5", "Permiso practica - estado"),
        ("6", "Permiso Credito - entidad"),
        ("7", "Permiso Credito - estado"),
        ("8", "Permiso Matricula - estados"),
        ("9", "Permiso Matricula - tipo"),
        ("10", "Permiso Practica - Modalidad"),
        ("11", "Permiso Inscripciones - programa"),
        ("12", "Permiso Inscripciones - estado"),
        ("13", "Permiso Matricula - programa"),
        ("14", "Permisos Becas - Estados"),
        ("15", "Permisos Becas -Tipos"),
        ("16", "Permisos Credito - Tipos"),
        ("17", "Permisos Reportes - Tipos"),
        ("18", "Permisos Rea - Tipos"),
        ("19", "Permisos Validaciones - Programas"),
        ("20", "Permisos Validaciones - Estados"),
        ("21", "Permisos Consultorias - Tipos"),
        ("22", "Permisos Consultorias - Estados"),
        ("23", "Permisos Tutorias - Tipo"),
        ("24", "Permisos Tutorias - Estados"),
        ("25", "Permisos Autodiagnostico - Estados"),
        ("26", "Permisos Retos - Equipos"),
        ("27", "Permisos Retos - Estados"),
        ("28", "Permisos Inscripciones - Tipos"),
        ("29", "Permisos internacionalizacion - tipos"),
        ("30", "Permisos internacionalizacion - programas"),
        ("31", "Permisos internacionalizacion - estados"),
        ("32", "Permisos Investigacion - Tipos"),
        ("33", "Permisos Investigacion - Estados"),
        ("34", "Permisos Grados - Programas"),
        ("35", "Permisos Grados - Estados"),
        ("36", "Permisos Financieros - Programas"),
        ("37", "Permisos Invitados Virtual - Estados"),
        ("38", "Permisos Grados - Tipo"), 
        ("39", "Permisos Retos - Programas"), 
        ("40", "Permisos Retos - Estados"), 
        ("41", "Permisos Salas - Salas"), 
        ("42", "Permiso Inscripciones_posgrado - programas"), 
        ("43", "Permiso Inscripciones_posgrado - estado"),
        ("44", "Permisos Cursos- Tipos"), 
        ("45", "Permisos Cursos - Estados"),
        ("46", "Permisos Atencion - Tipo"),
        ("47", "Permisos Atencion - Estado estudiante"),
        ("48", "Permisos Atencion - Incidente"),
        ("49", "Permisos Atencion - Estados"),
        ("50", "Permisos Centro - Tipos"),
        ("51", "Permisos Centro - Estados"),
        ("52", "Permisos internacionalizacion - Departamentos"),
        ("53", "Permisos Atencion - Programa"),
    ], max_length=10)
    valora = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)
    interno = models.ForeignKey('Generica', on_delete=models.PROTECT, related_name='interno_relacion', null=True)

    def __str__(self):
        return self.tipo


class Carnet(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.PROTECT)
    codigo_carnet = models.TextField()
    llave_decimal = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizo = models.DateTimeField(blank=True, null=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('Persona', on_delete=models.PROTECT, related_name='usuario_add_carnet')
    usuario_actualizo = models.ForeignKey('Persona', on_delete=models.PROTECT,  related_name='usuario_act_carnet', null=True)
    usuario_elimino = models.ForeignKey('Persona', on_delete=models.PROTECT,  related_name='usuario_del_carnet', null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)

    def __str__(self):
        return self.estado

class Encuesta_Genero(models.Model):
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name= 'usuario_add_encuesta_genero', null=True)
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name= 'usuario_del_encuesta_genero', null=True)
    estado_encuesta = models.CharField(choices= [("1", "Finalizada"), ("0", "No Finalizada")], default="1", max_length=1)
    estado = models.CharField(choices= [("1", "Activo"), ("0", "Inactivo")], default="1", max_length=1)
    periodo = models.CharField(max_length=5)
    fecha_registro = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.estado

class Encuesta_Genero_Pregunta(models.Model):
    encuesta_genero = models.ForeignKey(Encuesta_Genero, on_delete=models.PROTECT, related_name= 'encuesta_genero_pregunta')
    pregunta = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name= 'pregunta_encuesta_genero')
    respuesta = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name= 'respuesta_encuesta_genero', null=True)
    valor = models.TextField(max_length=254, blank=True, null=True)
    estado = models.CharField(choices= [("1", "Activo"), ("0", "Inactivo")], default="1", max_length=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.estado

class Aceptacion_Politica(models.Model):
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name= 'usuario_add_politica', null=True)
    periodo = models.CharField(max_length=5)
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name= 'usuario_del_politica', null=True)
    estado = models.CharField(choices= [("1", "Activo"), ("0", "Inactivo")], default="1", max_length=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.estado