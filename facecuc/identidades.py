from django.db.models import query
import pymysql
from django.utils.encoding import smart_str
from decouple import config

IDENTIDADES_USER = config("IDENTIDADES_USER")
IDENTIDADES_PASS = config("IDENTIDADES_PASS")
IDENTIDADES_HOST = config("IDENTIDADES_HOST")
IDENTIDADES_DB = config("IDENTIDADES_DB")


# linea para error con oracle (local)
# cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_3")

# CONEXION A SICUC
def connect_sql():
  conn = pymysql.connect(host=IDENTIDADES_HOST, port=3306, user=IDENTIDADES_USER, password=IDENTIDADES_PASS, database=IDENTIDADES_DB)
  c = conn.cursor()
  return c, conn

def consultaIdentidades(identificacion):
  query = "SELECT a.nombres,a.primer_apellido,a.segundo_apellido,a.logon_name,a.num_documento,a.celular FROM inf_identidades a WHERE a.num_documento = '{}';".format(identificacion)                    
  c=connect_sql()
  c[0].execute(query)
  return c[0].fetchall()

def consultaIdentidadesBarrcode(identificacion):
  query = "SELECT CAST(a.codigo_barras AS CHAR) FROM inf_identidades a WHERE a.num_documento = '{}';".format(identificacion)                    
  c=connect_sql()
  c[0].execute(query)
  return c[0].fetchall()
  #codigo_barras