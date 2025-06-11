from ..models import Credito, Solicitud, Estado, Adjunto
from rest_framework import serializers
from ...personas.api.serializers import PersonaSerializer, PersonaSerializerListSimple
from ...genericas.api.serializers import Valores_genericaSerializer, Valores_genericaSerializerListSimple


class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = "__all__"
        
        
class CreditoSerializerList(serializers.ModelSerializer):
    usuario_registro = PersonaSerializer(read_only=True)
    gestor = PersonaSerializer(read_only=True)
    programa = Valores_genericaSerializer(read_only=True)
    entidad = Valores_genericaSerializer(read_only=True)
    motivo_negado = Valores_genericaSerializer(read_only=True)
    estado_actual = Valores_genericaSerializer(read_only=True)
    permiso = serializers.CharField(default = 0)
    tipo = Valores_genericaSerializerListSimple(read_only=True)
    tipo_pago = Valores_genericaSerializerListSimple(read_only=True)
    subtipo_pago = Valores_genericaSerializerListSimple(read_only=True)
    solicitud_descongela = Valores_genericaSerializerListSimple(read_only=True)
    origen_descongela = Valores_genericaSerializerListSimple(read_only=True)
    modalidad_congela = Valores_genericaSerializerListSimple(read_only=True)
    solicitud_dev = Valores_genericaSerializerListSimple(read_only=True)
    entidades_dev = Valores_genericaSerializerListSimple(read_only=True)
    origen_dinero_dev = Valores_genericaSerializerListSimple(read_only=True)

    class Meta:
        model = Credito
        fields = "__all__"
        

class CreditoSerializerListSimple(serializers.ModelSerializer):
    usuario_registro = PersonaSerializerListSimple(read_only=True)
    entidad = Valores_genericaSerializerListSimple(read_only=True)
    estado_actual = Valores_genericaSerializerListSimple(read_only=True)
    tipo = Valores_genericaSerializerListSimple(read_only=True)
    permiso = serializers.CharField(default=0)
    experiencia = serializers.CharField() 
    aspectos_a_mejorar = serializers.CharField()  
    comentario = serializers.CharField()
    estado_encuesta = serializers.ChoiceField(choices=[("1", "Activo"), ("0", "Inactivo")])  

    class Meta:
        model = Credito
        fields = ['categoria', 'fecha_registro', 'gestor_nombre', 'usuario_registro', 'entidad', 'estado_actual', 'permiso', 'id', 'tipo', 'fecha_limite', 'programa', 'Programa_cre_d', 'lugar_recidencia', 'experiencia', 'aspectos_a_mejorar', 'comentario', 'estado_encuesta']



class EstadoSerializerList(serializers.ModelSerializer):
    tipo_estado = Valores_genericaSerializer(read_only=True)
    usuario_registro = PersonaSerializer(read_only=True)

    class Meta:
        model = Estado
        fields = "__all__"

class AdjuntoSerializerList(serializers.ModelSerializer):
    usuario_registro = PersonaSerializer(read_only=True)

    class Meta:
        model = Adjunto
        fields = "__all__"

class PagosSerializerList(serializers.ModelSerializer):
    solicitud = Valores_genericaSerializer(read_only=True)
    usuario_registro = PersonaSerializer(read_only=True)

    class Meta:
        model = Solicitud
        fields = "__all__"

class EncuestaSerializer(serializers.Serializer):
    experiencia = serializers.CharField()
    aspectos_a_mejorar = serializers.CharField()
    comentario = serializers.CharField()
    estado_encuesta = serializers.ChoiceField(choices=[("1", "Activo"), ("0", "Inactivo")], default="1")

class EncuestaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = ['experiencia', 'aspectos_a_mejorar', 'comentario']