import pymysql
from decouple import config

# OBTENIENDO EL AMBIENTE DE EJECUCIÓN
# VARIABLES DE CONEXIÓN

AGIL_USER = config("AGIL_USER")
AGIL_PASS = config("AGIL_PASS")
AGIL_HOST = config("SICUC_HOST")
AGIL_DB = config("AGIL_DB")

def connect_sql():
  conn = pymysql.connect(host=AGIL_HOST, port=3306,  user=r'{}'.format(AGIL_USER), password=AGIL_PASS, database=AGIL_DB)
  c = conn.cursor()
  return c

#informacion de profesores en Agil y horario de Atencion
def tutoriaProfesores(codigo_asignatura):
    query = ''' 
            SELECT
              P.id,
              P.identificacion,
              P.nombre,
              P.segundo_nombre,
              P.apellido,
              P.segundo_apellido,
              P.correo,
              P.usuario,
              P.telefono,
              DATE_FORMAT(P.fecha_registra, '%Y-%m-%d') `P.fecha_registra`,
              DATE_FORMAT(P.fecha_elimina, '%Y-%m-%d') `P.fecha_elimina`,
              CEA.id,
              CEA.id_profesor,
              DIA.valor,
              DATE_FORMAT(CEA.hora_inicio, '%H:%i:%s') `CEA.hora_inicio`,
              DATE_FORMAT(CEA.hora_fin, '%H:%i:%s') `CEA.hora_fin`,
              CEA.lugar,
              DATE_FORMAT(CEA.fecha_registra, '%Y-%m-%d') `CEA.fecha_registra`,
              DATE_FORMAT(CEA.fecha_elimina, '%Y-%m-%d') `CEA.fecha_elimina`,
              CEA.id_usuario_registra,
              CEA.id_usuario_elimina,
              CEA.estado,
              CEA.id_tipo,
              CEA.id_asignatura,
              ASIG.valory,
              ASIG.valor
          FROM
              csep_profesor_atencion CEA,
              valor_parametro ASIG, valor_parametro DIA,
              personas P
          RIGHT JOIN csep_profesores C ON
              C.id_persona = P.id
          WHERE ASIG.valory = {} AND C.id = CEA.id_profesor
              AND CEA.id_tipo='Ate_Est'
              AND CEA.estado='1'
              AND DIA.id= CEA.id_dia
              AND CEA.id_asignatura=ASIG.id '''.format(codigo_asignatura)
                #P.identificacion                       
    conn = connect_sql()
    conn.execute(query)
    return conn.fetchall()




