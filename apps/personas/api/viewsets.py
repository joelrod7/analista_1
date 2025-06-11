from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
# NUEVO PRUEBA
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.settings import api_settings
# from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
# from rest_framework_jwt.settings import api_settings
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Persona, Generica, Carnet, Encuesta_Genero, Encuesta_Genero_Pregunta, Aceptacion_Politica
from ...genericas.models import Valores_generica, Permiso
from .serializers import (
    PersonaSerializer,
    PersonaSerializerList,
    PersonaSerializerListSimple,
    GenericaSerializerList,
    GenericaSerializer,
    GenericaSerializerSimpleList,
    PersonaSerializerAdd,
    Valores_genericaSerializer,
    PersonaSerializerListAPP,
    GenericaSerializerListSimple,
    CarnetSerializerList,
    PermisoSerializerListAPP,
    PersonaSerializerListConRol,
    GenericaSerializerListV2
)
from ...genericas.api.serializers import (
    PermisoSerializer,
    Valores_genericaPermisoSerializer,
    PermisoSerializerV2
)
from django.template import loader
from django.utils import timezone
from random import choice, randint
from facecuc.microsoft import EnviarCorreo, ValidarCredencialesLdap, getPhotoMS
from facecuc.sinu import obtenerInformacionSICUC
from facecuc.identidades import consultaIdentidades,consultaIdentidadesBarrcode
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import transaction, connection
from django.utils import timezone
import re
import requests

from django.conf import settings
import requests
import hashlib
import base64
import secrets
import datetime
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['token'] = data.pop('access')  
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.correo
        token['correo'] = user.correo
        return token

@api_view(["GET"])
def current_user(request):
    persona = Persona.objects.get(id=request.user.id)
    # persona.last_login = datetime.datetime.now()
    persona.last_login = timezone.now()
    persona.save()
    serializer = PersonaSerializerListConRol(request.user)
    return Response(serializer.data)



# class ValidarCredenciales(TokenObtainPairView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         correo = request.data["correo"]
#         password = request.data["password"]
#         req_codigo = request.data["codigo"]
#         txt_codigo = request.data["txtcodigo"]
#         no_valido = Response(
#             {"titulo": "Usuario o clave incorrectos."}, status=status.HTTP_302_FOUND
#         )
#         try:
#             persona = Persona.objects.get(estado=1, correo=correo)
#         except (KeyError, Persona.DoesNotExist):
#             return no_valido
#         else:
#             if int(persona.login_directorio) == 1:
#                 request.data[
#                     "password"
#                 ] = (
#                     persona.pass_interna
#                 )  # los usuarios cuyo ingreso es por el directorio activo, deben tener como password el valor asignado en pass_interna para poder validar las credenciales en el software.
#                 valido = ValidarCredencialesLdap(correo, password)
#                 if not (valido):
#                     return no_valido
#             response = super().post(request, *args, **kwargs)
#             if response.status_code == 200:
#                 if int(persona.verificado) == 0 and int(persona.login_directorio) == 0:
#                     if not (req_codigo):
#                         codigo = GenerarCodigo(6)
#                         persona.codigo_verificacion = codigo
#                         persona.save()
#                         template = loader.get_template("correos/plantilla.html")
#                         context = {
#                             "mensajes" :  [
#                                 {
#                                     "mensaje" : "¡Genial!",
#                                     "clase": "titulo",
#                                 },
#                                 {
#                                     "mensaje" : "Aquí tienes el código de verificación de tu cuenta:",
#                                     "clase": "normal",
#                                 },
#                                 {
#                                     "mensaje" : codigo,
#                                     "clase": "importante",
#                                 },
#                             ]
#                         }
#                         html_content = template.render(context)
#                         EnviarCorreo([persona.correo],html_content,"código de verificación",)
#                         return Response(
#                             {
#                                 "titulo": "La cuenta no ha sido activada, se envió un código de verificación al correo "
#                                 + persona.correo,
#                                 "codigo": True,
#                             },
#                             status=status.HTTP_302_FOUND,
#                         )
#                     else:
#                         if not (txt_codigo):
#                             return Response(
#                                 {
#                                     "titulo": "El campo código es obligatorio.",
#                                     "codigo": True,
#                                 },
#                                 status=status.HTTP_302_FOUND,
#                             )
#                         else:
#                             if persona.codigo_verificacion != txt_codigo:
#                                 return Response(
#                                     {
#                                         "titulo": "El código de verificación es incorrecto",
#                                         "codigo": True,
#                                     },
#                                     status=status.HTTP_302_FOUND,
#                                 )
#                             else:
#                                 persona.verificado = 1
#                                 persona.save()
#                 return response
#             else:
#                 return no_valido


class PersonaListar(generics.ListAPIView):
    queryset = Persona.objects.filter(estado=1)
    serializer_class = PersonaSerializerList


class PersonaBuscar(viewsets.ViewSet):
    def list(self, request):
        queryset = request.data["dato"]
        resp = []
        try:
            es_estudiante = request.data["es_estudiante"]
            tipo = request.data["tipo"]
        except:
            es_estudiante = None
            tipo = None
        if queryset:
            if len(queryset) >= 4:
                if es_estudiante:
                    resp = Persona.objects.annotate(
                            nombre_completo=Concat('primer_nombre', Value(' '), 'primer_apellido', Value(' '), 'segundo_apellido')
                        ).filter(
                            Q(identificacion__icontains=queryset)
                            | Q(correo__icontains=queryset)
                            | Q(usuario__icontains=queryset)
                            | Q(nombre_completo__icontains=queryset),
                            es_estudiante=es_estudiante,
                            tipo=tipo,
                            # estado=1,
                        )[:30]
                else:
                    resp = Persona.objects.annotate(
                            nombre_completo=Concat('primer_nombre', Value(' '), 'primer_apellido', Value(' '), 'segundo_apellido')
                        ).filter(
                            Q(identificacion__icontains=queryset)
                            | Q(correo__icontains=queryset)
                            | Q(usuario__icontains=queryset)
                            | Q(nombre_completo__icontains=queryset),
                            # estado=1,
                        )[:30]
        serializer = PersonaSerializerList(resp, many=True)
        return Response(serializer.data)
        


