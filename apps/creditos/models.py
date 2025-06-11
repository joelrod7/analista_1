from django.db import models
import os
from uuid import uuid4

# Create your models here.
def path_and_rename(instance, filename):
    upload_to = 'adjuntos/creditos'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Credito(models.Model):
    motivo_negado = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='motivo_negado_credito', null=True)
    gestor = models.ForeignKey('personas.Persona', on_delete=models.PROTECT,  related_name='gestor_credito', null=True)
    gestor_nombre = models.TextField(max_length=254, null=True)
    periodo = models.TextField(max_length=254)
    promedio_nivel = models.TextField(max_length=254, null=True)
    promedio_acumulado = models.TextField(max_length=254, null=True)
    categoria = models.CharField(choices=[("-1", "No Aplica"), ("1", "Nuevo"), ("2", "Renovacion")], default="1", max_length=10)
    programa = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='programa_credito',null=True)
    entidad = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='entidad_credito', null=True)
    solicitud_realizada = models.CharField(choices=[("-1", "No Aplica"), ("1", "si"), ("2", "no")], default="-1", max_length=10)
    requiere_asesoria = models.CharField(choices=[("-1", "No Aplica"), ("1", "si"), ("2", "no")], default="-1", max_length=10)
    creditos_matricula = models.IntegerField(null=True)
    mensaje = models.TextField(blank=True)
    Valor_solicitado = models.TextField(max_length=254, null=True)
    CreditoPara = models.TextField(max_length=254, null=True)
    Valor_de_la_matricula = models.TextField(max_length=254, null=True)
    Programa_cre_d = models.TextField(max_length=254, null=True)
    telefono = models.TextField(max_length=254, null=True)
    direccion = models.TextField(max_length=254, null=True)
    correo = models.TextField(max_length=254, null=True)
    lugar_expe_documento = models.TextField(max_length=254, null=True)
    estado_civil = models.TextField(max_length=254, null=True)
    lugar_recidencia = models.TextField(max_length=254, null=True)
    documento = models.TextField(max_length=254, null=True)
    fecha_expedicion = models.TextField(max_length=254, null=True)
    nombre_completo = models.TextField(max_length=254, null=True)
    fecha_nacimiento = models.TextField(max_length=254, null=True)
    lugar_nacimiento = models.TextField(max_length=254, null=True)
    telefono_estu = models.TextField(max_length=254, null=True)
    direccion_estu = models.TextField(max_length=254, null=True)
    correo_estu = models.TextField(max_length=254, null=True)
    documento_co = models.TextField(max_length=254, null=True)
    fecha_expedicion_co = models.TextField(max_length=254, null=True)
    nombre_completo_co = models.TextField(max_length=254, null=True)
    fecha_nacimiento_co = models.TextField(max_length=254, null=True)
    lugar_nacimiento_co = models.TextField(max_length=254, null=True)
    telefono_co = models.TextField(max_length=254, null=True)
    direccion_co = models.TextField(max_length=254, null=True)
    correo_co = models.TextField(max_length=254, null=True)
    lugar_expe_documento_co = models.TextField(max_length=254, null=True)
    estado_civil_co = models.TextField(max_length=254, null=True)
    direccion_resi_co = models.TextField(max_length=254, null=True)
    lugar_resi_co = models.TextField(max_length=254, null=True)
    ocupacion_co = models.TextField(max_length=254, null=True)
    ciudad_empresa_co = models.TextField(max_length=254, null=True)
    direccion_empresa_co = models.TextField(max_length=254, null=True)
    telefono_empresa_co = models.TextField(max_length=254, null=True)
    empresa_co = models.TextField(max_length=254, null=True)
    ingreso_co = models.TextField(max_length=254, null=True)
    documento_re = models.TextField(max_length=254, null=True)
    fecha_expedicion_re = models.TextField(max_length=254, null=True)
    nombre_completo_re = models.TextField(max_length=254, null=True)
    fecha_nacimiento_re = models.TextField(max_length=254, null=True)
    lugar_nacimiento_re = models.TextField(max_length=254, null=True)
    telefono_re = models.TextField(max_length=254, null=True)
    direccion_re = models.TextField(max_length=254, null=True)
    correo_re = models.TextField(max_length=254, null=True)
    estado_actual = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='estado_actual_credito', null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimina = models.DateTimeField(null=True)
    fecha_limite = models.DateTimeField(null=True)
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT,related_name='usuario_add_credito')
    usuario_elimina = models.ForeignKey('personas.Persona', on_delete=models.PROTECT,  related_name='usuario_can_credito', null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)
    valor_aprobado = models.IntegerField(null=True)
    primer_semestre = models.CharField(choices=[("-1", "No Aplica"), ("si", "Si"), ("no", "No")], default="no", max_length=10)
    tipo = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='tipo_solicitud_credito', null=True)
    tipo_pago = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='tipo_pago_credito', null=True)
    subtipo_pago = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='subtipo_pago_credito', null=True)
    solicitud_descongela = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='solicitud_descongela_credito', null=True)
    # procedimiento_descongela = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='procedimiento_descongela_credito', null=True)
    origen_descongela = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='origen_descongela_credito', null=True)
    asignatura_descongela = models.TextField(blank=True)
    modalidad_congela = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='modalidad_congela_credito', null=True)
    solicitud_dev = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='tipo_solicitud_devolucion', null=True)
    origen_dinero_dev = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='origen_dinero_devolucion', null=True)
    codigo_icetex_dev = models.TextField(blank=True)
    entidades_dev = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='entidades_devolucion', null=True)
    nombre_titular_dev = models.TextField(blank=True)
    numero_documento_dev = models.TextField(blank=True)
    nombre_entidad_dev = models.TextField(blank=True)
    experiencia= models.TextField(max_length=5, null=True)
    aspectos_a_mejorar = models.TextField(default='') 
    comentario = models.TextField(max_length=700, null=True)
    estado_encuesta= models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)
    estado_solicitud_financ = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='estado_solicitud_financiera', null=True)
    valor_solicitud_estado_finan = models.IntegerField(null=True)
    solicitud_estado_finan = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='solitiud_estado_financiero', null=True)
    plazo_dias = models.IntegerField(null=True)
    numero_cuotas = models.IntegerField(null=True)
    def __str__(self):
        return self.estado
    


