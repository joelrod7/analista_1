from django.urls import path
from .api.viewsets import EstadoSolicitudes, GuardarEncuesta,ObtenerEncuesta, ObtenerPeriodos,validarPromedios,AdjuntarArchivos,ListarGestores, GestionarCredito, ObtenerEstados,ObtenerAdjuntos,ObtenerPagos,ObtenerCredito,CreditoCrear, obtenerDetalleCredito, CreditosListar,CreditodirectoCrear

urlpatterns = [
    path('creditos/crear', CreditoCrear.as_view(), name=None),
    path('creditos/<int:pk>/detalle', obtenerDetalleCredito.as_view({'get': 'list'}), name=None),
    path('credito', ObtenerCredito.as_view(), name=None),
    path('credito/estados', ObtenerEstados.as_view(), name=None),
    path('credito/adjuntos', ObtenerAdjuntos.as_view(), name=None),
    path('credito/pagos', ObtenerPagos.as_view(), name=None),
    path('creditos/<int:tipo>', CreditosListar.as_view(), name=None),
    path('creditos/gestores', ListarGestores.as_view({'get': 'list'}), name=None),
    path('creditos/<int:pk>/gestionar', GestionarCredito.as_view(), name=None),
    path('creditos/<int:pk>/adjuntar', AdjuntarArchivos.as_view(), name=None),
    path('creditos/estudiante/promedios', validarPromedios, name=None),
    path("creditos/periodos", ObtenerPeriodos.as_view({'get': 'list'}), name=None),
    path("creditos/estados/<int:periodo>", EstadoSolicitudes.as_view({'get': 'list'}), name = None),
    path('creditos/directocrear', CreditodirectoCrear.as_view(), name=None),
    path('guardar-encuesta', GuardarEncuesta.as_view(), name='guardar_encuesta'),
    path('obtener-encuesta', ObtenerEncuesta.as_view(), name='obtener_encuesta'),
]

