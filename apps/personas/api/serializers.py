from ..models import Persona, Generica, Carnet, Encuesta_Genero
#from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers
from ...genericas.api.serializers import Valores_genericaSerializer, Valores_genericaSerializerListSimple
from ...genericas.models import Valores_generica

# SERIALIZER PARA PERSONAS


# class PersonaSerializerAdd(serializers.ModelSerializer):
#     # class Meta:
    #     model = Persona
    #     # fields = "__all__"
    #     fields = [
    #         "celular",
    #         "correo",
    #         "correo_personal",
    #         "es_estudiante",
    #         "estado",
    #         "id",
    #         "identificacion",
    #         "last_login",
    #         "perfil",
    #         "primer_apellido",
    #         "primer_nombre",
    #         "segundo_apellido",
    #         "segundo_nombre",
    #         "telefono",
    #         "tipo",
    #         "tipo_identificacion",
    #         "usuario"
    #         ]
    #     extra_kwargs = {'password': {'write_only': True}}
    #     read_only_fields = fields


class PersonaSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Persona
        # fields = "__all__"
        fields = [
            "celular",
            "correo",
            "correo_personal",
            "es_estudiante",
            "estado",
            "id",
            "identificacion",
            "last_login",
            "perfil",
            "primer_apellido",
            "primer_nombre",
            "segundo_apellido",
            "segundo_nombre",
            "telefono",
            "tipo",
            "tipo_identificacion",
            "usuario",
            "activo",
            "indicativo_celular",
            "login_directorio",
            "perfil",
            "lugar_expedicion"
        ]
        extra_kwargs = {'password': {'write_only': True}}
        #read_only_fields = fields


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "id",
            "login_directorio",
            "tipo",
            "tipo_identificacion",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "correo",
            "usuario",
            "fecha_registro",
            "usuario_registro",
            "usuario_elimino",
            "perfil",
            "estado",
            "telefono",
            "indicativo_celular",
            "celular",
            "correo_personal",
            "lugar_expedicion",
            "lugar_residencia",
            "fecha_nacimiento",
            "lugar_nacimiento",
            "direccion",
            "fecha_expedicion"
            # "ubicacion_residencia",
            # "ciudad_expedicion"
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        persona = Persona(
            # tipo=validated_data['tipo'],
            login_directorio=validated_data['login_directorio'],
            tipo_identificacion=validated_data['tipo_identificacion'],
            identificacion=validated_data['identificacion'],
            primer_nombre=validated_data['primer_nombre'],
            segundo_nombre=validated_data['segundo_nombre'],
            primer_apellido=validated_data['primer_apellido'],
            segundo_apellido=validated_data['segundo_apellido'],
            correo=validated_data['correo'],
            usuario=validated_data['usuario'],
            usuario_registro=validated_data['usuario_registro'],
            perfil=validated_data['perfil'],
            # celular=validated_data['celular'],
            # correo_personal=validated_data['correo_personal'],
        )
        persona.set_password(validated_data['identificacion'])
        persona.save()
        return persona


class PersonaSerializerList(serializers.ModelSerializer):
    tipo_identificacion = Valores_genericaSerializer(read_only=True)
    perfil = Valores_genericaSerializer(read_only=True)
    genero = Valores_genericaSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = [
            "id",
            "perfil",
            "tipo_identificacion",
            "libreta_militar",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "correo",
            "usuario",
            "telefono",
            "indicativo_celular",
            "celular",
            "correo_personal",
            "login_directorio",
            "es_estudiante",
            "genero",
            "activo",
            "tipo"
        ]
        extra_kwargs = {'password': {'write_only': True}}


class PersonaSerializerListSimple(serializers.ModelSerializer):
    # genero = Valores_genericaSerializer(read_only=True)
    # categoria_investigacion=Valores_genericaSerializer(read_only=True)
    class Meta:
        model = Persona
        fields = [
            "id",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "indicativo_celular",
            "celular",
            "correo",
            "telefono",
            "correo_personal",
            # "fecha_nacimiento",
            # "genero",
            # direccion_residencia CAMBIADO por direccion
            # "direccion",
            # ubicacion_residencia CAMBIADO por lugar_residencia
            # "lugar_residencia",
            # "nacionalidad",
            # "categoria_investigacion",
            # "lugar_expedicion"
        ]
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = fields


