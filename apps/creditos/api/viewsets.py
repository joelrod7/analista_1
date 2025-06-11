from .serializers import CreditoSerializer, EncuestaSerializer, EncuestaDetailSerializer, CreditoSerializerList,EstadoSerializerList,AdjuntoSerializerList,PagosSerializerList, CreditoSerializerListSimple
from ..models import Credito, Solicitud, Estado, Adjunto
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from rest_framework_simplejwt.authentication import JWTAuthentication
from ...personas.api.serializers import PersonaSerializerList
from ...genericas.api.serializers import Valores_genericaSerializer, PermisoSerializer
from ...personas.models import Persona, Generica as Generica_per
from ...genericas.models import Valores_generica, Generica, Permiso
from django_filters.rest_framework import DjangoFilterBackend
from django.template import loader
from facecuc.microsoft import EnviarCorreo
from facecuc.sinu import comprobar_promedio_acumulado, comprobar_promedio_nivel
from facecuc.utils import servidor, validar_archivo_general
import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.db.models import Count
from django.db.models import Value, IntegerField
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import json
class CreditoCrear(generics.CreateAPIView):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        # Antes de proceder a crear el credito se debe validar el archivo adjunto
        if ("total" in request.data and int(request.data["total"]) > 0):
            for a in range(0, int(request.data["total"])):
                check_archivo = validar_archivo_general(request.FILES["archivo" + str(a)])
                if not check_archivo:
                    return Response({"titulo": "El archivo no es válido"}, status=status.HTTP_302_FOUND)

        try:
            tipo_estado = Valores_generica.objects.get(codigo="Cre_Env", estado=1)
        except (KeyError, Valores_generica.DoesNotExist):
            return Response({"titulo": "El estado inicial no existe."}, status=status.HTTP_302_FOUND)
        else:
            try:
                periodo = Valores_generica.objects.get(codigo="Per_Cre")
            except (KeyError, Valores_generica.DoesNotExist):
                return Response({"titulo": "No hay ningún periodo activo."}, status=status.HTTP_302_FOUND)
            else:
                (usuario, token) = JWTAuthentication().authenticate(request)
                _mutable = request.data._mutable
                request.data._mutable = True

                tipo_credito = Valores_generica.objects.get(id=request.data["tipo"])
                if(tipo_credito.codigo == 'sol_lega' or tipo_credito.codigo == 'sol_directo'):
                    entidad_default = Valores_generica.objects.get(codigo="Ent_Def", estado=1)
                    request.data["entidad"] = entidad_default.id
                elif(tipo_credito.codigo == 'sol_desc' or tipo_credito.codigo == 'sol_cong' or tipo_credito.codigo =='sol_dev'):
                    entidad_default = Valores_generica.objects.get(codigo="Ent_Na", estado=1)
                    request.data["entidad"] = entidad_default.id
                elif(tipo_credito.codigo == 'sol_dev'):
                    solicitud_dev = Valores_generica.objects.get(pk=request.data["solicitud_dev"], estado=1)
                    entidades_dev = Valores_generica.objects.get(pk=request.data["entidades_dev"], estado=1)
                    origen_dinero_dev = Valores_generica.objects.get(pk=request.data["origen_dinero_dev"], estado=1)
                    request.data["tipo_devolucion"] = solicitud_dev.id
                    request.data["entidad_devolucion"] = entidades_dev.id
                    request.data["origen_dinero_devolucion"] = origen_dinero_dev.id                

                request.data["usuario_registro"] = usuario.id
                request.data["estado_actual"] = tipo_estado.id
                request.data["periodo"] = periodo.nombre
                request.data._mutable = _mutable
                telefono = request.data["telefono"]
                celular = request.data["celular"]
                entidad = request.data["entidad"]
                categoria = request.data["categoria"]
                solicitudes= request.data["solicitudes"].split(',') if request.data["solicitudes"] else []
                total = request.data["total"]
                codigo_icetex_dev = request.data["codigo_icetex_dev"]
                nombre_titular_dev = request.data["nombre_titular_dev"]
                numero_documento_dev = request.data["numero_documento_dev"]
                nombre_entidad_dev = request.data["nombre_entidad_dev"]
                solicitud_estado_finan = request.data["solicitud_estado_finan"]

                creditos_activos = Credito.objects.filter(Q(estado_actual__codigo='Cre_Pen') | Q(estado_actual__codigo='Cre_Pag'), tipo__codigo='sol_cred', usuario_registro=usuario.id, estado=1, periodo=periodo.nombre)
                if(creditos_activos):
                    return Response({"titulo": "Usted cuenta con una solicitud pendiente por documentos, carguelos en la solicitud para continuar con el proceso."},status=status.HTTP_302_FOUND,) 

                procesos_activos = Credito.objects.filter(~Q(estado_actual__codigo = 'Cre_Car') & ~Q(estado_actual__codigo = 'Cre_Rec') & ~Q(estado_actual__codigo = 'Cre_Rech') & ~Q(estado_actual__codigo = 'Cre_ProRea'), usuario_registro=usuario.id, estado= 1, periodo=periodo.nombre, tipo__codigo=tipo_credito.codigo)
                if(procesos_activos):
                    return Response({"titulo": "Usted ya cuenta con una solicitud en proceso."},status=status.HTTP_302_FOUND,) 
                
                entidad = request.data.get('entidad', '')
                # Verificar si 'entidad' tiene un valor
                if entidad:
                    try:
                        info_entidad = Valores_generica.objects.get(id=entidad)
                    except Valores_generica.DoesNotExist:
                        raise Response({ "titulo": "La entidad con el id proporcionado no existe."}, status=status.HTTP_302_FOUND)
                else:
                # Si no hay entidad, continuar con el flujo del código
                    info_entidad = None
                #info_entidad = Valores_generica.objects.get(id=entidad)
                if(not(telefono) or not(str(telefono).isnumeric())):
                    return Response({"titulo": "Ingrese numero de telefono."},status=status.HTTP_302_FOUND,) 
                elif(not(celular) or not(str(celular).isnumeric())):
                    return Response({"titulo": "Ingrese numero de celular."},status=status.HTTP_302_FOUND,) 
                # elif(not(solicitudes)):
                #     return Response({"titulo": "Seleccione tipo de solicitud."},status=status.HTTP_302_FOUND,)
                    
                elif (int(total) == 0 and not((tipo_credito.codigo == 'sol_cred' and categoria == '1' and info_entidad.valora == 'icetex') or tipo_credito.codigo == 'sol_conestfin')):
                    return Response({"titulo": "Debe cargar los documentos para continuar."},status=status.HTTP_302_FOUND,)
                else:
                    super(CreditoCrear, self).create(request, args, kwargs)
                    credito = Credito.objects.filter(usuario_registro=usuario.id, estado= 1).last()
                    #actulizo los datos de la persona
                    usuario_registro = Persona.objects.get(pk=usuario.id)
                    usuario_registro.telefono = telefono
                    usuario_registro.celular = celular
                    usuario_registro.save()
                    #se guarda el estado
                    estado = Estado( usuario_registro=usuario_registro, credito=credito, tipo_estado=tipo_estado,)
                    estado.save()
                    #si fue exitoso se guardan los documentos
                    if(int(total) > 0):
                        archivos_guardar = []
                        for a in range(0, int(total)):
                            nombre_archivo = request.FILES["archivo" + str(a)].name
                            archivo = request.data["archivo" + str(a)]
                            data = Adjunto(credito=credito,archivo=archivo,usuario_registro=usuario_registro,nombre_archivo = nombre_archivo)
                            archivos_guardar.append(data)
                        Adjunto.objects.bulk_create(archivos_guardar)
                    #se guardan las solicitudes requeridas
                    solicitudes_guardar = []

                    if not solicitudes or len(solicitudes) == 0:
                        solicitudes = [solicitud_estado_finan] if solicitud_estado_finan else []
                    for a in solicitudes:
                        solicitud = Valores_generica.objects.get(id = a)
                        data = Solicitud(credito = credito, usuario_registro = usuario_registro, solicitud = solicitud)
                        solicitudes_guardar.append(data)
                    Solicitud.objects.bulk_create(solicitudes_guardar)
                    correos = [usuario_registro.correo]
                    if not entidad:
                        gestores = Persona.objects.filter(generica__estado = 1, generica__tipo = 6 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__codigo = 'Cre_Env' ,generica__estado = 1, generica__tipo = 7 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.tipo.id ,generica__estado = 1, generica__tipo = 16 ,generica__relacion__estado = 1, estado = 1).values('correo')
                    else:
                        gestores = Persona.objects.filter(generica__relacion__id = entidad, generica__estado = 1, generica__tipo = 6 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__codigo = 'Cre_Env' ,generica__estado = 1, generica__tipo = 7 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.tipo.id ,generica__estado = 1, generica__tipo = 16 ,generica__relacion__estado = 1, estado = 1).values('correo')
                    
                    for c in gestores:
                        correos.append(c['correo'])
                    #enviarCorreoCredito('Cre_Env',correos)
                    return Response({"titulo": "Datos Enviados"})
                