class Solicitud(models.Model):
    credito = models.ForeignKey(Credito, on_delete=models.PROTECT,related_name='solicitud_credito')
    solicitud = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='solcitud_solicitud_credito')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_add_solicitud_credito')
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_del_solicitud_credito', null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)
    def __str__(self):
      return self.estado


class Estado(models.Model):
    mensaje = models.TextField(null=True, blank=True)
    credito = models.ForeignKey(Credito, on_delete=models.PROTECT,related_name='estados_credito')
    tipo_estado = models.ForeignKey('genericas.Valores_generica', on_delete=models.PROTECT, related_name='tipo_estado_credito')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_add_estado_credito')
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT,  related_name='usuario_del_estado_credito', null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)

    def __str__(self):
      return self.tipo_estado.nombre


class Adjunto(models.Model):
    credito = models.ForeignKey(Credito, on_delete=models.PROTECT,related_name='adjunto_credito')
    adjunto_ant =  models.ForeignKey('Adjunto', on_delete=models.PROTECT,null=True, related_name='adjunto_anterior_credito')
    archivo = models.FileField(upload_to=path_and_rename, null=True)
    nombre_archivo = models.CharField(max_length=200, null=True)
    validacion = models.CharField(choices=[("0", "Enviado"), ("1", "Negado"), ("2", "Aprobado"), ("3", "Remplazado"), ("4", "Pendiente")], default="0", max_length=10)
    fecha_valida = models.DateTimeField(blank=True, null=True)
    usuario_valida = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_val_adjunto_credito', null=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_elimino = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_add_adjunto_credito')
    usuario_elimino = models.ForeignKey('personas.Persona', on_delete=models.PROTECT, related_name='usuario_del_adjunto_credito', null=True)
    estado = models.CharField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1", max_length=10)

    def __str__(self):
      return self.validacion
