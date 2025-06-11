from rest_framework import generics, status, viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Value, IntegerField, Q
from django.template import loader
from django.conf import settings
import os
from ..models import Generica, Valores_generica, Permiso
from ...personas.models import Persona
from .serializers import (
    GenericaSerializer,
    Valores_genericaSerializerList,
    Valores_genericaSerializer,
    PermisoSerializer,
    Valores_genericaPermisoSerializer,
    PermisoSerializerCreate,
    Valores_genericaSerializerListSimple
)
import datetime
from facecuc.microsoft import create_event, EnviarCorreo
from decouple import config
from rest_framework.decorators import api_view, action, permission_classes
from facecuc.utils import ListaFiltros
from django_filters import rest_framework as filters
from rest_framework_simplejwt.authentication import JWTAuthentication


# view genericas
class GenericaListar(generics.ListAPIView):
    queryset = Generica.objects.all().order_by('id')
    serializer_class = GenericaSerializer


class GenericasCrear(generics.CreateAPIView):
    queryset = Generica.objects.all()
    serializer_class = GenericaSerializer

    def create(self, request, *args, **kwargs):
        super(GenericasCrear, self).create(request, args, kwargs)
        return Response({"titulo": "Parametro Guardado"})


class GenericasDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Generica.objects.all()
    serializer_class = GenericaSerializer

    def retrieve(self, request, *args, **kwargs):
        super(GenericasDetalle, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"titulo": "Proceso Exitoso", "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        super(GenericasDetalle, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response({"titulo": "Parametro Modificado"})

    # def delete(self, request, *args, **kwargs):
    #     super(GenericasDetalle, self).delete(request, args, kwargs)
    #     return Response({"titulo": "Parametro Eliminado"})


# view valores
class GenericaListarTodo(generics.ListAPIView):
    queryset = Valores_generica.objects.all()
    serializer_class = Valores_genericaSerializerList


def validate_header(view_func):
    def wrapper(self, request, *args, **kwargs):
        expected_header = 'x_api_key'
        header_value = request.META.get(f'HTTP_{expected_header.upper()}')
        esperado = config("API_KEY_GENERICAS")

        if header_value is None or not header_value == esperado:
            return Response({'error': 'Acceso Denegado.'}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(self, request, *args, **kwargs)
    return wrapper


class ValoresGenericaListar(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    # @action(detail=True, methods=['GET'])
    # @validate_header
    def list(self, request, pk=None):
        queryset = Valores_generica.objects.filter(generica=pk, estado=1).order_by('nombre')
        serializer = Valores_genericaSerializerList(queryset, many=True)
        return Response(serializer.data)

class ValoresPermisosListar(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PermisoSerializer
    queryset = Permiso.objects.filter(estado=1,secundario__estado = 1 ,principal__estado = 1).select_related('secundario', 'principal', 'usuario_registro', 'usuario_elimino').order_by('secundario__nombre')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['principal__generica', 'principal', 'principal__codigo', 'secundario__generica', 'secundario__valora' , 'secundario__valorb', 'secundario__valorc', 'secundario__valori']

    # @validate_header
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

class GenericasValoresPermiso(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = Valores_genericaSerializer
    queryset = Valores_generica.objects.filter(estado = 1)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['generica', 'codigo', 'nombre', 'valora', 'valorb', 'valorc','valord']

    # @validate_header
    def list(self, request, pk):
        queryset = self.get_queryset()
        self.object_list = self.filter_queryset(queryset)
        valores =  self.object_list
        permisos = Permiso.objects.filter(principal=pk, estado=1)
        for valor in valores:
            setattr(valor, 'permiso', 0)
            for permiso in permisos:
                if valor.id == permiso.secundario.id:
                    setattr(valor, 'permiso', permiso.id)
        serializer = Valores_genericaPermisoSerializer(valores, many=True)
        return Response(serializer.data)

class ObtenerEstadosProceso(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PermisoSerializer
    queryset = Permiso.objects.filter(estado=1,secundario__estado = 1 ,principal__estado = 1, ).order_by('secundario__nombre')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['principal__generica','secundario__generica', 'principal']

    # @validate_header
    def list(self, request, pk):
        estados_disponibles = Permiso.objects.filter(principal=pk, estado=1, secundario__estado = 1 ,principal__estado = 1).values_list('secundario__id')
        queryset = self.get_queryset().filter(secundario__id__in = estados_disponibles)
        self.object_list = self.filter_queryset(queryset)
        valores =  self.object_list
        serializer = PermisoSerializer(valores, many=True)
        return Response(serializer.data)


class ValoresGenericaCrear(generics.CreateAPIView):
    queryset = Valores_generica.objects.all()
    serializer_class = Valores_genericaSerializer

    def create(self, request, *args, **kwargs):
        (usuario, token) = JWTAuthentication().authenticate(request)
        request.data._mutable = True
        request.data["usuario_registro"] = usuario.id
        if request.data['codigo']:
            valores = Valores_generica.objects.filter(codigo=request.data['codigo'])
            if len(valores) > 0:
                return Response(
                    {"titulo": "Ya existe un valor con el codigo ingresado."},
                    status=status.HTTP_302_FOUND
                )
        instance = super(ValoresGenericaCrear, self).create(request, args, kwargs)
        return Response({"titulo": "Valor Guardado", "valor_id": instance.data['id'] })

class PermisosGenericaCrear(generics.CreateAPIView):
    queryset = Permiso.objects.all()
    serializer_class = PermisoSerializerCreate

    def create(self, request, *args, **kwargs):
        (usuario, token) = JWTAuthentication().authenticate(request)
        request.data["usuario_registro"] = usuario.id
        super(PermisosGenericaCrear, self).create(request, args, kwargs)
        return Response({"Titulo": "Permiso Agregado"})

class ValoresGenericaEliminar(generics.UpdateAPIView):
    def update(self, request, pk):
        try:
            valores = Valores_generica.objects.get(pk=pk)
        except (KeyError, Valores_generica.DoesNotExist):
            return Response(
                {"titulo": "El valor no existe."}, status=status.HTTP_302_FOUND
            )
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            valores.estado = 0
            valores.fecha_elimino = datetime.datetime.now()
            valores.usuario_elimino = Persona.objects.get(pk=usuario.id)
            valores.save()
            return Response({"titulo": "Valor Eliminado"})

class PermisoGenericaEliminar(generics.UpdateAPIView):
    def update(self, request, pk):
        try:
            permisos = Permiso.objects.get(pk=pk)
        except (KeyError, Permiso.DoesNotExist):
            return Response(
                {"titulo": "El permiso no existe."}, status=status.HTTP_302_FOUND
            )
        else:
            (usuario, token) = JWTAuthentication().authenticate(request)
            permisos.estado = 0
            permisos.fecha_elimino = datetime.datetime.now()
            permisos.usuario_elimino = Persona.objects.get(pk=usuario.id)
            permisos.save()
            return Response({"titulo": "Valor Eliminado"})


class ValoresGenericasDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Valores_generica.objects.all()
    serializer_class = Valores_genericaSerializerList

    def retrieve(self, request, *args, **kwargs):
        super(ValoresGenericasDetalle, self).retrieve(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response = {"titulo": "Proceso Exitoso", "result": data}
        return Response(response)

    def patch(self, request, *args, **kwargs):
        (usuario, token) = JWTAuthentication().authenticate(request)
        request.data._mutable = True
        if 'archivo' in request.data.keys():
            if not request.data['archivo'] or request.data['archivo'] == 'undefined': request.data.pop('archivo')
        if 'codigo' in request.data.keys() and request.data['codigo']:
            valores = Valores_generica.objects.filter(codigo=request.data['codigo'])
            if len(valores) > 0 and kwargs['pk'] != valores[0].id:
                return Response(
                    {"titulo": "Ya existe un valor con el codigo ingresado."},
                    status=status.HTTP_302_FOUND
                )
        request.data['usuario_elimino'] = usuario.id
        super(ValoresGenericasDetalle, self).patch(request, args, kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response({"titulo": "Valor Modificado"})

    # def delete(self, request, *args, **kwargs):
    #     super(ValoresGenericasDetalle, self).delete(request, args, kwargs)
    #     return Response({"titulo": "Valor Eliminado"})

# class BuscarValores(generics.ListAPIView):
#     permission_classes = (permissions.AllowAny,)
#     queryset = Valores_generica.objects.filter(estado=1).order_by('nombre')
#     serializer_class = Valores_genericaSerializerList
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['generica', 'codigo', 'nombre', 'valora', 'valorb', 'valorc', 'valore', 'estado', 'valori', 'valorf']

class FiltrosValores(filters.FilterSet):   
    valora = filters.CharFilter(method='filter_valora')
    codigos_in = ListaFiltros(field_name='codigo',lookup_expr='in')
    valorc_in = ListaFiltros(field_name='valorc',lookup_expr='in')

    def filter_valora(self, queryset, name, value):
        # Mapeo de los códigos de solicitud
        mapping = {
            'sol_cred': 'credito',
            'sol_lega': 'legalizacion',
            'sol_desc': 'descongelamiento',
            'sol_cong': 'congelamiento',
            'sol_dev': 'devoluciones'
        }
        # Verificar si el valor está en el mapeo, si no devolver el queryset sin cambios
        valora_value = mapping.get(value, value)


        if valora_value in ['descongelamiento', 'congelamiento', 'devoluciones']:
            return queryset.filter(
                Q(valora__icontains=valora_value) | Q(valora__icontains='otro_mot_rech')
            )

        return queryset.filter(valora__icontains=valora_value)
        
        #return queryset.filter(valora=valora_value)

    class Meta:
        model = Valores_generica
        fields = ['generica', 'codigo', 'nombre', 'valora', 'valorb', 'valorc', 'valore', 'estado', 'valori', 'valorf', 'codigos_in', 'valorc_in']


class BuscarValores(generics.ListAPIView): 
    permission_classes = (permissions.AllowAny,)
    queryset = Valores_generica.objects.filter(estado=1).order_by('nombre')
    serializer_class = Valores_genericaSerializerList
    # codigos_in = ListaFiltros(field_name='codigo',lookup_expr='in')
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['generica', 'codigo', 'nombre', 'valora', 'valorb', 'valorc', 'valore', 'estado', 'valori', 'valorf', 'codigos_in']
    filterset_class = FiltrosValores


class ObtenerValoresContenido(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = Valores_genericaSerializerList
    queryset = Valores_generica.objects.filter(estado=1).order_by('nombre')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['generica','valora']

    # @validate_header
    def list(self, request, buscar):
        # queryset = self.get_queryset().filter(nombre__contains = buscar)
        queryset = self.get_queryset().filter(Q(nombre__contains = buscar) | Q(valora__contains = buscar) | Q(codigo__contains = buscar)) # buscar tanto en nombre como en valora y codigo
        self.object_list = self.filter_queryset(queryset)
        valores =  self.object_list
        serializer = Valores_genericaSerializerList(valores, many=True)
        return Response(serializer.data)


class ObtenerPermisosListarContenido(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PermisoSerializer
    queryset = Permiso.objects.filter(estado=1,secundario__estado = 1 ,principal__estado = 1).order_by('secundario__nombre')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['principal__generica', 'principal', 'secundario__generica', 'secundario__valora' , 'secundario__valorb']

    # @validate_header
    def list(self, request, buscar):
        queryset = self.get_queryset().filter(principal__nombre__contains = buscar)
        self.object_list = self.filter_queryset(queryset)
        valores =  self.object_list
        serializer = PermisoSerializer(valores, many=True)
        return Response(serializer.data)


# consultaa de genericas en el modulo preuniversitario agregado por Juan Caceres
class GenericaListarPreUniversitario(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    # @validate_header
    def list(self, request, buscar):
        dato=buscar.split(',')
        queryset = Generica.objects.filter(id__in=dato)
        serializer = GenericaSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def CheckService(req):
    return Response({"titulo": "Ok"} , status=status.HTTP_200_OK)