class CreditodirectoCrear(generics.CreateAPIView):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer
    
    def create(self, request, *args, **kwargs):
        # Antes de procede a crear el credito se debe validar el archivo adjunto
        if ("total" in request.data and int(request.data["total"]) > 0):
            for a in range(0, int(request.data["total"])):
                check_archivo = validar_archivo_general(request.FILES["archivo" + str(a)])
                if not check_archivo:
                    return Response({"titulo": "El archivo no es válido"}, status=status.HTTP_302_FOUND)

        try:
            tipo_estado = Valores_generica.objects.get(codigo="Cre_Env")
        except (KeyError, Valores_generica.DoesNotExist):
            return Response({"titulo": "El estado inicial no existe."}, status=status.HTTP_302_FOUND)
        else:
            try:
                periodo = Valores_generica.objects.get(codigo="Per_Cre")
            except (KeyError, Valores_generica.DoesNotExist):
                return Response({"titulo": "No hay ningún periodo activo."}, status=status.HTTP_302_FOUND)
            try:
                idPrograma = request.data["Programa_cre_d"]
                programa = Valores_generica.objects.get(id=idPrograma)
            except (KeyError, Valores_generica.DoesNotExist):
                return Response({"titulo": "No hay ningún programa activo."}, status=status.HTTP_302_FOUND)
            else:
                (usuario, token) = JWTAuthentication().authenticate(request)
                _mutable = request.data._mutable
                request.data._mutable = True
                
                tipo_credito = Valores_generica.objects.get(id=request.data["tipo"])
                if(tipo_credito.codigo == 'sol_directo'):
                    entidad_default = Valores_generica.objects.get(codigo="Ent_Def")
                    request.data["entidad"] = entidad_default.id
                elif(tipo_credito.codigo == 'sol_desc' or tipo_credito.codigo == 'sol_cong'):
                    entidad_default = Valores_generica.objects.get(codigo="Ent_Na")
                    request.data["entidad"] = entidad_default.id
                    
                request.data["usuario_registro"] = usuario.id
                request.data["estado_actual"] = tipo_estado.id
                request.data["periodo"] = periodo.nombre
                request.data["Programa_cre_d"] = programa.nombre
                request.data["programa"] = programa.id
                request.data["gestor"] = usuario.id
                request.data["gestor_nombre"] = usuario.usuario
                request.data._mutable = _mutable
                telefono_contacto = request.data["telefono_contacto"]
                direccion_per = request.data["direccion_per"]
                correo_personal = request.data["correo_personal"]
                lugar_expedicion = request.data["lugar_expedicion"]
                estado_civil = request.data["estado_civil"]
                lugar_residencia = request.data["lugar_residencia"]
                
                archivo= request.data["archivo"].split(',') if request.data["archivo"] else []
                total = request.data["total"]

                creditos_activos = Credito.objects.filter(Q(estado_actual__codigo='Cre_Pen') | Q(estado_actual__codigo='Cre_Pag'), tipo__codigo='sol_directo', usuario_registro=usuario.id, estado=1, periodo=periodo.nombre)
                if(creditos_activos):
                    return Response({"titulo": "Usted cuenta con una solicitud pendiente por documentos, carguelos en la solicitud para continuar con el proceso."},status=status.HTTP_302_FOUND,) 
                else:
                    procesos_activos = Credito.objects.filter(~Q(estado_actual__codigo = 'Cre_Car') & ~Q(estado_actual__codigo = 'Cre_Rec') & ~Q(estado_actual__codigo = 'Cre_Rech'), usuario_registro=usuario.id, estado= 1, periodo=periodo.nombre, tipo__codigo=tipo_credito.codigo)
                    if(procesos_activos):
                        return Response({"titulo": "Usted ya cuenta con una solicitud en proceso."},status=status.HTTP_302_FOUND,) 
                    
                    else:
                        super(CreditodirectoCrear, self).create(request, args, kwargs)
                        credito = Credito.objects.filter(usuario_registro=usuario.id, estado= 1).last()
                        #actulizo los datos de la persona
                        usuario_registro = Persona.objects.get(pk=usuario.id)
                        usuario_registro.celular = telefono_contacto
                        usuario_registro.direccion = direccion_per
                        usuario_registro.correo_personal = correo_personal
                        usuario_registro.lugar_expedicion = lugar_expedicion
                        usuario_registro.estado_civil = estado_civil
                        usuario_registro.lugar_residencia = lugar_residencia
                        usuario_registro.save()
                        #se guarda el estado
                        estado = Estado( usuario_registro=usuario_registro, credito=credito, tipo_estado=tipo_estado,)
                        estado.save()
                        #si fue exitoso se guardan los documentos
                        if(int(total) > 0):
                            archivos_guardar = []
                            for a in range(0, int(total)):
                                 nombre_archivo = request.FILES["archivo" + str(a)].name
                                 archivo = request.data["archivo" + str(a)]
                                 data = Adjunto(credito=credito,archivo=archivo,usuario_registro=usuario_registro,nombre_archivo = nombre_archivo)
                                 archivos_guardar.append(data)
                            Adjunto.objects.bulk_create(archivos_guardar)
                        
                            
                            correos = [usuario_registro.correo]
                            gestores = Persona.objects.filter(generica__estado = 1, generica__tipo = 6 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__codigo = 'Cre_Env' ,generica__estado = 1, generica__tipo = 7 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.tipo.id ,generica__estado = 1, generica__tipo = 16 ,generica__relacion__estado = 1, estado = 1).values('correo')
                            for c in gestores:
                                correos.append(c['correo'])
                            enviarCorreoCredito('Cre_Env',correos)
                            return Response({"titulo": "Datos Enviados"})
    
    
    
class CreditoDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer

    def patch(self, request, *args, **kwargs):
        super(CreditoDetalle, self).patch(request, args, kwargs)
        return Response({"titulo": "Datos modificados"})


class obtenerDetalleCredito(viewsets.ViewSet):
    def list(self, request, pk):
        try:
            periodo = Valores_generica.objects.get(codigo="Per_Cre")
        except (KeyError, Valores_generica.DoesNotExist):
            return Response({"titulo": "No hay ningún periodo activo."}, status=status.HTTP_302_FOUND)
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            credito = Credito.objects.get(pk = pk)
            serializer_credito = CreditoSerializerList(credito)
            linea_estados = Permiso.objects.filter(~Q(secundario__valorb = '') & ~Q(secundario__valorb = None), principal=credito.tipo.id, secundario__generica = 37 , estado=1,secundario__estado = 1 ,principal__estado = 1,).order_by('secundario__valorb')
            serializer_linea = PermisoSerializer(linea_estados, many=True)
            return Response({'credito' : serializer_credito.data, 'linea' : serializer_linea.data})


class CreditosListar(generics.ListAPIView):
    serializer_class = CreditoSerializerListSimple
    queryset = Credito.objects.filter(estado = 1)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'estado_actual__valord', 'estado_actual__codigo','periodo','categoria','estado_actual','entidad','programa','tipo', 'usuario_registro','Programa_cre_d']

    def list(self, request, tipo):
        (usuario, token) = JWTAuthentication().authenticate(request)
        if tipo == 1:
            if usuario.perfil.codigo == 'Per_Adm':
                queryset = Credito.objects.filter(estado=1).extra(select = {'permiso' : "select 1"},)
            else:
                entidades = Generica_per.objects.filter(tipo = 6, estado = 1, relacion__estado = 1, persona = usuario.id).values_list('relacion__id')
                estados = Generica_per.objects.filter(tipo = 7, estado = 1, relacion__estado = 1, persona = usuario.id).values('relacion__id')
                tipos = Generica_per.objects.filter(tipo = 16, estado = 1, relacion__estado = 1, persona = usuario.id).values('relacion__id')
                programas = Generica_per.objects.filter(tipo = 36, estado = 1, relacion__estado = 1, persona = usuario.id).values('relacion__id')
                permisos = convertir(estados)
                if programas:
                    queryset = Credito.objects.filter(estado=1, entidad__id__in = entidades, tipo__id__in = tipos, programa__id__in=programas).extra(select = {'permiso' : "select IIF(CONVERT(varchar(11), estado_actual_id) IN ({}), 1, 0)".format(permisos)},)
                else:
                    queryset = Credito.objects.filter(estado=1, entidad__id__in = entidades, tipo__id__in = tipos).extra(select = {'permiso' : "select IIF(CONVERT(varchar(11), estado_actual_id) IN ({}), 1, 0)".format(permisos)},)
        else:
            queryset = Credito.objects.filter(estado=1, usuario_registro = usuario.id)
        self.object_list = self.filter_queryset(queryset)
        queryset =  self.object_list
        serializer = CreditoSerializerListSimple(queryset, many=True)
        return Response(serializer.data)
        
    