class PersonaSerializerListDetalle(serializers.ModelSerializer):
    tipo_identificacion = serializers.SlugRelatedField(slug_field = 'nombre', read_only=True)
    genero=Valores_genericaSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = [
            'tipo_identificacion',
            'identificacion',
            'fecha_expedicion',
            'primer_nombre',
            'segundo_nombre',
            'primer_apellido',
            'segundo_apellido',
            'fecha_nacimiento',
            # 'sexo',
            'genero',
            'lugar_expedicion',
            'correo'
        ]

    def create(self, validated_data):
        persona = Persona(
            # tipo=validated_data['tipo'],
            login_directorio=validated_data['login_directorio'],
            tipo_identificacion=validated_data['tipo_identificacion'],
            identificacion=validated_data['identificacion'],
            primer_nombre=validated_data['primer_nombre'],
            segundo_nombre=validated_data['segundo_nombre'],
            primer_apellido=validated_data['primer_apellido'],
            segundo_apellido=validated_data['segundo_apellido'],
            correo=validated_data['correo'],
            usuario=validated_data['usuario'],
            usuario_registro=validated_data['usuario_registro'],
            perfil=validated_data['perfil'],
            genero=validated_data['genero'],
            comunidad=validated_data['comunidad'],
            discapacidad=validated_data['discapacidad'],
            direccion=validated_data['direccion'],
            # barrio=validated_data['barrio'],
            barrio=validated_data['lugar_residencia'],
            ciudad=validated_data['ciudad'],
            departamento=validated_data['departamento'],
            telefono=validated_data['telefono'],
            # correo_personal=validated_data['correo_personal'],
        )
        persona.set_password(validated_data['identificacion'])
        persona.save()
        return persona


# SERIALIZER PARA GENERICAS DE PERSONAS
# class GenericaSerializerList(serializers.ModelSerializer):
#     relacion = Valores_genericaSerializer(read_only=True)
#     persona = PersonaSerializer(read_only=True)

#     class Meta:
#         model = Generica
#         fields = "__all__"

class GenericaSerializerList(serializers.ModelSerializer):
    relacion = Valores_genericaSerializerListSimple(read_only=True)
    persona = PersonaSerializerListSimple(read_only=True)

    class Meta:
        model = Generica
        # fields = "__all__"
        fields = [
            "estado",
            "id",
            "tipo",
            "relacion",
            "persona",
            "valora",
            "fecha_registro"
        ]
        read_only_fields = fields


class GenericaSerializerListV2():
    def __init__(self, generica, persona):
        self.valores_secundarios = Valores_generica.objects.filter(generica=generica, estado=1).values('id','descripcion','codigo','nombre', 'generica', 'valora', 'valorb', 'valorc', 'valorf', 'archivo')
        self.persona = persona

    def to_representation(self, validated_data):
        resp = []

        for per in validated_data:
            data = {
                "estado": per['estado'],
                "id": per['id'],
                "tipo": per['tipo'],
                "relacion": {},
                "persona": {
                    "id": self.persona.id,
                    "identificacion": self.persona.identificacion,
                    "primer_nombre": self.persona.primer_nombre,
                    "segundo_nombre": self.persona.segundo_nombre,
                    "primer_apellido": self.persona.primer_apellido,
                    "segundo_apellido": self.persona.segundo_apellido,
                    "indicativo_celular": self.persona.indicativo_celular,
                    "celular": self.persona.celular,
                    "correo": self.persona.correo,
                    "telefono": self.persona.telefono,
                    "correo_personal": self.persona.correo_personal
                }
            }
        
            for act in self.valores_secundarios:
                if(act['id'] == per['relacion']):
                    if act['archivo']:
                        act['archivo'] = '/media/' + act['archivo']
                    data['relacion'] = act
                    resp.append(data)
                    break        


        return resp

class GenericaSerializerSimpleList(serializers.ModelSerializer):
    relacion = Valores_genericaSerializer(read_only=True)

    class Meta:
        model = Generica
        fields = "__all__"


class GenericaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Generica
        fields = "__all__"


class GenericaSerializerListSimple(serializers.ModelSerializer):
    relacion = Valores_genericaSerializerListSimple(read_only=True)
    persona = PersonaSerializerListSimple(read_only=True)

    class Meta:
        model = Generica
        # fields = "__all__"
        fields = [
            "estado",
            "id",
            "tipo",
            "relacion",
            "persona"
        ]
        read_only_fields = fields


# SERIALIZER DE PERSONAS PARA CONSULTORIO
class PersonaSerializerConsultoria(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "id",
            "login_directorio",
            # "tipo",
            "tipo_identificacion",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "correo",
            "usuario",
            "fecha_registro",
            "usuario_registro",
            "usuario_elimino",
            "perfil",
            "estado",
            "telefono",
            "indicativo_celular",
            "celular",
            "genero",
            "comunidad",
            "discapacidad",
            "direccion",
            # "barrio",
            "lugar_residencia",
            "ciudad",
            "departamento",
            "correo_personal"
        ]
        extra_kwargs = {'password': {'write_only': True}}


class PersonaSerializerListDetalleConsultoria(serializers.ModelSerializer):
    ciudad = Valores_genericaSerializer(read_only=True)
    departamento = Valores_genericaSerializer(read_only=True)
    genero = Valores_genericaSerializer(read_only=True)
    comunidad = Valores_genericaSerializer(read_only=True)
    tipo_identificacion = Valores_genericaSerializer(read_only=True)

    class Meta():
        model = Persona
        fields = fields = [
            "id",
            "login_directorio",
            "tipo_identificacion",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "correo",
            "usuario",
            "fecha_registro",
            "usuario_registro",
            "usuario_elimino",
            "perfil",
            "estado",
            "telefono",
            "indicativo_celular",
            "celular",
            "genero",
            "comunidad",
            "discapacidad",
            "direccion",
            # "barrio",
            "lugar_residencia",
            "ciudad",
            "departamento",
            "correo_personal",
            'fecha_expedicion',
            'fecha_nacimiento',
            # 'sexo',
            'lugar_expedicion'
        ]


# SERIALIZER DE PERSONAS PARA INVITADOS
class PersonaSerializerListConPrograma(serializers.ModelSerializer):
    def to_representation(self, validated_data):
        programas = Generica.objects.filter(tipo = 3, estado = 1, relacion__estado = 1, persona = validated_data.id)
        nombre_programa = Valores_genericaSerializer(programas[0].relacion).data if programas else None
        return {
            'id' : validated_data.id,
            'login_directorio' : validated_data.login_directorio,
            'tipo_identificacion' : validated_data.tipo_identificacion.id,
            'identificacion' : validated_data.identificacion,
            'primer_nombre' : validated_data.primer_nombre,
            'segundo_nombre' : validated_data.segundo_nombre,
            'primer_apellido' : validated_data.primer_apellido,
            'segundo_apellido' : validated_data.segundo_apellido,
            'correo' : validated_data.correo,
            'usuario' : validated_data.usuario,
            'telefono' : validated_data.telefono,
            'indicativo_celular' : validated_data.indicativo_celular, # add
            'celular' : validated_data.celular,
            'correo_personal' : validated_data.correo_personal,
            'perfil' : validated_data.perfil.id,
            'programa' : nombre_programa
        }


