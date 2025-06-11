from ..models import Generica, Valores_generica, Permiso
from ...personas.models import Persona
from rest_framework import serializers

class Valores_genericaSerializerListSimpleConArchivo(serializers.ModelSerializer):
    class Meta:
        model = Valores_generica
        fields = [
            "id",
            "descripcion",
            "nombre",
            "codigo",
            "valora",
            "valorb",
            "valorc",
            "valord",
            "valore",
            "valorf",
            "generica",
            "archivo"
        ]

class GenericaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generica
        fields = "__all__"
# --------------------------------------------------------------------- #
# Serializer para listar genericas ✅
class GenericaSerializer2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=200,)
    descripcion = serializers.CharField(max_length=500 ,allow_blank=True, allow_null=True)
    fecha_registro = serializers.DateTimeField(read_only=True)

    # def to_representation(self, instance):
    #     return {
    #         'id': instance.id,
    #         'nombre': instance.nombre,
    #         'descripcion': instance.descripcion,
    #         'fecha_registro': instance.fecha_registro,
    #     }

    def create(self, validated_data):
        return Generica.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.save()
        return instance

# class Valores_genericaSerializerListSimple(serializers.ModelSerializer):
#     class Meta:
#         model = Valores_generica
#         fields = [
#             "id",
#             "descripcion",
#             "nombre",
#             "codigo",
#             "valora",
#             "valorb",
#             "valorc",
#             "valorf",
#             "generica",
#         ]
# --------------------------------------------------------------------- #
# Serializer para listar valores de generica simple optimizado
class Valores_genericaSerializerListSimple(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    descripcion = serializers.CharField(allow_blank=True, allow_null=True)
    nombre = serializers.CharField()
    codigo = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    valora = serializers.CharField(allow_blank=True, allow_null=True)
    valorb = serializers.CharField(allow_blank=True, allow_null=True)
    valorc = serializers.CharField(allow_blank=True, allow_null=True)
    valore = serializers.CharField(allow_blank=True, allow_null=True)
    valorf = serializers.CharField(allow_blank=True, allow_null=True)
    generica_id = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'descripcion': instance.descripcion,
            'nombre': instance.nombre,
            'codigo': instance.codigo,
            'valora': instance.valora,
            'valorb': instance.valorb,
            'valorc': instance.valorc,
            'valore': instance.valore,
            'valorf': instance.valorf,
            'generica_id': instance.generica_id,
        }


# class Valores_genericaSerializerList(serializers.ModelSerializer):
#     permiso = serializers.IntegerField(default=0)