class EstadoSolicitudes(viewsets.ViewSet):
    def list(self, request, periodo):
        (usuario, token) = JWTAuthentication().authenticate(request)
        
        if usuario.perfil.codigo == 'Per_Adm':
            data = Credito.objects.values('estado_actual__nombre', 'estado_actual__codigo').filter(estado=1, periodo=periodo).order_by('-estado_actual__valord', 'estado_actual__valorb').annotate(
                num_sol=Count('estado_actual'),
                orden=Value(2, output_field=IntegerField()),
                )
            info_extra = [{'solicitudes': '', 'nombre': 'Todos', 'codigo': 'Tod_Cre', 'orden' : 1}]
        else:
            tipos = Generica_per.objects.filter(tipo = 16, estado = 1, relacion__estado = 1, persona = usuario.id).values_list('relacion__id')
            entidades = Generica_per.objects.filter(tipo = 6, estado = 1, relacion__estado = 1, persona = usuario.id).values_list('relacion__id')
            programas = Generica_per.objects.filter(tipo = 36, estado = 1, relacion__estado = 1, persona = usuario.id).values('relacion__id')
            if programas:
                data = Credito.objects.values('estado_actual__nombre', 'estado_actual__codigo').filter(Q(tipo__id__in=tipos, entidad__id__in=entidades, programa__id__in=programas), estado=1, periodo=periodo).order_by('-estado_actual__valord', 'estado_actual__valorb').annotate(
                    num_sol=Count('estado_actual'),
                    orden=Value(2, output_field=IntegerField())
                    )
            else:
                data = Credito.objects.values('estado_actual__nombre', 'estado_actual__codigo').filter(Q(tipo__id__in=tipos, entidad__id__in=entidades), estado=1, periodo=periodo).order_by('-estado_actual__valord', 'estado_actual__valorb').annotate(
                    num_sol=Count('estado_actual'),
                    orden=Value(2, output_field=IntegerField())
                    )
            info_extra = [{'solicitudes': '', 'nombre': 'Todos', 'codigo': 'Tod_Cre', 'orden' : 1}]

        return Response({'general': data, 'extra': info_extra})

def convertir(data):
    resp = '-1111,'
    for d in data:
        resp = resp + str(d['relacion__id']) + ','
    return resp.rstrip(',')

class ObtenerCredito(generics.ListAPIView):
    serializer_class = CreditoSerializerList
    queryset = Credito.objects.filter(estado = 1)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    

class ObtenerEstados(generics.ListAPIView):
    serializer_class = EstadoSerializerList
    queryset = Estado.objects.filter(estado = 1)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['credito']

class ObtenerAdjuntos(generics.ListAPIView):
    serializer_class = AdjuntoSerializerList
    queryset = Adjunto.objects.filter(estado = 1)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['credito']

class ObtenerPagos(generics.ListAPIView):
    serializer_class = PagosSerializerList
    queryset = Solicitud.objects.filter(estado = 1)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['credito']