class PersonaCrear(generics.CreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def create(self, request, *args, **kwargs):
        (usuario, token) = JWTAuthentication().authenticate(request)
        roles = request.data["roles"]
        perfiles = request.data["perfiles"]
        programas = request.data["programas"]
        tipo = request.data["tipo"]
        pass_interna = request.data["identificacion"]
        request.data["password"] = request.data["identificacion"]
        request.data["usuario_registro"] = usuario.id
        request.data["perfil"] = perfiles[0]
        # GUARDANDO PERSONA
        #request.data["perfil"] = Valores_generica.objects.get(codigo="Per_Nor").id
        super(PersonaCrear, self).create(request, args, kwargs)
        persona = Persona.objects.filter(usuario_registro=usuario.id).last()
        usuario_registro = Persona.objects.get(pk=usuario.id)
        
        # GUARDANDO REGISTRO EN TABLA DE CARNET
        # llave_decimal = randint(1,999999999)
        # llave_hex = (hex(llave_decimal).lstrip("0x")).rjust(8, '0')
        # identificacion = int(persona.identificacion)
        # identificacion = (hex(identificacion).lstrip("0x")).rjust(8, '0')
        # codigo_carnet = (identificacion + llave_hex).upper()

        # carnet = Carnet(persona=persona, usuario_registro=usuario_registro, codigo_carnet=codigo_carnet, llave_decimal=llave_decimal)
        # carnet.save()

        permisos_guardar = []
        es_estudiante = 0
        encontrado = False
        # CONFIGURANDO PERMISOS ROLES
        for r in roles:
            relacion = Valores_generica.objects.get(pk=r)
            if(not(encontrado)):
                if(relacion.codigo == 'rol_est'):
                    es_estudiante = 1
                    encontrado = True
            data = Generica(
                persona=persona,
                relacion=relacion,
                usuario_registro=usuario_registro,
                tipo=2,
            )
            permisos_guardar.append(data)

        # CONFIGURANDO PERMISOS PERFILES
        for p in perfiles:
            relacion = Valores_generica.objects.get(pk=p)
            data = Generica(
                persona=persona,
                relacion=relacion,
                usuario_registro=usuario_registro,
                tipo=1,
            )
            permisos_guardar.append(data)

        # CONFIGURANDO PERMISOS PROGRAMAS
        for pr in programas:
            relacion = Valores_generica.objects.get(pk=pr)
            data = Generica(
                persona=persona,
                relacion=relacion,
                usuario_registro=usuario_registro,
                tipo=3,
            )
            permisos_guardar.append(data)
        
        # ACTUALIZANDO ALGUNOS DATOS DE LA PERSONA CREADA
        persona.tipo = tipo
        persona.pass_interna = pass_interna
        # persona.activo = 1
        persona.es_estudiante = es_estudiante
        persona.save()
        # GUARDANDO TODOS LOS PERMISOS ASOCIADOS
        Generica.objects.bulk_create(permisos_guardar)

        return Response({"titulo": "Persona Guardada"})


class PersonaEliminar(generics.UpdateAPIView):
    def update(self, request, pk):
        try:
            persona = Persona.objects.get(pk=pk)
        except (KeyError, Persona.DoesNotExist):
            return Response(
                {"titulo": "La persona no existe"}, status=status.HTTP_302_FOUND
            )
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            persona.estado = 0
            persona.is_active = 0
            persona.fecha_elimino = datetime.datetime.now()
            persona.usuario_elimino = Persona.objects.get(pk=usuario.id)
            persona.save()
            return Response({"titulo": "Persona Eliminada"})


class PersonaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializerAdd

    def retrieve(self, request, *args, **kwargs):
        request['estado'] = 1
        super(PersonaDetalle, self).retrieve(request, args, kwargs)
        response = {"titulo": "Proceso Exitoso", "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        (usuario, token) = JWTAuthentication().authenticate(request)
        persona = Persona.objects.get(id=kwargs['pk'])
        super(PersonaDetalle, self).patch(request, args, kwargs)

        if request.data['carnet']:
            if request.data['activo'] == 1:
                # Validando si ya un registro en carnet
                try:
                    carnet = Carnet.objects.get(persona=persona.id, estado=1)
                except (KeyError, Carnet.DoesNotExist):
                    pass
                    usuario_registro = Persona.objects.get(pk=usuario.id)

                    # GUARDANDO REGISTRO EN TABLA DE CARNET
                    llave_decimal = randint(1,999999999)
                    llave_hex = (hex(llave_decimal).lstrip("0x")).rjust(8, '0')
                    identificacion = int(persona.identificacion)
                    identificacion = (hex(identificacion).lstrip("0x")).rjust(8, '0')
                    codigo_carnet = (identificacion + llave_hex).upper()

                    carnet = Carnet(persona=persona, usuario_registro=usuario_registro, codigo_carnet=codigo_carnet, llave_decimal=llave_decimal)
                    carnet.save()

        return Response({"titulo": "Persona Modificada"})

class PersonaCambiarPass(generics.UpdateAPIView):
    def update(self, request, pk):
        try:
            persona = Persona.objects.get(pk=pk)
        except (KeyError, Persona.DoesNotExist):
            return Response(
                {"titulo": "La persona no existe"}, status=status.HTTP_302_FOUND
            )
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            if(request.data["pass"]):
                persona.is_staff = 1
                persona.is_active = 1
                persona.is_superuser = 0
                persona.pass_interna = request.data["pass"] if persona.login_directorio == '1' else None
                persona.set_password(request.data["pass"])
                persona.save()
                return Response({"titulo": "¡Contraseña modificada.!"})
            else:
                return Response({"titulo": "No existe una contraseña"}, status=status.HTTP_302_FOUND)


# view Generica


class GenericaListar(viewsets.ViewSet):
    def list(self, request, pk, tipo):
        queryset = Generica.objects.filter(persona_id=pk, tipo=tipo,relacion__estado=1, estado=1).order_by('relacion__nombre')
        serializer = GenericaSerializerList(queryset, many=True)
        return Response(serializer.data)

class GenericaListarPersonaSesion(viewsets.ViewSet):
    def list(self, request, tipo):
        (usuario, token) = JWTAuthentication().authenticate(request)
        queryset = Generica.objects.filter(persona_id=usuario.id, tipo=tipo, relacion__estado=1 , estado=1)
        serializer = GenericaSerializerList(queryset, many=True)
        return Response(serializer.data)


class PermisosPerfil(viewsets.ViewSet):
    def list(self, request, pk):
        try:
            persona = Persona.objects.get(pk=pk)
        except (KeyError, Persona.DoesNotExist):
            return Response( {"titulo": "La persona no existe"}, status=status.HTTP_302_FOUND)
        else:
            data = Permiso.objects.filter(principal=persona.perfil, secundario__generica=10, principal__estado = 1, secundario__estado = 1, estado=1).exclude(secundario__valorb='deshabilitado').values('id','principal','secundario','estado', 'valora', 'usuario_registro')
            permiso_serializer = PermisoSerializerV2(10, persona.perfil.id)
            serializer = permiso_serializer.to_representation(data)
            return Response(serializer)

class PermisosPerfilSubmodulos(viewsets.ViewSet):
    def list(self, request, pk, codigo):
        try:
            persona = Persona.objects.get(pk=pk)
        except (KeyError, Persona.DoesNotExist):
            return Response( {"titulo": "La persona no existe"}, status=status.HTTP_302_FOUND)
        else:
            try:
                # Se obtiene el valor generica de la actividad principal
                actividad = Valores_generica.objects.get(codigo=codigo)
            except (KeyError, Valores_generica.DoesNotExist):
                return Response( {"titulo": "No existe la actividad"}, status=status.HTTP_302_FOUND)
            else:
                # Se obtienen los permisos del perfil que están relacionados con los submodulos o actividades, las cuales deben tener en el valora 'submodulo' para poder identificarlos.
                
                data = Permiso.objects.filter(principal=persona.perfil, principal__estado = 1, secundario__estado = 1, estado=1, secundario__valora = 'submodulo').values('id','principal','secundario','estado', 'valora', 'usuario_registro')
                permiso_serializer = PermisoSerializerV2(10, persona.perfil.id)
                serializer = permiso_serializer.to_representation(data)
                # resp = serializer.data
                return Response(serializer)

class GenericaCrear(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            persona = Persona.objects.get(pk=kwargs["pk"])
        except (KeyError, Persona.DoesNotExist):
            return Response(
                {"titulo": "La persona no existe"}, status=status.HTTP_302_FOUND
            )
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            relaciones = request.data["relaciones"]
            tipo = request.data["tipo"]
            default = None
            relaciones_act = persona.generica_set.filter(estado=1, tipo=tipo)
            usuario_registro = Persona.objects.get(pk=usuario.id)
            relaciones_guardar = []
            sw = False
            add = False

            for r in relaciones:
                if r not in [ract.relacion.id for ract in relaciones_act]:
                    add = True
                    relacion = Valores_generica.objects.get(pk=r)
                    data = Generica(
                        persona=persona,
                        relacion=relacion,
                        usuario_registro=usuario_registro,
                        tipo=tipo,
                    )
                    default = relacion
                    relaciones_guardar.append(data)
                else:
                    sw = True

            if(default and int(tipo) == 1):
                persona.perfil = default
                persona.save()

            if add:
                Generica.objects.bulk_create(relaciones_guardar)
                nota = (
                    "(Se excluyeron algunas relaciones que ya estaban asignados)."
                    if sw
                    else "."
                )
                return Response(
                    {"titulo": "Datos Agregados" + nota}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "titulo": "Las datos seleccionados ya fueron asignados anteriormente."
                    },
                    status=status.HTTP_302_FOUND,
                )


class GenericaEliminar(generics.UpdateAPIView):
    def update(self, request, pk):
        try:
            generica = Generica.objects.get(pk=pk)
        except (KeyError, Generica.DoesNotExist):
            return Response(
                {"titulo": "El dato no existe"}, status=status.HTTP_302_FOUND
            )
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            generica.estado = 0
            generica.fecha_elimino = datetime.datetime.now()
            generica.usuario_elimino = Persona.objects.get(pk=usuario.id)
            generica.save()
            return Response({"titulo": "Dato Eliminado"})

class GenericaDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Generica.objects.all()
    serializer_class = GenericaSerializer

    def patch(self, request, *args, **kwargs):
        super(GenericaDetalle, self).patch(request, args, kwargs)
        return Response({"titulo": "Datos Modificados"})

def GenerarCodigo(longitud):
    valores = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    codigo = ""
    codigo = codigo.join([choice(valores) for i in range(longitud)])
    return codigo


class DatosPersona(viewsets.ViewSet):
    def list(self, request, pk):
        try:
            (usuario, token) = JWTAuthentication().authenticate(request)
            if pk == 0:
                pk = usuario.id
            persona = Persona.objects.get(Q(pk=pk))
        except (KeyError, Persona.DoesNotExist):
            return Response( {"titulo": "la persona no existe"}, status=status.HTTP_302_FOUND)
        else:
            programas = Generica.objects.filter(estado = 1, tipo = 3, persona = persona.id,relacion__estado = 1).values("estado","id","tipo", "relacion","persona")
            perfiles = Generica.objects.filter(estado = 1, tipo = 1, persona = persona.id,relacion__estado = 1).values("estado","id","tipo", "relacion","persona")
            persona_ser = PersonaSerializerAdd(persona).data;


            programa_serializer = GenericaSerializerListV2(5, persona)
            programa_ser = programa_serializer.to_representation(programas)
            
            perfiles_serializer = GenericaSerializerListV2(3, persona)
            perfiles_ser = perfiles_serializer.to_representation(perfiles)

            return Response({'persona' : persona_ser,'programas' : programa_ser, 'perfiles' : perfiles_ser})


class RolesPersona(viewsets.ViewSet):
    def list(self, request):
        try:
            (usuario, token) = JWTAuthentication().authenticate(request)
            pk = usuario.id
            persona = Persona.objects.get(Q(pk=pk))
        except (KeyError, Persona.DoesNotExist):
            return Response( {"titulo": "la persona no existe"}, status=status.HTTP_302_FOUND)
        else:
            roles = Generica.objects.filter(estado = 1, tipo = 2, persona = persona.id, relacion__estado = 1, relacion__valora='secundario').order_by('relacion__valorb')
            roles_ser = GenericaSerializerList(roles, many=True).data;
            return Response({'roles' : roles_ser})

class PersonaGenericaBuscar(viewsets.ViewSet):
    def list(self, request, tipo):
        dato = request.data["dato"]
        relacion = request.data["relacion"]
        resp = []
        if dato and len(dato) >= 4:
            for term in dato.split():
                resp = Persona.objects.filter(
                    Q(identificacion__icontains=term)
                    | Q(primer_nombre__icontains=term)
                    | Q(segundo_nombre__icontains=term)
                    | Q(primer_apellido__icontains=term)
                    | Q(segundo_nombre__icontains=term)
                    | Q(correo__icontains=term)
                    | Q(usuario__icontains=term),
                    estado=1,
                    generica__tipo = tipo,
                    generica__estado = 1,
                    generica__relacion__codigo = relacion,
                    generica__relacion__estado = 1)
                    
            serializer = PersonaSerializerList(resp, many=True)
            return Response(serializer.data)

class DesasignarPermiso(generics.UpdateAPIView):
    def update(self, request, *args, **kwargs):
        try:
            (usuario, token) = JWTAuthentication().authenticate(request)
            persona = Persona.objects.get(pk=kwargs['pk'])
            perfil = Valores_generica.objects.get(pk=usuario.perfil_id)
            rol = Generica.objects.get(persona_id=persona.id, relacion_id=perfil.id, tipo=5, estado=1)
            if not rol:
                return Response({ "titulo": "Esta persona no es un coordinador" }, status=status.HTTP_400_BAD_REQUEST)
            elif (perfil.valora != "Dir_Prog"):
                return Response({"titulo": "No tiene permisos para realizar esta acción"}, status=status.HTTP_401_UNAUTHORIZED)
        except (KeyError, Persona.DoesNotExist):
            return Response({"titulo": "Esta persona no se encuentra registrada." }, status=status.HTTP_404_NOT_FOUND)
        except (KeyError, Valores_generica.DoesNotExist):
            return Response({"titulo": "Este perfil no existe!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            rol.estado = 0
            rol.fecha_elimino = datetime.datetime.now()
            rol.usuario_elimino = usuario
            rol.save()
            return Response({ "titulo": "Rol desasignado exitosamente!", "ok": True }, status=status.HTTP_200_OK)


class GenericasValoresPermisoPersona(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = Valores_genericaSerializer
    queryset = Valores_generica.objects.filter(estado = 1)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['generica', 'codigo', 'nombre', 'valora', 'valorb', 'valorc']

    def list(self, request, pk, tipo):
        queryset = self.get_queryset()
        self.object_list = self.filter_queryset(queryset)
        valores =  self.object_list
        permisos = Generica.objects.filter(persona=pk, tipo=tipo, estado=1)
        for valor in valores:
            setattr(valor, 'permiso', 0)
            for permiso in permisos:
                if valor.id == permiso.relacion_id:
                    setattr(valor, 'permiso', permiso.id)
        serializer = Valores_genericaPermisoSerializer(valores, many=True)
        return Response(serializer.data)

class EliminarGenericaPermiso(generics.UpdateAPIView):
    
    def update(self, request, pk, val, tipo):
        try:
            (usuario, token) = JWTAuthentication().authenticate(request)
            persona = Persona.objects.get(pk=pk)
            valor = Valores_generica.objects.get(pk=val)
            permiso = Generica.objects.get(persona=pk, tipo=tipo, relacion=valor, estado=1)
            if not permiso:
                return Response({ "titulo": "Esta persona tiene asignado este parámetrpo" }, status=status.HTTP_400_BAD_REQUEST)
        except (KeyError, Persona.DoesNotExist):
            return Response({"titulo": "Esta persona no se encuentra registrada." }, status=status.HTTP_404_NOT_FOUND)
        except (KeyError, Valores_generica.DoesNotExist):
            return Response({"titulo": "Este parámetro no existe!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            pass
            permiso.estado = 0
            permiso.fecha_elimino = datetime.datetime.now()
            permiso.usuario_elimino = usuario
            permiso.save()
        return Response({ "titulo": "Parámetro desasignado exitosamente!", "ok": True }, status=status.HTTP_200_OK)



class ProgramasUsuario(viewsets.ViewSet):
    def list(self, request, pk):
        try:
            persona = Persona.objects.get(pk=pk)
        except (KeyError, Persona.DoesNotExist):
            return Response( {"titulo": "La persona no existe"}, status=status.HTTP_302_FOUND)
        else:
            # (usuario, token) = JWTAuthentication().authenticate(request)
            programas = Generica.objects.filter(estado=1, tipo=3, persona=persona, relacion__estado=1)
            serializer = GenericaSerializerList(programas, many=True)
            return Response(serializer.data)            


class ValidarCredencialesNew(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    def calculate_code_challenge(self, code_verifier):
        code_challenge_bytes = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge_bytes).rstrip(b'=').decode()
        return code_challenge
    def calculate_state_token(self):
        # Genera un token único y guárdalo temporalmente en la sesión del usuario
        state_token = secrets.token_urlsafe(16)
        return state_token
    def construct_microsoft_auth_url(self, code_challenge,correo):
        # Construye la URL de autenticación de Microsoft con PKCE
        tenant_id = settings.MICROSOFT_AUTH_TENANT_ID
        client_id = settings.MICROSOFT_AUTH_CLIENT_ID
        redirect_uri = settings.MICROSOFT_REDIRECT_URI
        scope = 'openid profile email'
        prompt = 'login'
        login_hint_param = f'&login_hint={correo}' if correo else ''
        login_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope={scope}&code_challenge={code_challenge}&code_challenge_method=S256&prompt={prompt}{login_hint_param}'
        return login_url
    
    # NUEVO PRUEBA
    def generar_token(self, request, persona):
        refresh = RefreshToken.for_user(persona)

        # Personalizar la expiración del token si es necesario
        access_token = refresh.access_token
        if 'no_expiry' in request.data:
            # Configurar expiración personalizada para el token de acceso
            access_token.set_exp(lifetime=datetime.timedelta(days=30))
        else:
            # Usar la configuración predeterminada de Simple JWT
            access_token.set_exp(lifetime=datetime.timedelta(days=30))

        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
            'usuario': PersonaSerializer(persona).data,
        }, status=status.HTTP_200_OK)
    
    # def construct_microsoft_auth_url(self, correo, state_token):
    #     tenant_id = settings.MICROSOFT_AUTH_TENANT_ID
    #     client_id = settings.MICROSOFT_AUTH_CLIENT_ID
    #     redirect_uri = 'http://localhost:3000'
    #     scope = 'openid profile email'
    #     prompt = 'login'
    #     login_hint_param = f'&login_hint={correo}' if correo else ''
    #     state_param = f'&state={state_token}'
    #     nonce = secrets.token_urlsafe(16)  # Genera un nonce único
    #     nonce_param = f'&nonce={nonce}'
    #     login_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?client_id={client_id}&response_type=id_token%20code&redirect_uri={redirect_uri}&response_mode=form_post&scope={scope}&prompt={prompt}{login_hint_param}{state_param}{nonce_param}'
    #     return login_url
   
    def post(self, request, *args, **kwargs):
        correo = request.data["correo"]
        correo_regex = r'^[a-zA-Z0-9._-]+(\.[a-zA-Z0-9._-]+)*@[a-zA-Z0-9._-]+(\.[a-zA-Z0-9._-]+)*\.[a-zA-Z]+$'
        if not re.match(correo_regex, correo):
            return Response({"titulo": "Correo no válido, por favor verifique la información ingresada."}, status=status.HTTP_302_FOUND)
        password = request.data["password"]
        req_codigo = request.data["codigo"]
        txt_codigo = request.data["txtcodigo"]
        intentos = int(request.data["intentos"])
        registro = int(request.data["registro"])
        no_valido = Response(
            {"titulo": "Usuario o clave incorrectos, si necesitas ayuda contactate con tecnologia@cuc.edu.co."}, status=status.HTTP_302_FOUND
        )
        vp_intentos = int(Valores_generica.objects.get(codigo="Int_Log").valora) - 1
        if '@cuc.edu.co' in correo:
            try:
                persona = Persona.objects.get(estado=1, correo=correo)
            except (KeyError, Persona.DoesNotExist):
                if registro >= vp_intentos:
                    return Response({"titulo": "No se encontró un usuario asociado a este correo, valide que este bien escrito e intente de nuevo.", "show_modal": True}, status=status.HTTP_302_FOUND)
                else:
                    return Response({"titulo": "No se encontró un usuario asociado a este correo, valide que este bien escrito e intente de nuevo.", "registro": True}, status=status.HTTP_302_FOUND)
            else:
                if int(persona.login_directorio) == 1:
                    persona.set_password(persona.identificacion)
                    persona.pass_interna = persona.identificacion
                    persona.save()

                    #msLogin
                    request.data["password"] = (persona.pass_interna)
                    code_verifier = secrets.token_urlsafe(64)
                    # state_token = self.calculate_state_token()
                    code_challenge = self.calculate_code_challenge(code_verifier)
                    microsoft_url = self.construct_microsoft_auth_url(code_challenge,correo)
                    # microsoft_url = self.construct_microsoft_auth_url(correo,state_token)
                    return Response({"microsoft_auth_url": microsoft_url,"code_verifier": code_verifier})
                else:
                    if not password:
                        return Response({"autenticacion": False})
            try:
                response = super().post(request, *args, **kwargs)
            except AuthenticationFailed:
                return no_valido
            
            if response.status_code == 200:
                # Ajuste tokens sin expiracion
                response = self.generar_token(request, persona)
                return response
            else:
                return no_valido
        else:
            if not password:
                return Response({"autenticacion": False})
            try:
                persona = Persona.objects.get(estado=1, correo=correo)
            except (KeyError, Persona.DoesNotExist):
                return Response({"titulo": "No se encontro un usuario asociado a este correo."}, status=status.HTTP_302_FOUND)
            else:
                response = super().post(request, *args, **kwargs)
                if response.status_code == 200:
                    response = self.generar_token(request, persona)
                    if int(persona.verificado) == 0 and int(persona.login_directorio) == 0:
                        if not (req_codigo):
                            codigo = GenerarCodigo(6)
                            persona.codigo_verificacion = codigo
                            persona.save()
                            enviarCorreoFuncion(persona.correo, codigo)
                            return Response(
                                {
                                    "titulo": "La cuenta no ha sido activada, se envió un código de verificación al correo "
                                    + persona.correo,
                                    "codigo": True,
                                },
                                status=status.HTTP_302_FOUND,
                            )
                        else:
                            if not (txt_codigo):
                                return Response(
                                    {
                                        "titulo": "El campo código es obligatorio.",
                                        "codigo": True,
                                    },
                                    status=status.HTTP_302_FOUND,
                                )
                            else:
                                if persona.codigo_verificacion != txt_codigo:
                                    return Response(
                                        {
                                            "titulo": "El código de verificación es incorrecto",
                                            "codigo": True,
                                        },
                                        status=status.HTTP_302_FOUND,
                                    )
                                else:
                                    persona.verificado = 1
                                    persona.save()
                    return response
                else:
                    return no_valido

class MicrosoftTokenValidator(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def exchange_code_for_token(self,code,code_verifier):
        tenant_id = settings.MICROSOFT_AUTH_TENANT_ID  # Reemplaza 'TU_TENANT_ID' por el ID de tu inquilino de Azure
        token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        client_id = settings.MICROSOFT_AUTH_CLIENT_ID  # Reemplaza 'TU_CLIENT_ID' por el ID de cliente de tu aplicación registrada en Azure
        client_secret = settings.MICROSOFT_AUTH_CLIENT_SECRET # Reemplaza 'TU_CLIENT_SECRET' por el secreto de cliente de tu aplicación registrada en Azure

        payload = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'code': code,
            'client_secret': client_secret,
            'redirect_uri': settings.MICROSOFT_REDIRECT_URI,
            'code_verifier': code_verifier,
            'scope':'User.Read'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        response = requests.post(token_endpoint, data=payload, headers=headers).json()
        return response

    # Método para obtener información del usuario autenticado desde Microsoft
    def get_user_info_from_microsoft(self, microsoft_token):
        user_info_endpoint = 'https://graph.microsoft.com/v1.0/me'

        headers = {
            'Authorization': f'Bearer {microsoft_token}'
        }

        response = requests.get(user_info_endpoint, headers=headers).json()
        return response
    
    def post(self, request, *args, **kwargs):
        code = request.data.get('sessionState')
        code_verifier = request.data.get('code_verifier')

        if code:
            token_data = self.exchange_code_for_token(code,code_verifier)
            if token_data.get('access_token'):
                microsoft_token = token_data['access_token']
                user_info = self.get_user_info_from_microsoft(microsoft_token)
                correo = user_info.get('mail')
                if correo:
                    persona = Persona.objects.get(correo=correo, estado=1)
                    jwt_token = AccessToken().for_user(persona)
                    return Response({'token': str(jwt_token)}, status=status.HTTP_200_OK)
                else:
                    error_message = 'Error al obtener el ID del usuario desde la respuesta de Microsoft'
                    return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
                
            else:
                error_message = 'Error al intercambiar el código de autorización por el token de acceso'
                return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'No se proporcionó el código de autorización'}, status=status.HTTP_400_BAD_REQUEST)

    # def generar_token(self, request, persona):
    #     payload = jwt_payload_handler(persona)

    #     # Personalizar la expiración del token si es necesario
    #     if 'no_expiry' in request.data:
    #         # payload.pop('exp', None)  # Elimina el campo de expiración
    #         expiration_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    #         payload['exp'] = expiration_datetime.timestamp()
    #     else:
    #         # Configura la expiración personalizada según tus necesidades
    #         payload['exp'] = datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA

    #     token = jwt_encode_handler(payload)

    #     return Response({
    #         'token': token,
    #         'usuario': PersonaSerializer(persona).data,
    #     }, status=status.HTTP_200_OK)

class ValidarCredencialesNewApp(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        correo = request.data["correo"]
        correo_regex = r'^[a-zA-Z0-9._-]+(\.[a-zA-Z0-9._-]+)*@[a-zA-Z0-9._-]+(\.[a-zA-Z0-9._-]+)*\.[a-zA-Z]+$'
        if not re.match(correo_regex, correo):
            return Response({"titulo": "Correo no válido, por favor verifique la información ingresada."}, status=status.HTTP_302_FOUND)
        password = request.data["password"]
        req_codigo = request.data["codigo"]
        txt_codigo = request.data["txtcodigo"]
        intentos = int(request.data["intentos"])
        registro = int(request.data["registro"])
        no_valido = Response(
            {"titulo": "Usuario o clave incorrectos, si necesitas ayuda contactate con tecnologia@cuc.edu.co."}, status=status.HTTP_302_FOUND
        )
        vp_intentos = int(Valores_generica.objects.get(codigo="Int_Log").valora) - 1
        if '@cuc.edu.co' in correo:
            try:
                persona = Persona.objects.get(estado=1, correo=correo)
            except (KeyError, Persona.DoesNotExist):
                if registro >= vp_intentos:
                    return Response({"titulo": "No se encontró un usuario asociado a este correo, valide que este bien escrito e intente de nuevo.", "show_modal": True}, status=status.HTTP_302_FOUND)
                else:
                    return Response({"titulo": "No se encontró un usuario asociado a este correo, valide que este bien escrito e intente de nuevo.", "registro": True}, status=status.HTTP_302_FOUND)
            else:
                if int(persona.login_directorio) == 1:
                    persona.set_password(persona.identificacion)
                    persona.pass_interna = persona.identificacion
                    persona.save()
                    request.data["password"] = (persona.pass_interna)  # los usuarios cuyo ingreso es por el directorio activo, deben tener como password el valor asignado en pass_interna para poder validar las credenciales en el software.
                    try:
                        valido = ValidarCredencialesLdap(correo, password)
                        # valido = False
                    except:
                        return no_valido
                    if not valido:
                        if intentos >= vp_intentos:
                            # enviarCorreoTecnologia(correo, persona)
                            # return Response(
                            #     {"titulo": "Se ha enviado un correo automatico al Dpto Tecnologia, en maximo 24 horas se le dara gestion a su inconveniente.", "dis_btn": True}, status=status.HTTP_302_FOUND
                            # )
                            return Response({"titulo": "Correo o contraseña incorrectos, por favor intente nuevamente.", "show_modal": True}, status=status.HTTP_302_FOUND)
                        else:
                            return Response(
                                {"titulo": "Correo o contraseña incorrectos, por favor intente nuevamente.", "intentos": True}, status=status.HTTP_302_FOUND
                            )
            try:
                response = super().post(request, *args, **kwargs)
                if response.status_code == 200:
                    return self.generar_token(request, persona)
                else:
                    return no_valido
            except AuthenticationFailed:
                return no_valido
        else:
            try:
                persona = Persona.objects.get(estado=1, correo=correo)
            except (KeyError, Persona.DoesNotExist):
                return Response({"titulo": "No se encontro un usuario asociado a este correo, por favor contáctenos en tecnologia@cuc.edu.co"}, status=status.HTTP_302_FOUND)
            else:
                response = super().post(request, *args, **kwargs)
                if response.status_code == 200:
                    response = self.generar_token(request, persona)
                    if int(persona.verificado) == 0 and int(persona.login_directorio) == 0:
                        if not (req_codigo):
                            codigo = GenerarCodigo(6)
                            persona.codigo_verificacion = codigo
                            persona.save()
                            enviarCorreoFuncion(persona.correo, codigo)
                            return Response(
                                {
                                    "titulo": "La cuenta no ha sido activada, se envió un código de verificación al correo "
                                    + persona.correo,
                                    "codigo": True,
                                },
                                status=status.HTTP_302_FOUND,
                            )
                        else:
                            if not (txt_codigo):
                                return Response(
                                    {
                                        "titulo": "El campo código es obligatorio.",
                                        "codigo": True,
                                    },
                                    status=status.HTTP_302_FOUND,
                                )
                            else:
                                if persona.codigo_verificacion != txt_codigo:
                                    return Response(
                                        {
                                            "titulo": "El código de verificación es incorrecto",
                                            "codigo": True,
                                        },
                                        status=status.HTTP_302_FOUND,
                                    )
                                else:
                                    persona.verificado = 1
                                    persona.save()
                    return response
                else:
                    return no_valido

    # NUEVO PRUEBA
    def generar_token(self, request, persona):
        refresh = RefreshToken.for_user(persona)
        access_token = AccessToken()
        access_token.set_jti()
        access_token.payload.update({"user_id": persona.id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)})
        return Response({'refresh': str(refresh), 'token': str(access_token), 'usuario': PersonaSerializer(persona).data, }, status=status.HTTP_200_OK)
    
class RegistroCrear(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializerAdd

    def create(self, request, *args, **kwargs):
        correo = request.data["correoV"]
        identificacion = request.data["identificacion"]
        data=obtenerInformacionSICUC(identificacion)
        if(len(data) > 0):
            usuario_registro= Persona.objects.get(identificacion='12345')
            progr=data[0][7]
            tipo_perfil = Valores_generica.objects.get(codigo="Per_Nor")
            tipoDoc = Valores_generica.objects.get(codigo='cc')
            # estudiante_invitado = Valores_generica.objects.get(codigo="Est_Inv")
            estudiante_perfil = Valores_generica.objects.get(codigo="Per_Nor")
            try:
                programa = Valores_generica.objects.get(codigo=progr, estado=1)
            except (KeyError,Valores_generica.DoesNotExist):
                return Response({"titulo": "No existe el programa."}, status=status.HTTP_302_FOUND)
            else:
                personaBuscar = Persona.objects.filter(Q(identificacion=identificacion) | Q(correo=correo))
                if(len(personaBuscar) <= 0):
                    p=Persona(
                        password=identificacion,
                        login_directorio=1,
                        identificacion=identificacion,
                        primer_nombre=data[0][2],
                        segundo_apellido=data[0][4],
                        primer_apellido=data[0][3],
                        correo=data[0][5], 
                        usuario=data[0][6], 
                        estado=1,
                        perfil= tipo_perfil, 
                        tipo_identificacion=tipoDoc, 
                        usuario_registro_id= usuario_registro.id, 
                        segundo_nombre=""
                    )
                    p.pass_interna = identificacion if p.login_directorio == '1' else None
                    p.set_password(identificacion)
                    p.save()
        
                    try:
                        persona = Persona.objects.get(estado=1, identificacion=identificacion)
                    except (KeyError, Persona.DoesNotExist):
                        return Response({"titulo": "Lo siento no pude ayudarte, escribe un correo a tecnologia@cuc.edu.co"}, status=status.HTTP_302_FOUND)
                    else:
                        persona.is_staff = 1
                        persona.is_active = 1
                        persona.is_superuser = 0
                        persona.save()
                        valorPerfil=Generica(tipo=1, estado=1, persona=persona, relacion=tipo_perfil, usuario_registro_id=usuario_registro.id)
                        valorPerfil.save()
                        valorPrograma=Generica(tipo=3, estado=1, persona=persona, relacion_id=programa.id, usuario_registro_id=usuario_registro.id)
                        valorPrograma.save()
                        return Response({"titulo": "Listo, por favor ingresa nuevamente con tu correo y contraseña institucional."}, status=status.HTTP_200_OK)
                else:
                    personaBuscar[0].login_directorio = 1
                    personaBuscar[0].correo = correo
                    personaBuscar[0].pass_interna = identificacion
                    personaBuscar[0].perfil_id = tipo_perfil.id
                    personaBuscar[0].primer_nombre = data[0][2]
                    personaBuscar[0].primer_apellido = data[0][3]
                    personaBuscar[0].segundo_apellido = data[0][4]
                    personaBuscar[0].usuario = data[0][6]
                    personaBuscar[0].set_password(identificacion)
                    personaBuscar[0].save()
                    queryset=Generica.objects.filter(persona_id = personaBuscar[0], tipo=1, estado=1, relacion_id = estudiante_perfil.id) 
                    # serializer = GenericaSerializer(queryset, many=True)
                    # info=list(serializer.data)
                    # print(info)
                    # if()
                    # sw=True
                    # if len(info) > 0:
                    #     for data in info:
                    #         if data["relacion"] == estudiante_invitado.id:
                    #             t=Generica.objects.get(persona_id = personaBuscar[0], tipo=1, estado=1, relacion= estudiante_invitado.id) 
                    #             t.relacion=tipo_perfil
                    #             t.save()
                    #             sw=False
                    #         if data["relacion"] == estudiante_perfil.id:
                    #             sw=False
                    if not(queryset):
                        valorPerfil=Generica(tipo=1, estado=1, persona=personaBuscar[0], relacion=tipo_perfil, usuario_registro_id=usuario_registro.id)
                        valorPerfil.save()
                    queryset=Generica.objects.filter(persona_id = personaBuscar[0], tipo=3, estado=1) 
                    serializer = GenericaSerializer(queryset, many=True)
                    info=list(serializer.data)
                    if len(info) <= 0:
                        valorPrograma=Generica(tipo=3, estado=1, persona=personaBuscar[0], relacion_id=programa.id, usuario_registro_id=usuario_registro.id)
                        valorPrograma.save()
                    return Response({"titulo": "Listo, por favor ingresa nuevamente con tu correo y contraseña institucional."}, status=status.HTTP_200_OK)
            

def enviarCorreoFuncion(correo, codigo):
    context = {
        "mensajes" :  [
            {
                "mensaje" : "¡Genial!",
                "clase": "titulo",
            },
            {
                "mensaje" : "Aquí tienes el código de verificación de tu cuenta:",
                "clase": "normal",
            },
            {
                "mensaje" : codigo,
                "clase": "importante",
            },
        ]
    }
    template = loader.get_template("correos/plantilla.html")
    html_content = template.render(context)
    EnviarCorreo([correo],html_content,"código de verificación",)
    return True

def enviarCorreoTecnologia(correo_persona, estudiante):
    correo = Valores_generica.objects.get(codigo = "Cor_Tec", estado=1).nombre
    context = {
        "mensajes": [
            {
                "mensaje" : "Buen día",
                "clase" : "titulo",
            },
            {
                "mensaje" : "Cordial saludo,",
                "clase" : "normal",
            },
            {
                "mensaje" : "El siguiente estudiante presenta problemas para ingresar a la plataforma EMMA, por favor revisar.",
                "clase" : "normal",
            },
                      {
            "mensaje": [
              {
                "item": "Identificacion: " + estudiante.identificacion,
              },
              {
                "item": "Correo: " + correo_persona
              }
            ],
            "clase": "lista",
          }
        ]
    }
    template = loader.get_template("correos/plantilla.html")
    html_content = template.render(context)
    EnviarCorreo([correo, correo_persona], html_content, "Restablecimiento contraseña institucional")
    return True


class CrearMasivos(viewsets.ViewSet):
    def list(self, request):
        empresas = Persona.objects.filter(password='empresas_portal')
        for e in empresas:
            e.set_password(e.usuario)
            e.save()
            # print(e.password)
        return Response({"titulo": "{} Empresas actualizadas".format(len(empresas))})


class DatosPersonaApp(viewsets.ViewSet):
    def list(self, request):
        try:
            (usuario, token) = JWTAuthentication().authenticate(request)
            pk = usuario.id
            persona = Persona.objects.get(pk=pk)
        except (KeyError, Persona.DoesNotExist):
            return Response( {"titulo": "la persona no existe"}, status=status.HTTP_302_FOUND)
        else:
            try:
                carnet = Carnet.objects.get(persona=pk, estado=1)
            except Carnet.DoesNotExist:
                carnet = None
            persona_ser = PersonaSerializerListAPP(persona).data;
            roles = Generica.objects.filter(estado = 1, tipo = 2, persona = persona.id, relacion__estado = 1, relacion__valora='secundario').order_by('relacion__valorb')
            rol_ser = PermisoSerializerListAPP(roles[0] if roles else None).data;
            carnet_ser = CarnetSerializerList(carnet).data
            return Response({'persona': persona_ser, 'carnet': carnet_ser, 'rol' : rol_ser})


# class ActualizarCodigosQr(viewsets.ViewSet):
#     def list(self, request):
#         (usuario, token) = JWTAuthentication().authenticate(request)
#         personas = Persona.objects.filter(estado=1, activo=1)
#         usuario_registro = Persona.objects.get(pk=usuario.id)
#         actualizados = 0
#         creados = 0
#         for p in personas:
#             # No actualizara los estudiantes de pasantias (nacionalidad: pasantes)
#             if p.nacionalidad != "pasantes":
#                 # Creando nuevo codigo
#                 llave_decimal = randint(1,999999999)
#                 llave_hex = (hex(llave_decimal).lstrip("0x")).rjust(8, '0')
#                 identificacion = int(p.identificacion)
#                 identificacion = (hex(identificacion).lstrip("0x")).rjust(8, '0')
#                 nuevo_codigo = (identificacion + llave_hex).upper()

#                 # Validando si ya tiene un codigo para actualizar o si no para crearlo.
#                 try:
#                     carnet = Carnet.objects.get(persona=p.id, estado=1)
#                 except (KeyError, Carnet.DoesNotExist):
#                     creados += 1
#                     carnet = Carnet(persona=p, usuario_registro=usuario_registro, codigo_carnet=nuevo_codigo, llave_decimal=llave_decimal)
#                     carnet.save()
#                 else:
#                     actualizados += 1
#                     carnet.codigo_carnet = nuevo_codigo
#                     carnet.llave_decimal = llave_decimal
#                     carnet.usuario_actualizo = usuario_registro
#                     carnet.fecha_actualizo = datetime.datetime.now()
#                     carnet.save()
#         return Response({'resultado': '{} Codigos actualizados, {} Codigos Creados'.format(actualizados, creados)})

class ActualizarCodigosQr(APIView):
    def post(self, request):
        (usuario, token) = JWTAuthentication().authenticate(request)
        usuario_registro = usuario
        actualizados = 0
        creados = 0
        lote_tamano = 100

        tiempo_minimo = datetime.datetime.now() - datetime.timedelta(days=30)
        personas = Persona.objects.filter(estado=1, activo=1, last_login__gte=tiempo_minimo).values('id', 'identificacion', 'nacionalidad')
        ids_personas = [p['id'] for p in personas]

        while ids_personas:
            # Tomar un lote de IDs
            lote_ids = ids_personas[:lote_tamano]
            ids_personas = ids_personas[lote_tamano:]

            # Obtener carnets existentes en una sola consulta
            carnets_existentes = {c['persona_id']: c for c in Carnet.objects.filter(persona_id__in=lote_ids, estado=1).values('id', 'persona_id')}

            nuevos_carnets = []
            carnets_actualizar = []

            with transaction.atomic():
                for p in personas:
                    if p['id'] not in lote_ids:
                        continue  # Solo procesar IDs en el lote actual
                    
                    if p['nacionalidad'] != "pasantes":
                        llave_decimal = randint(1, 999999999)
                        llave_hex = (hex(llave_decimal).lstrip("0x")).rjust(8, '0')
                        identificacion = hex(int(p['identificacion'])).lstrip("0x").rjust(8, '0')
                        nuevo_codigo = (identificacion + llave_hex).upper()

                        if p['id'] in carnets_existentes:
                            # carnet = carnets_existentes[p['id']]
                            # carnet.codigo_carnet = nuevo_codigo
                            # carnet.llave_decimal = llave_decimal
                            # carnet.usuario_actualizo = usuario_registro
                            # carnet.fecha_actualizo = datetime.datetime.now()
                            # carnets_actualizar.append(carnet)

                            carnets_actualizar.append({
                                'id': carnets_existentes[p['id']]['id'],
                                'codigo_carnet': nuevo_codigo,
                                'llave_decimal': llave_decimal,
                                'usuario_actualizo_id': usuario_registro.id,
                                'fecha_actualizo': datetime.datetime.now()
                            })

                            actualizados += 1
                        else:
                            creados += 1
                            nuevos_carnets.append(
                                Carnet(
                                    persona_id=p['id'],
                                    usuario_registro=usuario_registro,
                                    codigo_carnet=nuevo_codigo,
                                    llave_decimal=llave_decimal
                                )
                            )

                # Guardar los nuevos carnets en lotes
                if nuevos_carnets:
                    Carnet.objects.bulk_create(nuevos_carnets, batch_size=lote_tamano)
                
                if carnets_actualizar:
                    for c in carnets_actualizar:
                        Carnet.objects.filter(id=c['id']).update(
                            codigo_carnet=c['codigo_carnet'],
                            llave_decimal=c['llave_decimal'],
                            usuario_actualizo_id=c['usuario_actualizo_id'],
                            fecha_actualizo=c['fecha_actualizo']
                        )

            # LIBERA LA CONEXIÓN AL FINAL DE CADA LOTE
            connection.close()

        return Response({'resultado': f'{actualizados} Códigos actualizados, {creados} Códigos Creados'})


class CrearCodigosQr(viewsets.ViewSet):
    def list(self, request):
        (usuario, token) = JWTAuthentication().authenticate(request)
        personas = Persona.objects.filter(estado=1, activo=1)
        usuario_registro = Persona.objects.get(pk=usuario.id)
        creados = 0
        for p in personas:
            # Creando nuevo codigo
            llave_decimal = randint(1,999999999)
            llave_hex = (hex(llave_decimal).lstrip("0x")).rjust(8, '0')
            identificacion = int(p.identificacion)
            identificacion = (hex(identificacion).lstrip("0x")).rjust(8, '0')
            nuevo_codigo = (identificacion + llave_hex).upper()

            # Validando si ya tiene un codigo para actualizar o si no para crearlo.
            try:
                carnet = Carnet.objects.get(persona=p.id, estado=1)
            except (KeyError, Carnet.DoesNotExist):
                creados += 1
                carnet = Carnet(persona=p, usuario_registro=usuario_registro, codigo_carnet=nuevo_codigo, llave_decimal=llave_decimal)
                carnet.save()
            
        return Response({'resultado': '{} Codigos Creados'.format(creados)})

# class CrearBarracode(viewsets.ViewSet):
#     def list(self,request):
#         (usuario, token) = JWTAuthentication().authenticate(request)
#         codigo_barra=consultaIdentidadesBarrcode(usuario.identificacion)
#         # print(codigo_barra)
#         if(codigo_barra):
#             return Response({'codigo_barra': codigo_barra[0][0]})
#         else:
#             return Response({})

class CrearBarracode(viewsets.ViewSet):
    def list(self,request):
        (usuario, token) = JWTAuthentication().authenticate(request)
        identificacion = usuario.identificacion
        
        api_idcuc = "https://idcuc-backend.cuc.edu.co/personas/codigo/"
        payload = {
            'identificacion': identificacion
        }
        res = requests.post(api_idcuc, data=payload, headers=[])
        if(res.status_code == 200):
            data = res.json()            
            return Response({'codigo_barra': data['codigo']})
        else:
            return Response({})



class buscarIdentidades(viewsets.ViewSet):
    def list(self, request):
        identificacion = request.data["identificacion"]

        api_idcuc = "https://idcuc-backend.cuc.edu.co/personas/buscar_persona/"
        payload = {
            'identificacion': identificacion
        }
        res = requests.post(api_idcuc, data=payload, headers=[])

        if(res.status_code == 200):
            data = res.json()

            try:
                tipo_id = Valores_generica.objects.get(estado=1, codigo=data['tipo_identificacion'])
                tipo_id = tipo_id.id
            except (KeyError, Valores_generica.DoesNotExist):
                tipo_id = ""

            return Response({'primer_nombre': data['primer_nombre'], 'segundo_nombre': data['segundo_nombre'], 'primer_apellido': data['primer_apellido'], 'segundo_apellido': data['segundo_apellido'], 'correo': data['correo_institucional'], 'usuario': data['username'], 'tipo_identificacion': tipo_id })
        # data=consultaIdentidades(identificacion)
        else:
            return Response({})


@api_view(["GET"])
def fotoMs(request):
    try:
        habilitado = Valores_generica.objects.get(estado=1, codigo="Hab_Fto_MS")
    except(KeyError, Valores_generica.DoesNotExist):
        return Response({"estado": False, "data": ""})
    else:
        if(habilitado.valora == "si"):
            (usuario, token) = JWTAuthentication().authenticate(request)
            consultaFoto = getPhotoMS(usuario.correo)
            fotoMs = consultaFoto if consultaFoto else None
            return Response({"estado": True, "data": fotoMs})
        else:
            return Response({"estado": False, "data": ""})


class EncuestaSPA(viewsets.ViewSet):
    # permission_classes = (permissions.AllowAny,)
    def list(self, request):
        try:
            correo_form = request.data["correo"]
        except (KeyError):
            return Response({"res": "no_ok"}, status=status.HTTP_200_OK)
        else:
            try:
                correo_form = Persona.objects.get(correo=correo_form)
            except Persona.DoesNotExist:
                return Response({"res": "no_ok"}, status=status.HTTP_200_OK)
            else:
                persona = Persona.objects.get(correo=correo_form)
                persona.encuesta_spa = 1
                persona.save()
                return Response({"res": "ok"}, status=status.HTTP_200_OK)
            
class ObtenerEncuestaGenero(viewsets.ViewSet):
    def list(self, request):
        try:
            preguntas_y_respuestas_formateadas = []
            preguntas_id = []
            valor = Valores_generica.objects.get(codigo="pre_encu_gen")
            preguntas = Valores_generica.objects.filter(generica=valor.generica, estado=1).values('id', 'nombre', 'valora').order_by('valorb')
            for pregunta in preguntas:
                preguntas_id.append(pregunta['id'])
            preguntas_y_respuestas_multiples = Permiso.objects.select_related('principal', 'secundario').filter(principal__in=preguntas_id, estado=1).values('principal', 'secundario', 'secundario__nombre')
            for pregunta in preguntas:
                respuestas = []
                for pregunta_y_respuesta in preguntas_y_respuestas_multiples:
                    if pregunta_y_respuesta['principal'] == pregunta['id']:
                        respuestas.append({"id": pregunta_y_respuesta['secundario'], "nombre": pregunta_y_respuesta['secundario__nombre']})
                preguntas_y_respuestas_formateadas.append({"id": pregunta['id'], "pregunta": pregunta['nombre'], "tipo": pregunta['valora'], "respuestas": respuestas})
            return Response({"preguntas": list(preguntas_y_respuestas_formateadas)}, status=status.HTTP_200_OK)
        except Valores_generica.DoesNotExist:
            return Response({"titulo": "No hay preguntas registradas"}, status=status.HTTP_302_FOUND)
        
class ValidarEncuestaGenero(APIView):
    def post(self, request):
        (usuario, token) = JWTAuthentication().authenticate(request)
        periodo = Valores_generica.objects.get(codigo="per_enc_gen", estado=1)
        encuesta = Encuesta_Genero.objects.filter(usuario_registro=usuario.id, estado=1, periodo=periodo.valora).first()
        if not encuesta and periodo.valorb == 'activo':
            return Response({"estado_encuesta": False}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"estado_encuesta": True}, status=status.HTTP_200_OK)
        
class GuardarEncuestaGenero(APIView):
    def post(self, request):
        try:
            (usuario, token) = JWTAuthentication().authenticate(request)
            persona = Persona.objects.get(pk=usuario.id)
            respuestas = request.data['respuestas']
            # Validamos si las respuestas vienen vacias o si vienen menos de 5 respuestas
            if len(respuestas) < 6:
                return Response({"titulo": "Debes responder todas las preguntas!"}, status=status.HTTP_400_BAD_REQUEST)
            # Procedemos a crear la encuesta 
            periodo = Valores_generica.objects.get(codigo="per_enc_gen", estado=1)
            encuesta = Encuesta_Genero(usuario_registro=persona, estado=1, estado_encuesta=1, periodo=periodo.valora)
            encuesta.save()
            respuestas_a_guardar = []
            
            for respuesta in respuestas:
                if respuesta['tipo'] == '1':
                    respuestas_a_guardar.append(Encuesta_Genero_Pregunta(encuesta_genero=encuesta, pregunta_id=respuesta['pregunta_id'], valor=respuesta['valor'], estado=1))
                else:
                    respuestas_a_guardar.append(Encuesta_Genero_Pregunta(encuesta_genero=encuesta, pregunta_id=respuesta['pregunta_id'], respuesta_id=respuesta['valor'], estado=1))
            
            Encuesta_Genero_Pregunta.objects.bulk_create(respuestas_a_guardar)
            
            return Response({"titulo": "Encuesta registrada con éxito"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"titulo": "Error inesperado", "detalle": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ValidarPolitica(APIView):
    def get(self, request):
        (usuario, token) = JWTAuthentication().authenticate(request)
        periodo = Valores_generica.objects.get(codigo="Pol_Dat_Cuc", estado=1)
        valido = Aceptacion_Politica.objects.filter(usuario_registro=usuario.id, estado=1, periodo=periodo.valora).first()
        if not valido:
            return Response({"valido": False}, status=status.HTTP_200_OK)
        else:
            return Response({"valido": True}, status=status.HTTP_200_OK)
        
class AceptarPolitica(APIView):
    def post(self, request):
        (usuario, token) = JWTAuthentication().authenticate(request)
        periodo = Valores_generica.objects.get(codigo="Pol_Dat_Cuc", estado=1)
        
        politica = Aceptacion_Politica(usuario_registro=usuario, estado=1, periodo=periodo.valora)
        politica.save()
        return Response({"titulo": "Política Aceptada con éxito"}, status=status.HTTP_201_CREATED)
