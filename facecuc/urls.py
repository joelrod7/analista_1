from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
# from rest_framework_jwt.views import obtain_jwt_token

apiv1 = "api/v1.0/"

urlpatterns = [
    # path("admin/", admin.site.urls),
    path(apiv1, include("apps.genericas.urls")),
    path(apiv1, include("apps.personas.urls")),
    path(apiv1, include("apps.elecciones.urls")),
    path(apiv1, include("apps.practicas.urls")),
    path(apiv1, include("apps.inscripciones.urls")),
    path(apiv1, include("apps.internacionalizacion.urls")),
    path(apiv1, include("apps.grados.urls")),
    path(apiv1, include("apps.becas.urls")),
    path(apiv1, include("apps.matriculas.urls")),
    # path(apiv1, include("apps.movilidades.urls")),
    path(apiv1, include("apps.comentarios.urls")),
    path(apiv1, include("apps.portal.urls")),
    path(apiv1, include("apps.creditos.urls")),
    path(apiv1, include("apps.consultas.urls")),
    path(apiv1, include("apps.invitados.urls")),
    path(apiv1, include("apps.asistencia.urls")),
    path(apiv1, include("apps.reportes.urls")),
    path(apiv1, include("apps.retos.urls")),
    path(apiv1, include("apps.retoscuc.urls")),
    path(apiv1, include("apps.validaciones.urls")),
    path(apiv1, include("apps.rea.urls")),
    path(apiv1, include("apps.tutorias.urls")),
    path(apiv1, include("apps.consultoria.urls")),
    path(apiv1, include("apps.autodiagnostico.urls")),
    path(apiv1, include("apps.apiOva.urls")),
    path(apiv1, include("apps.reporteVac.urls")),
    path(apiv1, include("apps.integracionesAPI.urls")),
    path(apiv1, include("apps.invitadosVirtual.urls")),
    # path('token-auth', obtain_jwt_token),
    path(apiv1, include("apps.encuesta.urls")),
    path(apiv1, include("apps.investigacion.urls")),
    path(apiv1, include("apps.entrevistas.urls")),
    path(apiv1, include("apps.bloques.urls")),
    path(apiv1, include("apps.promocion.urls")),
    path(apiv1, include("apps.inscripciones_posgrado.urls")),
    path(apiv1, include("apps.cursoformacion.urls")),
    path(apiv1, include("apps.atencion.urls")),
    path(apiv1, include("apps.centro.urls")),
    path(apiv1, include("apps.sisef.urls")),
    path(apiv1, include("apps.autogestion_estudiantil.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
