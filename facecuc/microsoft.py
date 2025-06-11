from django.template import loader
from apps.genericas.models import Valores_generica
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os.path
from email.mime.multipart import MIMEMultipart
from ldap3 import Server, Connection, ALL, AUTO_BIND_TLS_BEFORE_BIND, AUTO_BIND_NO_TLS
from ldap3.core.exceptions import LDAPBindError
from decouple import config
import requests
import json
import msal
import base64
import logging

#autenticacion
def get_token():
  auth = requests.get('https://login.microsoftonline.com/0507e5ce-0f95-49aa-abde-c90dcdedbd12/oauth2/token', data = {
    'client_id' : '02a9efb2-f64c-408b-b846-7868e9e764fa',
    'client_secret' : 'E8HOt26~29-kE9SUd4Q-pZzA2Kxz-L0a-6',
    'resource' : 'https://graph.microsoft.com',
    'grant_type' : 'client_credentials'
  });

  return auth.json()['access_token']

#obtener evento de usuario
def get_events(email):
  data = request.get('https://graph.microsoft.com/v1.0/users/{}/calendar/events'.format(email), headers = {
    'Authorization' : '{}'.format(get_token())
  })
  return data.json()

def create_event(email, subject, start_date, end_date, attendees, html_content, is_online=False, location=""):
  payload = {
    'subject': subject,
    'body': {
      'contentType': 'html',
      'content': html_content
    },
    "start": {
      "dateTime": "{}".format(start_date),
      "timeZone": "SA Pacific Standard Time"
    },
    "end": {
      "dateTime": "{}".format(end_date),
      "timeZone": "SA Pacific Standard Time"
    },
    "location":{
      "displayName": "{}".format(location)
    },
    "attendees": attendees,
    "isOnlineMeeting": is_online, 
    "onlineMeetingProvider": "teamsForBusiness"
  }

  main = requests.post('https://graph.microsoft.com/v1.0/users/{}/calendar/events'.format(email), headers = {
    'Authorization' : '{}'.format(get_token()),
    'Content-Type' : 'application/json'
  }, data = json.dumps(payload))

  # return main.status_code == requests.codes.ok
  return main.json()
  
def edit_event(email, event, start_date, end_date, html_content):
  payload = {
    'body': {
      'contentType': 'html',
      'content': html_content
    },
    "start": {
      "dateTime": "{}".format(start_date),
      "timeZone": "SA Pacific Standard Time"
    },
    "end": {
      "dateTime": "{}".format(end_date),
      "timeZone": "SA Pacific Standard Time"
    },
  }

  main = requests.patch('https://graph.microsoft.com/v1.0/users/{}/calendar/events/{}'.format(email, event), headers = {
    'Authorization' : '{}'.format(get_token()),
    'Content-Type' : 'application/json'
  }, data = json.dumps(payload))

  return main.json()

def delete_event(email, event):
  main = requests.delete('https://graph.microsoft.com/v1.0/users/{}/calendar/events/{}'.format(email, event), headers = {
    'Authorization' : '{}'.format(get_token())
  })
  
  return main.status_code

# Obtener la ruta absoluta al directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ajusta esta línea si el script no está en la raíz
# Ruta al archivo de logs dentro de la carpeta 'logs' en la raíz del proyecto
log_file_path = os.path.join(os.path.dirname(BASE_DIR), 'logs', 'email_errors.log')
# Crear el directorio de logs si no existe
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
# Configuración básica del logger
logging.basicConfig(
    filename=log_file_path,  # Nombre del archivo de log
    level=logging.ERROR,  # Nivel de log (ERROR para capturar solo errores)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de los mensajes de log
)

#ENVIO DE CORREOS
def EnviarCorreo(sendto, message, subject, files_location = [], typed_files = 0, codigo = 'Cor_Emma'):
    try:
        correo = Valores_generica.objects.get(codigo = codigo, estado=1)
    except (KeyError, Valores_generica.DoesNotExist):
        return ({"titulo": "El correo no existe."})
    else:
      smtp_server = "smtp.office365.com"
      port = 587  # For starttls
      sender_email = correo.nombre
      password = correo.valora
      server = None  # Inicializar server como None
      # Try to log in to server and send email
      try:
          # Create a secure SSL context
          context = ssl.create_default_context()
          server = smtplib.SMTP(smtp_server, port)
          server.ehlo()  # Can be omitted
          server.starttls(context=context)  # Secure the connection
          server.ehlo()  # Can be omitted
          server.login(sender_email, password)

          user = correo.nombre
          # TODO: Send email here
          msg = MIMEMultipart()
          msg["Subject"] = subject
          msg["From"] = user
          msg["To"] = ", ".join(sendto)
          msg.attach(MIMEText(message, 'html'))

          # Adjuntar archivos si los hay
          if files_location:
              for file in files_location:
                  if typed_files:
                      array_ext = str(file['db_name']).split(".")
                      ext = array_ext[len(array_ext) - 1]
                      filename = os.path.basename("{}{}".format(file['name'], "." + ext))
                      attachment = open(file['ruta'], "rb")
                  else:
                      filename = os.path.basename(file)
                      attachment = open(file, "rb")
                  
                  part = MIMEBase('application', 'octet-stream')
                  part.set_payload(attachment.read())
                  encoders.encode_base64(part)
                  part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                  # Attach the attachment to the MIMEMultipart object
                  msg.attach(part)
          # Enviar correo
          server.sendmail(user, sendto, msg.as_string())
      except Exception as e:
          # Print any error messages to stdout
          print(f"Error al enviar el correo: {e}")
          logging.error(f"Error al enviar el correo: {e}")
      finally:
          # Cerrar conexión SMTP solo si fue inicializada
          if server is not None:
            server.quit()

# LDAP config
def ValidarCredencialesLdap(user, password):
    server = Server('172.30.1.4', port=389)
    auto_bind = (AUTO_BIND_TLS_BEFORE_BIND or AUTO_BIND_NO_TLS)
    try:
        conn = Connection(server, user, password, auto_bind=auto_bind)
        return True
    except LDAPBindError as e:
        return False


def get_token_ms():
    app = msal.ConfidentialClientApplication(
        config("AZURE_CLIENT_ID"),
        authority=config("AZURE_AUTHORITY"),
        client_credential=config("AZURE_CLIENT_SECRET")
    )

    result = app.acquire_token_for_client(scopes=[config("AZURE_GRAPH_ENDPOINT1")])
    if "access_token" in result:
        return result["access_token"]
    else:
        # raise Exception("No access token found.")
        return None


def getPhotoMS(user_id):
    access_token = get_token_ms()
    photo_base64 = None
    cargo_ms = None
    # print(access_token)

    api_graph = config("AZURE_GRAPH_ENDPOINT2")
    endpoint = f"{api_graph}/users/{user_id}/photo/$value"
    endpoint_cargo = f"{api_graph}/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        photo_base64 = base64.b64encode(response.content).decode('utf-8')

    response2 = requests.get(endpoint_cargo, headers=headers)
    if response2.status_code == 200:
      cargo_ms= response2.json()['jobTitle'] if response2.json()['jobTitle'] else None
    
    return {'foto': photo_base64, 'cargo': cargo_ms}
