from rest_framework import permissions, authentication
from apps.genericas.models import Valores_generica, Permiso
import re 

def validarRuta1( ruta, auxruta):
    return ruta.startswith(auxruta)

def validarRuta2( ruta, expresion):
    patron = re.compile(r''+expresion) 
    return True if ( not patron.match(ruta) == None ) else False

def validarRuta(ruta , rutaActual):
    if (ruta.valora == '2'):
        return validarRuta2(
            rutaActual,
            ruta.valorb
        )
    elif (ruta.valora == '1'):
        return rutaActual == ruta.nombre
    else:
        return False

class HavePermission(permissions.BasePermission):
    def has_permission(self, request, view):      
        rutas = Permiso.objects.filter(
            secundario = request.user.perfil,
            principal__generica_id = 60,
            estado = 1
        )
        ruta = request.build_absolute_uri().split('/api/v1.0/')[1].split('?')[0]
        for i in rutas:
            aux = validarRuta(i.principal, ruta)
            if  aux:
                return True
        return False