# SERIALIZER DE PERSONAS PARA EMMA APP
class PersonaSerializerListConRol(serializers.ModelSerializer):
    def to_representation(self, validated_data):
        roles = Generica.objects.filter(estado = 1, tipo = 2, persona = validated_data.id, relacion__estado = 1, relacion__valora='secundario').order_by('relacion__valorb')
        nombre_rol = Valores_genericaSerializer(roles[0].relacion).data if roles else None
        
        # from facecuc.utils import getPhotoMS
        # valor_adicional = getPhotoMS(validated_data.correo)
        # fotoMs = valor_adicional if valor_adicional else None
        fotoMs = None
        
        return {
            'id' : validated_data.id,
            'login_directorio' : validated_data.login_directorio,
            'tipo_identificacion' : Valores_genericaSerializerListSimple(validated_data.tipo_identificacion).data if (validated_data.tipo_identificacion) else validated_data.tipo_identificacion,
            'identificacion' : validated_data.identificacion,
            'primer_nombre' : validated_data.primer_nombre,
            'segundo_nombre' : validated_data.segundo_nombre,
            'primer_apellido' : validated_data.primer_apellido,
            'segundo_apellido' : validated_data.segundo_apellido,
            'correo' : validated_data.correo,
            'usuario' : validated_data.usuario,
            'telefono' : validated_data.telefono,
            'indicativo_celular' : validated_data.indicativo_celular, # add
            'celular' : validated_data.celular,
            'correo_personal' : validated_data.correo_personal,
            'perfil' : Valores_genericaSerializerListSimple(validated_data.perfil).data if (validated_data.perfil) else validated_data.perfil,
            'login_directorio': validated_data.login_directorio,
            'es_estudiante': validated_data.es_estudiante,
            'genero': Valores_genericaSerializerListSimple(validated_data.genero).data if (validated_data.genero) else validated_data.genero,
            'activo': validated_data.activo,
            'rol' : nombre_rol,
            'fotoMS': fotoMs
        }

class PersonaSerializerListAPP(serializers.ModelSerializer):
    tipo_identificacion = Valores_genericaSerializerListSimple(read_only=True)

    class Meta:
        model = Persona
        fields = [
            "id",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "celular",
            "correo",
            "tipo_identificacion",
            "activo",
        ]
        extra_kwargs = {'password': {'write_only': True}}

    # def to_representation(self, instance):
    #     # Obtén la representación original del objeto
    #     representation = super().to_representation(instance)
        
    #     from facecuc.utils import getPhotoMS
    #     valor_adicional = getPhotoMS(representation['correo'])
    #     fotoMs = valor_adicional if valor_adicional else None
    #     # añade su valor a la representación
    #     representation['fotoMS'] = fotoMs
        
    #     return representation


# SERIALIZER DE CARNET PARA EMMA APP
class CarnetSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Carnet
        # fields = "__all__"
        fields = [
            "id",
            "persona",
            "codigo_carnet",
            "llave_decimal",
            "fecha_registro",
            "fecha_actualizo",
            "fecha_elimino",
            "usuario_registro",
            "usuario_actualizo",
            "usuario_elimino",
            "estado"
        ]


# SERIALIZER DE GENERICAS PARA EMMA APP
class PermisoSerializerListAPP(serializers.ModelSerializer):
    relacion = Valores_genericaSerializerListSimple(read_only=True)

    class Meta:
        model = Generica
        fields = ['relacion']  
class PersonaSerializerInter(serializers.ModelSerializer):#
    tipo_identificacion = Valores_genericaSerializerListSimple(read_only=True)
    genero = Valores_genericaSerializerListSimple(read_only=True)
    class Meta:
        model = Persona
        fields = [
            "id",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "celular",
            "correo",
            "tipo_identificacion",
            "activo",
            "fecha_nacimiento",
            "genero",
            "correo_personal",
            "nacionalidad",
            "direccion",
            "lugar_residencia",
            "indicativo_celular",
            "telefono"
            # "ubicacion_residencia"
        ]

class PersonaSerializerSimpleListar(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "id",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido"
        ]

        
class PersonaSerializerListParticipante(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "id",
            "tipo_identificacion",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "nacionalidad",
            "correo",
            "indicativo_celular",
            "celular",
        ]
        
