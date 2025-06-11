from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def plantilla(request):
    template = loader.get_template('correos/plantilla.html')
    # CLASES : titulo, normal, importante, lista
    context = { 
      "mensajes" :  [
          {
            "mensaje" : "¡Genial!",
            "clase": "titulo",
          },
          {
            "mensaje" : "Adjunto encontraras volante de pago de inscripción que puedes pagar en los siguientes medios:",
            "clase": "normal",
          },
          {
            "mensaje" : [
              {'item':'Bancos grupo AVAL: Banco de Bogotá, Occidente o Av Villas.'},
              {'item':'Caja de la universidad ubicada en el bloque 11 piso 1.'},
              # {'item':'Pago en línea.', 'link' : 'https://admisiones.cuc.edu.co/sgacampus/inscripciones.jsp#home'},
              {
                'mensaje':'',
                'nombre': 'prueba',
                'url' : 'https://emma.cuc.edu.co/',
              }
              ],
            "clase": "lista",
          },
          {
            'mensaje':'Puede ingresar al siguiente link para verificar la información:',
            'nombre':'emma.cuc.edu.co',
            'url' : 'https://emma.cuc.edu.co/',
            "clase": "link",
          },
      ]
    }
    return HttpResponse(template.render(context, request))