class GuardarEncuesta(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = EncuestaSerializer(data=request.data)
        if serializer.is_valid():
            experiencia = serializer.validated_data.get('experiencia', '')
            aspectos_a_mejorar = serializer.validated_data.get('aspectos_a_mejorar', '')
            comentario = serializer.validated_data.get('comentario', '')
            # Imprimir los datos que se van a guardar
            print('Datos a guardar:')
            print(f'Experiencia: {experiencia}')
            print(f'Aspectos a mejorar: {aspectos_a_mejorar}')
            print(f'Comentario: {comentario}')
            try:
                updated_count = Credito.objects.filter(estado_encuesta="1").update(
                    experiencia=experiencia,
                    aspectos_a_mejorar=aspectos_a_mejorar,
                    comentario=comentario,
                    estado_encuesta="0"
                )
                if updated_count > 0:
                    return Response({'message': 'Encuesta guardada exitosamente'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Ya realizaste esta encuesta'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Datos inválidos', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ObtenerEncuesta(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            encuesta = Credito.objects.get(estado_encuesta=0)
            serializer = EncuestaDetailSerializer(encuesta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Credito.DoesNotExist:
            return Response({'message': 'El estudiante no ha realizado la encuesta'}, status=status.HTTP_404_NOT_FOUND)   
        
def validarEstadoSiguiente(credito, estado_nue):
    try:
        estado = Valores_generica.objects.get(codigo=estado_nue)
    except (KeyError, Valores_generica.DoesNotExist):
        return {'mensaje': 'El estado no existe', 'sw': False}
    else:
        estados_disponibles = Permiso.objects.filter(principal=credito.tipo.id, estado=1).values_list('secundario__id')
        queryset = Permiso.objects.filter(principal = credito.estado_actual.id, secundario = estado.id, secundario__id__in = estados_disponibles, estado=1, secundario__estado = 1 , principal__estado = 1 ).order_by('secundario__nombre')
        if (queryset):
            return {'mensaje': 'Estado Valido', 'sw': True, 'estado' : estado}
        return {'mensaje': 'Estado No Valido', 'sw': False}
               
class GestionarCredito(generics.CreateAPIView):
    def create(self, request, pk, *args, **kwargs):
        #Antes de proceder a crear el credito se debe validar el archivo adjunto
        if ("total" in request.data and int(request.data["total"]) > 0):
            for a in range(0, int(request.data["total"])):
                check_archivo = validar_archivo_general(request.FILES["archivo" + str(a)])
                if not check_archivo:
                    return Response({"titulo": "El archivo no es válido"}, status=status.HTTP_302_FOUND)

        try:
            credito = Credito.objects.get(pk=pk)
        except (KeyError, Credito.DoesNotExist):
            return Response({'titulo': 'el crédito no existe'},status=status.HTTP_302_FOUND)
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data["usuario_registro"] = usuario.id
            request.data._mutable = _mutable
            usuario_registro = Persona.objects.get(pk=usuario.id)
            estado_siguiente = request.data["estado"]
            motivo = request.data["motivo"]
            # motivo = request.data["motivo"].strip('"')
            # if motivo:
            #         motivo_json = json.loads(motivo)
            #         id_motivo = motivo_json['id']
            total = request.data["total"]
            entidad = request.data["entidad"]
            observaciones = request.data["observaciones"]
            archivos_correo = []
            valor_aprobado = request.data["valor_aprobado"] if request.data["valor_aprobado"] else 0
            mensaje = ''

            #se valida parametros para consulta de permiso
            estado_actual_id = credito.estado_actual.id if credito.estado_actual else None
            entidad_id = credito.entidad.id if credito.entidad else None
            tipo_id = credito.tipo.id if credito.tipo else None
            if(estado_siguiente):
                #se verifica que tenga los permisos asignados
                #permiso = Generica_per.objects.filter(Q(tipo = 6) | Q(tipo = 7) | Q(tipo = 16),Q(relacion = credito.estado_actual.id) | Q(relacion = credito.entidad.id) | Q(relacion = credito.tipo.id), persona = usuario.id, estado=1, relacion__estado = 1).values_list('relacion__nombre')
                filtros = Q(tipo=6) | Q(tipo=7) | Q(tipo=16)
                if estado_actual_id:
                    filtros |= Q(relacion=estado_actual_id)
                if entidad_id:
                    filtros |= Q(relacion=entidad_id)
                if tipo_id:
                    filtros |= Q(relacion=tipo_id)
                permiso = Generica_per.objects.filter(
                    filtros,
                    persona=usuario.id,
                    estado=1,
                    relacion__estado=1
                ).values_list('relacion__nombre', flat=True)
                codigo_solicitud_actual = None
                respuesta = request.data["respuesta"].strip('"')
                if respuesta:
                    respuesta_json = json.loads(respuesta)
                    codigo_solicitud_actual = respuesta_json['codigo']
                if(len(permiso) < 3 and not(usuario.perfil.codigo == 'Per_Adm')):
                    return Response({"titulo": "No cuenta con el permiso para realizar esta acción."},status=status.HTTP_302_FOUND,)
                if(estado_siguiente == 'Cre_Rec' and not(motivo)):
                    return Response({"titulo": "Seleccione Motivo del rechazo."},status=status.HTTP_302_FOUND,)
                if(estado_siguiente == 'Cre_Rech' and not(motivo) and credito.tipo.codigo == 'sol_pazsalvo'):
                    return Response({"titulo": "Seleccione Motivo del rechazo."},status=status.HTTP_302_FOUND,)
                if(credito.tipo.codigo == 'sol_lega' and not(entidad) and estado_siguiente == 'Cre_Ges'):
                    return Response({"titulo": "Seleccione Entidad Financiera."},status=status.HTTP_302_FOUND,)
                if(not(observaciones) and estado_siguiente == 'Cre_Pen'):
                    return Response({"titulo": "Escribir Observaciones."},status=status.HTTP_302_FOUND,)
                # if(estado_siguiente == 'Cre_Ace' and (not(valor_aprobado) or int(valor_aprobado) < 1)):
                #     return Response({"titulo": "Digite el valor aprobado."},status=status.HTTP_302_FOUND,)
                #se verifica que el estado siguiente sea valido
                valido = validarEstadoSiguiente(credito, estado_siguiente)
                if(valido['sw']):
                    #algunas validaciones previas
                    if (int(total) == 0 and valido['estado'].valorc == 'si' and codigo_solicitud_actual and codigo_solicitud_actual not in ('posee_cred', 'posee_salfav', 'noposee_cred', 'noposee_saldfav') and not respuesta):
                        return Response({"titulo": "Debe cargar los documentos para continuar."},status=status.HTTP_302_FOUND,)
                    #cuando el credito guarda el motivo
                    if(estado_siguiente == 'Cre_Rec'):
                        motivo = Valores_generica.objects.get(id=motivo)
                        mensaje = motivo.nombre
                        credito.motivo_negado = motivo
                    # guardar el valor aprobado cuando es aceptada
                    if(estado_siguiente == 'Cre_Ace'):
                        credito.valor_aprobado = valor_aprobado
                    # se asigna el gestor solo en el primer cambio de estado
                    if(credito.estado_actual.codigo == 'Cre_Env'):
                        credito.gestor = usuario_registro
                        credito.gestor_nombre = usuario_registro.usuario
                    # se agrega la fecha de finalizado
                    if(estado_siguiente == 'Cre_Car'):
                        credito.fecha_limite = datetime.datetime.now()
                        json_parse_resp = request.data["respuesta"]
                        if json_parse_resp:
                            resp_json = json.loads(json_parse_resp)
                            resp_valor = request.data.get("valor_respuesta", None)
                            credito.valor_solicitud_estado_finan = resp_valor if resp_valor else None
                            # resp_valor = request.data["valor_respuesta"]
                            # credito.valor_solicitud_estado_finan = resp_valor
                            id_solicitud_finan = resp_json['id']
                            estado_solicitud_financ = Valores_generica.objects.get(id=id_solicitud_finan)
                            credito.estado_solicitud_financ = estado_solicitud_financ 

                            if(not(resp_valor) and estado_siguiente == 'Cre_Car' and (resp_json['codigo'] != 'noposee_cred' and resp_json['codigo'] != 'noposee_saldfav')):
                                return Response({"titulo": "Escribir Valor."},status=status.HTTP_302_FOUND,)                   
                        
                    # se asigna la entidad de las legalizaciones
                    if(estado_siguiente == 'Cre_Ges' and credito.tipo.codigo == 'sol_lega'):
                        entidad = Valores_generica.objects.get(id=entidad)
                        credito.entidad = entidad
                    #se asigna la informacion
                    estado_siguiente = valido['estado']
                    credito.estado_actual = estado_siguiente
                    #SE CONFIGURA EL LOG DE ESTADO
                    estado = Estado(usuario_registro=usuario_registro, credito=credito, tipo_estado=estado_siguiente, mensaje=observaciones)
                    credito.save()
                    estado.save()
                    #si fue exitoso se guardan los documentos
                    if(int(total) > 0):
                        usuario_registro = Persona.objects.get(pk=usuario.id)
                        archivos_guardar = []
                        for a in range(0, int(total)):
                            nombre_archivo = request.FILES["archivo" + str(a)].name
                            archivo = request.data["archivo" + str(a)]
                            data = Adjunto(credito=credito,archivo=archivo,usuario_registro=usuario_registro,nombre_archivo = nombre_archivo)
                            archivos_guardar.append(data)
                        Adjunto.objects.bulk_create(archivos_guardar)
                        adjuntos = Adjunto.objects.filter(credito__id = credito.id).order_by('-fecha_registro')[:int(total)]
                        for adj in adjuntos:
                            archivos_correo.append( {'item': adj.nombre_archivo + ' - ', 'link' : servidor()+ 'media/' + str(adj.archivo)},)

                    #al final se notifica
                    correos = [] if(credito.estado_actual.codigo == 'Cre_Neg') else [credito.usuario_registro.correo]
                    mensaje_correo = mensaje if(credito.estado_actual.codigo == 'Cre_Rec') else observaciones
                    
                    if motivo:
                        motivo = Valores_generica.objects.filter(id=motivo).first() if isinstance(motivo, (str, int)) else motivo
                        if getattr(motivo, "codigo", "") == "otro_mot_rech":
                            mensaje_correo = observaciones
                    
                    
            
                    gestores = Persona.objects.filter(~Q(id = usuario.id),generica__relacion__id = credito.entidad.id ,generica__estado = 1, generica__tipo = 6 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.estado_actual.id ,generica__estado = 1, generica__tipo = 7 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.tipo.id ,generica__estado = 1, generica__tipo = 16 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.programa.id ,generica__estado = 1, generica__tipo = 36 ,generica__relacion__estado = 1, estado = 1).values('correo')
                    if not(gestores):
                        gestores = Persona.objects.filter(~Q(id = usuario.id),generica__relacion__id = credito.entidad.id ,generica__estado = 1, generica__tipo = 6 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.estado_actual.id ,generica__estado = 1, generica__tipo = 7 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.tipo.id ,generica__estado = 1, generica__tipo = 16 ,generica__relacion__estado = 1, estado = 1).values('correo')
                    for c in gestores:
                        correos.append(c['correo'])
                    enviarCorreoCredito(credito.estado_actual.codigo,correos, mensaje_correo ,credito, archivos_correo)
                    return Response({"titulo": "Crédito Gestionado"})
                return Response({"titulo": valido['mensaje']},status=status.HTTP_302_FOUND,)
            else:
                return Response({"titulo": "Seleccione estado siguiente."},status=status.HTTP_302_FOUND,)
               
class AdjuntarArchivos(generics.CreateAPIView):
    def create(self, request, pk, *args, **kwargs):
        #Antes de proceder a crear el credito se debe validar el archivo adjunto
        if ("total" in request.data and int(request.data["total"]) > 0):
            for a in range(0, int(request.data["total"])):
                check_archivo = validar_archivo_general(request.FILES["archivo" + str(a)])
                if not check_archivo:
                    return Response({"titulo": "El archivo no es válido"}, status=status.HTTP_302_FOUND)
        
        try:
            credito = Credito.objects.get(pk=pk)
        except (KeyError, Credito.DoesNotExist):
            return Response({'titulo': 'el crédito no existe'},status=status.HTTP_302_FOUND)
        else:
            try:
                estado_siguiente = Valores_generica.objects.get(codigo="Cre_Env")
            except (KeyError, Valores_generica.DoesNotExist):
                return Response({'titulo': 'el estado no existe'},status=status.HTTP_302_FOUND)
            else:
                (usuario, token) = JWTAuthentication().authenticate(request)
                total = request.data["total"]
                archivos_correo = []
                correos = []
                if(int(total) > 0):
                    request.data["usuario_registro"] = usuario.id
                    usuario_registro = Persona.objects.get(pk=usuario.id)
                    archivos_guardar = []
                    for a in range(0, int(total)):
                        nombre_archivo = request.FILES["archivo" + str(a)].name
                        archivo = request.data["archivo" + str(a)]
                        data = Adjunto(credito=credito,archivo=archivo,usuario_registro=usuario_registro,nombre_archivo = nombre_archivo)
                        archivos_guardar.append(data)
                    Adjunto.objects.bulk_create(archivos_guardar)

                    if credito.estado_actual.codigo == 'Cre_Pen':
                        # cambiando estado al cargar documentos pendientes si es pendiente doc
                        credito.estado_actual = estado_siguiente
                        estado = Estado(usuario_registro=usuario_registro, credito=credito, tipo_estado=estado_siguiente, mensaje='')
                        credito.save()
                        estado.save()
                    
                    if(usuario.id == credito.usuario_registro.id):
                        adjuntos = Adjunto.objects.filter(credito__id = credito.id).order_by('-fecha_registro')[:int(total)]
                        for adj in adjuntos:
                            archivos_correo.append( {'item': adj.nombre_archivo + ' - ', 'link' : servidor()+ 'media/' + str(adj.archivo)},)
                        gestores = Persona.objects.filter(generica__relacion__id = credito.entidad.id ,generica__estado = 1, generica__tipo = 6 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.estado_actual.id ,generica__estado = 1, generica__tipo = 7 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.tipo.id ,generica__estado = 1, generica__tipo = 16 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.programa.id ,generica__estado = 1, generica__tipo = 36 ,generica__relacion__estado = 1, estado = 1).values('correo')
                        if not(gestores):
                            gestores = Persona.objects.filter(generica__relacion__id = credito.entidad.id ,generica__estado = 1, generica__tipo = 6 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.estado_actual.id ,generica__estado = 1, generica__tipo = 7 ,generica__relacion__estado = 1, estado = 1).filter(generica__relacion__id = credito.tipo.id ,generica__estado = 1, generica__tipo = 16 ,generica__relacion__estado = 1, estado = 1).values('correo')
                        for c in gestores:
                            correos.append(c['correo'])
                        enviarCorreoCredito('Adj', correos, '', credito, archivos_correo)
                    return Response({"titulo": "Documentos Cargados."})
                else:
                    return Response({"titulo": "Seleccione Adjuntos."},status=status.HTTP_302_FOUND,)


class ListarGestores(viewsets.ViewSet):
    def list(self, request):
        perfiles = Permiso.objects.filter(~Q(principal__codigo = 'Per_Adm'),secundario__generica = 10, principal__generica = 3, secundario__codigo = 'creditos_adm_act',  estado = 1, secundario__estado = 1 ,principal__estado = 1).values_list('principal__codigo')
        queryset = Persona.objects.filter(generica__relacion__codigo__in = perfiles, generica__estado = 1, generica__tipo = 1, estado = 1, generica__relacion__estado = 1).annotate(total=Count('id'))
        serializer = PersonaSerializerList(queryset, many=True)
        return Response(serializer.data)


@api_view(["POST"])
def validarPromedios(request):
    programa = Valores_generica.objects.filter(id=request.data["programa"])
    periodo = Valores_generica.objects.filter(codigo='Per_Cre')
    if(not(periodo) or not(programa)):
        return Response({'titulo' : 'No hay ningún periodo activo o el programa no existe'},status=status.HTTP_302_FOUND,) 
    (usuario, token) = JWTAuthentication().authenticate(request)
    acumulado = comprobar_promedio_acumulado(usuario.identificacion,programa[0].codigo)
    nivel = comprobar_promedio_nivel(usuario.identificacion,programa[0].codigo)
    # acumulado = 0
    # nivel = 0
    return Response({'promedio_nivel' : nivel[0] if nivel else 0, 'promedio_acumulado' : acumulado[0] if acumulado else 0, 'titulo' : 'Datos cargados.'})

class ObtenerPeriodos(viewsets.ViewSet):
    def list(self, request):
        periodos = Credito.objects.order_by().values('periodo').distinct()
        return Response(periodos)

def enviarCorreoCredito(estado, correos, mensaje = '', credito = {}, adjuntos=[]):
    tipo_adjunto = 1
    context = ''
    if correos:
        if(estado == 'Cre_Env'):
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
                        "mensaje" : "Su solicitud fue enviada con éxito, en estos momentos esta siendo revisada por un asesor.",
                        "clase" : "normal",
                    },
                    {
                        'mensaje':'Puedes ingresar a EMMA para verificar la información: ',
                        'nombre':'emma.cuc.edu.co',
                        'url' : 'https://emma.cuc.edu.co/',
                        "clase": "link",
                    },
                ]
            }
        elif(estado == 'Cre_Rec'):
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
                        "mensaje" : "Apreciado estudiante Unicosta, en vista de que su solicitud no fue aprobada, la universidad le ofrece otros medios de financiamiento; estamos prestos a ayudarle." if credito.tipo.codigo == 'sol_cred' else "Se informa que su solicitud de {} ha sido rechazada por lo siguiente : ".format(credito.tipo.nombre.lower()),
                        "clase" : "normal",
                    },
                    {
                        "mensaje" : "Motivo : " + mensaje,
                        "clase" : "normal",
                    },
                    {
                        'mensaje':'Coméntenos tu caso, para orientarle de la mejor manera. Puedes ingresar a EMMA para verificar la información: ',
                        'nombre':'emma.cuc.edu.co',
                        'url' : 'https://emma.cuc.edu.co/',
                        "clase": "link",
                    },
                ]
            }
        elif(estado == 'Cre_Pen'):
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
                        "mensaje" : "Se informa que su solicitud se encuentra en el estado Pendiente DOC. Observaciones : " + mensaje,
                        "clase" : "normal",
                    },
                    {
                        "mensaje": "Recuerde que en la solicitud ya creada puede cargar los documentos faltantes, en la opción Mis Documentos. Al realizar un ajuste en su solicitud, a partir de la fecha volverá a trascurrir 48 horas para que esta sea finalizada.",
                        "clase": "normal",
                    },
                    {
                        "mensaje": "Puedes ingresar a EMMA para verificar la información: ",
                        "nombre": "emma.cuc.edu.co",
                        "url": "https://emma.cuc.edu.co/",
                        "clase": "link",
                    },
                ]
            }
        elif(estado == 'Adj'):
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
                        "mensaje" : "Se han cargado algunos documentos al siguiente proceso: ",
                        "clase" : "normal",
                    },
                    {
                        "mensaje" : 
                        [
                            {
                                'item':'Estudiante : ' + credito.usuario_registro.primer_nombre + ' ' + credito.usuario_registro.primer_apellido, 
                            },
                            {
                                'item':'Telefono : ' + str(credito.usuario_registro.telefono) 
                            },
                            {
                                'item':'Celular : ' + str(credito.usuario_registro.celular) 
                            },
                            {
                                'item':'Tipo : ' + credito.tipo.nombre
                            },
                            {
                                'item':'Entidad Financiera : ' + credito.entidad.nombre
                            },
                            {
                                'item':'Categoria : ' + (('Nuevo' if credito.categoria == '1' else 'Renovacion') if credito.categoria != '-1' else 'Legalización')
                            },
                            {
                                'item':'Estado Actual : ' + credito.estado_actual.nombre
                            },
                           
                        ] if (credito.tipo.codigo == 'sol_cred' or credito.tipo.codigo == 'sol_lega') else 
                        [
                            {
                                'item':'Estudiante : ' + credito.usuario_registro.primer_nombre + ' ' + credito.usuario_registro.primer_apellido, 
                            }, 
                            {
                                'item':'Telefono : ' + str(credito.usuario_registro.telefono) 
                            },
                            {
                                'item':'Celular : ' + str(credito.usuario_registro.celular) 
                            },
                            {
                                'item':'Tipo : ' + credito.tipo.nombre
                            },
                            {
                                'item':'Estado Actual : ' + credito.estado_actual.nombre
                            },
                            {
                                'item':'Programa : ' + credito.programa.nombre
                            }
                        ],
                        "clase" : "lista",
                    },
                    {
                        "mensaje" : "Documentos cargados:" if(adjuntos) else '',
                        "clase" : "normal",
                    },
                    {
                        "mensaje" : adjuntos,
                        "clase": "lista",
                    },
                    {
                        'mensaje':'Puedes ingresar a EMMA para verificar la información: ',
                        'nombre':'emma.cuc.edu.co',
                        'url' : 'https://emma.cuc.edu.co/',
                        "clase": "link",
                    },
                ]
            }
        elif (credito.tipo.codigo == 'sol_conestfin' and estado == 'Cre_Car'):
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
                        "mensaje" : "Su solicitud se encuentra '" + credito.estado_actual.nombre + "'. A continuación  se relaciona toda la información de su proceso: ",
                        "clase" : "normal",
                    },
                    {
                        "mensaje" : 
                        [ 
                            {
                                'item':'Estudiante : ' + credito.usuario_registro.primer_nombre + ' ' + credito.usuario_registro.primer_apellido, 
                            },
                            {
                                'item':'Telefono : ' + str(credito.usuario_registro.telefono) 
                            },
                            {
                                'item':'Celular : ' + str(credito.usuario_registro.celular) 
                            },
                            {
                                'item':'Tipo : ' + credito.tipo.nombre
                            },
                            {
                                'item': 'Estado Financiero : ' + credito.estado_solicitud_financ.nombre + 
                                ((' - ' + "{:,}".format(float(credito.valor_solicitud_estado_finan))) if credito.estado_solicitud_financ.codigo == 'posee_cred' or credito.estado_solicitud_financ.codigo == 'posee_salfav' else 
                                ((' - ' + str(credito.valor_solicitud_estado_finan)) if credito.valor_solicitud_estado_finan else ''))
                            },
                            {
                                'item':'Estado Actual : ' + credito.estado_actual.nombre
                            },
                           
                        ],
                        
                        "clase" : "lista",
                    },
                    {
                        "mensaje" : "Documentos cargados:" if(adjuntos) else '',
                        "clase" : "normal",
                    },
                    {
                        "mensaje" : adjuntos,
                        "clase": "lista",
                    },
                    {
                        'mensaje':'Puedes ingresar a EMMA para verificar la información: ',
                        'nombre':'emma.cuc.edu.co',
                        'url' : 'https://emma.cuc.edu.co/',
                        "clase": "link",
                    },
                ]
            }           
        else:
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
                        "mensaje" : "Su solicitud se encuentra '" + credito.estado_actual.nombre + "'. A continuación  se relaciona toda la información de su proceso: ",
                        "clase" : "normal",
                    },
                    {
                        "mensaje" : 
                        [
                            {
                                'item':'Estudiante : ' + credito.usuario_registro.primer_nombre + ' ' + credito.usuario_registro.primer_apellido, 
                            },
                            {
                                'item':'Telefono : ' + str(credito.usuario_registro.telefono) 
                            },
                            {
                                'item':'Celular : ' + str(credito.usuario_registro.celular) 
                            },
                            {
                                'item':'Tipo : ' + credito.tipo.nombre
                            },
                            {
                                'item':'Entidad Financiera : ' + credito.entidad.nombre
                            },
                            {
                                'item':'Categoria : ' + (('Nuevo' if credito.categoria == '1' else 'Renovacion') if credito.categoria != '-1' else 'Legalización')
                            },
                            {
                                'item':'Estado Actual : ' + credito.estado_actual.nombre
                            },
                           
                        ] if (credito.tipo.codigo == 'sol_cred' or credito.tipo.codigo == 'sol_lega') else 
                        [
                            {
                                'item':'Estudiante : ' + credito.usuario_registro.primer_nombre + ' ' + credito.usuario_registro.primer_apellido, 
                            }, 
                            {
                                'item':'Telefono : ' + str(credito.usuario_registro.telefono) 
                            },
                            {
                                'item':'Celular : ' + str(credito.usuario_registro.celular) 
                            },
                            {
                                'item':'Tipo : ' + credito.tipo.nombre
                            },
                            {
                                'item':'Estado Actual : ' + credito.estado_actual.nombre
                            },
                            {
                                'item':'Programa : ' + credito.programa.nombre
                            }
                        ]                                     
                        ,
                        "clase" : "lista",
                    },
                    {
                        "mensaje" : "Documentos cargados:" if(adjuntos) else '',
                        "clase" : "normal",
                    },
                    {
                        "mensaje" : adjuntos,
                        "clase": "lista",
                    },
                    {
                        'mensaje':'Puedes ingresar a EMMA para verificar la información: ',
                        'nombre':'emma.cuc.edu.co',
                        'url' : 'https://emma.cuc.edu.co/',
                        "clase": "link",
                    },
                ]
            }           

        if(context):
            template = loader.get_template("correos/plantilla.html")
            html_content = template.render(context)   
            buscar_correo = Permiso.objects.filter(principal__codigo = 'creditos_adm_act', principal__generica = 10, secundario__generica = 58, estado = 1, secundario__estado = 1 ,principal__estado = 1)
            correo_envia = buscar_correo[0].secundario.codigo if buscar_correo else "Cor_Emma"
            EnviarCorreo(correos, html_content, "Proceso Financiero", [], 0, correo_envia)
            return True
    return False