#     class Meta:
#         model = Valores_generica
#         fields = "__all__"
# --------------------------------------------------------------------- #
# Serializer optimizado para listar valores de generica ✅
class Valores_genericaSerializerList(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    generica = serializers.PrimaryKeyRelatedField(queryset=Generica.objects.all())
    # permiso = serializers.IntegerField(default=0) 
    codigo = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    archivo = serializers.FileField(allow_null=True)
    nombre = serializers.CharField()
    descripcion = serializers.CharField(allow_blank=True, allow_null=True)
    valora = serializers.CharField(allow_blank=True, allow_null=True)
    valorb = serializers.CharField(allow_blank=True, allow_null=True)
    valorc = serializers.CharField(allow_blank=True, allow_null=True)
    valord = serializers.CharField(allow_blank=True, allow_null=True)
    valore = serializers.CharField(allow_blank=True, allow_null=True)
    valorf = serializers.CharField(allow_blank=True, allow_null=True)
    valorg = serializers.CharField(allow_blank=True, allow_null=True)
    valorh = serializers.CharField(allow_blank=True, allow_null=True)
    valori = serializers.CharField(allow_blank=True, allow_null=True)
    fecha_registro = serializers.DateTimeField(read_only=True)
    fecha_elimino = serializers.DateTimeField(allow_null=True, read_only=True)
    usuario_registro = serializers.PrimaryKeyRelatedField(read_only=True)
    usuario_elimino = serializers.PrimaryKeyRelatedField(read_only=True) 
    estado = serializers.ChoiceField(choices=[("1", "Activo"), ("0", "Inactivo")])

    # def to_representation(self, instance):
    #     return {
    #         'id': instance.id,
    #         'generica': instance.generica_id,
    #         'codigo': instance.codigo,
    #         'archivo': instance.archivo,
    #         'nombre': instance.nombre,
    #         'descripcion': instance.descripcion,
    #         'valora': instance.valora,
    #         'valorb': instance.valorb,
    #         'valorc': instance.valorc,
    #         'valord': instance.valord,
    #         'valore': instance.valore,
    #         'valorf': instance.valorf,
    #         'valorg': instance.valorg,
    #         'valorh': instance.valorh,
    #         'valori': instance.valori,
    #         'fecha_registro': instance.fecha_registro,
    #         'fecha_elimino': instance.fecha_elimino,
    #         'usuario_registro': instance.usuario_registro_id,
    #         'usuario_elimino': instance.usuario_elimino_id,
    #         'estado': instance.estado,
    #     }

    # def create(self, validated_data):
    #     return Valores_generica.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.codigo = validated_data.get('codigo', instance.codigo)
        instance.archivo = validated_data.get('archivo', instance.archivo)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.valora = validated_data.get('valora', instance.valora)
        instance.valorb = validated_data.get('valorb', instance.valorb)
        instance.valorc = validated_data.get('valorc', instance.valorc)
        instance.valord = validated_data.get('valord', instance.valord)
        instance.valore = validated_data.get('valore', instance.valore)
        instance.valorf = validated_data.get('valorf', instance.valorf)
        instance.valorg = validated_data.get('valorg', instance.valorg)
        instance.valorh = validated_data.get('valorh', instance.valorh)
        instance.valori = validated_data.get('valori', instance.valori)
        instance.save()
        return instance


# class Valores_genericaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Valores_generica
#         fields = "__all__"
# --------------------------------------------------------------------- #
# Serializer para valores de generica
class Valores_genericaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    generica = serializers.PrimaryKeyRelatedField(queryset=Generica.objects.all())
    codigo = serializers.CharField(max_length=50, allow_blank=True, allow_null=True, required=False)
    archivo = serializers.FileField(allow_null=True, required=False)
    nombre = serializers.CharField()
    descripcion = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valora = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valorb = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valorc = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valord = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valore = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valorf = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valorg = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    valorh = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    usuario_registro = serializers.PrimaryKeyRelatedField(queryset=Persona.objects.all())
    # usuario_elimino = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return Valores_generica.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.codigo = validated_data.get('codigo', instance.codigo)
        instance.archivo = validated_data.get('archivo', instance.archivo)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.valora = validated_data.get('valora', instance.valora)
        instance.valorb = validated_data.get('valorb', instance.valorb)
        instance.valorc = validated_data.get('valorc', instance.valorc)
        instance.valord = validated_data.get('valord', instance.valord)
        instance.valore = validated_data.get('valore', instance.valore)
        instance.valorf = validated_data.get('valorf', instance.valorf)
        instance.valorg = validated_data.get('valorg', instance.valorg)
        instance.save()
        return instance

    # def to_representation(self, instance):
    #     return {
    #         'id': instance.id,
    #         'generica': instance.generica_id,
    #         'codigo': instance.codigo,
    #         'archivo': instance.archivo,
    #         'nombre': instance.nombre,
    #         'descripcion': instance.descripcion,
    #         'valora': instance.valora,
    #         'valorb': instance.valorb,
    #         'valorc': instance.valorc,
    #         'valord': instance.valord,
    #         'valore': instance.valore,
    #         'valorf': instance.valorf,
    #         'valorg': instance.valorg,
    #         'valorh': instance.valorh,
    #         'valori': instance.valori,
    #         'fecha_registro': instance.fecha_registro,
    #         'fecha_elimino': instance.fecha_elimino,
    #         'usuario_registro': instance.usuario_registro_id,
    #         'usuario_elimino': instance.usuario_elimino_id,
    #         'estado': instance.estado,
    #     }


# class Valores_genericaPermisoSerializer(serializers.ModelSerializer):
#     permiso = serializers.IntegerField()

#     class Meta:
#         model = Valores_generica
#         fields = "__all__"
# --------------------------------------------------------------------- #
# Serializer para valores de generica con permiso ✅
class Valores_genericaPermisoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    generica = serializers.PrimaryKeyRelatedField(queryset=Generica.objects.all())
    permiso = serializers.IntegerField()
    codigo = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    archivo = serializers.FileField(allow_null=True)
    nombre = serializers.CharField()
    descripcion = serializers.CharField(allow_blank=True, allow_null=True)
    valora = serializers.CharField(allow_blank=True, allow_null=True)
    valorb = serializers.CharField(allow_blank=True, allow_null=True)
    valorc = serializers.CharField(allow_blank=True, allow_null=True)
    valord = serializers.CharField(allow_blank=True, allow_null=True)
    valore = serializers.CharField(allow_blank=True, allow_null=True)
    valorf = serializers.CharField(allow_blank=True, allow_null=True)
    valorg = serializers.CharField(allow_blank=True, allow_null=True)
    valorh = serializers.CharField(allow_blank=True, allow_null=True)
    valori = serializers.CharField(allow_blank=True, allow_null=True)
    estado = serializers.ChoiceField(choices=[("1", "Activo"), ("0", "Inactivo")])

    def create(self, validated_data):
        return Valores_generica.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.codigo = validated_data.get('codigo', instance.codigo)
        instance.archivo = validated_data.get('archivo', instance.archivo)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.valora = validated_data.get('valora', instance.valora)
        instance.valorb = validated_data.get('valorb', instance.valorb)
        instance.valorc = validated_data.get('valorc', instance.valorc)
        instance.valord = validated_data.get('valord', instance.valord)
        instance.valore = validated_data.get('valore', instance.valore)
        instance.valorf = validated_data.get('valorf', instance.valorf)
        instance.valorg = validated_data.get('valorg', instance.valorg)
        instance.valorh = validated_data.get('valorh', instance.valorh)
        instance.valori = validated_data.get('valori', instance.valori)
        instance.save()
        return instance


class PermisoSerializer(serializers.ModelSerializer):
    secundario = Valores_genericaSerializerListSimpleConArchivo(read_only=True)
    principal = Valores_genericaSerializerListSimple(read_only=True)

    class Meta:
        model = Permiso
        # fields = "__all__"
        fields = ['id', 'principal', 'secundario',
                  'valora', 'usuario_registro']


class PermisoSerializerV2():
    def __init__(self, generica, principal):
        self.valores_secundarios = Valores_generica.objects.filter(generica=generica, estado=1).values('id','codigo','nombre','estado','generica', 'valora', 'valorb', 'valorc', 'archivo')
        self.principal = Valores_generica.objects.filter(id=principal, estado=1).values('id','codigo','nombre','estado','generica', 'valora', 'valorb', 'valorc')

    def to_representation(self, validated_data):
        resp = []

        for per in validated_data:
            data = {
                'id' : per['id'],
                'principal' : self.principal[0],
                'secundario' : {},
                'valora' : per['valora'],
                'usuario_registro' : per['usuario_registro']
            }
        
            for act in self.valores_secundarios:
                if(act['id'] == per['secundario']):
                    if act['archivo']:
                        act['archivo'] = '/media/' + act['archivo']
                    data['secundario'] = act
                    resp.append(data)
                    break

        return resp


class PermisoSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Permiso
        fields = "__all__"