class PersonaSerializerInscripcionPosgrado(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            "id",
            "identificacion",
            "tipo_identificacion",
            "libreta_militar",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "telefono",
            "celular",
            "correo",
            "perfil",
            "estado",
            "estado_civil",
            "lugar_residencia",
            "direccion",
            "departamento",
            "ciudad",
            "discapacidad",
            "lugar_nacimiento",
            "genero",
            "fecha_nacimiento",
            "es_estudiante",
            "login_directorio",
            "activo",
            "tipo",
            "usuario",
            "fecha_registro",
            "usuario_registro",
            "usuario_elimino",
        ]
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            persona = Persona(
                celular=validated_data['celular'],
                ciudad=validated_data['ciudad'],
                correo=validated_data['correo'],
                correo_personal=validated_data['correo_personal'],
                departamento=validated_data['departamento'],
                discapacidad=validated_data['discapacidad'],
                direccion=validated_data['direccion'],
                estado_civil=validated_data['estado_civil'],
                fecha_nacimiento=validated_data['fecha_nacimiento'],
                identificacion=validated_data['identificacion'],
                genero=validated_data['genero'],
                libreta_militar=validated_data['libreta_militar'],
                login_directorio=validated_data['login_directorio'],
                lugar_nacimiento=validated_data['lugar_nacimiento'],
                lugar_residencia=validated_data['lugar_residencia'],
                perfil=validated_data['perfil'],
                primer_apellido=validated_data['primer_apellido'],
                primer_nombre=validated_data['primer_nombre'],
                segundo_apellido=validated_data['segundo_apellido'],
                segundo_nombre=validated_data['segundo_nombre'],
                telefono=validated_data['telefono'],
                tipo_identificacion=validated_data['tipo_identificacion'],
                usuario_registro=validated_data['usuario_registro'],
                usuario=validated_data['usuario'],
            )
            persona.set_password(validated_data['identificacion'])
            persona.save()
            return persona


class PersonaSerializerInscripcionPosgradosDetalle(serializers.ModelSerializer):
    tipo_identificacion = Valores_genericaSerializer(read_only=True)
    genero = Valores_genericaSerializer(read_only=True)
    departamento = Valores_genericaSerializer(read_only=True)
    ciudad = Valores_genericaSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = [
            "id",
            "identificacion",
            "tipo_identificacion",
            "libreta_militar",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "telefono",
            "celular",
            "correo",
            "estado_civil",
            "lugar_residencia",
            "direccion",
            "departamento",
            "ciudad",
            "discapacidad",
            "lugar_nacimiento",
            "genero",
            "fecha_nacimiento",
            "usuario",
            "fecha_registro",
            "usuario_registro",
            "usuario_elimino",
        ]
        
class EncuestaGeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta_Genero
        fields = [
            "id",
            "usuario_registro",
            "estado_encuesta",
        ]

class PersonaSerializerInscripcionPosgrados(serializers.ModelSerializer):
    from apps.inscripciones_posgrado.api.serializers import InscripcionPosgradoSerializerList
    estudiante_inscripcion_posgrados = InscripcionPosgradoSerializerList(many=True, read_only=True)
    tipo_identificacion = Valores_genericaSerializer(read_only=True)
    genero = Valores_genericaSerializer(read_only=True)
    departamento = Valores_genericaSerializer(read_only=True)
    ciudad = Valores_genericaSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = [
            "id",
            "identificacion",
            "tipo_identificacion",
            "libreta_militar",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "telefono",
            "celular",
            "correo",
            "estado_civil",
            "lugar_residencia",
            "direccion",
            "departamento",
            "ciudad",
            "discapacidad",
            "lugar_nacimiento",
            "genero",
            "fecha_nacimiento",
            "usuario",
            "fecha_registro",
            "usuario_registro",
            "usuario_elimino",
            'estudiante_inscripcion_posgrados',
        ]
        
class PersonaSerializerInscripcion(serializers.ModelSerializer):
    from apps.inscripciones.api.serializers import InscripcionSerializerlistPersona
    estudiante_inscripcion = InscripcionSerializerlistPersona(many=True, read_only=True)
    tipo_identificacion = Valores_genericaSerializer(read_only=True)
    perfil = Valores_genericaSerializer(read_only=True)
    genero = Valores_genericaSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = [
            "id",
            "perfil",
            "tipo_identificacion",
            "libreta_militar",
            "identificacion",
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "correo",
            "usuario",
            "telefono",
            "indicativo_celular",
            "celular",
            "correo_personal",
            "login_directorio",
            "es_estudiante",
            "genero",
            "activo",
            "tipo",
            "estudiante_inscripcion",
        ]
        extra_kwargs = {'password': {'write_only': True}}