from django.urls import path
from . import views
from .api.viewsets import GenericaListarPreUniversitario, ObtenerPermisosListarContenido,ObtenerValoresContenido,ObtenerEstadosProceso, BuscarValores, GenericaListar, GenericasCrear, GenericasDetalle,ValoresGenericaListar, ValoresGenericaCrear, ValoresGenericasDetalle, ValoresGenericaEliminar, GenericaListarTodo, ValoresPermisosListar, GenericasValoresPermiso, PermisosGenericaCrear, PermisoGenericaEliminar, CheckService

urlpatterns = [
    path('genericas', GenericaListar.as_view(), name=None),
    path('genericas/valores/buscar', BuscarValores.as_view(), name=None),
    path('genericas/crear', GenericasCrear.as_view(), name=None),
    path('genericas/<int:pk>', GenericasDetalle.as_view(), name=None),
    path('generica/<int:pk>/valores', ValoresGenericaListar.as_view({'get': 'list'}), name=None),
    path('valores', GenericaListarTodo.as_view(), name=None),
    path('valores/crear', ValoresGenericaCrear.as_view(), name=None),
    path('valores/<int:pk>', ValoresGenericasDetalle.as_view(), name=None),
    path('valores/<int:pk>/eliminar', ValoresGenericaEliminar.as_view(), name=None),
    path('valores/permisos', ValoresPermisosListar.as_view(), name=None),
    path('valores/<int:pk>/permisos/valores', GenericasValoresPermiso.as_view(), name=None),
    path('estados/<int:pk>', ObtenerEstadosProceso.as_view(), name=None),
    path('genericas/valores/buscar/contenido/<str:buscar>', ObtenerValoresContenido.as_view(), name=None),
    path('genericas/permisos/buscar/contenido/<str:buscar>', ObtenerPermisosListarContenido.as_view(), name=None),
    path('permisos/crear', PermisosGenericaCrear.as_view(), name=None),
    path('permisos/<int:pk>/eliminar', PermisoGenericaEliminar.as_view(), name=None),

    path('genericas/preuniversitario/<str:buscar>',GenericaListarPreUniversitario.as_view({'get': 'list'}), name=None),
    path('check_service', CheckService, name=None),
]
