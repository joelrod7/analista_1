from apps.personas.api.serializers import PersonaSerializer
from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
import datetime
import calendar
import re
from xhtml2pdf import pisa
from django_filters import rest_framework as filters
from django.shortcuts import _get_queryset
from urllib.parse import urlparse
import pymysql.cursors
import openpyxl
from decouple import config
import requests

def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'usuario': PersonaSerializer(user, context={'request': request}).data
    }


def mostrar_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def descargar_pdf_servido(data="""Hello <b>World</b><br/><img src="img/test.jpg"/>""",dest="Desktop/test.pdf"):
    file = open(dest, "w+b")
    pdf = pisa.CreatePDF(StringIO(data),dest=file)
    if pdf.err:
        return False
    else:
        return True

def sumar_mes(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def validarCampos(campos = []):
    for c in campos:
        if not(c["valor"]):
            return {"sw" : -1, "campo" : c["campo"] ,"mensaje" : "El campo " + c["campo"] + " es obligatorio"}
        if(c["tipo"] == 'numero'):
            sw = validarNumero(c["valor"])
            if(not(sw)):
                return {"sw" : -2, "campo" : c["campo"],"mensaje" : "El campo " + c["campo"] + " debe ser un numero"}
        if(c["tipo"] == 'correo'):
            sw = validarCorreo(c["valor"])
            if(not(sw)):
                return {"sw" : -2, "campo" : c["campo"],"mensaje" : "El campo " + c["campo"] + " no es valido"}
    return  {"sw" : 1}


def validarCorreo(correo):  
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,correo)):  
        return True  
    else:  
        return False


def validarNumero(n):
    try:
        val = int(n)
    except ValueError:
        try:
            val = float(n)
        except ValueError:
            return False
    return True


def servidor():
    return 'https://backend.cuc.edu.co/'


class ListaFiltros(filters.Filter):
    def filter(self,qs,valores):
        if valores not in (None,''):
            filtros = [(v) for v in valores.split(',')]
            return qs.filter(**{'%s__%s'%(self.field_name, self.lookup_expr):filtros})
        return qs

def vistaWeb():
    return 'https://emma.cuc.edu.co/'

def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except:
        return None


def validacion_evaluacion_docente(identificacion):
    # Conexion a la BD
    try:
        connection = pymysql.connect(host='10.0.0.45',
                                    user='emma',
                                    password='emma#2021',
                                    database='eval',
                                    cursorclass=pymysql.cursors.DictCursor)
    except Exception:
        connection = None

    if(connection):
        with connection:
            with connection.cursor() as cursor:
                sql = '''SELECT datos.Nombres, datos.Usuario, datos.Email, datos.Documento, datos.id_tercero,
                            IF(SUM(datos.valor) > 0 , 'EN CURSO','FINALIZADO') Estado_Evaluacion
                        FROM
                        (SELECT CONCAT(PrimerNombre,' ',SegundoNombre,' ',PrimerApellido,' ',SegundoApellido) Nombres, Usuario, Email ,Documento, id_tercero,
                        CASE
                            when ee.estado_eap LIKE 'FINALIZADO' THEN 0
                            when ee.estado_eap LIKE 'EN CURSO' THEN 1
                            ELSE 1
                        END valor
                        FROM extidi_usuarios eu
                            JOIN eval_grupo_estudiantes_materias egem ON egem.usuarios_id = eu.id
                            LEFT JOIN eval_evaluacion ee ON ee.grupo_materias_id_evaluado = egem.grupo_materias_id AND ee.usuarios_usuarioevaluador_id = eu.id
                        WHERE eu.IdGruposUsuario = 5
                        AND eu.estado = 1
                        AND eu.Documento LIKE '%{}%') datos
                        GROUP BY datos.documento'''.format(identificacion)
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
    else:
        return None


def validar_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False        

def excel_to_rows_array(url_excel):
    # Define variable to load the dataframe book
    book = openpyxl.load_workbook(url_excel)

    # Define variable to read sheet
    sheet = book.active

    # Define rows to sheet
    rows = sheet.rows

    # Define headers of sheet
    headers = [cell.value for cell in next(rows)]

    # Define variable to save data
    data = []


    for row in rows:
        element = {}
        for title, cell in zip(headers, row):
            element[title] = cell.value
        data.append(element)
    
    return data

def obtenerResultadoEvalDocente(documento):
    API = "https://evaluacionprofesores.cuc.edu.co:4000/external/consultaEstudiante"
    APP_ID = config("EVADOC_APP_ID")
    KEY_ID = config("EVADOC_KEY_ID")

    data = {
        'documento': documento,
        'app_id': APP_ID,
        'token': KEY_ID
    }

    return requests.post(API, data=data, headers=[])  

# Funcion que valida si un archivo esta dentro la lista de extensiones no permitidas
def validar_archivo_general(archivo):
    extensiones_no_permitidas = ['php', 'py', 'sh', 'bat', 'ps1', 'ps', 'pl', 'js', 'yml', 'json', 'exe', 'txt']
    extension = archivo.name.split('.')[-1].lower()
    if extension in extensiones_no_permitidas:
        return False
    
    # Si el archivo es de tipo txt o csv, se valida su contenido
    if extension == 'txt':
        contenido = archivo.read().decode('utf-8')

        # Definir patrones de código malicioso
        patrones_codigo = [
            r'\bif\b',            # Palabra clave 'if'
            r'\belse\b',          # Palabra clave 'else'
            r'\bfor\b',           # Bucle 'for'
            r'\bwhile\b',         # Bucle 'while'
            r'\bfunction\b',      # Función en JavaScript o PHP
            r'\bdef\b',           # Función en Python
            r'\bclass\b',         # Clases en varios lenguajes
            r'\bvar\b',           # Variable en JavaScript o PHP
            r'\blet\b',           # Variable en JavaScript
            r'\bconst\b',         # Constantes en varios lenguajes
            r'==',                # Operador de comparación
            r'!=',                # Operador de desigualdad
            r'\bprint\b',         # Función print (Python, PHP)
            r'\becho\b',          # Echo en PHP
            r'<\?php',            # Código PHP embebido
            r'\bimport\b',        # Importación de módulos
            r'\brequire\b',       # Importación de módulos
            r'\bfrom\b',          # Importación de módulos
            r'\breturn\b',        # Palabra clave 'return'
            r'\btry\b',           # Palabra clave 'try'
            r'\bcatch\b',         # Palabra clave 'catch'
            r'\bthrow\b',         # Palabra clave 'throw'
            r'\bfinally\b',       # Palabra clave 'finally'
            r'\basync\b',         # Palabra clave 'async'
            r'\bawait\b',         # Palabra clave 'await'
            r'\bnew\b',           # Palabra clave 'new'
            r'\bdelete\b',        # Palabra clave 'delete'
            r'\bthis\b',          # Palabra clave 'this'
            r'\bself\b',          # Palabra clave 'self'
        ]

        # Verificar si el contenido del archivo coincide con algún patrón
        for patron in patrones_codigo:
            if re.search(patron, contenido, re.IGNORECASE):
                return False
    
    return True
