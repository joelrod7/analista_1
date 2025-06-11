from django.db.models import query
import cx_Oracle
from django.utils.encoding import smart_str
from decouple import config

SICUC_USER = config("SICUC_USER")
SICUC_PASS = config("SICUC_PASS")
SICUC_HOST = config("SICUC_HOST")
SICUC_SERVICE = config("SICUC_SERVICE")

# linea para error con oracle (local)
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_10")

# CONEXION A SICUC
def connect_oracle():
    dsn_tns = cx_Oracle.makedsn(SICUC_HOST, 1521, service_name=SICUC_SERVICE)
    conn = cx_Oracle.connect(user=r'{}'.format(SICUC_USER),
                             password=SICUC_PASS, dsn=dsn_tns, encoding="UTF-8")
    c = conn.cursor()
    return c


def transformar_data(data):
    resp = ""
    i = 0
    if len(data):
        for d in data:
            resp = resp + "'" + str(d) + "'"
            i = i + 1
            if (i < len(data)):
                resp = resp + ","
    else:
        resp = "''"
    return resp

# OBTENER PRACTICAS POR PERIODO Y MATERIA


def obtener_matriculados_sicuc(periodo, materias, programas):
    query = '''SELECT
          C.num_identificacion identificacion,
          C.nom_largo alumno,
          b.cod_periodo Periodo,
          A.cod_unidad Cod_programa,
          J.nom_unidad programa,
          A.cod_pensum Pensum,
          B.fec_matricula fec_matricula,
          B.est_matricula matricula,
          I.nom_tabla est_matricula,
          D.cod_materia cod_materia,
          E.nom_materia materia,
          NVL(D.num_grupo,0) num_grupo,
          F.nom_largo docente,
          G.cod_aula cod_aula,
          E.num_nivel semestre,
          b.cod_materia mat_pensum,
          e.uni_teorica Creditos,
          C.dir_email correo_cuc,
		  (SELECT k.num_nivel FROM sinu.SRC_TEM_MATRICULA k
		   WHERE k.id_alum_programa  = b.id_alum_programa
		    AND         k.cod_periodo = b.cod_periodo
		   AND          k.id_grupo  = b.id_grupo) Nivel_materia,
          c.tel_cecular celular,
          c.dir_email_per
FROM sinu.SRC_ALUM_PROGRAMA A,sinu.SRC_ENC_MATRICULA B,sinu.BAS_TERCERO C,sinu.SRC_GRUPO D,sinu.SRC_MAT_PENSUM E,
     sinu.BAS_TERCERO F,sinu.SRC_AULA G,sinu.SRC_VINCULACION H,sinu.SRC_GENERICA I,sinu.SRC_UNI_ACADEMICA J
WHERE B.id_alum_programa = A.id_alum_programa
      AND A.id_tercero = C.id_tercero
      AND A.cod_unidad = J.cod_unidad
      AND B.id_grupo = D.id_grupo
      AND d.cod_unidad = E.cod_unidad
      AND d.cod_pensum = E.cod_pensum
      AND D.cod_materia = E.cod_materia
      AND D.id_vinculacion = H.id_vinculacion(+)
      AND H.id_tercero = F.id_tercero (+)
      AND D.id_aula = G.id_aula(+)
      AND TO_CHAR(B.est_matricula) = I.cod_tabla
      AND I.tip_tabla = 'ESTMAT'
      AND I.cod_tabla != I.tip_tabla
      AND b.cod_periodo = '{}' ---Periodo Actual
      AND j.cod_modalidad = '1' ---Modalidad Pregrado
      AND d.cod_materia in ({})
      AND A.cod_unidad in ({})
order by 3'''.format(periodo, transformar_data(materias), transformar_data(programas))
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def obtener_matriculados_sicuc(periodo, materias, programas):
    query = '''SELECT
          C.num_identificacion identificacion,
          C.nom_largo alumno,
          b.cod_periodo Periodo,
          A.cod_unidad Cod_programa,
          J.nom_unidad programa,
          A.cod_pensum Pensum,
          B.fec_matricula fec_matricula,
          B.est_matricula matricula,
          I.nom_tabla est_matricula,
          D.cod_materia cod_materia,
          E.nom_materia materia,
          NVL(D.num_grupo,0) num_grupo,
          F.nom_largo docente,
          G.cod_aula cod_aula,
          E.num_nivel semestre,
          b.cod_materia mat_pensum,
          e.uni_teorica Creditos,
          C.dir_email correo_cuc,
		  (SELECT k.num_nivel FROM sinu.SRC_TEM_MATRICULA k
		   WHERE k.id_alum_programa  = b.id_alum_programa
		    AND         k.cod_periodo = b.cod_periodo
		   AND          k.id_grupo  = b.id_grupo) Nivel_materia,
          c.tel_cecular celular,
          c.dir_email_per
FROM sinu.SRC_ALUM_PROGRAMA A,sinu.SRC_ENC_MATRICULA B,sinu.BAS_TERCERO C,sinu.SRC_GRUPO D,sinu.SRC_MAT_PENSUM E,
     sinu.BAS_TERCERO F,sinu.SRC_AULA G,sinu.SRC_VINCULACION H,sinu.SRC_GENERICA I,sinu.SRC_UNI_ACADEMICA J
WHERE B.id_alum_programa = A.id_alum_programa
      AND A.id_tercero = C.id_tercero
      AND A.cod_unidad = J.cod_unidad
      AND B.id_grupo = D.id_grupo
      AND d.cod_unidad = E.cod_unidad
      AND d.cod_pensum = E.cod_pensum
      AND D.cod_materia = E.cod_materia
      AND D.id_vinculacion = H.id_vinculacion(+)
      AND H.id_tercero = F.id_tercero (+)
      AND D.id_aula = G.id_aula(+)
      AND TO_CHAR(B.est_matricula) = I.cod_tabla
      AND I.tip_tabla = 'ESTMAT'
      AND I.cod_tabla != I.tip_tabla
      AND b.cod_periodo = '{}' ---Periodo Actual
      AND j.cod_modalidad = '1' ---Modalidad Pregrado
      AND d.cod_materia in ({})
      AND A.cod_unidad in ({})
order by 3'''.format(periodo, transformar_data(materias), transformar_data(programas))
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# VALIDAR MATRICULA POR ESTUDIANTE (NUMERO DE IDENTIFICACIÓN) SICUC


def validar_matricula_sicuc(periodo, identificacion, materias):
    query = '''SELECT    C.num_identificacion identificacion,
          C.nom_largo alumno,
          b.cod_periodo Periodo,
          A.cod_unidad Cod_programa,
          J.nom_unidad programa,
          A.cod_pensum Pensum,
          B.fec_matricula fec_matricula,
          B.est_matricula matricula,
          I.nom_tabla est_matricula,
          D.cod_materia cod_materia,
          E.nom_materia materia,
          NVL(D.num_grupo,0) num_grupo,
          F.nom_largo docente,
          G.cod_aula cod_aula,
          E.num_nivel semestre,
          b.cod_materia mat_pensum,
          e.uni_teorica Creditos,
		  (SELECT k.num_nivel FROM sinu.SRC_TEM_MATRICULA k
		   WHERE k.id_alum_programa  = b.id_alum_programa
		    AND         k.cod_periodo = b.cod_periodo
		   AND          k.id_grupo  = b.id_grupo) Nivel_materia
FROM sinu.SRC_ALUM_PROGRAMA A,sinu.SRC_ENC_MATRICULA B,sinu.BAS_TERCERO C,sinu.SRC_GRUPO D,sinu.SRC_MAT_PENSUM E,
     sinu.BAS_TERCERO F,sinu.SRC_AULA G,sinu.SRC_VINCULACION H,sinu.SRC_GENERICA I,sinu.SRC_UNI_ACADEMICA J
WHERE B.id_alum_programa = A.id_alum_programa
      AND A.id_tercero = C.id_tercero
      AND A.cod_unidad = J.cod_unidad
      AND B.id_grupo = D.id_grupo
      AND d.cod_unidad = E.cod_unidad
      AND d.cod_pensum = E.cod_pensum
      AND D.cod_materia = E.cod_materia
      AND D.id_vinculacion = H.id_vinculacion(+)
      AND H.id_tercero = F.id_tercero (+)
      AND D.id_aula = G.id_aula(+)
      AND TO_CHAR(B.est_matricula) = I.cod_tabla
      AND I.tip_tabla = 'ESTMAT'
      AND I.cod_tabla != I.tip_tabla
      AND b.cod_periodo = '{}' ---Periodo Actual
      AND j.cod_modalidad = '1' ---Modalidad Pregrado
      AND C.num_identificacion = '{}' ---Identificacion del estudiante
      AND d.cod_materia in ({}) ---materias'''.format(periodo, identificacion, transformar_data(materias))
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchone()

# OBTENER COCEPTOS APLICADOS


def obtener_coceptos_aplicados(periodo, identificacion):
    query = '''SELECT
              bas_tercero.NUM_IDENTIFICACION,
              bas_tercero.NOM_LARGO,
              B.NOM_CONCEPTO,
              A.VAL_CONCEPTO,
              DECODE (src_uni_academica.cod_modalidad,1,'Pregrado',2,'Posgrado',3, 'Edu_Continua') Modalidad, A.COD_PERIODO
              FROM  sinu.src_des_liquidacion A
              LEFT JOIN sinu.fin_concepto B ON A.ID_CONCEPTO = B.ID_CONCEPTO
              LEFT JOIN sinu.src_alum_programa ON A.ID_ALUM_PROGRAMA = sinu.src_alum_programa.ID_ALUM_PROGRAMA
              LEFT JOIN sinu.bas_tercero ON sinu.src_alum_programa.ID_TERCERO = sinu.bas_tercero.ID_TERCERO
              LEFT JOIN sinu.src_uni_academica  ON sinu.src_alum_programa.COD_UNIDAD = sinu.src_uni_academica.COD_UNIDAD
              WHERE sinu.bas_tercero.NUM_IDENTIFICACION = '{}'
                AND A.COD_PERIODO = '{}'
                AND B.NOM_CONCEPTO LIKE '%BECA%'
              order by 4'''.format(identificacion, periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def comprobar_promedio_acumulado(identificacion, programa):
    query = '''
          select Promedio_Acumulado from (
          select a.num_identificacion Identificacion,
          v.cod_periodo Periodo,
          v.pro_nivel Promedio_Nivel,
          v.pro_acumulado Promedio_Acumulado,
          d.cod_unidad Cod_Programa,
          d.nom_unidad Programa
          from sinu.bas_tercero a,
          sinu.src_alum_programa b,
          sinu.src_uni_academica d,
          sinu.src_vis_alum_per_est_web v
          where
          a.id_tercero=b.id_tercero
          and b.id_alum_programa=v.id_aLum_programa
          and b.cod_unidad=d.cod_unidad
          and v.est_mat_fin='1'
          and v.est_mat_aca='1'
          --and b.est_alumno='1'
          --and d.cod_modalidad='1'
          and v.pro_acumulado is not null
          and a.num_identificacion = '{}'
          and d.cod_unidad = '{}'
          order by 2 desc
          ) where rownum <=1
        '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return info

def consultar_promedios(identificacion, programa):
    query = '''
      SELECT Promedio_Nivel, Promedio_Acumulado 
      FROM (
          SELECT 
              a.num_identificacion Identificacion,
              v.cod_periodo Periodo,
              v.pro_nivel Promedio_Nivel,
              v.pro_acumulado Promedio_Acumulado,
              d.cod_unidad Cod_Programa,
              d.nom_unidad Programa
          FROM sinu.bas_tercero a
          JOIN sinu.src_alum_programa b ON a.id_tercero = b.id_tercero
          JOIN sinu.src_vis_alum_per_est_web v ON b.id_alum_programa = v.id_aLum_programa
          JOIN sinu.src_uni_academica d ON b.cod_unidad = d.cod_unidad
          WHERE 
              v.est_mat_fin = '1'
              AND v.est_mat_aca = '1'
              AND b.est_alumno = '1'
              AND d.cod_modalidad = '1'
              AND v.pro_nivel IS NOT NULL
              AND a.num_identificacion = '{}'
              AND d.cod_unidad = '{}'
          ORDER BY v.cod_periodo DESC
      ) 
      WHERE rownum <= 1
        '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return info

def comprobar_semestre_actual(identificacion, programa, periodo):
    query = '''
        select semestre from (
        select c.num_identificacion,
        c.nom_largo,
        a.num_niv_cursa semestre,
        a.cod_periodo periodo,
        b.cod_unidad programa
        from sinu.bas_tercero c
        left join sinu.src_alum_programa b on c.id_tercero=b.id_tercero
        left join sinu.src_alum_periodo a on b.id_alum_programa=a.id_alum_programa
        where c.num_identificacion in ('{}')
        and a.cod_periodo='{}'
        and b.cod_unidad = '{}'
        order by 2 desc
        ) where rownum <=1
        '''.format(identificacion, periodo, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return info


def comprobar_promedio_nivel(identificacion, programa):
    query = '''
        select Promedio_Nivel from (
        select a.num_identificacion Identificacion,
        v.cod_periodo Periodo,
        v.pro_nivel Promedio_Nivel,
        v.pro_acumulado Promedio_Acumulado,
        d.cod_unidad Cod_Programa,
        d.nom_unidad Programa
        from
        sinu.bas_tercero a,
        sinu.src_alum_programa b,
        sinu.src_uni_academica d,
        sinu.src_vis_alum_per_est_web v
        where
        a.id_tercero=b.id_tercero
        and b.id_alum_programa=v.id_aLum_programa
        and b.cod_unidad=d.cod_unidad
        and v.est_mat_fin='1'
        and v.est_mat_aca='1'
        --and b.est_alumno='1'
        and d.cod_modalidad='1'
        and v.pro_nivel is not null
        and a.num_identificacion = '{}'
        and d.cod_unidad = '{}'
        order by 2 desc
        ) where rownum <=1
        '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return info


def horario(identificacion, periodo):
    # identificacion = '1000035386'
    # periodo = '20241'
    query = '''
          SELECT DISTINCT
              C.num_identificacion,
              C.nom_largo alumno,
              b.cod_periodo,
              E.nom_materia,
              D.cod_materia,
              NVL(D.num_grupo,0) num_grupo,
              DECODE (i.num_dia,2,'Lunes',3,'Martes',4,'Miercoles',5,'Jueves',6,'Viernes',7,'Sabado',1,'Domingo') dia,
              i.num_dia,
              sinu.funb_hora_militar (i.hor_inicio) hor_inicio,
              sinu.funb_hora_militar(i.hor_fin) hor_fin,
              F.nom_largo profesor,
              A.cod_unidad,
              DECODE(e.cod_tip_materia,1,'TEORICA',2,'PRACTICA',3,'TEORICO-PRACTICA') TIPO_ASIGNATURA,
              e.uni_teorica creditos,
              e.int_horaria,
              g.nom_aula,
              ( select LISTAGG (l.cod_requisito, ',') WITHIN GROUP (order by l.cod_requisito)
              from sinu.src_req_materia l
              where l.cod_materia = d.cod_materia
              and l.cod_pensum = d.cod_pensum
              and l.cod_unidad = d.cod_unidad) pre_requisito
              FROM sinu.SRC_ALUM_PROGRAMA A
              LEFT JOIN sinu.SRC_ENC_MATRICULA B
              ON B.id_alum_programa = A.id_alum_programa
              LEFT JOIN sinu.BAS_TERCERO C
              ON A.id_tercero = C.id_tercero
              LEFT JOIN sinu.SRC_GRUPO D
              ON B.id_grupo = D.id_grupo
              LEFT JOIN sinu.SRC_MAT_PENSUM E
              ON d.cod_unidad = E.cod_unidad AND d.cod_pensum = E.cod_pensum AND D.cod_materia = E.cod_materia
              LEFT JOIN sinu.SRC_AULA G
              ON D.id_aula = G.id_aula
              LEFT JOIN sinu.SRC_VINCULACION H
              ON D.id_vinculacion = H.id_vinculacion
              LEFT JOIN sinu.BAS_TERCERO F
              ON H.id_tercero = F.id_tercero
              LEFT JOIN sinu.SRC_UNI_ACADEMICA J
              ON A.cod_unidad = J.cod_unidad
              LEFT JOIN sinu.src_hor_grupo I
              ON D.id_grupo = i.id_grupo
              WHERE
              b.cod_periodo = '{}'
              AND j.cod_modalidad = '1'
              AND C.num_identificacion = '{}'
              and b.est_matricula <> 5
              order by 8, 9
          '''.format(periodo, identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def comprobar_promedio(**kwargs):
    query = '''
        select a.num_identificacion,
          v.pro_nivel,
          d.nom_unidad,
          v.cod_periodo
          from SINU.bas_tercero a,
          SINU.src_alum_programa b,
          SINU.src_uni_academica d,
          SINU.src_vis_alum_per_est_web v
        WHERE
          a.id_tercero=b.id_tercero
          and b.id_alum_programa=v.id_aLum_programa
          and v.cod_periodo = (SELECT max(per_acumula) ultimo_periodo_cursado
                                from
                                (select DISTINCT per_acumula from sinu.src_his_academica where id_alum_programa in
                                  (select id_alum_programa from sinu.src_alum_programa
                                    where id_tercero in
                                    (select id_tercero from sinu.bas_tercero
                                      where num_identificacion = '{num_iden}'
                                      and cod_unidad = '{cod_prog}'
                                    ))
                                and per_acumula not like '%F'
                                and per_acumula not like '%X'
				and id_grupo is not null
                                order by per_acumula desc)
                              )
          and b.cod_unidad=d.cod_unidad
          and v.est_mat_fin='1'
          and v.est_mat_aca='1'
          --and b.est_alumno='1'
          and d.cod_modalidad='1'
          and d.nom_unidad not like 'BIENESTAR%'
          and a.num_identificacion = '{num_iden}'
          and b.cod_unidad = '{cod_prog}'
          order by 2
        '''.format(num_iden=kwargs['identificacion'], cod_prog=kwargs['programa'])
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return True if info and info[1] >= (float(kwargs['promedio'])) else False


def verificar_asignatura_perdida(**kwargs):
    query = '''
          select DISTINCT
            c.num_identificacion,
            a.cod_periodo periodo_consultado,
            COUNT(a.ind_aprobada) cantidad_perdidas
            from SINU.src_his_academica a,
            SINU.src_alum_programa b,
            SINU.bas_tercero c,
            SINU.src_uni_academica d,
            SINU.src_materia e
          WHERE
            a.cod_periodo = (SELECT max(per_acumula) ultimo_periodo_cursado
                              from
                              (select DISTINCT per_acumula from sinu.src_his_academica where id_alum_programa in
                                (select id_alum_programa from sinu.src_alum_programa
                                  where id_tercero in
                                  (select id_tercero from sinu.bas_tercero
                                    where num_identificacion = '{num_iden}'
                                    and cod_unidad = '{cod_prog}'
                                  ))
                              and per_acumula not like '%F'
                              and per_acumula not like '%X'
                              order by per_acumula desc)
                            )
            AND a.id_alum_programa=b.id_alum_programa
            AND a.cod_materia=e.cod_materia
            AND b.cod_unidad=d.cod_unidad
            AND b.id_tercero=c.id_tercero
            AND a.IND_APROBADA = '0'
            AND a.est_materia != '5'
            AND b.cod_unidad != '31132'
            AND b.cod_unidad != '40027'
            AND c.num_identificacion = '{num_iden}'
            AND b.cod_unidad = '{cod_prog}'
            GROUP BY a.cod_periodo,c.num_identificacion, a.ind_aprobada
            order by 2
          '''.format(num_iden=kwargs['identificacion'], cod_prog=kwargs['programa'])
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return False if info else True


def validar_egresado(**kwargs):  # No se usa
    query = '''SELECT b.num_identificacion identificacion,
              b.nom_largo Nombre,
              a.cod_unidad cod_programa,
              d.nom_unidad Programa,
              DECODE(d.cod_modalidad,1,'PREGRADO',2,'POSGRADO',3,'EDU CONTINUADA') Modalidad,
              DECODE (a.est_alumno, 2,'EGRESADO',9,'GRADUADO') Estado
            FROM SINU.src_alum_programa a, SINU.bas_tercero b, SINU.src_uni_academica d
            WHERE a.id_tercero=b.id_tercero
              and a.cod_unidad=d.cod_unidad
              and a.est_alumno in ('9') --- 2 Egresado, 9 Graduado
              and b.num_identificacion = '{}'
              --and a.cod_periodo = 'PERIODO'
              --and d.cod_modalidad = 'MODALIDAD' --- Modalidad 1 - Pregrado, 2 - Posgrado, 3 - Edu Continuada
              order by 2'''.format(kwargs['identificacion'])
    conn = connect_oracle()
    result = conn.execute(query)
    return True if result.fetchone() else False


def validar_ingles(**kwargs):
    query = ''' select distinct
                c.num_identificacion,
                c.nom_largo,
                a.COD_UNIDAD,
                f.nom_unidad,
                a.COD_MATERIA,
                e.nom_materia,
                a.NUM_NIVEL,
                a.NUM_NOTA, decode(a.IND_APROBADA,0,'NO_APROBADO',1,'APROBADO') Estado,
                a.COD_PERIODO periodo_cursado
                from sinu.src_semaforo a, sinu.src_alum_programa b, sinu.bas_tercero c, sinu.src_alum_periodo d,
                sinu.src_materia e, sinu.src_uni_academica f
                where
                  a.id_alum_programa = b.id_alum_programa and
                  b.id_tercero = c.id_tercero and
                  b.id_alum_programa = d.id_alum_programa and
                  a.cod_materia = e.cod_materia and
                  a.cod_unidad = f.cod_unidad and
                  (d.est_mat_aca=1 or d.est_mat_aca=0)
                  and
                  d.est_mat_fin = '1' and
                  f.cod_modalidad = '3' and
                  b.cod_unidad = '31132' and
                  a.ind_aprobada = '1' and
                  b.est_alumno IN (1,7) and
                  c.num_identificacion = '{}'
                order by 2'''.format(kwargs['identificacion'])
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return True if info and info[8] == 'APROBADO' else False

# Asignaturas de un programa a las que el estudiante puede acceder


def asignaturas_programa_estudiante(identificacion, programa):
    query = '''
            select distinct
            a.COD_MATERIA,
            e.nom_materia,
            a.NUM_NIVEL semestre_materia,
            a.uni_teorica creditos,
            d.cod_periodo
            from sinu.src_semaforo a,
            sinu.src_alum_programa b,
            sinu.bas_tercero c,
            sinu.src_alum_periodo d,
            sinu.src_materia e,
            sinu.src_uni_academica f
            where
            a.id_alum_programa = b.id_alum_programa and
            b.id_tercero = c.id_tercero and
            b.id_alum_programa = d.id_alum_programa and
            a.cod_materia = e.cod_materia and
            a.cod_unidad = f.cod_unidad and
            --d.est_mat_aca='1' and
            d.est_mat_fin = '1' and
            f.cod_modalidad = '1' and
            a.IND_APROBADA = '0' and
            d.cod_periodo = (
              select periodo||mes periodo from
              (
                select to_char(sysdate, 'YYYY') periodo,
                case to_char(sysdate,'MM')
                  when '01' then '1'
                  when '02' then '1'
                  when '03' then '1'
                  when '04' then '1'
                  when '05' then '1'
                  when '06' then '1'
                  when '07' then '2'
                  when '08' then '2'
                  when '09' then '2'
                  when '10' then '2'
                  when '11' then '2'
                  when '12' then '2'

                  end mes from dual
              )
            )
            and
            c.num_identificacion = '{}' and
            b.cod_unidad = '{}'
            order by 2
            '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# Grupos creados en el pediodo de una asignatura


def grupos_asignatura(asignatura, periodo):
    query = '''
            select distinct
            a.cod_materia,
            b.nom_materia,
            a.id_grupo,
            a.num_grupo grupo,
            DECODE(d.NUM_DIA,2,'Lunes',3,'Martes',4,'Miercoles',5,'Jueves',6,'Viernes',7,'Sabado',1,'Domingo') DIA,
            sinu.funb_hora_militar(d.hor_inicio) hor_inicio,
            sinu.funb_hora_militar(d.hor_fin) hor_fin,
            f.nom_tercero nombre_docente,
            f.pri_apellido apellido_docente,
            f.NUM_IDENTIFICACION id_docente,
            a.cod_periodo periodo,
            d.id_div_grupo
            from
            sinu.SRC_GRUPO A,
            sinu.SRC_MAT_PENSUM B,
            sinu.SRC_UNI_ACADEMICA C,
            sinu.src_hor_grupo d,
            sinu.src_vinculacion e,
            sinu.bas_tercero f,
            sinu.src_jornada g,
            sinu.src_doc_grupo h
            where a.cod_unidad = b.cod_unidad
            and a.cod_pensum = b.cod_pensum
            and a.cod_materia= b.cod_materia
            and a.cod_unidad = c.cod_unidad
            and a.id_grupo   = d.id_grupo (+)
            and a.id_vinculacion (+) = e.id_vinculacion
            and f.id_tercero=e.id_tercero
            and c.id_jornada = g.id_jornada
            and a.id_vinculacion = h.id_vinculacion
            and a.id_grupo = h.id_grupo
            and a.cod_periodo = '{}'
            and a.cod_materia = '{}'
            and c.nom_unidad not like '%ESPECI%'
            and c.nom_unidad not like '%DIPL%'
            and c.nom_unidad not like '%CURS%'
            and (a.num_grupo like 'MAGIS%' or a.num_grupo like 'REMOT%')
            group by f.num_identificacion,f.nom_tercero,f.seg_nombre,f.pri_apellido,f.seg_apellido,e.id_tercero,a.cod_unidad, c.nom_unidad,b.uni_teorica,b.num_nivel, a.cod_materia, b.nom_materia, a.id_grupo,a.num_grupo, d.num_dia,
            g.nom_jornada, a.id_vinculacion, h.tip_docente, a.cod_periodo, sinu.funb_hora_militar(
                d.hor_inicio), sinu.funb_hora_militar(d.hor_fin), d.id_div_grupo
            order by 4
            '''.format(periodo, asignatura)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def obtenerGruposProfesor(identificacion, periodo):
    query = '''select distinct
      f.num_identificacion Num_Identificacion,
      f.nom_tercero primer_nombre,
      f.seg_nombre segundo_nombre,
      f.pri_apellido primer_Apellido,
      f.seg_apellido segundo_pellido,
      a.cod_unidad cod_programa,
      c.nom_unidad programa,
      a.cod_materia,
      b.nom_materia,
      a.id_grupo,
      a.num_grupo grupo,
      a.cod_periodo periodo
      from
      sinu.SRC_GRUPO A,
      sinu.SRC_MAT_PENSUM B,
      sinu.SRC_UNI_ACADEMICA C,
      sinu.src_hor_grupo d,
      sinu.src_vinculacion e,
      sinu.bas_tercero f,
      sinu.src_jornada g,
      sinu.src_doc_grupo h
      where  a.cod_unidad = b.cod_unidad
      and a.cod_pensum = b.cod_pensum
      and a.cod_materia= b.cod_materia
      and a.cod_unidad = c.cod_unidad
      and a.id_grupo   = d.id_grupo (+)
      and a.id_vinculacion (+) = e.id_vinculacion
      and f.id_tercero=e.id_tercero
      and c.id_jornada = g.id_jornada
      and a.id_vinculacion = h.id_vinculacion
      and a.id_grupo = h.id_grupo
      and f.num_identificacion = '{}'
      and a.cod_periodo = '{}'
      and c.nom_unidad not like '%ESPECI%'
      and c.nom_unidad not like '%DIPL%'
      and c.nom_unidad not like '%CURS%'
      group by f.num_identificacion,f.nom_tercero,f.seg_nombre,f.pri_apellido,f.seg_apellido,e.id_tercero,a.cod_unidad, c.nom_unidad,b.uni_teorica,b.num_nivel, a.cod_materia, b.nom_materia, a.id_grupo,a.num_grupo, d.num_dia,
      g.nom_jornada, a.id_vinculacion, h.tip_docente, a.cod_periodo
      order by   3, 8'''.format(identificacion, periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def obtenerGruposEstudiantesProfesor(identificacion, id_grupo, periodo):
    query = '''SELECT distinct
    a.num_identificacion Cedula_Estudiante,
    a.nom_tercero primer_nombre,
    a.seg_nombre segundo_nombre,
    a.pri_apellido primer_Apellido,
    a.seg_apellido segundo_pellido,
    f.cod_materia CodigoMateria,
    m.nom_materia NomMateria,
    f.id_grupo Id_Grupo,
    f.num_grupo GrupoMateria,
    Nvl(i.num_identificacion,'NA') Cedula_Docente,
    c.nom_unidad Programa,
    f.cod_periodo Periodo
    FROM
    sinu.bas_tercero a,
    sinu.src_alum_programa b,
    sinu.src_uni_academica c,
    sinu.src_alum_periodo d,
    sinu.src_enc_matricula e ,
    sinu.src_grupo f,
    sinu.src_mat_pensum g,
    sinu.src_vinculacion h,
    sinu.bas_tercero i,
    sinu.src_materia m,
    sinu.src_hor_grupo x,
    sinu.src_aula y,
    sinu.src_bloque i
    WHERE 1=1
    AND a.id_tercero=b.id_tercero
    AND b.cod_unidad=c.cod_unidad
    AND b.id_alum_programa=d.id_alum_programa
    AND b.id_alum_programa=e.id_alum_programa
    AND f.cod_unidad=g.cod_unidad
    AND f.cod_pensum=g.cod_pensum
    AND f.cod_materia=g.cod_materia
    AND f.cod_materia=m.cod_materia
    AND e.id_grupo=f.id_grupo
    AND x.id_grupo=f.id_grupo
    AND f.ID_AULA = y.ID_AULA
    AND y.ID_BLOQUE = i.ID_BLOQUE
    AND f.id_vinculacion = h.id_vinculacion(+)
    AND h.id_tercero=i.id_tercero(+)
    AND b.est_alumno IN (1,7)
    AND d.cod_periodo='{}'
    AND d.est_mat_fin=1
    AND c.cod_modalidad=1
    AND e.cod_periodo=d.cod_periodo
    AND a.num_identificacion = '{}'
    order by 5
  '''.format(periodo, identificacion).encode('utf-8')
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def historicoNotas(identificacion, periodo):
    query = '''
  SELECT
  F.num_identificacion identificacion,
  G.cod_unidad cod_programa,
  C.nom_unidad programa,
  B.cod_pensum,
  B.cod_periodo,
  B.cod_materia,
  D.nom_materia,
  B.num_grupo grupo,
  DECODE(A.def_historia,NULL,'----',to_char(A.def_historia, '0D9')) definitiva
  FROM    sinu.src_his_academica A,
          sinu.src_grupo B,
          sinu.src_uni_academica C,
          sinu.src_mat_pensum D,
          sinu.src_vinculacion E,
          sinu.bas_tercero F,
          sinu.src_alum_programa G,
          sinu.bas_tercero H
  WHERE   G.cod_unidad = C.cod_unidad and
          B.cod_unidad = D.cod_unidad and
          B.cod_pensum = D.cod_pensum and
          B.cod_materia = D.cod_materia and
          B.id_vinculacion = E.id_vinculacion(+) and
          E.id_tercero = H.id_tercero and
          B.id_grupo = A.id_grupo and
          A.id_alum_programa = G.id_alum_programa and
          G.id_tercero = F.id_tercero and
          F.num_identificacion = '{}' and
          B.cod_periodo = '{}'
  order by 2
  '''.format(identificacion, periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def semestre_creditos(identificacion, programa):
    query = '''
      SELECT
        --b.id_alum_programa,
        c.num_identificacion AS Num_Identificacion,
        c.nom_largo AS Nom_Largo,
        a.num_niv_cursa AS Semestre,
        a.tot_uni_matriculadas AS Creditos_Matriculados,
        d.nom_unidad AS Programa,
        b.cod_pensum AS Pensum,
        a.cod_periodo AS Periodo,
        I.nom_tabla AS Est_Alumno
      FROM sinu.src_alum_periodo a
      LEFT JOIN sinu.src_alum_programa b ON a.id_alum_programa = b.id_alum_programa
      LEFT JOIN sinu.bas_tercero c ON b.id_tercero = c.id_tercero
      LEFT JOIN sinu.src_uni_academica d ON b.cod_unidad = d.cod_unidad
      LEFT JOIN sinu.src_generica I ON TO_CHAR(b.est_alumno) = I.cod_tabla
      WHERE a.cod_periodo = (
          SELECT 
              MAX(sub_a.cod_periodo) AS ultimo_periodo
          FROM 
              sinu.src_alum_periodo sub_a
          WHERE 
              sub_a.id_alum_programa = a.id_alum_programa
              AND (sub_a.est_mat_fin = 1 OR sub_a.est_mat_aca = 1)
      )
      AND I.tip_tabla = 'ESTALU'
      AND I.cod_tabla != I.tip_tabla
      AND c.num_identificacion = '{}'
      AND b.cod_unidad = '{}'
      AND b.est_alumno = '1'
      ORDER BY Creditos_Matriculados
    '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchone()
    # CONSULTA VIEJA
# select
#     c.num_identificacion,
#     c.nom_largo,
#     a.num_niv_cursa semestre,
#     a.tot_uni_matriculadas creditos_matriculados,
#     d.nom_unidad Programa,
#     b.cod_pensum pensum,
#     a.cod_periodo periodo,
#     I.nom_tabla est_alumno
#     from sinu.src_alum_periodo a, sinu.src_alum_programa b, sinu.bas_tercero c, sinu.src_uni_academica d, sinu.SRC_GENERICA I
#     where a.cod_periodo='{}'
#     and a.est_mat_fin='1'
#     and a.id_alum_programa=b.id_alum_programa
#     and b.id_tercero=c.id_tercero
#     and b.cod_unidad=d.cod_unidad
#     --and d.cod_modalidad='1'
#     AND TO_CHAR(b.est_alumno) = I.cod_tabla
#     AND I.tip_tabla = 'ESTALU'
#     AND I.cod_tabla != I.tip_tabla
#     AND c.num_identificacion = '{}'
#     and b.cod_unidad = '{}'
#     order by 4

def obtenerGruposEstudiantesProfesorHis(identificacion, id_grupo, periodo):
    query = '''SELECT distinct
            f.num_identificacion Cedula_Estudiante,
            f.nom_tercero primer_nombre,
            f.seg_nombre segundo_nombre,
            f.pri_apellido primer_Apellido,
            f.seg_apellido segundo_pellido,
            B.cod_materia,
            D.nom_materia,
            B.id_grupo,
            B.num_grupo,
            H.num_identificacion num_identificacion_docente,
            C.nom_unidad programa,
            B.cod_periodo,
            y.COD_AULA,
            y.ID_BLOQUE,
            i.NOM_BLOQUE,
            y.NOM_AULA,
            x.hor_inicio,
            x.hor_fin
            from
            sinu.src_his_academica A,
            sinu.src_grupo B,
            sinu.src_uni_academica C,
            sinu.src_mat_pensum D,
            sinu.src_vinculacion E,
            sinu.bas_tercero F,
            sinu.src_alum_programa G,
            sinu.bas_tercero H,
            sinu.src_hor_grupo x,
            sinu.src_aula y,
            sinu.src_bloque i
        where   G.cod_unidad = C.cod_unidad and
        B.cod_unidad = D.cod_unidad and
        B.cod_pensum = D.cod_pensum and
        B.cod_materia = D.cod_materia and
        B.id_vinculacion = E.id_vinculacion(+) and
        E.id_tercero = H.id_tercero and
        B.id_grupo = A.id_grupo and
        x.id_grupo=b.id_grupo and
        y.ID_AULA = B.ID_AULA and
        y.ID_BLOQUE = i.ID_BLOQUE AND
        A.id_alum_programa = G.id_alum_programa and
        G.id_tercero = F.id_tercero and
        b.cod_periodo = '{}' and
        H.num_identificacion = '{}' and
        B.id_grupo = '{}' and
        c.cod_modalidad = '1'
        order by 4'''.format(periodo, identificacion, id_grupo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def estado_carrera_actual(identificacion, programa):
    query = '''
    select DISTINCT
    c.num_identificacion,
    c.nom_largo,
    (SELECT SUM(M.UNI_TEORICA)
    FROM sinu.SRC_ALUM_PROGRAMA A, sinu.SRC_MAT_PENSUM M, sinu.SRC_HIS_ACADEMICA H, sinu.BAS_TERCERO B, sinu.SRC_UNI_ACADEMICA U
    WHERE A.ID_ALUM_PROGRAMA = H.ID_ALUM_PROGRAMA
    AND A.COD_PENSUM = M.COD_PENSUM
    AND A.COD_UNIDAD = M.COD_UNIDAD
    AND A.ID_ALUM_PROGRAMA = b.ID_ALUM_PROGRAMA
    AND M.COD_MATERIA = H.COD_MATERIA
    AND H.DEF_HISTORIA >=3.0
    AND A.ID_TERCERO = B.ID_TERCERO
    AND A.COD_UNIDAD = U.COD_UNIDAD
    GROUP BY B.NUM_IDENTIFICACION, B.NOM_LARGO, A.ID_ALUM_PROGRAMA,M.COD_UNIDAD,U.NOM_UNIDAD,M.COD_PENSUM
    ) total_creditos_cursados,
    e.CREDITOS_PENSUM total_creditos_pensum,
    d.nom_unidad
    from sinu.src_alum_periodo a, sinu.src_alum_programa b, sinu.bas_tercero c, sinu.src_uni_academica d, sinu.DBACUC_CREDITOS_PENSUM e
    where
    c.num_identificacion = '{}'
    and a.est_mat_fin='1'
    --and b.est_alumno IN (1,7)
    and a.id_alum_programa=b.id_alum_programa
    and b.id_tercero=c.id_tercero
    and b.cod_unidad=d.cod_unidad
    and b.cod_unidad = e.COD_UNIDAD
    and b.cod_pensum = e.COD_PENSUM
    and b.cod_unidad = '{}'
  '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchone()

# def notas_nivel(identificacion, periodo, modalidad = 1):


def notas_nivel(id_alum):
    # id_alum = '429500'
    query = '''
    SELECT
        e.num_identificacion,
        c.nom_unidad,
        b.cod_materia,
        f.nom_materia,
        b.num_grupo,
        a.num_nota Corte,
        decode(a.val_nota,null,'-----',to_char(a.val_nota, '99D9')) nota,
        (select PES_NOTA
            from sinu.src_not_grupo
            where src_not_grupo.id_grupo = b.id_grupo
            and src_not_grupo.NUM_NOTA = a.num_nota and rownum<=1) peso,
        (SELECT DECODE(enc.not_definitiva,NULL,'----',to_char(enc.not_definitiva, '99D9'))
            from sinu.src_enc_matricula enc where enc.id_alum_programa = d.id_alum_programa and enc.id_grupo = b.id_grupo) not_definitiva,
        b.cod_periodo,
        (select x.nom_largo from sinu.bas_tercero x where v.id_tercero = x.id_tercero) profesor
    FROM
        sinu.src_det_matricula a
        LEFT JOIN sinu.src_alum_programa d ON a.id_alum_programa = d.id_alum_programa
        LEFT JOIN sinu.bas_tercero e ON e.id_tercero = d.id_tercero
        LEFT JOIN sinu.src_uni_academica c ON c.cod_unidad = d.cod_unidad
        LEFT JOIN sinu.src_grupo b ON b.id_grupo   = a.id_grupo
        LEFT JOIN sinu.src_materia f ON f.cod_materia = b.cod_materia
        LEFT JOIN sinu.src_vinculacion v ON b.id_vinculacion = v.id_vinculacion
    WHERE
        d.id_alum_programa = '{}'
        --c.cod_modalidad = ''
        and f.cod_modalidad in ('1','2','3')
        --and a.num_nota in ('1','2','3','4') -- No Focalizadas
        --and a.num_nota in ('1','4','7','10') -- Focalizadas
        and a.num_nota in ('1','2','3','4','5','6','7','8','9','10') -- Todas
        --and e.num_identificacion = ''
        --and b.cod_periodo in ()
        order by 6
  '''.format(id_alum)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def modalidades_periodo(identificacion):
    query = '''
        select distinct cod_periodo, cod_programa, nom_programa, cod_modalidad, modalidad, cod_pensum from
          (select
            distinct a.id_alum_programa,
              d.num_identificacion,
              b.cod_unidad cod_programa,
              b.nom_unidad nom_programa,
	      a.cod_pensum cod_pensum,
              c.cod_periodo,
              c.fec_creacion,
              c.est_mat_fin Matricula_Financiera,
              c.EST_MAT_ACA Matrícula_Academica,
              DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
              b.cod_modalidad,
              DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad
        from
          sinu.src_alum_programa a,
          sinu.src_uni_academica b,
          sinu.src_alum_periodo c,
          sinu.bas_tercero d,
          sinu.SRC_ENC_LIQUIDACION g,
          sinu.src_periodo p
        where a.id_tercero = d.id_tercero
              and a.id_alum_programa = c.id_alum_programa
              and a.cod_unidad = b.cod_unidad
              --and c.cod_periodo in ('20201')
              and g.COD_PERIODO = c.cod_periodo
              --and b.cod_modalidad = '2'
              and a.est_alumno IN (1,7)
              and c.est_mat_fin in (1,0)
              and g.est_liquidacion = 2
              and g.tip_liquidacion in (1)
              and a.id_alum_programa = g.id_alum_programa
              and d.num_identificacion = '{}'
              and c.cod_periodo = p.cod_periodo
              and p.est_periodo = 1
              and p.fec_inicio BETWEEN To_Date('01/11/21','dd/mm/yy')  and To_Date('30/01/22','dd/mm/yy') -- ojo fecha vigencia
              order by 5 desc)
      '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# quitar despues


def obtenerTipoMod(alum):
    query = '''
  SELECT
    COD_MODALIDAD,
    COD_PERIODO,
    NOM_UNIDAD
  FROM
    sinu.src_vis_alumno
  WHERE id_alum_programa = '{}'
   '''.format(alum)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchone()
    return info if info else ''


def encabezado_estudiante(identificacion):
    query = '''
  SELECT
    NUM_IDENTIFICACION ,
    NOM_LARGO ,
    COD_PERIODO ,
    COD_UNIDAD ,
    COD_PENSUM ,
    EST_ALUMNO ,
    FEC_INGRESO ,
    NOM_DEPENDENCIA ,
    NOM_UNIDAD ,
    COD_MODALIDAD,
    ID_ALUM_PROGRAMA
  FROM
    sinu.src_vis_alumno
  WHERE num_identificacion = '{}'
    and est_alumno in ('EGRESADO','ACTIVO')
   '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def comprobar_pago_reconocimiento(identificacion):
    query = '''
         SELECT
          C.num_documento "No. LIQUID VOLANTE",
          G.NUM_IDENTIFICACION,
          C.COD_PERIODO,
          b.cod_concepto,
          B.NOM_CONCEPTO,
          DECODE (C.EST_LIQUIDACION,1,'Liquidada',2,'Pagada') Estado_Liquidacion,
          C.fec_pago,
          E.NOM_BANCO banco
          FROM
            sinu.src_det_liquidacion A
          LEFT JOIN sinu.fin_concepto B
          ON
            A.ID_CONCEPTO = B.ID_CONCEPTO
          LEFT JOIN sinu.src_enc_liquidacion C
          ON
          a.id_enc_liquidacion = c.id_enc_liquidacion
          LEFT JOIN sinu.bas_cta_corriente D
          ON
          C.ID_CTA_INTERNA = D.ID_CTA_CORRIENTE
          LEFT JOIN sinu.bas_banco E
          ON
          D.ID_BANCO = E.ID_BANCO
          LEFT JOIN sinu.src_alum_programa F
          ON
            C.ID_ALUM_PROGRAMA = F.ID_ALUM_PROGRAMA
          LEFT JOIN sinu.bas_tercero G
          ON
            F.ID_TERCERO = G.ID_TERCERO
          LEFT JOIN sinu.src_uni_academica H
          ON
            F.COD_UNIDAD = H.COD_UNIDAD
          WHERE
            H.cod_modalidad=1
            and B.COD_CONCEPTO = 'PERCL'
            and C.EST_LIQUIDACION = '2' and
            G.NUM_IDENTIFICACION = '{}'
          order by 5
        '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchone()


def validar_creditos_aprobados(identificacion, periodo):

    # query1: Creditos totales por Pensum y programa del estuditante. Recibe Período e Identificación
    query_1 = '''SELECT num_identificacion NUM_IDENTIFICACION,
    cod_programa COD_PROGRAMA,
    creditos_pensum CREDITOS_TOTALES_PENSUM
    FROM (
    select c.num_identificacion,
    d.cod_unidad cod_programa,
    d.nom_unidad programa,
    a.cod_periodo,
    e.CREDITOS_PENSUM
    from sinu.src_alum_periodo a, sinu.src_alum_programa b, sinu.bas_tercero c, sinu.src_uni_academica d, sinu.DBACUC_CREDITOS_PENSUM e
    where a.cod_periodo='{}'
    and a.est_mat_fin='1'
    and a.id_alum_programa=b.id_alum_programa
    and b.id_tercero=c.id_tercero
    and b.cod_unidad=d.cod_unidad
    and d.cod_modalidad='1'
    and b.cod_unidad = e.COD_UNIDAD
    and b.cod_pensum = e.COD_PENSUM
    AND c.num_identificacion = '{}'
    )
  '''.format(periodo, identificacion)

    # query2: Creditos totales cursados por el estudiante en su historia académica. Recibe Identificación
    query_2 = '''SELECT SUM(M.UNI_TEORICA) TOTAL_CREDITOS_CURSADOS
    FROM sinu.SRC_ALUM_PROGRAMA A, sinu.SRC_MAT_PENSUM M, sinu.SRC_HIS_ACADEMICA H, sinu.BAS_TERCERO B, sinu.SRC_UNI_ACADEMICA U
    WHERE A.ID_ALUM_PROGRAMA = H.ID_ALUM_PROGRAMA
    AND A.COD_PENSUM = M.COD_PENSUM
    AND A.COD_UNIDAD = M.COD_UNIDAD
    AND M.COD_MATERIA = H.COD_MATERIA
    AND H.DEF_HISTORIA >=3.0
    AND A.ID_TERCERO = B.ID_TERCERO
    AND A.COD_UNIDAD = U.COD_UNIDAD
    AND U.cod_modalidad = '1'
    AND B.NUM_IDENTIFICACION = '{}'
    GROUP BY B.NUM_IDENTIFICACION
  '''.format(identificacion)

    conn = connect_oracle()
    result_1 = conn.execute(query_1)
    result_1 = result_1.fetchone()
    result_2 = conn.execute(query_2)
    result_2 = result_2.fetchone()
    if result_1 and result_2:
        result = result_1 + result_2
    else:
        result = None
    return result


def comprobar_pago_supletorio_sustentacion(identificacion, periodo):
    query = ''' SELECT  H.NUM_IDENTIFICACION,
      C.COD_PERIODO,
      B.NOM_CONCEPTO,
      I.COD_UNIDAD cod_programa,
      C.num_documento "No. LIQUID VOLANTE",
      C.val_pagado,
      C.fec_pago,
      F.NOM_BANCO banco,
      C.EST_LIQUIDACION
      FROM
        sinu.src_det_liquidacion A
      LEFT JOIN sinu.fin_concepto B
      ON
        A.ID_CONCEPTO = B.ID_CONCEPTO

      LEFT JOIN sinu.src_enc_liquidacion C
      ON
      a.id_enc_liquidacion = c.id_enc_liquidacion

      LEFT JOIN sinu.SRC_DIS_PAGO D
      ON
      C.ID_ENC_LIQUIDACION = D.ID_ENC_LIQUIDACION

      LEFT JOIN sinu.bas_cta_corriente E
      ON
      C.ID_CTA_INTERNA = E.ID_CTA_CORRIENTE
      LEFT JOIN sinu.bas_banco F
      ON
      E.ID_BANCO = F.ID_BANCO

      LEFT JOIN sinu.src_alum_programa G
      ON
        C.ID_ALUM_PROGRAMA = G.ID_ALUM_PROGRAMA

      LEFT JOIN sinu.bas_tercero H
      ON
        G.ID_TERCERO = H.ID_TERCERO

      LEFT JOIN sinu.src_uni_academica I
      ON
        G.COD_UNIDAD = I.COD_UNIDAD
      WHERE
        I.cod_modalidad=1
        and B.NOM_CONCEPTO like '%SUPLET%'
        and H.NUM_IDENTIFICACION = '{}'
        and C.COD_PERIODO = '{}'
        and C.EST_LIQUIDACION = '2'
      order by 5
        '''.format(identificacion, periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def grupos_docentes(identificacion, periodo):
    query = '''
    select
    (select nom_unidad from sinu.src_uni_academica where d.cod_unidad = cod_unidad) nom_unidad,
    d.cod_materia,
    (select nom_materia from sinu.src_materia where d.cod_materia = cod_materia) nom_materia,
    c.num_identificacion,
    A.id_grupo,
    D.num_grupo grupo,
    (select num_nivel from sinu.src_mat_pensum where d.cod_materia = cod_materia and rownum <2) semestre_materia,
    --c.dir_email,
    Decode(A.tip_docente,1,'PRINCIPAL',2,'SUPLENTE') ROL_DOCENTE

    from
        sinu.src_doc_grupo A
    LEFT JOIN sinu.SRC_VINCULACION  B
    ON
      a.id_vinculacion = B.ID_VINCULACION

    LEFT JOIN sinu.BAS_TERCERO  C
    ON
      b.id_tercero = c.id_tercero

    LEFT JOIN sinu.src_grupo  D
    ON
      A.id_grupo = d.id_grupo

    where d.cod_periodo = '{}'
    and c.num_identificacion = '{}'
    '''.format(periodo, identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
# ALEXIS DE LA HOZ MANOTAS	72230045	INGENIERÍA DE SISTEMAS  20211


def grupo_estudiante(codigo):
    query = '''
    SELECT
    a.num_identificacion                "_CedulaEstudiante",
    f.cod_materia                       "_CodigoMateria",
    Nvl(i.num_identificacion,'NA')      "_CedulaDocente",
    f.cod_unidad                        "_CodigoPrograma",
    g.num_nivel                         "_SemestreMateria",
    f.id_grupo                          "_Id_Grupo",
    f.num_grupo                         "_GrupoMateria"
    FROM sinu.bas_tercero a,
    sinu.src_alum_programa b,
    sinu.src_uni_academica c,
    sinu.src_alum_periodo d,
    sinu.src_enc_matricula e ,
    sinu.src_grupo f,
    sinu.src_mat_pensum g,
    sinu.src_vinculacion h,
    sinu.bas_tercero i
    WHERE 1=1
    AND a.id_tercero=b.id_tercero
    AND b.cod_unidad=c.cod_unidad
    AND b.id_alum_programa=d.id_alum_programa
    AND b.id_alum_programa=e.id_alum_programa
    AND f.cod_unidad=g.cod_unidad
    AND f.cod_pensum=g.cod_pensum
    AND f.cod_materia=g.cod_materia
    AND e.id_grupo=f.id_grupo
    AND f.id_vinculacion = h.id_vinculacion(+)
    AND h.id_tercero=i.id_tercero(+)
    AND b.est_alumno IN (1,7)
    --AND d.cod_periodo='20212'
    AND e.cod_periodo=d.cod_periodo
    AND d.est_mat_fin=1
    --AND c.cod_modalidad=1
    AND e.id_grupo = '{}'
    '''.format(codigo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


# Retorna los estudiantes activos de un programa
def estudiantes_programa(codigoPrograma):
    codigo = codigoPrograma.split(',')
    grupos = []
    texto = str()
    if len(codigo) > 0:
        for data in codigo:
            grupos.append(data)
        for clave in grupos:
            texto = texto+"".join("'"+clave+"'")+", "
        valores = texto[:-2]

    query = '''
    SELECT a.num_identificacion,
      a.nom_largo,
      b.cod_pensum,
      b.cod_unidad,
      b.cod_periodo,
      (select nom_unidad from sinu.src_uni_academica where b.cod_unidad = cod_unidad),
      decode (b.est_alumno, 0, 'INACTIVO', 1, 'ACTIVO',2,'EGRESADO',3, 'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO') "ESTADO"
    FROM sinu.bas_tercero a, sinu.src_alum_programa b
      WHERE a.id_tercero = b.id_tercero
      AND b.est_alumno ='1'
      AND b.cod_unidad IN ({})
      --AND b.cod_periodo = '20212'
  '''.format(valores)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def pre_inscritos_bienestar(periodo):
    query = '''
      SELECT
          a.cod_periodo,
          a.num_formulario,
          a.fec_venta,
          a.val_venta,
          a.fec_pago,
          a.cod_unidad,
          b.nom_unidad,
          a.cod_pensum,
          a.num_identificacion,
          a.pri_apellido,
          a.seg_apellido,
          a.nom_usuario,
          a.tel_aspirante,
          a.tel_cecular,
          a.dir_email,
          a.dir_residencia,
          DECODE(a.tip_inscripcion,
                    1, 'NORMAL',
                    2, 'TRANSFERENCIA INTERNA',
                    3, 'TRANSFERENCIA EXTERNA',
                    4, 'RESERVA CUPO',
                    5, 'REINTEGRO',
                    6, 'EXO.NORMAL',
                    7, 'EXO.TRANSF EXTERNA',
                    8, 'EXO.REINTEGRO',
                    9, 'EXO.TRANSF INTERNA') AS tip_inscripcion,
          c.num_est_economico
      FROM
          sinu.src_formulario a
      JOIN
          sinu.src_uni_academica b 
          ON a.cod_unidad = b.cod_unidad
      JOIN
          sinu.bas_tercero c
          ON a.id_tercero = c.id_tercero
      WHERE
          a.cod_periodo = '{}'
          AND a.cod_modalidad = 1
          AND a.tip_inscripcion != '5'
      ORDER BY
          a.num_formulario ASC
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def inscritos_bienestar(periodo):
    query = '''
        SELECT
            a.COD_PERIODO,
            b.NUM_IDENTIFICACION,
            b.NOM_LARGO,
            b.TEL_RESIDENCIA,
            b.TEL_CECULAR,
            b.DIR_EMAIL_PER,
            a.FEC_INSCRIPCION,
            decode(a.TIP_INSCRIPCION,1,'NORMAL',2,'TRANSFERENCIA INTERNA',3,'TRANSFERENCIA EXTERNA',4,'RESERVA CUPO',5,'REINTEGRO',6,'EXO.NORMAL',7,'EXO.TRANSF EXTERNA',8,'EXO.REINTEGRO',9,'EXO.TRANSF INTERNA') TIP_INSCRIPCION,
            a.COD_PROG_OPC_UNO,
            c.NOM_UNIDAD,
            a.COD_PENSUM,
            a.VAL_PAGO,
            a.FEC_PAGO,
            a.NUM_FORMULARIO,
            decode(a.EST_INSCRITO,0,'Pre-inscrito',1,'Inscrito',2,'Admitido',3,'Espera',9,'Rechazado') EST_INSCRITO,
            d.NOM_LARGO
        FROM
            sinu.src_inscrito a,
            SINU.BAS_TERCERO b,
            SINU.SRC_UNI_ACADEMICA c,
            SINU.BAS_TERCERO d
        WHERE
            a.COD_PERIODO='{}'
            and a.MOD_ESTUDIO='1'
            and a.ID_TERCERO=b.ID_TERCERO
            and a.COD_PROG_OPC_UNO=c.COD_UNIDAD
            and a.USU_CREACION=d.ID_TERCERO
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def pagos_derecho_grado(fechai):
    query = '''
        SELECT
            bas_tercero.ID_TERCERO,
            src_enc_liquidacion.num_documento "No. LIQUID VOLANTE",
            bas_tercero.NUM_IDENTIFICACION,
            bas_tercero.pri_apellido ||' '|| bas_tercero.seg_apellido "APELLIDOS",
            bas_tercero.NOM_TERCERO ||' '|| bas_tercero.seg_nombre "NOMBRES",
            B.NOM_CONCEPTO,
            src_uni_academica.COD_UNIDAD,
            src_uni_academica.NOM_UNIDAD,
            A.val_liquidado "VAL_LIQUIDADO_1",
            src_enc_liquidacion.val_liquidado,
            src_enc_liquidacion.val_pagado,
            src_enc_liquidacion.fec_liquidacion,
            src_enc_liquidacion.fec_pago,
            src_enc_liquidacion.COD_PERIODO
        FROM
            sinu.src_det_liquidacion A
            LEFT JOIN sinu.fin_concepto B
            ON A.ID_CONCEPTO = B.ID_CONCEPTO
            LEFT JOIN sinu.src_enc_liquidacion
            ON a.id_enc_liquidacion = sinu.src_enc_liquidacion.id_enc_liquidacion
            LEFT JOIN sinu.src_alum_programa
            ON sinu.src_enc_liquidacion.ID_ALUM_PROGRAMA = sinu.src_alum_programa.ID_ALUM_PROGRAMA
            LEFT JOIN sinu.bas_tercero
            ON sinu.src_alum_programa.ID_TERCERO = sinu.bas_tercero.ID_TERCERO
            LEFT JOIN sinu.src_uni_academica
            ON sinu.src_alum_programa.COD_UNIDAD = sinu.src_uni_academica.COD_UNIDAD
        WHERE
            B.NOM_CONCEPTO like '%DERECHO DE GRADO%'
            AND B.NOM_CONCEPTO not like '%BECA%'
            and sinu.src_enc_liquidacion.fec_pago BETWEEN TO_DATE('{}', 'DD/MM/YYYY') and sysdate
        ORDER BY 4
    '''.format(fechai)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matriculados_por_periodo(periodo, modalidad):
    query = '''
      SELECT
        distinct a.id_alum_programa,
        d.id_tercero,
        d.num_identificacion,
        decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
        d.nom_tercero||' '||d.seg_nombre as Nombres,
        d.pri_apellido||' '||d.seg_apellido Apellidos,
        decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
        ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
        ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
        ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
        ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
        ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
        (select b.id_entidad
        from sinu.bas_col_tercero A, sinu.bas_entidad B
        where a.id_entidad=b.id_entidad
        and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
        (select b.nom_entidad
        from sinu.bas_col_tercero A, sinu.bas_entidad B
        where a.id_entidad=b.id_entidad
        and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
        d.gen_tercero,
        d.fec_nacimiento,
        d.dir_residencia,
        (select bas_geopolitica.nom_div_geopolitica from sinu.bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
        d.tel_residencia,
        d.tel_cecular celular,
        d.num_est_economico estrato,
        d.DIR_EMAIL EMAIL_INSTITUCIONAL,
        d.DIR_EMAIL_PER EMAIL_PERSONAL,
        b.cod_unidad cod_programa,
        b.nom_unidad programa,
        c.num_niv_cursa semestre,
        c.cod_periodo,
        c.EST_MAT_ACA Matatricula_Academica,
        c.est_mat_fin Matricula_Financiera,
        d.eps_tercero cod_eps,
        a.cod_pensum,
        DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
        a.EST_ALUMNO,
        c.tot_uni_matricular,
        c.tot_uni_matriculadas,
        DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad
      FROM
        sinu.src_alum_programa a,
        sinu.src_uni_academica b,
        sinu.src_alum_periodo c,
        sinu.bas_tercero d,
        sinu.bas_geopolitica e,
        sinu.bas_geopolitica f,
        sinu.SRC_ENC_LIQUIDACION g
      WHERE
        a.id_tercero = d.id_tercero
        and a.id_alum_programa = c.id_alum_programa
        and a.cod_unidad = b.cod_unidad
        and d.id_ubi_nac=e.id_geopolitica
        and d.id_ubi_res=f.id_geopolitica
        and c.cod_periodo = '{}'
        and g.COD_PERIODO = c.cod_periodo
        and b.cod_modalidad = '{}'
        and a.est_alumno IN (1,7)
        and c.est_mat_fin=1
        and g.est_liquidacion = 2
        and g.tip_liquidacion = 1
        and a.id_alum_programa = g.id_alum_programa
      ORDER BY 5
    '''.format(periodo, modalidad)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def reporte_financiero(periodo):
    query = '''
      SELECT
      bas_tercero.ID_TERCERO,
      src_alum_programa.ID_ALUM_PROGRAMA,
      src_enc_liquidacion.num_documento "No. LIQUID VOLANTE",
      bas_tercero.NUM_IDENTIFICACION,
      bas_tercero.pri_apellido ||' '|| bas_tercero.seg_apellido "APELLIDOS",
      bas_tercero.NOM_TERCERO ||' '|| bas_tercero.seg_nombre "NOMBRES",
      src_enc_liquidacion.COD_PERIODO,
      b.cod_concepto,
      B.NOM_CONCEPTO,
        src_uni_academica.COD_UNIDAD cod_programa,
        src_uni_academica.NOM_UNIDAD nom_programa,
        A.val_liquidado,
        src_enc_liquidacion.val_pagado,
        src_enc_liquidacion.fec_liquidacion,
        src_enc_liquidacion.fec_pago,
        bas_banco.NOM_BANCO banco
      FROM
        sinu.src_det_liquidacion A
      LEFT JOIN sinu.fin_concepto B
      ON
        A.ID_CONCEPTO = B.ID_CONCEPTO
      LEFT JOIN sinu.src_enc_liquidacion
      ON
      a.id_enc_liquidacion = src_enc_liquidacion.id_enc_liquidacion
      LEFT JOIN sinu.bas_cta_corriente
      ON
      src_enc_liquidacion.ID_CTA_INTERNA = bas_cta_corriente.ID_CTA_CORRIENTE
      LEFT JOIN sinu.bas_banco
      ON
      bas_cta_corriente.ID_BANCO = bas_banco.ID_BANCO
      LEFT JOIN sinu.src_alum_programa
      ON
        src_enc_liquidacion.ID_ALUM_PROGRAMA = src_alum_programa.ID_ALUM_PROGRAMA
      LEFT JOIN sinu.bas_tercero
      ON
        src_alum_programa.ID_TERCERO = bas_tercero.ID_TERCERO
      LEFT JOIN sinu.src_uni_academica
      ON
        src_alum_programa.COD_UNIDAD = src_uni_academica.COD_UNIDAD
      WHERE
        src_enc_liquidacion.COD_PERIODO = '{}'
        and src_uni_academica.cod_modalidad=1
      order by 5
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matriculados_primer_semestre(periodo):
    query = '''
        SELECT distinct d.num_identificacion,
              RTRIM (d.nom_tercero||' '||d.seg_nombre) as Nombres,
              RTRIM (d.pri_apellido||' '||d.seg_apellido) as Apellidos,
              b.cod_unidad cod_programa,b.nom_unidad programa,
              c.num_niv_cursa semestre,
              d.dir_email correo_institucional,
              d.dir_email_per correo_personal,
              d.tel_cecular celular,
              d.tel_residencia telefono,
              d.dir_residencia,
              d.gen_tercero genero,
              d.fec_nacimiento,
              c.cod_periodo,
              decode(h.TIP_INSCRIPCION,1,'NORMAL',2,'TRANSFERENCIA INTERNA',3,'TRANSFERENCIA EXTERNA',4,'RESERVA CUPO',5,'REINTEGRO',6,'EXO.NORMAL',7,
              'EXO.TRANSF EXTERNA',8,'EXO.REINTEGRO',9,'EXO.TRANSF INTERNA') tipo_inscripcion,
              DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad,
              h.cod_periodo periodo,
              g.fec_pago
        FROM
          sinu.src_alum_programa a
          LEFT JOIN  sinu.bas_tercero d on a.id_tercero = d.id_tercero
          LEFT JOIN  sinu.src_alum_periodo c on a.id_alum_programa = c.id_alum_programa
          LEFT JOIN  sinu.src_uni_academica b on a.cod_unidad = b.cod_unidad
          LEFT JOIN  sinu.src_enc_liquidacion g on g.cod_periodo = c.cod_periodo
          LEFT JOIN  sinu.src_formulario h on d.num_identificacion = h.num_identificacion and g.cod_periodo = h.cod_periodo
        WHERE
            b.cod_modalidad = '1'
            and a.est_alumno IN (1,7)
            and (c.est_mat_fin = 1 or c.est_mat_fin = 0)
            and g.est_liquidacion = 2
            and g.tip_liquidacion = 1
            and a.id_alum_programa = g.id_alum_programa
            and c.num_niv_cursa = '1'
            and c.COD_PERIODO = '{}'
            and h.cod_modalidad = '1'
            and h.TIP_INSCRIPCION != '5'
            --and h.TIP_INSCRIPCION is not null
            order by 3
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

#  Asignaturas por programa - NO incluye las materias electivas


def asignaturas_programa_validaciones(identificacion, programa):
    query = '''
    SELECT DISTINCT
    --a.id_alum_programa,
    --a.cod_unidad,
        a.COD_MATERIA,
        e.nom_materia,
        a.cod_pensum,
        --(select sap.cod_pensum from src_alum_programa sap where sap.id_tercero = c.id_tercero and sap.cod_unidad = a.cod_unidad and sap.est_alumno = 1) codigo_pensum,
        a.NUM_NIVEL semestre_materia
    FROM
        sinu.src_semaforo a,
        sinu.src_alum_programa b,
        sinu.bas_tercero c,
        sinu.src_alum_periodo d,
        sinu.src_materia e,
        sinu.src_uni_academica f
    WHERE
        a.id_alum_programa = b.id_alum_programa AND
        b.est_alumno = 1 and
        b.id_tercero = c.id_tercero AND
        b.id_alum_programa = d.id_alum_programa AND
        a.cod_materia = e.cod_materia AND
        a.cod_unidad = f.cod_unidad AND
        --d.est_mat_aca='1' AND
        --d.est_mat_fin = '1' AND
        f.cod_modalidad in ('1','3') AND
        a.IND_APROBADA = '0' AND
        c.num_identificacion = '{}' AND
        b.cod_unidad = '{}'
    order by 3
  '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# Numero de validaciones ralizadas por el estudiante


def cantidad_validaciones(identifiacion, programa):
    query = '''
    SELECT COUNT(*)
        cantidad_validaciones
    FROM
        sinu.src_vis_dat_historicos
    WHERE
        id_tercero in (select id_tercero
    FROM
        sinu.bas_tercero
    WHERE
        num_identificacion = '{}')
    AND
        tip_nota = 'V' -- V - Validacion
    AND
        cod_unidad = '{}'
  '''.format(identifiacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# Cantidad de Materias por pensum activos - Programas de Pregrado


def cantidad_materias_pensum(programa, pensum):
    query = '''
    select A.cod_unidad_pk cod_programa,
    A.nom_unidad programa,
    A.cod_pensum_pk cod_pensum,
    A.nom_pensum,
    COUNT(*) cantidad_materias
    from sinu.src_vis_mat_pensum_web A
    LEFT JOIN sinu.src_uni_academica B ON A.cod_unidad_pk = B.cod_unidad
    where B.cod_modalidad = '1' AND a.cod_unidad_pk = '{}' AND a.cod_pensum_pk = '{}'
    GROUP BY A.cod_unidad_pk,A.nom_unidad, A.cod_pensum_pk, A.nom_pensum
    ORDER BY 1
  '''.format(programa, pensum)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# Debemos retornar las siguiente información, nombre, apellido, programa, pensum y código de pensum, pasando por parámetro el numero identificaron del estudiante.


def informacion_estudiante_validaciones(identifiacion, programa):
    query = '''
    SELECT
      bas.num_identificacion identificacion, bas.nom_tercero nombre,
      bas.pri_apellido, bas.seg_apellido,pro.cod_unidad cod_programa,uni.nom_unidad programa, pro.cod_pensum pensum, pro.est_alumno
    FROM
      sinu.bas_tercero bas
    LEFT JOIN
      sinu.SRC_ALUM_PROGRAMA pro
    ON bas.id_tercero = pro.id_tercero
    LEFT JOIN
      sinu.src_uni_academica uni
    ON pro.cod_unidad = uni.cod_unidad
    WHERE
      --pro.est_alumno = '1' --estado activo
    --AND
    uni.cod_modalidad in ('1','3')
    AND bas.num_identificacion = '{}'
    AND pro.cod_unidad = '{}'
    and pro.est_alumno = 1
    order by 3
  '''.format(identifiacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall();

# Numero de creditos por validacion realizada (opcion 1)


def cantidad_creditos_validaciones(identificacion, programa):
    query = '''
    select COUNT(*) cantidad_validaciones, SUM(mat.uni_teorica)cantidad_creditos
    from sinu.src_vis_dat_historicos dat LEFT JOIN sinu.src_mat_pensum mat
    ON dat.cod_unidad = mat.cod_unidad
    AND dat.cod_pensum = mat.cod_pensum
    AND dat.cod_materia = mat.cod_materia
    where dat.id_tercero in (select id_tercero
        from sinu.bas_tercero
        where num_identificacion = '{}')
    AND dat.cod_unidad = '{}'
    AND dat.tip_nota = 'V' -- V - Validacion
    GROUP BY dat.id_tercero
  '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


#  Numero de creditos por pemsum

def cantidad_creditos_materias(programa, pensum):
    query = '''
    select A.cod_unidad_pk cod_programa,
    A.nom_unidad programa,
    A.cod_pensum_pk cod_pensum,
    A.nom_pensum,
    COUNT(*) cantidad_materias,
    (select sum(uni_teorica)
    from sinu.src_mat_pensum
    where est_materia = '1'
    AND cod_unidad = A.cod_unidad_pk
    AND cod_pensum = A.cod_pensum_pk) cantidad_creditos
    from sinu.src_vis_mat_pensum_web A
    LEFT JOIN sinu.src_uni_academica B ON A.cod_unidad_pk = B.cod_unidad
    where B.cod_modalidad = '1'
    AND A.cod_unidad_pk = '{}'
    AND A.cod_pensum_pk = '{}'
    GROUP BY A.cod_unidad_pk,A.nom_unidad, A.cod_pensum_pk, A.nom_pensum
    ORDER BY 1
  '''.format(programa, pensum)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


# Materias electivas

def materias_electivas(codigomateria, programa, pensum):
  #   query = '''
  #   select DISTINCT
  #   B.COD_UNIDAD Cod_Programa, D.NOM_UNIDAD Programa, b.cod_pensum,b.num_nivel semestre,
  #   A.COD_MATERIA, A.NOM_MATERIA,b.uni_teorica creditos, C.MAT_EQUIVALE,
  #   (select nom_materia from sinu.src_materia where C.MAT_EQUIVALE = cod_materia) materia_equivalente,
  #   c.uni_equivale programa_equivale,
  #   pen_equivale,
  #   c.est_equ Estado,
  #   decode(c.est_equ,1,'Activo',0,'Inactivo') Desc_Estado
  #   from sinu.src_materia A
  #   LEFT JOIN sinu.SRC_MAT_PENSUM B
  #   ON A.COD_MATERIA = B.COD_MATERIA
  #   LEFT JOIN sinu.SRC_EQU_MATERIA C
  #   ON A.COD_MATERIA = C.COD_MATERIA
  #   LEFT JOIN sinu.SRC_UNI_ACADEMICA D
  #   ON B.COD_UNIDAD = D.COD_UNIDAD
  #   where
  #   C.cod_unidad = b.cod_unidad
  #   and C.cod_pensum   = b.cod_pensum
  #   and C.cod_materia  = b.cod_materia
  #   AND d.cod_modalidad = '1'
  #   AND c.est_equ = '1'
  #   AND c.fec_inicio is not null
  #   AND b.cod_materia = '{}'
  #   AND B.COD_UNIDAD = '{}'
  #   AND b.cod_pensum = '{}'
  #   order by 2
  # '''.format(codigomateria, programa, pensum)
    query = '''
      select DISTINCT
      B.COD_UNIDAD Cod_Programa, D.NOM_UNIDAD Programa, b.cod_pensum,b.num_nivel semestre,
      A.COD_MATERIA, A.NOM_MATERIA,b.uni_teorica creditos, C.MAT_EQUIVALE,
      (select nom_materia from sinu.src_materia where C.MAT_EQUIVALE = cod_materia) materia_equivalente,
      c.uni_equivale programa_equivale,
      pen_equivale,
      c.est_equ Estado,
      decode(c.est_equ,1,'Activo',0,'Inactivo') Desc_Estado
      from sinu.src_materia A
      LEFT JOIN sinu.SRC_MAT_PENSUM B
      ON A.COD_MATERIA = B.COD_MATERIA
      LEFT JOIN 
      (
      select distinct mat_equivale,cod_materia, cod_unidad, cod_pensum,uni_equivale, pen_equivale,est_equ,fec_inicio
        from
                  (
                      select  mat_equivale mat_equivale, cod_materia cod_materia, cod_unidad cod_unidad,uni_equivale uni_equivale, cod_pensum cod_pensum, pen_equivale pen_equivale,est_equ est_equ,fec_inicio  from sinu.src_equ_materia
                      union all
                      select  cod_materia mat_equivale, mat_equivale cod_materia, uni_equivale cod_unidad, cod_unidad uni_equivale, pen_equivale cod_pensum, cod_pensum pen_equivale,est_equ est_equ,fec_inicio from sinu.src_equ_materia 
                  )          

              ) 
      C ON A.COD_MATERIA = C.COD_MATERIA
      LEFT JOIN sinu.SRC_UNI_ACADEMICA D
      ON B.COD_UNIDAD = D.COD_UNIDAD
      where
      C.cod_unidad = b.cod_unidad
      and C.cod_pensum   = b.cod_pensum
      and C.cod_materia  = b.cod_materia
      AND d.cod_modalidad = '1'
      AND c.est_equ = '1'
      AND c.fec_inicio is not null
      AND b.cod_materia = '{}'
      AND B.COD_UNIDAD = '{}'
      AND b.cod_pensum = '{}'
      order by 2
  '''.format(codigomateria, programa, pensum)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# datos estudiantes


def validar_estudiantes(identificacion):
    query = '''
    SELECT DISTINCT
    a.num_identificacion Documento,
    a.nom_tercero,
    a.seg_nombre,
    a.pri_apellido,
    a.seg_apellido,
    a.dir_email_per Correo_Personal,
    c.cod_unidad
    FROM sinu.bas_tercero a,
    sinu.src_inscrito b,
    sinu.src_uni_academica c,
    sinu.src_enc_res_admision d
    WHERE a.id_tercero = b.id_tercero
    AND c.cod_unidad = b.cod_prog_opc_uno
    AND d.id_inscripcion= b.id_inscripcion
    --AND a.dir_email_per = ''
    AND a.num_identificacion = ('{}')
    AND b.mod_estudio =('1')
    AND b.est_inscrito =('2')
    order by 2 '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def estudiantesVinculados(idGrupo):
    query = '''
    SELECT
      a.nom_largo,
      a.pri_apellido,
      a.seg_apellido,
      a.num_identificacion identificacion,
      a.id_tercero
    FROM sinu.bas_tercero a,
    sinu.src_alum_programa b,
    sinu.src_uni_academica c,
    sinu.src_alum_periodo d,
    sinu.src_enc_matricula e ,
    sinu.src_grupo f,
    sinu.src_mat_pensum g,
    sinu.src_vinculacion h,
    sinu.bas_tercero i
    WHERE 1=1
    AND a.id_tercero=b.id_tercero
    AND b.cod_unidad=c.cod_unidad
    AND b.id_alum_programa=d.id_alum_programa
    AND b.id_alum_programa=e.id_alum_programa
    AND f.cod_unidad=g.cod_unidad
    AND f.cod_pensum=g.cod_pensum
    AND f.cod_materia=g.cod_materia
    AND e.id_grupo=f.id_grupo
    AND f.id_vinculacion = h.id_vinculacion(+)
    AND h.id_tercero=i.id_tercero(+)
    AND b.est_alumno IN (1,7)
    --AND d.cod_periodo='20212'
    AND e.cod_periodo=d.cod_periodo
    AND d.est_mat_fin=1
    --AND c.cod_modalidad=1
    AND e.id_grupo = '{}'
    '''.format(idGrupo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def docentesMaterias(periodo, identificacion):
    query = '''
  SELECT
    C.num_identificacion identificacion_doc,
    d.cod_materia,
    (select nom_materia from sinu.src_materia where D.cod_materia = cod_materia) materia,
    A.id_grupo cod_grupo,
    D.num_grupo grupo,
    (select num_nivel from sinu.src_mat_pensum where d.cod_materia = cod_materia and rownum <2) semestre,
    d.cod_unidad cod_programa,
    (select nom_unidad from sinu.src_uni_academica where d.cod_unidad = cod_unidad) nom_programa,
    CONCAT(d.cod_materia,A.id_grupo) id
    FROM sinu.src_doc_grupo A
    LEFT JOIN sinu.SRC_VINCULACION B ON A.id_vinculacion = B.ID_VINCULACION
    LEFT JOIN sinu.BAS_TERCERO C ON B.id_tercero = C.id_tercero
    LEFT JOIN sinu.src_grupo D ON A.id_grupo = D.id_grupo
  WHERE
    C.num_identificacion = '{}'
    AND D.cod_periodo = '{}'
  '''.format(identificacion, periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def obtenerInformacionSICUC(identificacion):
    query = '''
    SELECT
      a.num_identificacion,
      a.nom_largo,
      a.nom_tercero,
      a.pri_apellido,
      a.seg_apellido,
      a.dir_email,
      REPLACE(a.dir_email,'@cuc.edu.co','')usuario,
      b.cod_unidad,
      c.nom_unidad
      --decode (b.est_alumno, 0, 'INACTIVO', 1, 'ACTIVO',2,'EGRESADO',3, 'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO') "ESTADO"
    FROM sinu.bas_tercero a, sinu.src_alum_programa b, sinu.src_uni_academica c
    WHERE a.id_tercero = b.id_tercero
      AND b.cod_unidad = c.cod_unidad
      AND c.cod_modalidad=1
      AND a.num_identificacion ='{}'
      ORDER BY 2 '''.format(identificacion)

    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def obtenerIdTercero(identificacion):
    query = '''
    SELECT id_tercero
    FROM sinu.bas_tercero
    WHERE num_identificacion IN ({}) AND id_tercero IS NOT NULL
    '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def admitidos_periodo(periodo):
    query = '''
      SELECT DISTINCT
        A.ID_TERCERO,
        A.NOM_LARGO Nombre_Estudiante,
        A.NUM_IDENTIFICACION Documento,
        A.TEL_CECULAR Celular,
        A.DIR_EMAIL_PER Correo_Personal,
        A.DIR_EMAIL Correo_Institucional,
        B.COD_PROG_OPC_UNO Cod_Programa,
        C.NOM_UNIDAD Programa,
        B.COD_PERIODO,
        B.FEC_INSCRIPCION,
        B.FEC_PAGO,
        DECODE (B.EST_INSCRITO,  1,'INSCRITO',  2,'ADMITIDO',  3,'EN ESPERA',  9,'RECHAZADO', 0,'ANULADO')    EST_INSCRITO,
        (select nom_tabla
        from sinu.src_generica
        where TIP_TABLA = 'TIPINS'
        and cod_tabla = B.TIP_INSCRIPCION)TIP_INSCRIPCION
      FROM sinu.BAS_TERCERO A,
        sinu.SRC_INSCRITO B,
        sinu.SRC_UNI_ACADEMICA C,
        sinu.SRC_ENC_RES_ADMISION D
      WHERE A.ID_TERCERO = B.ID_TERCERO
        AND C.COD_UNIDAD = B.COD_PROG_OPC_UNO
        AND D.ID_INSCRIPCION = B.ID_INSCRIPCION
        AND B.ID_SEDE = C.ID_SEDE
        AND B.COD_PERIODO = '{}'
        AND B.MOD_ESTUDIO = '1'
        AND B.EST_INSCRITO = '2'
        order by 2
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def notas_por_corte(periodo):
    query = '''
      SELECT
        a.id_alum_programa,
        e.num_identificacion,
        e.nom_largo Estudiante,
        c.nom_unidad Programa,
        a.id_grupo,
        b.num_grupo,
        b.cod_materia,
        f.nom_materia,
        g.id_tercero,
        g.NUM_IDENTIFICACION CC_DOCENTE,
        g.nom_largo docente,
        g.dir_email_per Email_personal,
        g.dir_email Email_institucional,
        (select PES_NOTA
        from sinu.src_not_grupo
        where src_not_grupo.id_grupo = b.id_grupo
        and src_not_grupo.NUM_NOTA = a.num_nota and rownum<=1) peso,
        a.num_nota nota,
        decode(a.val_nota,null,'-----',to_char(a.val_nota, '99D9')) numérica,
        b.cod_periodo
      FROM
        sinu.src_det_matricula a,
        sinu.src_grupo b,
        sinu.src_uni_academica c,
        sinu.src_alum_programa d,
        sinu.bas_tercero e,
        sinu.src_materia f,
        sinu.src_vinculacion H,
        sinu.bas_tercero g
      WHERE a.id_alum_programa = d.id_alum_programa
        and d.id_alum_programa = a.id_alum_programa
        and e.id_tercero = d.id_tercero
        and b.id_grupo   = a.id_grupo
        and c.cod_unidad = d.cod_unidad
        AND b.id_vinculacion = H.id_vinculacion(+)
        AND H.id_tercero = g.id_tercero (+)
        and f.cod_materia = b.cod_materia
        and b.cod_periodo = '{}'
        order by 3
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def carga_academica_periodo(periodo):
    query = '''      
   
  select distinct e.id_tercero,
      (select nom_largo from sinu.bas_tercero where id_tercero=e.id_tercero) "Nombre_Docente",
      (select num_identificacion from sinu.bas_tercero where id_tercero=e.id_tercero) "Num_Identificacion",
      a.cod_unidad,
      c.nom_unidad ||' '||g.nom_jornada nom_unidad,
      b.uni_teorica,
      b.num_nivel,
      a.cod_materia,
      b.nom_materia,
      B.COD_PENSUM,
      a.id_grupo,
      a.num_grupo,
      i.id_div_grupo id_subgrupo,
      i.cod_div_grupo sub_grupo,
      DECODE(h.tip_docente,1,'Principal',2,'Suplente') Rol,
      (select unique e.nom_cargo
      from sinu.bas_tercero a,
      sinu.src_vinculacion b,
      sinu.bas_dependencia c,
      sinu.bas_cargo e
      where a.id_tercero = b.id_tercero
      and c.id_dependencia = decode(b.id_dependencia,null,c.id_dependencia,b.id_dependencia)
      and e.id_cargo = decode(b.id_cargo,null,e.id_cargo,b.id_cargo)
      and b.id_vinculacion=a.id_vinculacion and rownum<=1
      and e.nom_cargo like '%PRO%'
      ) "Cargo"
      from   sinu.SRC_GRUPO A, sinu.SRC_MAT_PENSUM B, sinu.SRC_UNI_ACADEMICA C, sinu.src_hor_grupo d,
      sinu.src_vinculacion e,  sinu.src_jornada g, sinu.src_doc_grupo h,  sinu.SRC_DIV_GRUPO i
      where  a.cod_periodo= '{}'
      and    a.cod_unidad = b.cod_unidad
      and    a.cod_pensum = b.cod_pensum
      and    a.cod_materia= b.cod_materia
      and    a.cod_unidad = c.cod_unidad
      and    a.id_grupo   = d.id_grupo (+)
      and    a.id_vinculacion (+) = e.id_vinculacion
      and    c.id_jornada = g.id_jornada
      and    a.id_vinculacion = h.id_vinculacion
      and    a.id_grupo = h.id_grupo
      and  c.nom_unidad not like '%ESPECI%'
      and  c.nom_unidad not like '%DIPL%'
      and (d.id_div_grupo     = i.id_div_grupo(+))
      and c.nom_unidad not like '%CURS%'
      group by e.id_tercero,a.cod_unidad, c.nom_unidad,b.uni_teorica,b.num_nivel, a.cod_materia, b.nom_materia, a.id_grupo,a.num_grupo, d.num_dia,
      to_char(d.fec_inicio,'day'), sinu.funb_hora_militar(d.hor_inicio), sinu.funb_hora_militar(
          d.hor_fin), g.nom_jornada, a.id_vinculacion, h.tip_docente, i.id_div_grupo,
      i.cod_div_grupo, b.cod_pensum
      order by   "Nombre_Docente"
          
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


# def matricula_financiera(periodo):
# query = '''
#       SELECT
#         d.num_identificacion,
#         d.nom_largo nombres,
#         c.cod_unidad cod_programa,
#         e.nom_unidad,
#         a.cod_periodo,
#         a.num_documento liquidacion,
#         f.nom_concepto,
#         decode(f.tip_concepto,1,b.val_liquidado,0) val_cobros,
#         decode(f.tip_concepto,2,b.val_liquidado,0) val_descuentos,
#         decode(f.tip_concepto,1,(case when a.val_liquidado < 0 then 0 else a.val_liquidado end),0) val_Pago,
#         decode(f.tip_concepto,1,decode(a.est_liquidacion,1,'Sin pago','Pagada')) est_pago,
#         a.fec_pago pago_matricula,
#         f.tip_concepto
#       FROM
#         SINU.SRC_ENC_LIQUIDACION a,
#         SINU.SRC_DET_LIQUIDACION b,
#         SINU.SRC_ALUM_PROGRAMA c,
#         SINU.BAS_TERCERO d,
#         SINU.SRC_UNI_ACADEMICA e,
#         SINU.FIN_CONCEPTO f,
#         SINU.SRC_ALUM_PERIODO g,
#         SINU.SRC_SEDE h,
#         SINU.SRC_SECCIONAL i
#       WHERE
#         a.id_enc_liquidacion = b.id_enc_liquidacion
#         and a.id_alum_programa  = c.id_alum_programa
#         and c.id_tercero = d.id_tercero
#         and c.cod_unidad = e.cod_unidad
#         and b.id_concepto = f.id_concepto
#         and a.id_alum_programa = g.id_alum_programa
#         and a.cod_periodo = g.cod_periodo
#         and a.tip_liquidacion = 1
#         and a.cod_periodo = '{}'
#         and e.id_sede = h.id_sede
#         and h.id_seccional = i.id_seccional
#       order by 2
#     '''

def matricula_financiera_ingles(consulta):
    query = '''
    SELECT 
bas_tercero.ID_TERCERO,
src_alum_programa.ID_ALUM_PROGRAMA,
src_enc_liquidacion.num_documento "No. LIQUID VOLANTE",
bas_tercero.NUM_IDENTIFICACION,
bas_tercero.pri_apellido ||' '|| bas_tercero.seg_apellido "APELLIDOS",
bas_tercero.NOM_TERCERO ||' '|| bas_tercero.seg_nombre "NOMBRES",
src_enc_liquidacion.COD_PERIODO,
b.cod_concepto,
B.NOM_CONCEPTO,
  src_uni_academica.COD_UNIDAD cod_programa,
  src_uni_academica.NOM_UNIDAD nom_programa,
  A.val_liquidado,
  src_enc_liquidacion.val_pagado,
  src_enc_liquidacion.fec_liquidacion,
  src_enc_liquidacion.fec_pago,
  bas_banco.NOM_BANCO banco
FROM 
  sinu.src_det_liquidacion A
LEFT JOIN sinu.fin_concepto B
ON
  A.ID_CONCEPTO = B.ID_CONCEPTO

LEFT JOIN sinu.src_enc_liquidacion
ON 
 a.id_enc_liquidacion = src_enc_liquidacion.id_enc_liquidacion

LEFT JOIN sinu.bas_cta_corriente
ON 
 src_enc_liquidacion.ID_CTA_INTERNA = bas_cta_corriente.ID_CTA_CORRIENTE

LEFT JOIN sinu.bas_banco
ON 
 bas_cta_corriente.ID_BANCO = bas_banco.ID_BANCO

LEFT JOIN sinu.src_alum_programa
ON
  src_enc_liquidacion.ID_ALUM_PROGRAMA = src_alum_programa.ID_ALUM_PROGRAMA

LEFT JOIN sinu.bas_tercero
ON
  src_alum_programa.ID_TERCERO = bas_tercero.ID_TERCERO

LEFT JOIN sinu.src_uni_academica
ON
  src_alum_programa.COD_UNIDAD = src_uni_academica.COD_UNIDAD
WHERE {}
order by 5
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matricula_financiera_pregrado(consulta):
    query = '''
    SELECT
    bas_tercero.ID_TERCERO,
    src_enc_liquidacion.num_documento "No. LIQUID VOLANTE",
    bas_tercero.NUM_IDENTIFICACION,
    bas_tercero.pri_apellido ||' '|| bas_tercero.seg_apellido "APELLIDOS",
    bas_tercero.NOM_TERCERO ||' '|| bas_tercero.seg_nombre "NOMBRES",
    src_enc_liquidacion.COD_PERIODO,
    b.cod_concepto,
    B.NOM_CONCEPTO,
    src_uni_academica.COD_UNIDAD cod_programa,
    src_uni_academica.NOM_UNIDAD nom_programa,
    A.val_liquidado,
    src_enc_liquidacion.val_pagado,
    src_enc_liquidacion.fec_liquidacion,
    src_enc_liquidacion.fec_pago,
    bas_banco.NOM_BANCO banco
    FROM sinu.src_det_liquidacion A
    INNER JOIN sinu.fin_concepto B
    ON
    A.ID_CONCEPTO = B.ID_CONCEPTO
    INNER JOIN sinu.src_enc_liquidacion
    ON
    a.id_enc_liquidacion = src_enc_liquidacion.id_enc_liquidacion
    INNER JOIN sinu.bas_cta_corriente
    ON
    src_enc_liquidacion.ID_CTA_INTERNA = bas_cta_corriente.ID_CTA_CORRIENTE
    INNER JOIN sinu.bas_banco
    ON
    bas_cta_corriente.ID_BANCO = bas_banco.ID_BANCO
    INNER JOIN sinu.src_alum_programa
    ON
    src_enc_liquidacion.ID_ALUM_PROGRAMA = src_alum_programa.ID_ALUM_PROGRAMA
    INNER JOIN sinu.bas_tercero
    ON
    src_alum_programa.ID_TERCERO = bas_tercero.ID_TERCERO
    INNER JOIN sinu.src_uni_academica
    ON
    src_alum_programa.COD_UNIDAD = src_uni_academica.COD_UNIDAD
    WHERE
    {}
    and src_uni_academica.cod_modalidad=1
    order by 4
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matricula_academica(consulta):
    query = '''
    SELECT DISTINCT
    c.id_tercero,
    b.id_alum_programa,
    C.num_identificacion,
    C.nom_largo alumno,
    c.gen_tercero genero,
    c.dir_email_per email_personal,
    c.dir_email email_institucional,
    a.est_alumno,
    a.cod_unidad,
    j.nom_unidad,
    j.cod_modalidad,
    a.cod_pensum,
    b.cod_periodo,
    D.cod_materia,
    d.id_grupo,
    l.cod_div_grupo nom_subgrupo,
    --(select id_div_grupo||'|'||cod_div_grupo from src_div_grupo where id_div_grupo = i.id_div_grupo)codigo_del_grupo, i.id_horario,
    --i.id_div_grupo id_subgrupo,
    NVL(D.num_grupo,0) num_grupo,
    E.nom_materia,
    e.int_horaria,
    i.num_dia,
    DECODE (i.num_dia,2,'Lunes',3,'Martes',4,'Miercoles',5,'Jueves',6,'Viernes',7,'Sabado',1,'Domingo') dia,
    sinu.funb_hora_militar (i.hor_inicio) hor_inicio,
    sinu.funb_hora_militar(i.hor_fin) hor_fin,
    E.num_nivel,
    F.id_tercero id_tercero_docente,
    F.num_identificacion NUM_IDENTIFICACION_DOCENTE,
    F.nom_largo docente,
    f.dir_email,
    G.cod_aula,
    D.id_jornada,
    J.id_dependencia,
    b.cod_materia mat_pensum,
    b.ind_operacion
    FROM sinu.SRC_ALUM_PROGRAMA A
    LEFT JOIN sinu.SRC_ENC_MATRICULA B
    ON B.id_alum_programa = A.id_alum_programa
    LEFT JOIN sinu.BAS_TERCERO C
    ON A.id_tercero = C.id_tercero
    LEFT JOIN sinu.SRC_GRUPO D
    ON B.id_grupo = D.id_grupo
    LEFT JOIN sinu.SRC_MAT_PENSUM E
    ON d.cod_unidad = E.cod_unidad AND d.cod_pensum = E.cod_pensum AND D.cod_materia = E.cod_materia
    LEFT JOIN sinu.SRC_AULA G
    ON D.id_aula = G.id_aula
    LEFT JOIN sinu.SRC_VINCULACION H
    ON D.id_vinculacion = H.id_vinculacion
    LEFT JOIN sinu.BAS_TERCERO F
    ON H.id_tercero = F.id_tercero
    LEFT JOIN sinu.SRC_UNI_ACADEMICA J
    ON A.cod_unidad = J.cod_unidad
    LEFT JOIN sinu.src_hor_grupo I
    ON D.id_grupo = i.id_grupo and nvl(b.id_div_grupo,0) = nvl(i.id_div_grupo,0)
    LEFT JOIN sinu.SRC_DIV_GRUPO L
    ON i.id_div_grupo = l.id_div_grupo
    WHERE
    {}
    and a.cod_unidad not in ('17034','17033','31132','31139')
    order by 3
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def definitivas(periodo, consulta):
    query = '''
        select  
        F.id_tercero,
        A.id_alum_programa,
        F.num_identificacion,
        F.nom_largo Alumno,
        G.EST_ALUMNO,
        G.COD_UNIDAD,
        C.nom_unidad, 
        B.id_grupo, 
        B.cod_pensum, 
        B.cod_periodo, 
        B.num_grupo, 
        B.cod_materia, 
        D.nom_materia,
        D.NUM_NIVEL,
        H.id_tercero id_tercero_docente,
        H.num_identificacion num_identificacion_docente,
        H.nom_largo Docente, 
        DECODE(A.def_historia,NULL,'----',to_char(A.def_historia, '0D9')) def_historia,
        A.NUM_FALLAS,
        A.EST_MATERIA matricula,
        DECODE(a.est_materia,1,'PRIMERA VEZ',2,'SEGUNDA VEZ',3,'TERCERA VEZ',4,'CUARTA VEZ',6,'QUINTA VEZ',7,'SEXTA VEZ',8,'SEPTIMA VEZ',9,'OCTAVA VEZ',10,'NOVENA VEZ',1,'PRIMERA VEZ',2,'SEGUNDA VEZ',5,'CANCELADA') est_matricula,
        d.int_horaria,
        d.uni_teorica Creditos,
        (select distinct num_niv_cursa 
        from sinu.src_alum_periodo 
        where cod_periodo = '{}' 
        and id_alum_programa in (select id_alum_programa 
                                 from sinu.src_alum_programa
                                 where id_tercero=f.id_tercero) and rownum<2) as Nivel_estudiante
        from   
            sinu.src_his_academica A, 
            sinu.src_grupo B, 
            sinu.src_uni_academica C, 
            sinu.src_mat_pensum D, 
            sinu.src_vinculacion E, 
            sinu.bas_tercero F, 
            sinu.src_alum_programa G, 
            sinu.bas_tercero H 
        where   G.cod_unidad = C.cod_unidad and 
        B.cod_unidad = D.cod_unidad and 
        B.cod_pensum = D.cod_pensum and 
        B.cod_materia = D.cod_materia and 
        B.id_vinculacion = E.id_vinculacion(+) and 
        E.id_tercero = H.id_tercero and 
        B.id_grupo = A.id_grupo and 
        A.id_alum_programa = G.id_alum_programa and 
        G.id_tercero = F.id_tercero
        {}
        order by 4
    '''.format(periodo, consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def reporte_promedio_acumulado(consulta):
    query = '''
    select a.num_identificacion, a.nom_largo,
    v.num_niv_cursa, v.cod_periodo,b.est_alumno, v.tot_uni_matricular, v.tot_uni_matriculadas,
    (v.tot_uni_matriculadas-v.tot_uni_pierde) TOT_UNI_APROBADAS, v.pro_nivel, v.pro_acumulado, d.nom_unidad, v.tot_uni_matriculadas "TOT_UNI_CURSADAS"
    from sinu.bas_tercero a,
    sinu.src_alum_programa b,
    sinu.src_uni_academica d, 
    sinu.src_vis_alum_per_est_web v
    where
    a.id_tercero=b.id_tercero
    and b.id_alum_programa=v.id_aLum_programa
    {}
    and b.cod_unidad=d.cod_unidad
    and v.est_mat_fin='1'
    and v.est_mat_aca='1'
    and b.est_alumno='1'
    and d.nom_unidad not like 'BIENESTAR%'
    order by 2
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def historia_academica(consulta):
    query = '''
        select
       a.id_alum_programa,
       g.ID_TERCERO,
       g.num_identificacion,
       g.nom_largo,
       a.cod_periodo periodo,
       b.cod_unidad,
       h.nom_unidad programa,
       b.cod_pensum pensum,
       a.cod_materia,
       c.nom_materia,
       c.num_nivel,
       c.int_horaria,
       c.uni_teorica creditos,
       a.cod_uni_e Cod_Programa_Equivalente,
       a.cod_pen_e,
       a.cod_materia_e Cod_Asignatura_Equivalente,
       (select nom_materia from sinu.src_materia
        where cod_materia = a.cod_materia_e) Asignatura_Equivalente,
       decode (tip_periodo,'N','Normal','Vacacional') tipo_periodo,
       v.pro_nivel, 
       v.pro_acumulado,
       a.tip_nota,
       e.nom_tabla tipo_nota,
       d.num_niv_cursa sem_cursada,
       f.nom_tabla est_materia,
       a.def_historia,
       a.ind_aprobada,
       decode(a.ind_aprobada,1,'Si','No') aprobada,
        v.tot_uni_matricular,
        v.tot_uni_matriculadas,
       (v.tot_uni_matriculadas-v.tot_uni_pierde) TOT_UNI_APROBADAS,
        v.tot_uni_matriculadas "TOT_UNI_CURSADAS",
       nvl(c.val_posibles,
        (select decode(c.tip_nota,'N',x.val_posibles,x.val_posibles_alfa)
         from sinu.SRC_REGLAMENTO x,
              sinu.SRC_PENSUM y
         where x.id_reglamento = y.id_reglamento
         and y.cod_pensum      = c.cod_pensum
         and y.cod_unidad      = c.cod_unidad)) val_posibles,
         decode (b.est_alumno,0,'INACTIVO',1,'ACTIVO',2,'EGRESADO',3,'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO',12,'GRADUADO TEMPORAL')"ESTADO"
    from sinu.SRC_HIS_ACADEMICA a,
        sinu.SRC_ALUM_PROGRAMA b,
        sinu.SRC_MAT_PENSUM c,
        sinu.BAS_TERCERO g,
        sinu.SRC_UNI_ACADEMICA h,
        sinu.SRC_ALUM_PERIODO d,
        sinu.SRC_GENERICA e,
        sinu.SRC_GENERICA f,
        sinu.src_vis_alum_per_est_web v
    where a.id_alum_programa = b.id_alum_programa
        and b.cod_unidad         = c.cod_unidad
        and b.cod_pensum         = c.cod_pensum
        and a.cod_materia        = c.cod_materia
        and b.cod_unidad         = h.cod_unidad
        and b.id_tercero         = g.id_tercero
        and e.tip_tabla          = 'TIPNOT'
        and e.cod_tabla          <> e.tip_tabla
        and e.cod_tabla          = a.tip_nota
        and f.tip_tabla          = 'ESTMAT'
        and f.cod_tabla          <> f.tip_tabla
        and f.cod_tabla          = a.est_materia
        and a.id_alum_programa   = d.id_alum_programa(+)
        and a.per_acumula        = d.cod_periodo(+)
        {}
        and b.id_alum_programa=v.id_alum_programa 
 order by 3
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def reporte_semaforo(consulta):
    query = '''
      select distinct  
        a.ID_ALUM_PROGRAMA,
        b.id_tercero,
        c.num_identificacion, 
        c.nom_largo, 
        a.COD_MATERIA,
        e.nom_materia, 
        a.NUM_NOTA,
        a.TIP_NOTA, 
        a.NUM_NIVEL,
        a.IND_APROBADA, 
        a.COD_UNIDAD, 
        f.nom_unidad,
        a.cod_pensum, 
        a.COD_PERIODO, 
        d.est_mat_fin,
        d.est_alumno, 
        d.cod_periodo Periodo_Actual
        from 
          sinu.src_semaforo a,
          sinu.src_alum_programa b, 
          sinu.bas_tercero c, 
          sinu.src_alum_periodo d,
          sinu.src_materia e, 
          sinu.src_uni_academica f
        where 
          a.id_alum_programa = b.id_alum_programa and
          b.id_tercero = c.id_tercero and
          b.id_alum_programa = d.id_alum_programa and
          a.cod_materia = e.cod_materia and
          a.cod_unidad = f.cod_unidad and
          (d.est_mat_aca=1 or d.est_mat_aca=0) and
          d.est_mat_fin = '1' and
          b.est_alumno IN (1,7) and
          {}
        order by 4
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
# actualización de consulta semaforo reporte
#   SELECT
    #         a.id_alum_programa,
    #         g.ID_TERCERO,
    #         g.num_identificacion,
    #         g.nom_largo,
    #         a.cod_periodo periodo,
    #         b.cod_unidad,
    #         h.nom_unidad programa,
    #         b.cod_pensum pensum,
    #         a.cod_materia,
    #         c.nom_materia,
    #         c.num_nivel,
    #         c.int_horaria,
    #         c.uni_teorica creditos,
    #         a.cod_uni_e Cod_Programa_Equivalente,
    #         a.cod_pen_e,
    #         a.cod_materia_e Cod_Asignatura_Equivalente,
    #         (select nom_materia from SINU.src_materia
    #           where cod_materia = a.cod_materia_e) Asignatura_Equivalente,
    #         decode (tip_periodo,'N','Normal','Vacacional') tipo_periodo,
    #         v.pro_nivel,
    #         v.pro_acumulado,
    #         a.tip_nota,
    #         e.nom_tabla tipo_nota,
    #         d.num_niv_cursa sem_cursada,
    #         f.nom_tabla est_materia,
    #         a.def_historia,
    #         a.ind_aprobada,
    #         decode(a.ind_aprobada,1,'Si','No') aprobada,
    #           v.tot_uni_matricular,
    #           v.tot_uni_matriculadas,
    #         (v.tot_uni_matriculadas-v.tot_uni_pierde) TOT_UNI_APROBADAS,
    #           v.tot_uni_matriculadas "TOT_UNI_CURSADAS",
    #         nvl(c.val_posibles,
    #           (select decode(c.tip_nota,'N',x.val_posibles,x.val_posibles_alfa)
    #           from SINU.SRC_REGLAMENTO x,
    #                 SINU.SRC_PENSUM y
    #           where x.id_reglamento = y.id_reglamento
    #           and y.cod_pensum      = c.cod_pensum
    #           and y.cod_unidad      = c.cod_unidad)) val_posibles,
    #           decode (b.est_alumno,0,'INACTIVO',1,'ACTIVO',2,'EGRESADO',3,'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO',12,'GRADUADO TEMPORAL')"ESTADO"
    #   FROM SINU.SRC_HIS_ACADEMICA a,
    #       SINU.SRC_ALUM_PROGRAMA b,
    #       SINU.SRC_MAT_PENSUM c,
    #       SINU.BAS_TERCERO g,
    #       SINU.SRC_UNI_ACADEMICA h,
    #       SINU.SRC_ALUM_PERIODO d,
    #       SINU.SRC_GENERICA e,
    #       SINU.SRC_GENERICA f,
    #       SINU.src_vis_alum_per_est_web v
    #   WHERE a.id_alum_programa = b.id_alum_programa
    #   and b.cod_unidad         = c.cod_unidad
    #   and b.cod_pensum         = c.cod_pensum
    #   and a.cod_materia        = c.cod_materia
    #   and b.cod_unidad         = h.cod_unidad
    #   and b.id_tercero         = g.id_tercero
    #   and e.tip_tabla          = 'TIPNOT'
    #   and e.cod_tabla          <> e.tip_tabla
    #   and e.cod_tabla          = a.tip_nota
    #   and f.tip_tabla          = 'ESTMAT'
    #   and f.cod_tabla          <> f.tip_tabla
    #   and f.cod_tabla          = a.est_materia
    #   and a.id_alum_programa   = d.id_alum_programa(+)
    #   and a.per_acumula        = d.cod_periodo(+)
    #   and h.cod_modalidad      = '1'
    #   and a.cod_periodo = '{}'
    #   and b.id_alum_programa=v.id_alum_programa
    #   order by 3
    # SELECT
    #          a.id_alum_programa,
    #          g.ID_TERCERO,
    #          g.num_identificacion,
    #          g.nom_largo,
    #          a.cod_periodo periodo,
    #          b.cod_unidad,
    #          h.nom_unidad programa,
    #          b.cod_pensum pensum,
    #          a.cod_materia,
    #          c.nom_materia,
    #          c.num_nivel,
    #          c.int_horaria,
    #          c.uni_teorica creditos,
    #          a.cod_uni_e Cod_Programa_Equivalente,
    #          a.cod_pen_e,
    #          a.cod_materia_e Cod_Asignatura_Equivalente,
    #          (select nom_materia from SINU.src_materia
    #            where cod_materia = a.cod_materia_e) Asignatura_Equivalente,
    #          decode (tip_periodo,'N','Normal','Vacacional') tipo_periodo,
    #          v.pro_nivel,
    #          v.pro_acumulado,
    #          a.tip_nota,
    #          e.nom_tabla tipo_nota,
    #          d.num_niv_cursa sem_cursada,
    #          f.nom_tabla est_materia,
    #          a.def_historia,
    #          a.ind_aprobada,
    #          decode(a.ind_aprobada,1,'Si','No') aprobada,
    #            v.tot_uni_matricular,
    #            v.tot_uni_matriculadas,
    #          (v.tot_uni_matriculadas-v.tot_uni_pierde) TOT_UNI_APROBADAS,
    #        v.tot_uni_matriculadas "TOT_UNI_CURSADAS",
    #          nvl(c.val_posibles,
    #            (select decode(c.tip_nota,'N',x.val_posibles,x.val_posibles_alfa)
    #            from SINU.SRC_REGLAMENTO x,
    #                  SINU.SRC_PENSUM y
    #         where x.id_reglamento = y.id_reglamento
    #            and y.cod_pensum      = c.cod_pensum
    #         and y.cod_unidad      = c.cod_unidad)) val_posibles,
    #            decode (b.est_alumno,0,'INACTIVO',1,'ACTIVO',2,'EGRESADO',3,'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO',12,'GRADUADO TEMPORAL')"ESTADO"
    #    FROM SINU.SRC_HIS_ACADEMICA a,
    #       SINU.SRC_ALUM_PROGRAMA b,
    #        SINU.SRC_MAT_PENSUM c,
    #        SINU.BAS_TERCERO g,
    #        SINU.SRC_UNI_ACADEMICA h,
    #        SINU.SRC_ALUM_PERIODO d,
    #        SINU.SRC_GENERICA e,
    #        SINU.SRC_GENERICA f,
    #        SINU.src_vis_alum_per_est_web v
    #    WHERE a.id_alum_programa = b.id_alum_programa
    #    and b.cod_unidad         = c.cod_unidad
    #    and b.cod_pensum         = c.cod_pensum
    #    and a.cod_materia        = c.cod_materia
    #    and b.cod_unidad         = h.cod_unidad
    #    and b.id_tercero         = g.id_tercero
    #    and e.tip_tabla          = 'TIPNOT'
    #    and e.cod_tabla          <> e.tip_tabla
    #    and e.cod_tabla          = a.tip_nota
    #    and f.tip_tabla          = 'ESTMAT'
    #    and f.cod_tabla          <> f.tip_tabla
    #    and f.cod_tabla          = a.est_materia
    #    and a.id_alum_programa   = d.id_alum_programa(+)
    #    and a.per_acumula        = d.cod_periodo(+)
    #    and h.cod_modalidad      = '1'
    #    and a.cod_periodo = '{}'
    #    and b.id_alum_programa=v.id_alum_programa
    #    order by 3


def semaforo(identificacion):
    query = '''
    SELECT distinct
      c.num_identificacion,
      c.nom_largo estudiante,
      a.COD_MATERIA,
      e.nom_materia,
      a.NUM_NOTA,
      a.TIP_NOTA,
      a.NUM_NIVEL semestre_materia,
      decode(a.IND_APROBADA,0,'No_Aprobada',1,'Aprobada') Estado_materia,
      f.nom_unidad programa,
      a.cod_pensum pensum,
      a.COD_PERIODO periodo,
      (select x.nom_largo from sinu.bas_tercero x where v.id_tercero = x.id_tercero) profesor
    FROM sinu.src_semaforo a
      LEFT JOIN sinu.src_alum_programa b ON a.id_alum_programa = b.id_alum_programa
      LEFT JOIN sinu.bas_tercero c ON b.id_tercero = c.id_tercero
      LEFT JOIN sinu.src_alum_periodo d ON b.id_alum_programa = d.id_alum_programa
      LEFT JOIN sinu.src_materia e ON a.cod_materia = e.cod_materia
      LEFT JOIN sinu.src_uni_academica f ON a.cod_unidad = f.cod_unidad
      LEFT JOIN sinu.src_grupo h ON h.id_grupo = a.id_grupo
      LEFT JOIN sinu.src_vinculacion v ON h.id_vinculacion = v.id_vinculacion
    WHERE
      (d.est_mat_aca=1 or d.est_mat_aca=0) and
      d.est_mat_fin = '1' and
      f.cod_modalidad = '1' and
      b.est_alumno = '1' and
      c.num_identificacion = '{}'
      order by 1
    '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# def matricula_academica(periodo):
#     query='''
#     SELECT DISTINCT
#     c.id_tercero,
#     b.id_alum_programa,
#     C.num_identificacion,
#     C.nom_largo alumno,
#     c.gen_tercero genero,
#     c.dir_email_per email_personal,
#     c.dir_email email_institucional,
#     a.est_alumno,
#     a.cod_unidad,
#     j.nom_unidad,
#     j.cod_modalidad,
#     a.cod_pensum,
#     b.cod_periodo,
#     D.cod_materia,
#     d.id_grupo,
#     l.cod_div_grupo nom_subgrupo,
#     --(select id_div_grupo||'|'||cod_div_grupo from src_div_grupo where id_div_grupo = i.id_div_grupo)codigo_del_grupo, i.id_horario,
#     --i.id_div_grupo id_subgrupo,
#     NVL(D.num_grupo,0) num_grupo,
#     E.nom_materia,
#     e.int_horaria,
#     i.num_dia,
# DECODE (i.num_dia,2,'Lunes',3,'Martes',4,'Miercoles',5,'Jueves',6,'Viernes',7,'Sabado',1,'Domingo') dia,
#         sinu.funb_hora_militar (i.hor_inicio) hor_inicio,
#         sinu.funb_hora_militar(i.hor_fin) hor_fin,
#         E.num_nivel,
#         F.id_tercero id_tercero_docente,
#         F.num_identificacion NUM_IDENTIFICACION_DOCENTE,
#         F.nom_largo docente,
#         f.dir_email,
#         G.cod_aula,
#         D.id_jornada,
#         J.id_dependencia,
#         b.cod_materia mat_pensum,
#         b.ind_operacion
# FROM sinu.SRC_ALUM_PROGRAMA A
#         LEFT JOIN sinu.SRC_ENC_MATRICULA B
#         ON B.id_alum_programa = A.id_alum_programa
#         LEFT JOIN sinu.BAS_TERCERO C
#         ON A.id_tercero = C.id_tercero
#         LEFT JOIN sinu.SRC_GRUPO D
#         ON B.id_grupo = D.id_grupo
#         LEFT JOIN sinu.SRC_MAT_PENSUM E
#         ON d.cod_unidad = E.cod_unidad AND d.cod_pensum = E.cod_pensum AND D.cod_materia = E.cod_materia
#         LEFT JOIN sinu.SRC_AULA G
#         ON D.id_aula = G.id_aula
#         LEFT JOIN sinu.SRC_VINCULACION H
#         ON D.id_vinculacion = H.id_vinculacion
#         LEFT JOIN sinu.BAS_TERCERO F
#         ON H.id_tercero = F.id_tercero
#         LEFT JOIN sinu.SRC_UNI_ACADEMICA J
#         ON A.cod_unidad = J.cod_unidad
#         LEFT JOIN sinu.src_hor_grupo I
#         ON D.id_grupo = i.id_grupo and nvl(b.id_div_grupo,0) = nvl(i.id_div_grupo,0)
#         LEFT JOIN sinu.SRC_DIV_GRUPO L
#         ON i.id_div_grupo = l.id_div_grupo
# WHERE
# -- ASI PARA
# -- ASI PARA POSGRADOS E INTERSEMESTRALES b.cod_periodo like ('2020%')
# -- ASI PARA MAESTRIAS b.cod_periodo like ('21%')
# -- ASI PARA POSGRADOS Y MAESTRIAS AND j.cod_modalidad in ('2')
# -- ASI PARA PREGRADO j.cod_modalidad in ('1')
# and a.cod_unidad not in ('17034','17033','31132','31139')
# order by 3;
#     '''.format(periodo)
#     conn = connect_oracle()
#     result = conn.execute(query)
#     return result.fetchall()

# actualización de admitidos e


def admitidos_e_inscritos(periodo):
    # query = '''
    #   SELECT
    #     a.COD_PERIODO,b.NUM_IDENTIFICACION,
    #     decode(b.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
    #     b.NOM_LARGO,b.TEL_RESIDENCIA,b.TEL_CECULAR,b.DIR_EMAIL_PER,a.FEC_INSCRIPCION,
    #     decode(a.TIP_INSCRIPCION,1,'NORMAL',2,'TRANSFERENCIA INTERNA',3,'TRANSFERENCIA EXTERNA',4,'RESERVA CUPO',5,'REINTEGRO',6,'EXO.NORMAL',7,'EXO.TRANSF EXTERNA',8,'EXO.REINTEGRO',9,'EXO.TRANSF INTERNA',10,'NORMAL POSGRADOS ADM',11,'NORMAL POSGRADOS VRT') TIP_INSCRIPCION,
    #     a.COD_PROG_OPC_UNO,
    #     c.NOM_UNIDAD,a.COD_PENSUM,
    #     a.VAL_PAGO,a.FEC_PAGO,a.NUM_FORMULARIO,decode(a.EST_INSCRITO,0,'Pre-inscrito',1,'Inscrito',2,'Admitido',3,'Espera',9,'Rechazado') EST_INSCRITO
    #   FROM
    #     sinu.src_inscrito a,
    #     SINU.BAS_TERCERO b,
    #     SINU.SRC_UNI_ACADEMICA c,
    #     SINU.BAS_TERCERO d
    #   WHERE
    #     a.COD_PERIODO = '{}'
    #     and a.MOD_ESTUDIO='1'
    #     and a.EST_INSCRITO in ('1','2')
    #     and a.ID_TERCERO=b.ID_TERCERO
    #     and a.COD_PROG_OPC_UNO=c.COD_UNIDAD
    #     and a.USU_CREACION=d.ID_TERCERO
    query = '''
    select a.COD_PERIODO,b.NUM_IDENTIFICACION,
decode(b.tip_identificacion,1,'CEDULA DE CIUDADA-NIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
b.NOM_LARGO,b.TEL_RESIDENCIA,b.TEL_CECULAR,b.DIR_EMAIL_PER,a.FEC_INSCRIPCION,
decode(a.TIP_INSCRIPCION,1,'NORMAL',2,'TRANSFERENCIA INTERNA',3,'TRANSFERENCIA EXTERNA',4,'RESERVA CUPO',5,'REINTEGRO',6,'EXO.NORMAL',7,'EXO.TRANSF EXTERNA',8,'EXO.REINTEGRO',9,'EXO.TRANSF INTERNA',10,'NORMAL POSGRADOS ADM',11,'NORMAL POSGRADOS VRT') TIP_INSCRIPCION,
a.COD_PROG_OPC_UNO,
c.NOM_UNIDAD,a.COD_PENSUM,
a.VAL_PAGO,a.FEC_PAGO,a.NUM_FORMULARIO,decode(a.EST_INSCRITO,0,'Pre-inscrito',1,'Inscrito',2,'Admitido',3,'Espera',9,'Rechazado') EST_INSCRITO
from sinu.src_inscrito a,SINU.BAS_TERCERO b,SINU.SRC_UNI_ACADEMICA c,SINU.BAS_TERCERO d
where
a.COD_PERIODO in '{}'
and a.MOD_ESTUDIO='1'
and a.EST_INSCRITO in ('1','2')
and a.ID_TERCERO=b.ID_TERCERO
and a.COD_PROG_OPC_UNO=c.COD_UNIDAD
and a.USU_CREACION=d.ID_TERCERO
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def creditos_cursados(consulta):
    query = '''
    select b.ID_ALUM_PROGRAMA,c.ID_TERCERO, c.num_identificacion, 
    c.nom_largo, a.num_niv_cursa, a.tot_uni_matriculadas, a.tot_uni_aprobadas, a.pro_nivel, a.pro_acumulado, d.cod_unidad, 
    d.nom_unidad, b.cod_pensum, a.cod_periodo, b.est_alumno cod_estado, I.nom_tabla est_alumno, 
    (SELECT SUM(M.UNI_TEORICA)
    FROM sinu.SRC_ALUM_PROGRAMA A, sinu.SRC_MAT_PENSUM M, sinu.SRC_HIS_ACADEMICA H, sinu.BAS_TERCERO B, sinu.SRC_UNI_ACADEMICA U
    WHERE A.ID_ALUM_PROGRAMA = H.ID_ALUM_PROGRAMA
    AND A.COD_PENSUM = M.COD_PENSUM
    AND A.COD_UNIDAD = M.COD_UNIDAD
    AND A.ID_ALUM_PROGRAMA = b.ID_ALUM_PROGRAMA
    AND M.COD_MATERIA = H.COD_MATERIA
    AND H.DEF_HISTORIA >=3.0
    AND A.ID_TERCERO = B.ID_TERCERO
    AND A.COD_UNIDAD = U.COD_UNIDAD
    AND U.NOM_UNIDAD NOT LIKE '%CURSO%'
    AND U.NOM_UNIDAD NOT LIKE '%DIPLOMA%'
    AND U.NOM_UNIDAD NOT LIKE '%ESPECIALIZAC%'
    AND U.NOM_UNIDAD NOT LIKE '%DIIPLOMA%'
    AND U.NOM_UNIDAD NOT LIKE '%MAESTRIA%'
    GROUP BY B.NUM_IDENTIFICACION, B.NOM_LARGO, A.ID_ALUM_PROGRAMA,M.COD_UNIDAD,U.NOM_UNIDAD,M.COD_PENSUM
    ) total_creditos_cursados 
    from sinu.src_alum_periodo a, sinu.src_alum_programa b, sinu.bas_tercero c, sinu.src_uni_academica d, sinu.SRC_GENERICA I 
    where  
    a.est_mat_fin='1' 
    and a.id_alum_programa=b.id_alum_programa 
    and b.id_tercero=c.id_tercero 
    and b.cod_unidad=d.cod_unidad 
    {}
    AND TO_CHAR(b.est_alumno) = I.cod_tabla
    AND I.tip_tabla = 'ESTALU'
    AND I.cod_tabla != I.tip_tabla
    order by 4
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


# def matriculados_ingles(periodo):
#     query = '''
# consulta
#     '''.format(periodo)
#     conn = connect_oracle()
#     result = conn.execute(query)
#     return result.fetchall()


def docentesPeriodos(identificacion):
    query = '''
    select
      distinct a.cod_periodo
    from
      sinu.src_grupo A,
      sinu.src_mat_pensum B,
      sinu.src_uni_academica C,
      sinu.src_hor_grupo D,
      sinu.src_vinculacion E,
      sinu.src_jornada G,
      sinu.src_doc_grupo H,
      sinu.SRC_DIV_GRUPO I,
      sinu.bas_tercero J
    where
      j.id_tercero=e.id_tercero
      and j.id_tercero=e.id_tercero
      and a.cod_unidad = b.cod_unidad
      and a.cod_pensum = b.cod_pensum
      and a.cod_materia= b.cod_materia
      and a.cod_unidad = c.cod_unidad
      and a.id_grupo   = d.id_grupo (+)
      and a.id_vinculacion (+) = e.id_vinculacion
      and c.id_jornada = g.id_jornada
      and a.id_vinculacion = h.id_vinculacion
      and a.id_grupo = h.id_grupo
      and c.nom_unidad not like '%ESPECI%'
      and c.nom_unidad not like '%DIPL%'
      and (d.id_div_grupo     = i.id_div_grupo(+))
      and c.nom_unidad not like '%CURS%'
      and j.num_identificacion = '{}'
    group by a.cod_periodo
  '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# Informancion del estudiante - modulo de retoscuc


def informacion_estudiante_retoscuc(identifiacion):
    query = '''
    SELECT
      bas.num_identificacion identificacion, bas.nom_tercero nombre,
      bas.pri_apellido, bas.seg_apellido,pro.cod_unidad cod_programa,uni.nom_unidad programa, pro.cod_pensum pensum
    FROM
      sinu.bas_tercero bas
    LEFT JOIN
      sinu.SRC_ALUM_PROGRAMA pro
    ON bas.id_tercero = pro.id_tercero
    LEFT JOIN
      sinu.src_uni_academica uni
    ON pro.cod_unidad = uni.cod_unidad
    WHERE
      pro.est_alumno = '1' --estado activo
    AND uni.cod_modalidad = '1' -- modalidad pregrado
    AND bas.num_identificacion = '{}'
    order by 3
  '''.format(identifiacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# Asignaturas - modulo de retoscuc


def asignaturas_programa_retoscuc(identificacion, programa):
    query = '''
    SELECT DISTINCT
        a.COD_MATERIA,
        e.nom_materia,
        a.NUM_NIVEL semestre_materia
    FROM
        sinu.src_semaforo a,
        sinu.src_alum_programa b,
        sinu.bas_tercero c,
        sinu.src_alum_periodo d,
        sinu.src_materia e,
        sinu.src_uni_academica f
    WHERE
        a.id_alum_programa = b.id_alum_programa AND
        b.id_tercero = c.id_tercero AND
        b.id_alum_programa = d.id_alum_programa AND
        a.cod_materia = e.cod_materia AND
        a.cod_unidad = f.cod_unidad AND
        d.est_mat_aca='1' AND
        d.est_mat_fin = '1' AND
        f.cod_modalidad = '1' AND
        a.IND_APROBADA = '0' AND
        c.num_identificacion = '{}' AND
        b.cod_unidad = '{}'
    order by 3
  '''.format(identificacion, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# Matriculados pregrado
# prueba de todas las matriculas


def matriculados(periodo, modalidad):
    query = '''
      select distinct a.id_alum_programa,
d.id_tercero,
d.num_identificacion,
decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
d.nom_tercero||' '||d.seg_nombre as Nombres,
       d.pri_apellido||' '||d.seg_apellido Apellidos,
       decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
       ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
       ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
       ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
       ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
       ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
        (select b.id_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
       (select b.nom_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
       d.gen_tercero,
       d.fec_nacimiento,
       d.dir_residencia,
       (select bas_geopolitica.nom_div_geopolitica from bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
       d.tel_residencia,
       d.tel_cecular celular,
       d.num_est_economico estrato,
       d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
       d.DIR_EMAIL_PER EMAIL_PERSONAL,
       b.cod_unidad cod_programa,
       b.nom_unidad programa,
       c.num_niv_cursa semestre,
       c.cod_periodo,
        c.EST_MAT_ACA Matrícula_Academica,
        c.est_mat_fin Matricula_Financiera,
        d.eps_tercero cod_eps,
        a.cod_pensum,
        DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
        a.EST_ALUMNO,
        c.tot_uni_matricular,
        c.tot_uni_matriculadas,
        DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad

from sinu.src_alum_programa a, sinu.src_uni_academica b, sinu.src_alum_periodo c, sinu.bas_tercero d, sinu.bas_geopolitica e, sinu.bas_geopolitica f, sinu.SRC_ENC_LIQUIDACION g
where a.id_tercero = d.id_tercero 
      and a.id_alum_programa = c.id_alum_programa 
      and a.cod_unidad = b.cod_unidad 
      and d.id_ubi_nac=e.id_geopolitica 
      and d.id_ubi_res=f.id_geopolitica 
      and c.cod_periodo in "{}"
      {}
      and g.COD_PERIODO = c.cod_periodo
      and a.est_alumno IN (1,7)
      and c.est_mat_fin=1
--asi para ingles:  and b.cod_unidad  in ('31132','31139') ("en este caso debe comentar la linea de cod_modalidad ya que no se debe tener en cuenta)
--asi para pregrados: and b.cod_modalidad = '2'      
--asi para posgrados: and b.cod_modalidad = '1'
--asi para para diplomado: and b.nom_unidad like '%DIPLO%'
--asi para curso libre: and b.nom_unidad like 'CURSO LIBRE%'
      and g.est_liquidacion = 2
      and g.tip_liquidacion = 1
      and a.id_alum_programa = g.id_alum_programa
      order by 5
    '''.format(periodo, modalidad)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matriculados_pregrado(periodo, modalidad):
    query = '''
      select distinct a.id_alum_programa,
d.id_tercero,
d.num_identificacion,
decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
d.nom_tercero||' '||d.seg_nombre as Nombres,
       d.pri_apellido||' '||d.seg_apellido Apellidos,
       decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
       ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
       ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
       ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
       ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
       ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
        (select b.id_entidad 
        from sinu.bas_col_tercero A, sinu.bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
       (select b.nom_entidad 
        from sinu.bas_col_tercero A, sinu.bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
       d.gen_tercero,
       d.fec_nacimiento,
       d.dir_residencia,
       (select bas_geopolitica.nom_div_geopolitica from sinu.bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
       d.tel_residencia,
       d.tel_cecular celular,
       d.num_est_economico estrato,
       d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
       d.DIR_EMAIL_PER EMAIL_PERSONAL,
       b.cod_unidad cod_programa,
       b.nom_unidad programa,
       c.num_niv_cursa semestre,
       c.cod_periodo,
        c.EST_MAT_ACA Matrícula_Academica,
        c.est_mat_fin Matricula_Financiera,
        d.eps_tercero cod_eps,
        a.cod_pensum,
        DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
        a.EST_ALUMNO,
        c.tot_uni_matricular,
        c.tot_uni_matriculadas,
        DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad

from sinu.src_alum_programa a, sinu.src_uni_academica b, sinu.src_alum_periodo c, sinu.bas_tercero d, sinu.bas_geopolitica e, sinu.bas_geopolitica f, sinu.SRC_ENC_LIQUIDACION g
where a.id_tercero = d.id_tercero 
      and a.id_alum_programa = c.id_alum_programa 
      and a.cod_unidad = b.cod_unidad 
      and d.id_ubi_nac=e.id_geopolitica 
      and d.id_ubi_res=f.id_geopolitica 
      and c.cod_periodo = '{}'
      and g.COD_PERIODO = c.cod_periodo
      and b.cod_modalidad IN ('{}')
      and a.est_alumno IN (1,7)
      and c.est_mat_fin=1
      and g.est_liquidacion = 2
      and g.tip_liquidacion = 1
      and a.id_alum_programa = g.id_alum_programa
      order by 5
    '''.format(periodo, modalidad)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matriculados_ingles(periodo, modalidad):
    query = '''
    select distinct a.id_alum_programa,
d.id_tercero,
d.num_identificacion,
decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
d.nom_tercero||' '||d.seg_nombre as Nombres,
       d.pri_apellido||' '||d.seg_apellido Apellidos,
       decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
       ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
       ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
       ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
       ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
       ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
        (select b.id_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
       (select b.nom_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
       d.gen_tercero,
       d.fec_nacimiento,
       d.dir_residencia,
       (select bas_geopolitica.nom_div_geopolitica from bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
       d.tel_residencia,
       d.tel_cecular celular,
       d.num_est_economico estrato,
       d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
       d.DIR_EMAIL_PER EMAIL_PERSONAL,
       b.cod_unidad cod_programa,
       b.nom_unidad programa,
       c.num_niv_cursa semestre,
       c.cod_periodo,
        c.EST_MAT_ACA Matrícula_Academica,
        c.est_mat_fin Matricula_Financiera,
        d.eps_tercero cod_eps,
        a.cod_pensum,
        DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
        a.EST_ALUMNO,
        c.tot_uni_matricular,
        c.tot_uni_matriculadas,
        DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad

from src_alum_programa a, src_uni_academica b, src_alum_periodo c, bas_tercero d, bas_geopolitica e, bas_geopolitica f, SRC_ENC_LIQUIDACION g
where a.id_tercero = d.id_tercero 
      and a.id_alum_programa = c.id_alum_programa 
      and a.cod_unidad = b.cod_unidad 
      and d.id_ubi_nac=e.id_geopolitica 
      and d.id_ubi_res=f.id_geopolitica 
      and c.cod_periodo= '{}'
      and g.COD_PERIODO = c.cod_periodo
     -- and b.cod_modalidad = '2'
      and a.est_alumno IN (1,7)
      and c.est_mat_fin=1
      and b.cod_unidad  in ('31132','31139')
      and g.est_liquidacion = 2
      and g.tip_liquidacion = 1
      and a.id_alum_programa = g.id_alum_programa
      order by 5
    '''.format(periodo, modalidad)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
    # Matriculados Posgrado


def matriculados_posgrado(periodo, modalidad):
    query = '''
select distinct a.id_alum_programa,
d.id_tercero,
d.num_identificacion,
decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
d.nom_tercero||' '||d.seg_nombre as Nombres,
       d.pri_apellido||' '||d.seg_apellido Apellidos,
       decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
       ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
       ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
       ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
       ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
       ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
        (select b.id_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
       (select b.nom_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
       d.gen_tercero,
       d.fec_nacimiento,
       d.dir_residencia,
       (select bas_geopolitica.nom_div_geopolitica from bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
       d.tel_residencia,
       d.tel_cecular celular,
       d.num_est_economico estrato,
       d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
       d.DIR_EMAIL_PER EMAIL_PERSONAL,
       b.cod_unidad cod_programa,
       b.nom_unidad programa,
       c.num_niv_cursa semestre,
       c.cod_periodo,
        c.EST_MAT_ACA Matrícula_Academica,
        c.est_mat_fin Matricula_Financiera,
        d.eps_tercero cod_eps,
        a.cod_pensum,
        DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
        a.EST_ALUMNO,
        c.tot_uni_matricular,
        c.tot_uni_matriculadas,
        DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad

from src_alum_programa a, src_uni_academica b, src_alum_periodo c, bas_tercero d, bas_geopolitica e, bas_geopolitica f, SRC_ENC_LIQUIDACION g
where a.id_tercero = d.id_tercero 
      and a.id_alum_programa = c.id_alum_programa 
      and a.cod_unidad = b.cod_unidad 
      and d.id_ubi_nac=e.id_geopolitica 
      and d.id_ubi_res=f.id_geopolitica 
      and c.cod_periodo '{}'
      and g.COD_PERIODO = c.cod_periodo
      and b.cod_modalidad = '2'
      and a.est_alumno IN (1,7)
      and c.est_mat_fin=1
      and g.est_liquidacion = 2
      and g.tip_liquidacion = 1
      and a.id_alum_programa = g.id_alum_programa
      order by 5 '''.format(periodo, modalidad)

    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

    # Matriculados diplomados


def matriculados_diplomados(modalidad):
    query = '''
  select distinct a.id_alum_programa,
d.id_tercero,
d.num_identificacion,
decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
d.nom_tercero||' '||d.seg_nombre as Nombres,
       d.pri_apellido||' '||d.seg_apellido Apellidos,
       decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
       ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
       ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
       ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
       ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
       ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
        (select b.id_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
       (select b.nom_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
       d.gen_tercero,
       d.fec_nacimiento,
       d.dir_residencia,
       (select bas_geopolitica.nom_div_geopolitica from bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
       d.tel_residencia,
       d.tel_cecular celular,
       d.num_est_economico estrato,
       d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
       d.DIR_EMAIL_PER EMAIL_PERSONAL,
       b.cod_unidad cod_programa,
       b.nom_unidad programa,
       c.num_niv_cursa semestre,
       c.cod_periodo,
        c.EST_MAT_ACA Matrícula_Academica,
        c.est_mat_fin Matricula_Financiera,
        d.eps_tercero cod_eps,
        a.cod_pensum,
        DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
        a.EST_ALUMNO,
        c.tot_uni_matricular,
        c.tot_uni_matriculadas,
        DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad

from src_alum_programa a, src_uni_academica b, src_alum_periodo c, bas_tercero d, bas_geopolitica e, bas_geopolitica f, SRC_ENC_LIQUIDACION g
where a.id_tercero = d.id_tercero 
      and a.id_alum_programa = c.id_alum_programa 
      and a.cod_unidad = b.cod_unidad 
      and d.id_ubi_nac=e.id_geopolitica 
      and d.id_ubi_res=f.id_geopolitica 
      and c.cod_periodo= '{}'
      and g.COD_PERIODO = c.cod_periodo
     -- and b.cod_modalidad = '2'
      and a.est_alumno IN (1,7)
      and c.est_mat_fin=1
      and b.nom_unidad like '%DIPLO%'
      and g.est_liquidacion = 2
      and g.tip_liquidacion = 1
      and a.id_alum_programa = g.id_alum_programa
      order by 5
  '''.format(modalidad)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
# matriculados cursos libres


def matriculados_cursos_libres(periodo, modalidad):
    query = '''
  select distinct a.id_alum_programa,
d.id_tercero,
d.num_identificacion,
decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
d.nom_tercero||' '||d.seg_nombre as Nombres,
       d.pri_apellido||' '||d.seg_apellido Apellidos,
       decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
       ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
       ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
       ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
       ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
       ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
        (select b.id_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
       (select b.nom_entidad 
        from bas_col_tercero A, bas_entidad B 
        where a.id_entidad=b.id_entidad 
        and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
       d.gen_tercero,
       d.fec_nacimiento,
       d.dir_residencia,
       (select bas_geopolitica.nom_div_geopolitica from bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
       d.tel_residencia,
       d.tel_cecular celular,
       d.num_est_economico estrato,
       d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
       d.DIR_EMAIL_PER EMAIL_PERSONAL,
       b.cod_unidad cod_programa,
       b.nom_unidad programa,
       c.num_niv_cursa semestre,
       c.cod_periodo,
        c.EST_MAT_ACA Matrícula_Academica,
        c.est_mat_fin Matricula_Financiera,
        d.eps_tercero cod_eps,
        a.cod_pensum,
        DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
        a.EST_ALUMNO,
        c.tot_uni_matricular,
        c.tot_uni_matriculadas,
        DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad

from src_alum_programa a, src_uni_academica b, src_alum_periodo c, bas_tercero d, bas_geopolitica e, bas_geopolitica f, SRC_ENC_LIQUIDACION g
where a.id_tercero = d.id_tercero 
      and a.id_alum_programa = c.id_alum_programa 
      and a.cod_unidad = b.cod_unidad 
      and d.id_ubi_nac=e.id_geopolitica 
      and d.id_ubi_res=f.id_geopolitica 
      and c.cod_periodo= '{}'
      and g.COD_PERIODO = c.cod_periodo
     -- and b.cod_modalidad = '2'
      and a.est_alumno IN (1,7)
      and c.est_mat_fin=1
      and b.nom_unidad  like 'CURSO LIBRE%'
      and g.est_liquidacion = 2
      and g.tip_liquidacion = 1
      and a.id_alum_programa = g.id_alum_programa
      order by 5
  '''.format(periodo, modalidad)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
# promedio acumulado (posgrados)


def promedio_acumulado(promedio):
    query = '''
  select a.num_identificacion, a.nom_largo,
v.num_niv_cursa, v.cod_periodo,b.est_alumno, v.tot_uni_matricular, v.tot_uni_matriculadas,
(v.tot_uni_matriculadas-v.tot_uni_pierde) TOT_UNI_APROBADAS, v.pro_nivel, v.pro_acumulado, d.nom_unidad, v.tot_uni_matriculadas "TOT_UNI_CURSADAS"
from bas_tercero a,
src_alum_programa b,
src_uni_academica d, 
src_vis_alum_per_est_web v
where
a.id_tercero=b.id_tercero
and b.id_alum_programa=v.id_aLum_programa
and v.cod_periodo= '{}'
and b.cod_unidad=d.cod_unidad
and v.est_mat_fin='1'
and v.est_mat_aca='1'
and b.est_alumno='1'
and d.cod_modalidad not in '1'
and d.nom_unidad not like 'BIENESTAR%'
---and b.cod_unidad in ('13035','19002','19001') 
order by 2
  '''.format(promedio)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

# inactivos


def inactivos(periodo, consulta):
    query = '''
SELECT 
a.id_tercero,
a.num_identificacion,
a.nom_largo,
a.dir_email correo_institucional,
a.tel_cecular,
b.cod_pensum,
b.cod_unidad,
c.nom_unidad,
c.cod_modalidad,
decode (b.est_alumno, 0, 'INACTIVO', 1, 'ACTIVO',2,'EGRESADO',3, 'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO') "ESTADO"
FROM sinu.bas_tercero a, sinu.src_alum_programa b, sinu.src_uni_academica c
WHERE a.id_tercero = b.id_tercero
AND b.cod_unidad = c.cod_unidad
AND b.est_alumno ='0'
{}
AND b.cod_periodo like '{}%'
ORDER BY 2
  '''.format(consulta, periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def activos(consulta):
    query = '''
SELECT a.num_identificacion,
a.nom_tercero,
a.seg_nombre,
a.pri_apellido,
a.seg_apellido,
a.dir_email,
a.dir_email_per,
a.tel_cecular,
b.cod_pensum,
b.cod_unidad,
b.cod_periodo,
c.nom_unidad,
decode (b.est_alumno, 0, 'INACTIVO', 1, 'ACTIVO',2,'EGRESADO',3, 'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO') "ESTADO"
FROM sinu.bas_tercero a, sinu.src_alum_programa b, sinu.src_uni_academica c
WHERE a.id_tercero = b.id_tercero
AND b.cod_unidad = c.cod_unidad
{}
AND b.est_alumno ='1'
ORDER BY 2
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def AC_icfes(identificacion):
    query = '''
    select id_tercero, num_identificacion, nom_largo,
    (select DISTINCT src_inscrito.snp_numero
    from sinu.src_inscrito 
    where src_inscrito.id_tercero = bas_tercero.id_tercero and src_inscrito.COD_PROG_OPC_UNO != '31132'
    and rownum <= 1) snp_numero,
    (select DISTINCT src_inscrito.snp_puntaje
    from sinu.src_inscrito 
    where src_inscrito.id_tercero = bas_tercero.id_tercero and src_inscrito.COD_PROG_OPC_UNO != '31132'
    and rownum <= 1) snp_puntaje
    from sinu.bas_tercero
    where num_identificacion in ({})
'''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def pagos_saber_pro(periodo):
    query = '''
SELECT 
bas_tercero.ID_TERCERO,
src_enc_liquidacion.num_documento "No. LIQUID VOLANTE",
bas_tercero.NUM_IDENTIFICACION,
bas_tercero.pri_apellido ||' '|| bas_tercero.seg_apellido "APELLIDOS",
bas_tercero.NOM_TERCERO ||' '|| bas_tercero.seg_nombre "NOMBRES",
B.NOM_CONCEPTO,
  src_uni_academica.COD_UNIDAD,
  src_uni_academica.NOM_UNIDAD,
  A.val_liquidado "VAL_LIQUIDADO_1",
  src_enc_liquidacion.val_liquidado,
  src_enc_liquidacion.val_pagado,
  src_enc_liquidacion.fec_liquidacion,
  src_enc_liquidacion.fec_pago,
  DECODE(src_enc_liquidacion.est_liquidacion,2,'Pagado',1,'Liquidado')Estado,
  src_enc_liquidacion.COD_PERIODO
FROM 
  sinu.src_det_liquidacion A
LEFT JOIN sinu.fin_concepto B
ON
  A.ID_CONCEPTO = B.ID_CONCEPTO

LEFT JOIN sinu.src_enc_liquidacion
ON 
 a.id_enc_liquidacion = src_enc_liquidacion.id_enc_liquidacion

LEFT JOIN sinu.src_alum_programa
ON
  src_enc_liquidacion.ID_ALUM_PROGRAMA = src_alum_programa.ID_ALUM_PROGRAMA

LEFT JOIN sinu.bas_tercero
ON
  src_alum_programa.ID_TERCERO = bas_tercero.ID_TERCERO

LEFT JOIN sinu.src_uni_academica
ON
  src_alum_programa.COD_UNIDAD = src_uni_academica.COD_UNIDAD
WHERE
  B.NOM_CONCEPTO like '%SABER%'
  and src_enc_liquidacion.COD_PERIODO like ('{}%')
  and src_enc_liquidacion.est_liquidacion = '2'
  --and src_uni_academica.NOM_UNIDAD like 'INGEN%'
order by 4
'''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
# REVISAR


def reporte_historico_notas(consulta):
    query = '''
    select  
        A.id_alum_programa,
        F.num_identificacion identificacion_estudiante,
        F.nom_largo Estudiante,
        G.cod_unidad, 
        C.nom_unidad,
        B.cod_periodo,
        B.cod_pensum,
        e.id_vinculacion id_docente,
        h.num_identificacion identificacion_profesor,
        H.nom_largo profesor,
        B.cod_materia, 
        D.nom_materia,
        D.NUM_NIVEL,
        B.id_grupo, 
        B.num_grupo, 
        A.def_historia def_historia
        from    
            sinu.src_his_academica A, 
            sinu.src_grupo B, 
            sinu.src_uni_academica C, 
            sinu.src_mat_pensum D, 
            sinu.src_vinculacion E, 
            sinu.bas_tercero F, 
            sinu.src_alum_programa G, 
            sinu.bas_tercero H 
        where  
            G.cod_unidad = C.cod_unidad and 
            B.cod_unidad = D.cod_unidad and 
            B.cod_pensum = D.cod_pensum and 
            B.cod_materia = D.cod_materia and 
            B.id_vinculacion = E.id_vinculacion(+) and 
            E.id_tercero = H.id_tercero and 
            B.id_grupo = A.id_grupo and 
            A.id_alum_programa = G.id_alum_programa and 
            G.id_tercero = F.id_tercero
            {}
            order by  F.num_identificacion
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
# CREDITOS CURSADOS


# def creditos_cursados(periodo, consulta):
#     query = '''
#   select b.ID_ALUM_PROGRAMA,c.ID_TERCERO, c.num_identificacion,
# c.nom_largo, a.num_niv_cursa, a.tot_uni_matriculadas, a.tot_uni_aprobadas, a.pro_nivel, a.pro_acumulado, d.cod_unidad,
# d.nom_unidad, b.cod_pensum, a.cod_periodo, b.est_alumno cod_estado, I.nom_tabla est_alumno,
# (SELECT SUM(M.UNI_TEORICA)
# FROM SRC_ALUM_PROGRAMA A, SRC_MAT_PENSUM M, SRC_HIS_ACADEMICA H, BAS_TERCERO B, SRC_UNI_ACADEMICA U
# WHERE A.ID_ALUM_PROGRAMA = H.ID_ALUM_PROGRAMA
# AND A.COD_PENSUM = M.COD_PENSUM
# AND A.COD_UNIDAD = M.COD_UNIDAD
# AND A.ID_ALUM_PROGRAMA = b.ID_ALUM_PROGRAMA
# AND M.COD_MATERIA = H.COD_MATERIA
# AND H.DEF_HISTORIA >=3.0
# AND A.ID_TERCERO = B.ID_TERCERO
# AND A.COD_UNIDAD = U.COD_UNIDAD
# AND U.NOM_UNIDAD NOT LIKE '%CURSO%'
# AND U.NOM_UNIDAD NOT LIKE '%DIPLOMA%'
# AND U.NOM_UNIDAD NOT LIKE '%ESPECIALIZAC%'
# AND U.NOM_UNIDAD NOT LIKE '%DIIPLOMA%'
# AND U.NOM_UNIDAD NOT LIKE '%MAESTRIA%'
# GROUP BY B.NUM_IDENTIFICACION, B.NOM_LARGO, A.ID_ALUM_PROGRAMA,M.COD_UNIDAD,U.NOM_UNIDAD,M.COD_PENSUM
# ) total_creditos_cursados
# from src_alum_periodo a, src_alum_programa b, bas_tercero c, src_uni_academica d, SRC_GENERICA I
# where
# a.est_mat_fin='1'
# and a.id_alum_programa=b.id_alum_programa
# and b.id_tercero=c.id_tercero
# and b.cod_unidad=d.cod_unidad
# -- asi para posgrados
# and a.cod_periodo like '{}'
# -- asi para posgrados
# and d.cod_modalidad='2'
# -- asi para pregrados and d.cod_modalidad='1'
# -- asi para pregrados
# and a.cod_periodo = ('{}')
# AND TO_CHAR(b.est_alumno) = I.cod_tabla
# AND I.tip_tabla = 'ESTALU'
# AND I.cod_tabla != I.tip_tabla
# order by 4'''.format(periodo, consulta)
#     conn = connect_oracle()
#     result = conn.execute(query)
#     return result.fetchall()

def creditos_cursados_aprobados(consulta):
    query = '''
    select b.ID_ALUM_PROGRAMA,c.ID_TERCERO, c.num_identificacion, 
    c.nom_largo, a.num_niv_cursa, a.tot_uni_matriculadas, a.tot_uni_aprobadas, a.pro_nivel, a.pro_acumulado, d.cod_unidad, 
    d.nom_unidad, b.cod_pensum, a.cod_periodo, b.est_alumno cod_estado, I.nom_tabla est_alumno, 
    (SELECT SUM(M.UNI_TEORICA)
    FROM SINU.SRC_ALUM_PROGRAMA A, SINU.SRC_MAT_PENSUM M, SINU.SRC_HIS_ACADEMICA H, SINU.BAS_TERCERO B, SINU.SRC_UNI_ACADEMICA U
    WHERE A.ID_ALUM_PROGRAMA = H.ID_ALUM_PROGRAMA
    AND A.COD_PENSUM = M.COD_PENSUM
    AND A.COD_UNIDAD = M.COD_UNIDAD
    AND A.ID_ALUM_PROGRAMA = b.ID_ALUM_PROGRAMA
    AND M.COD_MATERIA = H.COD_MATERIA
    AND H.DEF_HISTORIA >=3.0
    AND A.ID_TERCERO = B.ID_TERCERO
    AND A.COD_UNIDAD = U.COD_UNIDAD
    AND U.NOM_UNIDAD NOT LIKE '%CURSO%'
    AND U.NOM_UNIDAD NOT LIKE '%DIPLOMA%'
    AND U.NOM_UNIDAD NOT LIKE '%ESPECIALIZAC%'
    AND U.NOM_UNIDAD NOT LIKE '%DIIPLOMA%'
    AND U.NOM_UNIDAD NOT LIKE '%MAESTRIA%'
    GROUP BY B.NUM_IDENTIFICACION, B.NOM_LARGO, A.ID_ALUM_PROGRAMA,M.COD_UNIDAD,U.NOM_UNIDAD,M.COD_PENSUM
    ) total_creditos_cursados 
    from sinu.src_alum_periodo a, sinu.src_alum_programa b, sinu.bas_tercero c, sinu.src_uni_academica d, sinu.SRC_GENERICA I 
    where  a.est_mat_fin='1' 
    and a.id_alum_programa=b.id_alum_programa 
    and b.id_tercero=c.id_tercero 
    and b.cod_unidad=d.cod_unidad 
    {}
    AND TO_CHAR(b.est_alumno) = I.cod_tabla
    AND I.tip_tabla = 'ESTALU'
    AND I.cod_tabla != I.tip_tabla
    order by 4
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matriculados(consulta):
    query = '''
select distinct a.id_alum_programa,
  d.id_tercero,
  d.num_identificacion,
  decode(d.tip_identificacion,1,'CEDULA DE CIUDADANIA',2,'TARJETA DE IDENTIDAD',3,'CEDULA DE EXTRANJERIA',5,'PASAPORTE',8,'DOCUMENTO DE IDENTIFICACION EXTRANJERO') tip_identificacion,
  d.nom_tercero||' '||d.seg_nombre as Nombres,
  d.pri_apellido||' '||d.seg_apellido Apellidos,
  decode(d.eps_tercero,1,'COOMEVA',2,'SALUD TOTAL',3,'SALUDCOOP',4,'FAMISANAR',5,'COLMEDICA',6,'SISBEN'
  ,7,'CAFESALUD',8,'SANITAS',9,'UNIMEC',10,'COLPATRIA',11,'CAJANAL',12,'COLSEGUROS',13,'FIDUCIARIA LA PREVISORA'
  ,14,'EPS SEGURO SOCIAL',15,'SUSALUD',16,'CAPRECOM',17,'SANIDAD NAVAL',18,'NUEVA EPS',19,'HUMANAVIVIR'
  ,20,'NO REGISTRA',21,'SURA',23,'SANIDAD POLICIA NACIONAL',26,'MUTUAL SER',27,'DUSAKAWI',28,'COOSALUD',24,'MEDIESP'
  ,25,'SALUDVIDA',32,'MAGISTERIO',33,'UNION TEMPORAL',29,'BARRIOS UNIDOS',30,'COLSANITAS',31,'FOMAG',35,'SERVICIO MEDICO DEL SENA'
  ,34,'CAJACOPI',36,'COMPARTA ESP',37,'MEDIMAS EPS')Nombre_EPS,
  (select b.id_entidad 
  from sinu.bas_col_tercero A, sinu.bas_entidad B 
  where a.id_entidad=b.id_entidad 
  and a.id_tercero=d.id_tercero and rownum<=1) "Codigo_Colegio",
  (select b.nom_entidad 
  from sinu.bas_col_tercero A, sinu.bas_entidad B 
  where a.id_entidad=b.id_entidad 
  and a.id_tercero=d.id_tercero and rownum<=1) "Nombre_Colegio",
  d.gen_tercero,
  d.fec_nacimiento,
  d.dir_residencia,
  (select bas_geopolitica.nom_div_geopolitica from sinu.bas_geopolitica where d.id_ubi_res=bas_geopolitica.id_geopolitica) lugar_residencia,
  d.tel_residencia,
  d.tel_cecular celular,
  d.num_est_economico estrato,
  d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
  d.DIR_EMAIL_PER EMAIL_PERSONAL,
  b.cod_unidad cod_programa,
  b.nom_unidad programa,
  c.num_niv_cursa semestre,
  c.cod_periodo,
  c.EST_MAT_ACA Matrícula_Academica,
  c.est_mat_fin Matricula_Financiera,
  d.eps_tercero cod_eps,
  a.cod_pensum,
  DECODE(g.est_liquidacion,1,'Liquidado',2,'Pagado') Estado,
  a.EST_ALUMNO,
  c.tot_uni_matricular,
  c.tot_uni_matriculadas,
  DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad
  from sinu.src_alum_programa a, sinu.src_uni_academica b, sinu.src_alum_periodo c, sinu.bas_tercero d, sinu.bas_geopolitica e, sinu.bas_geopolitica f, sinu.SRC_ENC_LIQUIDACION g
  where a.id_tercero = d.id_tercero 
  and a.id_alum_programa = c.id_alum_programa 
  and a.cod_unidad = b.cod_unidad 
  and d.id_ubi_nac=e.id_geopolitica 
  and d.id_ubi_res=f.id_geopolitica 
  {}
  and g.COD_PERIODO = c.cod_periodo
  and a.est_alumno IN (1,7)
  and c.est_mat_fin=1

  and g.est_liquidacion = 2
  and g.tip_liquidacion = 1
  and a.id_alum_programa = g.id_alum_programa
  order by 5
  '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def materias_canceladas(periodo):
    query = '''
    SELECT B.id_alum_programa,
    C.id_tercero student,
    C.num_identificacion,
    C.nom_largo alumno,
    b.cod_periodo,
    A.cod_unidad,
    J.nom_unidad,
    A.cod_pensum,
    --B.not_definitiva,
    --B.fec_matricula,
    --B.est_pago,
    B.est_matricula matricula,
    I.nom_tabla est_matricula,
    D.cod_materia,
    --d.id_grupo,
    --NVL(D.num_grupo,0) grupo,
    --f.num_identificacion identificacion_profesor,
    --F.nom_largo profesor_grupo,
    --b.id_div_grupo,
    --(select cod_div_grupo from sinu.src_div_grupo where b.id_div_grupo = src_div_grupo.id_div_grupo) sub_grupo,
    --(select id_vinculacion  from sinu.src_div_grupo where b.id_div_grupo = src_div_grupo.id_div_grupo) vinculacion_subgrupo,
    E.nom_materia,
    --E.num_nivel,
    b.cod_materia mat_pensum,
    e.uni_teorica Creditos_equivalencia,
    (select sum(x.uni_teorica) from sinu.src_mat_pensum x 
    where b.cod_materia = x.cod_materia
    and a.cod_unidad = x.cod_unidad
    and a.cod_pensum = x.cod_pensum) creditos_mat_pensum
    FROM sinu.SRC_ALUM_PROGRAMA A, sinu.SRC_ENC_MATRICULA B, sinu.BAS_TERCERO C, sinu.SRC_GRUPO D, sinu.SRC_MAT_PENSUM E,
        sinu.BAS_TERCERO F, sinu.SRC_VINCULACION H, sinu.SRC_GENERICA I, sinu.SRC_UNI_ACADEMICA J
    WHERE B.id_alum_programa = A.id_alum_programa
    AND A.id_tercero = C.id_tercero
    AND A.cod_unidad = J.cod_unidad
    AND B.id_grupo = D.id_grupo
    AND d.cod_unidad = E.cod_unidad
    AND d.cod_pensum = E.cod_pensum
    AND D.cod_materia = E.cod_materia
    AND D.id_vinculacion = H.id_vinculacion(+)
    AND H.id_tercero = F.id_tercero (+)
    AND TO_CHAR(B.est_matricula) = I.cod_tabla
    --AND I.tip_tabla = 'ESTMAT'
    AND I.cod_tabla != I.tip_tabla
    AND b.cod_periodo = '{}'
    AND j.cod_modalidad IN ('1')
    AND B.est_matricula = 5
    order by 4
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def materias_no_aprobada_periodo(periodo):
    query = '''
    select distinct a.cod_periodo, d.cod_unidad, d.nom_unidad, b.cod_pensum, c.num_identificacion, 
    c.nom_largo, e.cod_materia, e.nom_materia, a.sem_cursada, a.not_periodo, a.ind_aprobada,
    DECODE(a.est_materia,3,'TERCERA VEZ',4,'CUARTA VEZ',6,'QUINTA VEZ',7,'SEXTA VEZ',8,'SEPTIMA VEZ',9,'OCTAVA VEZ',10,'NOVENA VEZ') est_materia
    from sinu.src_his_academica a, sinu.src_alum_programa b, sinu.bas_tercero c, sinu.src_uni_academica d, sinu.src_materia e
    where a.cod_periodo = '{}' 
    and a.id_alum_programa=b.id_alum_programa 
    and a.cod_materia=e.cod_materia 
    and b.cod_unidad=d.cod_unidad 
    and b.id_tercero=c.id_tercero
    and b.est_alumno IN (1,7)
    and a.est_materia not in (1,2,5)
    and a.ind_aprobada = '0'
    order by 6
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def materias_tomadas(consulta):
    query = '''
    SELECT distinct
    a.id_tercero                        "_IdTerceroEstudiante",
    a.num_identificacion                "_CedulaEstudiante",
    a.nom_tercero                       "_Nombre",
    a.pri_apellido                      "_Apellido",
    a.seg_apellido                      "_Seg_Apellido",
    (select distinct num_niv_cursa 
    from sinu.src_alum_periodo 
    where cod_periodo like '2022%' 
    and id_alum_programa in (select id_alum_programa 
                        from sinu.src_alum_programa
                        where id_tercero=a.id_tercero)
    and rownum<2) as "_SemestreEstudiante",
    f.cod_materia                       "_CodigoMateria",
    m.nom_materia                       "_NomMateria",
    i.id_tercero                        "_IdTerceroDocente",
    Nvl(i.num_identificacion,'NA')      "_CedulaDocente",
    i.nom_tercero                       "_NomDocente",
    i.pri_apellido                      "_ApeDocente",
    f.cod_unidad                        "_CodigoPrograma",
    c.nom_unidad                        "_Programa",
    f.cod_periodo                       "_CodigoPeriodo",
    f.cod_pensum                        "_Pensum",
    g.num_nivel                         "_SemestreMateria",
    e.fec_matricula                     "_Fecha Matricula",
    f.num_grupo                         "_GrupoMateria",
    f.id_grupo                          "_Id Grupo"

    FROM sinu.bas_tercero a, sinu.src_alum_programa b,sinu.src_uni_academica c, sinu.src_alum_periodo d,
    sinu.src_enc_matricula e , sinu.src_grupo f, sinu.src_mat_pensum g, sinu.src_vinculacion h, sinu.bas_tercero i, sinu.src_materia m
    WHERE 1=1
    AND a.id_tercero=b.id_tercero
    AND b.cod_unidad=c.cod_unidad
    AND b.id_alum_programa=d.id_alum_programa
    AND b.id_alum_programa=e.id_alum_programa
    AND f.cod_unidad=g.cod_unidad
    AND f.cod_pensum=g.cod_pensum
    AND f.cod_materia=g.cod_materia
    AND f.cod_materia=m.cod_materia
    AND e.id_grupo=f.id_grupo
    AND f.id_vinculacion = h.id_vinculacion(+)
    AND h.id_tercero=i.id_tercero(+)
    AND b.est_alumno IN (1,7)
    --AND f.NUM_GRUPO like 'VIRT%'
    AND d.est_mat_fin=1
    {}
    order by 5
    '''.format(consulta)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def matriculados_porestado_hep(periodo):
    query = '''
with q as
(
select
       a.id_alum_programa id_alum_programa_2,
       g.ID_TERCERO,
       g.num_identificacion identificacion,
       g.nom_largo,
       d.cod_periodo periodo,
       b.cod_unidad,
       h.nom_unidad programa,
       b.cod_pensum pensum,
       a.cod_materia,
       c.nom_materia,
       c.num_nivel,
       c.int_horaria,
       c.uni_teorica creditos,
       a.cod_uni_e Cod_Programa_Equivalente,
       a.cod_pen_e,
       a.cod_materia_e Cod_Asignatura_Equivalente,
       (select nom_materia from sinu.src_materia
        where cod_materia = a.cod_materia_e) Asignatura_Equivalente,
       decode (tip_periodo,'N','Normal','Vacacional') tipo_periodo,
       v.pro_nivel, 
       v.pro_acumulado,
       a.tip_nota,
       e.nom_tabla tipo_nota,
       d.num_niv_cursa sem_cursada,
       f.nom_tabla est_materia,
       a.def_historia,
       a.ind_aprobada,
       decode(a.ind_aprobada,1,'Si','No') aprobada,
        v.tot_uni_matricular,
        v.tot_uni_matriculadas,
       (v.tot_uni_matriculadas-v.tot_uni_pierde) TOT_UNI_APROBADAS,
        v.tot_uni_matriculadas TOT_UNI_CURSADAS,
       nvl(c.val_posibles,
        (select decode(c.tip_nota,'N',x.val_posibles,x.val_posibles_alfa)
         from sinu.SRC_REGLAMENTO x,
              sinu.SRC_PENSUM y
         where x.id_reglamento = y.id_reglamento
         and y.cod_pensum      = c.cod_pensum
         and y.cod_unidad      = c.cod_unidad)) val_posibles,
         decode (b.est_alumno,0,'INACTIVO',1,'ACTIVO',2,'EGRESADO',3,'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO',12,'GRADUADO TEMPORAL')"ESTADO"
from sinu.SRC_HIS_ACADEMICA a,
     sinu.SRC_ALUM_PROGRAMA b,
     sinu.SRC_MAT_PENSUM c,
     sinu.BAS_TERCERO g,
     sinu.SRC_UNI_ACADEMICA h,
     sinu.SRC_ALUM_PERIODO d,
     sinu.SRC_GENERICA e,
     sinu.SRC_GENERICA f,
     sinu.src_vis_alum_per_est_web v
where a.id_alum_programa = b.id_alum_programa
and b.cod_unidad         = c.cod_unidad
and b.cod_pensum         = c.cod_pensum
and a.cod_materia        = c.cod_materia
and b.cod_unidad         = h.cod_unidad
and b.id_tercero         = g.id_tercero
and e.tip_tabla          = 'TIPNOT'
and e.cod_tabla          <> e.tip_tabla
and e.cod_tabla          = a.tip_nota
and f.tip_tabla          = 'ESTMAT'
and f.cod_tabla          <> f.tip_tabla
and f.cod_tabla          = a.est_materia
and a.id_alum_programa   = d.id_alum_programa(+)
and a.per_acumula        = d.cod_periodo(+)
--and h.cod_modalidad      = '2'
--and a.cod_periodo in ('23CH1')
--and v.cod_periodo = '23CH1'
--AND g.num_identificacion in ('45530227','1102827442','1118832539','00100201722')
and b.id_alum_programa=v.id_alum_programa 
and h.cod_est_metodologica = 'ESTMET'
      and h.est_metodologica = 4
order by 3
)
/*select num_identificacion,num_identificacion_sig,periodo_actual,periodo_sig 
from (
select num_identificacion,periodo_actual,  
LEAD(num_identificacion,1) over(order by num_identificacion) num_identificacion_sig,
LEAD(periodo_actual,1) over(order by num_identificacion) periodo_sig
from
(*/
--- AQUI ESTAN LOS CAMPOS QUE MUESTRA EL ENDPOINT
select cod_programa,programa,id_alum_programa, 
--tipo TIPO2,
decode (total_periodos_matriculados,0,'MATRICULADO','REMATRICULADO') estado,
num_identificacion cedula,EMAIL_INSTITUCIONAL correo_institucional,EMAIL_PERSONAL,celular,tel_residencia,id_tercero, nombres|| ' ' ||apellidos nombre , periodo_actual, periodo_ingreso--,cantidad_periodos_hist,cantidad_periodos_mat,total_periodos_matriculado
from (
SELECT DISTINCT a.id_alum_programa id_alum_programa,
       d.id_tercero,
       (select gen.nom_tabla from sinu.src_generica gen where gen.tip_tabla ='TIPIDE' and gen.cod_tabla = d.TIP_IDENTIFICACION) tipo_identificacion,
       d.num_identificacion num_identificacion,
       d.nom_tercero||' '||d.seg_nombre as Nombres,
       d.pri_apellido||' '||d.seg_apellido Apellidos,
       d.gen_tercero,
       d.fec_nacimiento,
       d.tel_cecular celular,
       d.tel_residencia tel_residencia,
       d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
       d.DIR_EMAIL_PER EMAIL_PERSONAL,
       b.cod_unidad cod_programa,
       b.nom_unidad programa,
       c.num_niv_cursa semestre,
       c.cod_periodo periodo_Actual,
       a.cod_periodo periodo_ingreso,
       ---VALIDACIONES---------------------------------
       decode((select count(distinct(cod_periodo))  from sinu.src_his_academica y where y.id_alum_programa = a.id_alum_programa and cod_periodo not in (c.cod_periodo)),'0','MATRICULADO','REMATRICULADO') TIPO,
       (select count(distinct(cod_periodo))  from sinu.src_enc_matricula y where y.id_alum_programa = a.id_alum_programa and y.cod_periodo like '%CH%'and y.cod_periodo <> c.cod_periodo) cantidad_periodos_mat,
       (select count(distinct(cod_periodo))  from sinu.src_his_academica y where y.id_alum_programa = a.id_alum_programa and y.cod_periodo like '%CH%') + (select count(distinct(cod_periodo))  from sinu.src_enc_matricula y where y.id_alum_programa = a.id_alum_programa and y.cod_periodo like '%CH%'and y.cod_periodo <> c.cod_periodo) total_periodos_matriculados,---------------------
       -- (select distinct(to_char(max(em.fec_matricula),'YYYY-MM-DD')) fecha from sinu.src_enc_matricula em where em.id_alum_programa = a.id_alum_programa and cod_periodo = '23CH5')fec_matricula,
       c.EST_MAT_ACA Matricula_Academica,
       c.est_mat_fin Matricula_Financiera,
       a.cod_pensum,
       decode ( a.EST_ALUMNO, 0, 'INACTIVO', 1, 'ACTIVO',2,'EGRESADO',3, 'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO') "ESTADO_ALUMNO",
       c.tot_uni_matricular,
       c.tot_uni_matriculadas,
       DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad,
       ----------------------LA TRAMPA
        (select count(*) from q  where q.id_alum_programa_2 = a.id_alum_programa ) total_cursadas, 
        (select count(*) from q  where q.id_alum_programa_2 = a.id_alum_programa and aprobada = 'Si' ) total_aprobadas,
        (select count(*) from q  where q.id_alum_programa_2 = a.id_alum_programa and est_materia = 'Cancelada' ) total_canceladas,
        (select count(distinct(cod_periodo))  from sinu.src_his_academica y where y.id_alum_programa = a.id_alum_programa and y.cod_periodo like '%CH%') cantidad_periodos_hist
        --(select count(distinct(cod_periodo))  from sinu.src_his_academica y where y.id_alum_programa = a.id_alum_programa and y.cod_periodo like '%CH%') + (select count(distinct(cod_periodo))  from sinu.src_enc_matricula y where y.id_alum_programa = a.id_alum_programa and y.cod_periodo like '%CH%'and y.cod_periodo <> c.cod_periodo) total_periodos
---------------------
      FROM sinu.src_alum_programa a, sinu.src_uni_academica b, sinu.src_alum_periodo c, sinu.bas_tercero d, sinu.bas_geopolitica e, sinu.bas_geopolitica f, sinu.SRC_ENC_LIQUIDACION g
      WHERE a.id_tercero = d.id_tercero 
      and a.id_alum_programa = c.id_alum_programa 
      and a.cod_unidad = b.cod_unidad 
      and d.id_ubi_nac=e.id_geopolitica 
      and d.id_ubi_res=f.id_geopolitica 
      and c.cod_periodo = '{}'
      and g.COD_PERIODO = c.cod_periodo
    --  and b.cod_modalidad = '1'
      and a.est_alumno IN (1,7)
      and c.est_mat_fin=1 
      /*and d.num_identificacion in (
        '17357716',
        '1005575872',
        '64703985',
        '1083000125',
        '1065592434',
        '1143259105'
      )*/
      and g.est_liquidacion = 2
      and g.tip_liquidacion = 1
      and a.id_alum_programa = g.id_alum_programa
      order by 3--)
      )
      --order by 1--) where num_identificacion = num_identificacion_sig"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    '''.format(periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def estudiantes_primer_semestre(periodo, periodo_virtual):
    query = '''
      select distinct 
      d.num_identificacion,

      d.nom_tercero PRI_NOMBRE,
      d.seg_nombre as SEG_NOMBRE,
      d.pri_apellido PRI_APELLIDO,
      d.seg_apellido SEG_APELLIDO,
      --d.nom_tercero||' '||d.seg_nombre as Nombres,
      --      d.pri_apellido||' '||d.seg_apellido Apellidos,

            d.gen_tercero,
            d.fec_nacimiento,
            d.tel_residencia telefono,
            d.tel_cecular celular,

            d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
            d.DIR_EMAIL_PER EMAIL_PERSONAL,
            b.cod_unidad cod_programa

      from sinu.src_alum_programa a, sinu.src_uni_academica b, sinu.src_alum_periodo c, sinu.bas_tercero d, sinu.bas_geopolitica e, sinu.bas_geopolitica f, sinu.SRC_ENC_LIQUIDACION g
      where a.id_tercero = d.id_tercero 
            and a.id_alum_programa = c.id_alum_programa 
            and a.cod_unidad = b.cod_unidad 
            and d.id_ubi_nac=e.id_geopolitica 
            and d.id_ubi_res=f.id_geopolitica 
            and c.cod_periodo in ('{}','{}')
            and g.COD_PERIODO = c.cod_periodo
            and b.cod_modalidad = '1'
            and a.est_alumno IN (1,7)
            and c.est_mat_fin=1
            and g.est_liquidacion = 2
            and c.num_niv_cursa in ('1')
            and g.tip_liquidacion = 1
            and a.id_alum_programa = g.id_alum_programa
            order by 5
    '''.format(periodo, periodo_virtual)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

def asignaturas_programa_sisef(programa, periodo):
    query = '''    
  SELECT
    d.cod_unidad,
    (select nom_unidad from sinu.src_uni_academica where d.cod_unidad = cod_unidad)nom_programa,
    d.cod_materia,
    (select nom_materia from sinu.src_materia where d.cod_materia = cod_materia) nom_materia,
    A.id_grupo,
    D.num_grupo,
    d.cod_pensum
  FROM
    sinu.src_doc_grupo A
    LEFT JOIN sinu.SRC_VINCULACION B ON a.id_vinculacion = B.ID_VINCULACION
    LEFT JOIN sinu.BAS_TERCERO C ON  b.id_tercero = c.id_tercero
    LEFT JOIN sinu.src_grupo D  ON  A.id_grupo = d.id_grupo
  WHERE d.cod_periodo = '{}'
  AND d.cod_unidad = '{}'
  '''.format(periodo, programa)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def estudiantes_grupos_sisef(periodo, id_grupo):
  query = '''
  SELECT DISTINCT
  d.id_grupo,
  NVL(D.num_grupo,0) num_grupo,
  i.id_div_grupo id_subgrupo,
  l.cod_div_grupo nom_subgrupo,
  b.id_alum_programa,
  C.num_identificacion,
  C.nom_largo alumno
  FROM sinu.SRC_ALUM_PROGRAMA A
  LEFT JOIN sinu.SRC_ENC_MATRICULA B
  ON B.id_alum_programa = A.id_alum_programa
  LEFT JOIN sinu.BAS_TERCERO C
  ON A.id_tercero = C.id_tercero
  LEFT JOIN sinu.SRC_GRUPO D
  ON B.id_grupo = D.id_grupo
  LEFT JOIN sinu.SRC_MAT_PENSUM E
  ON d.cod_unidad = E.cod_unidad AND d.cod_pensum = E.cod_pensum AND D.cod_materia = E.cod_materia
  LEFT JOIN sinu.SRC_VINCULACION H
  ON D.id_vinculacion = H.id_vinculacion
  LEFT JOIN sinu.BAS_TERCERO F
  ON H.id_tercero = F.id_tercero
  LEFT JOIN sinu.SRC_UNI_ACADEMICA J
  ON A.cod_unidad = J.cod_unidad
  LEFT JOIN sinu.src_hor_grupo I
  ON D.id_grupo = i.id_grupo and nvl(b.id_div_grupo,0) = nvl(i.id_div_grupo,0)
  LEFT JOIN sinu.SRC_AULA G
  ON to_char(i.id_aula) = G.cod_aula
  LEFT JOIN sinu.SRC_DIV_GRUPO L
  ON i.id_div_grupo = l.id_div_grupo
  LEFT JOIN sinu.src_generica k
  ON k.tip_tabla = 'ESTMAT' AND k.cod_tabla != k.tip_tabla 
  AND TO_CHAR(B.est_matricula) = k.cod_tabla
  WHERE
  b.cod_periodo = '{}'
  AND j.cod_modalidad = ('1')
  and a.cod_unidad not in ('17034','17033','31132')
  and d.id_grupo = '{}'
  UNION ALL 
    select DISTINCT
        x.id_grupo,
        x.num_grupo num_grupo,
        w.id_div_grupo id_subgrupo,
        w.cod_div_grupo nom_subgrupo,
        b.id_alum_programa,
        g.num_identificacion,
        g.nom_largo
  from sinu.SRC_HIS_ACADEMICA a
  LEFT JOIN sinu.SRC_ALUM_PROGRAMA b
  ON a.id_alum_programa = b.id_alum_programa
  LEFT JOIN sinu.SRC_MAT_PENSUM c 
  ON a.cod_materia = c.cod_materia and b.cod_unidad = c.cod_unidad
  and b.cod_pensum = c.cod_pensum
  LEFT JOIN  sinu.BAS_TERCERO g
  ON b.id_tercero = g.id_tercero
  LEFT JOIN  sinu.SRC_UNI_ACADEMICA h
  ON b.cod_unidad = h.cod_unidad
  and h.cod_modalidad      = '1'
  LEFT JOIN  sinu.SRC_ALUM_PERIODO d
  ON a.id_alum_programa   = d.id_alum_programa
  and a.per_acumula        = d.cod_periodo
  LEFT JOIN sinu.SRC_GENERICA e
  ON  e.tip_tabla          = 'TIPNOT'
  and e.cod_tabla          <> e.tip_tabla
  and e.cod_tabla          = a.tip_nota
  LEFT JOIN  sinu.SRC_GENERICA f 
  ON f.tip_tabla          = 'ESTMAT'
  and f.cod_tabla          <> f.tip_tabla
  and f.cod_tabla          = a.est_materia
  LEFT JOIN sinu.src_vis_alum_per_est_web v
  ON b.id_alum_programa=v.id_alum_programa 
  and v.cod_periodo =  '{}'
  LEFT JOIN sinu.src_grupo x
  ON a.id_grupo= x.id_grupo
  LEFT JOIN sinu.src_hor_grupo y
  ON  x.id_grupo = y.id_grupo
  LEFT JOIN  sinu.SRC_DIV_GRUPO w
  ON y.id_div_grupo = w.id_div_grupo
  LEFT JOIN sinu.SRC_VINCULACION I
  ON x.id_vinculacion = i.id_vinculacion
  LEFT JOIN sinu.BAS_TERCERO Z
  ON i.id_tercero = z.id_tercero
  WHERE a.cod_periodo = '{}'
  AND  x.id_grupo = '{}'
  ORDER BY 2'''.format(periodo, id_grupo, periodo,periodo, id_grupo)
  conn = connect_oracle()
  result = conn.execute(query)
  return result.fetchall()


def grupos_asignatura(asignatura, periodo):
    query = '''
            select distinct
            a.cod_materia,
            b.nom_materia,
            a.id_grupo,
            a.num_grupo grupo,
            DECODE(d.NUM_DIA,2,'Lunes',3,'Martes',4,'Miercoles',5,'Jueves',6,'Viernes',7,'Sabado',1,'Domingo') DIA,
            sinu.funb_hora_militar(d.hor_inicio) hor_inicio,
            sinu.funb_hora_militar(d.hor_fin) hor_fin,
            f.nom_tercero nombre_docente,
            f.pri_apellido apellido_docente,
            f.NUM_IDENTIFICACION id_docente,
            a.cod_periodo periodo,
            d.id_div_grupo
            from
            sinu.SRC_GRUPO A,
            sinu.SRC_MAT_PENSUM B,
            sinu.SRC_UNI_ACADEMICA C,
            sinu.src_hor_grupo d,
            sinu.src_vinculacion e,
            sinu.bas_tercero f,
            sinu.src_jornada g,
            sinu.src_doc_grupo h
            where a.cod_unidad = b.cod_unidad
            and a.cod_pensum = b.cod_pensum
            and a.cod_materia= b.cod_materia
            and a.cod_unidad = c.cod_unidad
            and a.id_grupo   = d.id_grupo (+)
            and a.id_vinculacion (+) = e.id_vinculacion
            and f.id_tercero=e.id_tercero
            and c.id_jornada = g.id_jornada
            and a.id_vinculacion = h.id_vinculacion
            and a.id_grupo = h.id_grupo
            and a.cod_periodo = '{}'
            and a.cod_materia = '{}'
            and c.nom_unidad not like '%ESPECI%'
            and c.nom_unidad not like '%DIPL%'
            and c.nom_unidad not like '%CURS%'
            and (a.num_grupo like 'MAGIS%' or a.num_grupo like 'REMOT%')
            group by f.num_identificacion,f.nom_tercero,f.seg_nombre,f.pri_apellido,f.seg_apellido,e.id_tercero,a.cod_unidad, c.nom_unidad,b.uni_teorica,b.num_nivel, a.cod_materia, b.nom_materia, a.id_grupo,a.num_grupo, d.num_dia,
            g.nom_jornada, a.id_vinculacion, h.tip_docente, a.cod_periodo, sinu.funb_hora_militar(
                d.hor_inicio), sinu.funb_hora_militar(d.hor_fin), d.id_div_grupo
            order by 4
            '''.format(periodo, asignatura)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

def grupos_asignatura_sisef(asignatura, periodo, docente):
    query = '''
    SELECT DISTINCT e.id_tercero,
      j.num_identificacion Num_Identificacion,
      j.nom_largo Nombre_Docente,
      --(SELECT nom_largo FROM sinu.bas_tercero where id_tercero=e.id_tercero) "Nombre_Docente",
      a.cod_periodo,
      a.cod_unidad, c.nom_unidad ||' '||g.nom_jornada nom_unidad,
      a.cod_materia,
      b.nom_materia,
      decode (b.cod_tip_materia,1,'TEORICA',2,'PRACTICA',3,'TEORICO-PRACTICA') tip_materia,
      B.COD_PENSUM,
      a.id_grupo,
      a.num_grupo,
      i.id_div_grupo id_subgrupo,
      i.cod_div_grupo sub_grupo
    from   sinu.SRC_GRUPO A, sinu.SRC_MAT_PENSUM B, sinu.SRC_UNI_ACADEMICA C, sinu.src_hor_grupo d, sinu.src_vinculacion e,  sinu.src_jornada g, sinu.src_doc_grupo h,  sinu.SRC_DIV_GRUPO i, sinu.bas_tercero j
    where
      a.cod_unidad = b.cod_unidad
      and    a.cod_pensum = b.cod_pensum
      and    a.cod_unidad = c.cod_unidad
      and    a.cod_materia= ('{}')
      and    a.cod_materia= b.cod_materia
      and    a.id_grupo   = d.id_grupo (+)
      and    j.id_tercero=e.id_tercero
      and    a.id_vinculacion (+) = e.id_vinculacion
      and    c.id_jornada = g.id_jornada
      and    a.id_vinculacion = h.id_vinculacion
      and    a.id_grupo = h.id_grupo
      and    a.cod_periodo = ('{}')
      and  j.num_identificacion = ('{}')
      and (d.id_div_grupo     = i.id_div_grupo(+))
      group by e.id_tercero,a.cod_unidad, c.nom_unidad,b.uni_teorica,b.num_nivel, a.cod_materia, b.nom_materia, a.id_grupo,a.num_grupo, d.num_dia,
      to_char(d.fec_inicio,'day'), sinu.funb_hora_militar(d.hor_inicio), sinu.funb_hora_militar(d.hor_fin), g.nom_jornada, a.id_vinculacion, h.tip_docente, i.id_div_grupo,
      i.cod_div_grupo, b.cod_pensum, b.cod_tip_materia,j.num_identificacion, a.cod_periodo, j.nom_largo
      order by   3'''.format(asignatura, periodo, docente)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

def correccion_notas_matricula(periodo, num_identificacion, programa):
  # periodo= '20232'
  # num_identificacion= '72222244'
  # programa= '13011'
  query = '''
    select distinct e.id_tercero,
    j.nom_largo NOMBRE_DOCENTE,
    j.num_identificacion IDENTIFICACION,
    a.cod_unidad,
    c.nom_unidad ||' '||g.nom_jornada nom_unidad, 
    a.cod_materia,
    b.nom_materia,
    b.uni_teorica,
    b.num_nivel,
    decode (b.cod_tip_materia,1,'TEORICA',2,'PRACTICA',3,'TEORICO-PRACTICA') tip_materia,
    B.COD_PENSUM,
    a.id_grupo,
    a.num_grupo,
    i.id_div_grupo id_subgrupo,
    i.cod_div_grupo sub_grupo,
    DECODE(h.tip_docente,1,'Principal',2,'Suplente') Rol,
    (select unique e.nom_cargo  
    from sinu.bas_tercero a, sinu.src_vinculacion b, sinu.bas_dependencia c, sinu.bas_cargo e
    where a.id_tercero = b.id_tercero
    and c.id_dependencia = decode(b.id_dependencia,null,c.id_dependencia,b.id_dependencia)
    and e.id_cargo = decode(b.id_cargo,null,e.id_cargo,b.id_cargo)
    and b.id_vinculacion=a.id_vinculacion and rownum<=1
    and e.nom_cargo like '%PRO%'
    ) "Cargo"
    from   sinu.SRC_GRUPO A, sinu.SRC_MAT_PENSUM B, sinu.SRC_UNI_ACADEMICA C, sinu.src_hor_grupo d, sinu.src_vinculacion e,  sinu.src_jornada g, sinu.src_doc_grupo h,  sinu.SRC_DIV_GRUPO i, sinu.BAS_TERCERO J
    where  a.cod_unidad = b.cod_unidad
    and    j.id_tercero = e.id_tercero
    and    a.cod_pensum = b.cod_pensum
    and    a.cod_materia= b.cod_materia
    and    a.cod_unidad = c.cod_unidad
    and    a.id_grupo   = d.id_grupo (+)
    and    a.id_vinculacion (+) = e.id_vinculacion
    and    c.id_jornada = g.id_jornada
    and    a.id_vinculacion = h.id_vinculacion
    and    a.id_grupo = h.id_grupo
    and  c.nom_unidad not like '%ESPECI%'
    and  c.nom_unidad not like '%DIPL%'  
    and (d.id_div_grupo     = i.id_div_grupo(+))
    and c.nom_unidad not like '%CURS%'
    and a.cod_periodo in ({})
    and j.num_identificacion = '{}'
    and a.cod_unidad = '{}'
    group by e.id_tercero,
    a.cod_unidad,
    c.nom_unidad,
    b.uni_teorica,
    b.num_nivel, 
    a.cod_materia,
    b.nom_materia,
    a.id_grupo,
    a.num_grupo,
    d.num_dia,
    to_char(d.fec_inicio,'day'),
    sinu.funb_hora_militar(d.hor_inicio),
    sinu.funb_hora_militar(d.hor_fin),
    g.nom_jornada,
    a.id_vinculacion,
    h.tip_docente,
    i.id_div_grupo,
    i.cod_div_grupo, b.cod_pensum, b.cod_tip_materia,j.nom_largo,
    j.num_identificacion
    order by   "NOMBRE_DOCENTE"
  '''.format(periodo, num_identificacion, programa)
  conn = connect_oracle()
  result = conn.execute(query)
  return result.fetchall()

def horarioProfesores(identificacion, periodo):
    # quitar luego
    # periodo="20232"
    # identificacion="1143425157"
    query = '''
        select *
        from (
        select distinct e.id_tercero,
            (
                select nom_largo
                from sinu.bas_tercero
                where id_tercero = e.id_tercero
            ) "Nombre_Docente", --d.id_aula,
            (
                select num_identificacion
                from sinu.bas_tercero
                where id_tercero = e.id_tercero
            ) IDENTIFICACION,
            a.cod_unidad,
            c.nom_unidad || ' ' || g.nom_jornada nom_unidad,
            b.uni_teorica,
            b.num_nivel,
            a.cod_materia,
            b.nom_materia,
            a.id_grupo,
            a.num_grupo,
            DECODE(h.tip_docente, 1, 'Principal', 2, 'Suplente') Rol,
            d.id_aula,
            (
                select nom_aula
                from sinu.src_aula
                where to_char(cod_aula) = to_char(d.id_aula)
            ) aula,
            d.num_dia,
            upper(substr(to_char(d.fec_inicio, 'day'), 1, 2)) dia,
            sinu.funb_hora_militar (d.hor_inicio) hor_inicio,
            sinu.funb_hora_militar (d.hor_fin) hor_fin,
            (
                select unique e.nom_cargo
                from sinu.bas_tercero a,
                    sinu.src_vinculacion b,
                    sinu.bas_dependencia c,
                    sinu.bas_cargo e
                where a.id_tercero = b.id_tercero
                    and c.id_dependencia = decode(
                        b.id_dependencia,
                        null,
                        c.id_dependencia,
                        b.id_dependencia
                    )
                    and e.id_cargo = decode(b.id_cargo, null, e.id_cargo, b.id_cargo)
                    and b.id_vinculacion = a.id_vinculacion
                    and rownum <= 1
                    and e.nom_cargo like '%PRO%'
            ) "Cargo",
            a.cod_periodo
        from sinu.SRC_GRUPO A,
            sinu.SRC_MAT_PENSUM B,
            sinu.SRC_UNI_ACADEMICA C,
            sinu.src_hor_grupo d,
            sinu.src_vinculacion e,
            sinu.src_jornada g,
            sinu.src_doc_grupo h
        where a.cod_periodo in ('{}')
            and a.cod_unidad = b.cod_unidad
            and a.cod_pensum = b.cod_pensum
            and a.cod_materia = b.cod_materia
            and a.cod_unidad = c.cod_unidad
            and a.id_grupo = d.id_grupo (+)
            and a.id_vinculacion (+) = e.id_vinculacion
            and c.id_jornada = g.id_jornada
            and a.id_vinculacion = h.id_vinculacion
        group by e.id_tercero,
            a.cod_unidad,
            c.nom_unidad,
            b.uni_teorica,
            b.num_nivel,
            a.cod_materia,
            b.nom_materia,
            a.id_grupo,
            a.num_grupo,
            d.id_aula,
            d.num_dia,
            to_char(d.fec_inicio, 'day'),
            sinu.funb_hora_militar(d.hor_inicio),
            sinu.funb_hora_militar(d.hor_fin),
            g.nom_jornada,
            a.id_vinculacion,
            h.tip_docente,
            a.cod_periodo
        order by IDENTIFICACION)
        where IDENTIFICACION = '{}'
    '''.format(periodo, identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchall()
    return info


def gruposProfesores(identificacion, periodo):
    # quitar luego
    #periodo="20232"
    #identificacion="1143425157"
    query = '''select distinct e.id_tercero,
      j.nom_largo NOMBRE_DOCENTE,
      j.num_identificacion IDENTIFICACION,
      a.cod_unidad,
      c.nom_unidad ||' '||g.nom_jornada nom_unidad, 
      a.cod_materia,
      b.nom_materia,
      b.uni_teorica,
      b.num_nivel,
      decode (b.cod_tip_materia,1,'TEORICA',2,'PRACTICA',3,'TEORICO-PRACTICA') tip_materia,
      B.COD_PENSUM,
      a.id_grupo,
      a.num_grupo,
      i.id_div_grupo id_subgrupo,
      i.cod_div_grupo sub_grupo,
      DECODE(h.tip_docente,1,'Principal',2,'Suplente') Rol,
      (select unique e.nom_cargo  
      from sinu.bas_tercero a, sinu.src_vinculacion b, sinu.bas_dependencia c, sinu.bas_cargo e
      where a.id_tercero = b.id_tercero
      and c.id_dependencia = decode(b.id_dependencia,null,c.id_dependencia,b.id_dependencia)
      and e.id_cargo = decode(b.id_cargo,null,e.id_cargo,b.id_cargo)
      and b.id_vinculacion=a.id_vinculacion and rownum<=1
      and e.nom_cargo like '%PRO%'
      ) "Cargo"
      from   sinu.SRC_GRUPO A, sinu.SRC_MAT_PENSUM B, sinu.SRC_UNI_ACADEMICA C, sinu.src_hor_grupo d, sinu.src_vinculacion e,  sinu.src_jornada g, sinu.src_doc_grupo h,  sinu.SRC_DIV_GRUPO i, sinu.BAS_TERCERO J
      where  a.cod_unidad = b.cod_unidad
      and    j.id_tercero = e.id_tercero
      and    a.cod_pensum = b.cod_pensum
      and    a.cod_materia= b.cod_materia
      and    a.cod_unidad = c.cod_unidad
      and    a.id_grupo   = d.id_grupo (+)
      and    a.id_vinculacion (+) = e.id_vinculacion
      and    c.id_jornada = g.id_jornada
      and    a.id_vinculacion = h.id_vinculacion
      and    a.id_grupo = h.id_grupo
      and  c.nom_unidad not like '%ESPECI%'
      and  c.nom_unidad not like '%DIPL%'  
      and (d.id_div_grupo     = i.id_div_grupo(+))
      and c.nom_unidad not like '%CURS%'
      and a.cod_periodo in {}
      and j.num_identificacion = '{}'
      group by e.id_tercero,
      a.cod_unidad,
      c.nom_unidad,
      b.uni_teorica,
      b.num_nivel, 
      a.cod_materia,
      b.nom_materia,
      a.id_grupo,
      a.num_grupo,
      d.num_dia,
      to_char(d.fec_inicio,'day'),
      sinu.funb_hora_militar(d.hor_inicio),
      sinu.funb_hora_militar(d.hor_fin),
      g.nom_jornada,
      a.id_vinculacion,
      h.tip_docente,
      i.id_div_grupo,
      i.cod_div_grupo, b.cod_pensum, b.cod_tip_materia,j.nom_largo,
      j.num_identificacion
      order by "NOMBRE_DOCENTE"
    '''.format(periodo, identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchall()
    return info

def notasEstudiantesGrupo(idGrupo):
#     query = '''
# WITH Numeros AS (
#     SELECT 1 AS n FROM dual UNION ALL SELECT 2 FROM dual UNION ALL 
#     SELECT 3 FROM dual UNION ALL SELECT 4 FROM dual UNION ALL 
#     SELECT 5 FROM dual UNION ALL SELECT 6 FROM dual UNION ALL 
#     SELECT 7 FROM dual UNION ALL SELECT 8 FROM dual UNION ALL 
#     SELECT 9 FROM dual UNION ALL SELECT 10 FROM dual
# )
# SELECT   t.*
# FROM (
#     SELECT 
#         C.num_identificacion,
#         C.nom_largo AS estudiante,
#         J.nom_unidad AS programa,
#         m.pes_nota AS PESO,
#         m.num_nota AS NOTA,
#         m.val_nota AS NUMERICA,
#         NULL AS def,
#         B.COD_PERIODO
#     FROM
#         sinu.SRC_ALUM_PROGRAMA A
#         INNER JOIN sinu.SRC_ENC_MATRICULA B ON B.id_alum_programa = A.id_alum_programa
#         INNER JOIN sinu.BAS_TERCERO C ON A.id_tercero = C.id_tercero
#         LEFT JOIN sinu.SRC_GRUPO D ON B.id_grupo = D.id_grupo
#         LEFT JOIN sinu.SRC_UNI_ACADEMICA J ON A.cod_unidad = J.cod_unidad
#         LEFT JOIN sinu.SRC_DET_MATRICULA M ON M.id_alum_programa = B.id_alum_programa
#                                        AND M.id_grupo = B.id_grupo
#     WHERE
#         B.id_grupo = '{}'
#         AND A.cod_unidad NOT IN ('17034', '17033', '31132')

#     UNION ALL

#     SELECT
#         g.num_identificacion,
#         g.nom_largo AS estudiante,
#         a.nom_unidad AS programa,
#         peso_table.pes_nota AS PESO,
#         a.num_nota AS NOTA,
#         NVL(TO_NUMBER(a.val_nota DEFAULT NULL ON CONVERSION ERROR), 0) AS NUMERICA,
#         (
#             SELECT NVL(TO_CHAR(l.def_historia, '0D9'), '----')
#             FROM sinu.src_his_academica l
#             WHERE c.id_grupo = l.id_grupo
#               AND l.id_alum_programa = f.id_alum_programa
#               AND ROWNUM = 1
#         ) AS def,
#         A.COD_PERIODO
#     FROM
#         sinu.src_vis_not_parciales_hist a
#         LEFT JOIN sinu.bas_tercero g ON g.num_identificacion = a.num_identificacion
#         LEFT JOIN sinu.src_grupo c ON a.id_grupo = c.id_grupo
#         LEFT JOIN sinu.src_alum_programa f ON a.id_alum_programa = f.id_alum_programa
#         LEFT JOIN (
#             SELECT id_grupo, num_nota, pes_nota
#             FROM sinu.src_not_grupo
#         ) peso_table ON peso_table.id_grupo = a.id_grupo
#                       AND peso_table.num_nota = a.num_nota
#     WHERE
#         NOT EXISTS (
#             SELECT 1
#             FROM sinu.src_det_matricula m
#             WHERE m.id_alum_programa = a.id_alum_programa
#               AND m.id_grupo = a.id_grupo
#         )
#         AND c.id_grupo = '{}'
# ) t
# CROSS JOIN Numeros n
# ORDER BY estudiante, NOTA, n ASC
# '''.format(idGrupo, idGrupo)
    query = '''
      SELECT
      n.num_identificacion,
    -- n.id_alum_programa,
      n.nom_largo                         estudiante,
      n.nom_unidad                        programa,
  -- n.id_grupo,
  -- n.num_grupo,
  -- n.COD_MATERIA,
  -- n.nom_materia,
  -- l.num_identificacion CC_DOCENTE,
  -- l.nom_largo docente,
  -- l.dir_email_per Email_personal,
  -- l.dir_email Email_institucional,
      (
          SELECT
              pes_nota
          FROM
              sinu.src_not_grupo
          WHERE
                  src_not_grupo.id_grupo = n.id_grupo
              AND src_not_grupo.num_nota = n.num_nota
              AND ROWNUM <= 1
      )                                   peso,
      n.num_nota                          nota,
      decode(n.val_nota,
            NULL,
            '-----',
            to_char(n.val_nota, '99D9')) numérica,
      (
          SELECT
              decode(enc.not_definitiva,
                    NULL,
                    '----',
                    to_char(enc.not_definitiva, '99D9'))
          FROM
              sinu.src_enc_matricula enc
          WHERE
                  enc.id_alum_programa = n.id_alum_programa
              AND enc.id_grupo = n.id_grupo
      )                                   not_definitiva,
      n.cod_periodo
  FROM
      sinu.src_vis_not_parciales_hist n,
      sinu.bas_tercero                l,
      sinu.src_vinculacion            m,
      sinu.src_grupo                  v
  WHERE
          l.id_tercero = m.id_tercero
      AND v.id_vinculacion = m.id_vinculacion (+)
      AND v.id_grupo = n.id_grupo
  -- and n.cod_periodo = '20232'
      AND n.id_grupo = ( '{idGrupo}' )
  UNION ALL
  SELECT
      e.num_identificacion,
      -- a.id_alum_programa,
      e.nom_largo                         estudiante,
      c.nom_unidad                        programa,
    -- a.id_grupo, 
    -- b.num_grupo,
    -- b.cod_materia,
    -- f.nom_materia,
    -- g.num_identificacion CC_DOCENTE,
    -- g.nom_largo docente,
    -- g.dir_email_per Email_personal,
    -- g.dir_email Email_institucional,
      (
          SELECT
              pes_nota
          FROM
              sinu.src_not_grupo
          WHERE
                  src_not_grupo.id_grupo = b.id_grupo
              AND src_not_grupo.num_nota = a.num_nota
              AND ROWNUM <= 1
      )                                   peso,
      a.num_nota                          nota,
      decode(a.val_nota,
            NULL,
            '-----',
            to_char(a.val_nota, '99D9')) numérica,
      (
          SELECT
              decode(enc.not_definitiva,
                    NULL,
                    '----',
                    to_char(enc.not_definitiva, '99D9'))
          FROM
              sinu.src_enc_matricula enc
          WHERE
                  enc.id_alum_programa = a.id_alum_programa
              AND enc.id_grupo = b.id_grupo
      )                                   not_definitiva,
      b.cod_periodo
  FROM
      sinu.src_det_matricula a,
      sinu.src_grupo         b,
      sinu.src_uni_academica c,
      sinu.src_alum_programa d,
      sinu.bas_tercero       e,
      sinu.src_materia       f,
      sinu.src_vinculacion   h,
      sinu.bas_tercero       g
  WHERE
          a.id_alum_programa = d.id_alum_programa
      AND d.id_alum_programa = a.id_alum_programa
      AND e.id_tercero = d.id_tercero
      AND b.id_grupo = a.id_grupo
      AND c.cod_unidad = d.cod_unidad
      AND b.id_vinculacion = h.id_vinculacion (+)
      AND h.id_tercero = g.id_tercero (+)
      AND f.cod_materia = b.cod_materia
    -- and b.cod_periodo = ''
      AND a.id_grupo = ( '{idGrupo}' )
  ORDER BY
      estudiante ASC
  '''.format(idGrupo=idGrupo)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchall()
    return info

def listarAsignaturasAll(periodo):
    query = '''
    SELECT DISTINCT
    a.cod_unidad,
    j.nom_unidad,
    D.cod_materia,
    E.nom_materia,
    a.cod_pensum,
    b.cod_periodo
    FROM sinu.SRC_ALUM_PROGRAMA A
    LEFT JOIN sinu.SRC_ENC_MATRICULA B
    ON B.id_alum_programa = A.id_alum_programa
    LEFT JOIN sinu.SRC_TEM_MATRICULA M
    ON A.id_alum_programa = m.id_alum_programa AND b.cod_materia = m.cod_materia 
    and m.cod_periodo = ('{}')
    LEFT JOIN sinu.BAS_TERCERO C
    ON A.id_tercero = C.id_tercero
    LEFT JOIN sinu.SRC_GRUPO D
    ON B.id_grupo = D.id_grupo and m.num_grupo = d.num_grupo
    LEFT JOIN sinu.SRC_MAT_PENSUM E
    ON d.cod_unidad = E.cod_unidad AND d.cod_pensum = E.cod_pensum AND D.cod_materia = E.cod_materia
    LEFT JOIN sinu.SRC_VINCULACION H
    ON D.id_vinculacion = H.id_vinculacion
    LEFT JOIN sinu.BAS_TERCERO F
    ON H.id_tercero = F.id_tercero
    LEFT JOIN sinu.SRC_UNI_ACADEMICA J
    ON A.cod_unidad = J.cod_unidad
    LEFT JOIN sinu.src_hor_grupo I
    ON D.id_grupo = i.id_grupo and nvl(b.id_div_grupo,0) = nvl(i.id_div_grupo,0)
    LEFT JOIN sinu.SRC_AULA G
    ON to_char(i.id_aula) = G.cod_aula
    LEFT JOIN sinu.SRC_DIV_GRUPO L
    ON i.id_div_grupo = l.id_div_grupo
    LEFT JOIN sinu.src_generica k
    ON k.tip_tabla = 'ESTMAT' AND k.cod_tabla != k.tip_tabla 
    AND TO_CHAR(B.est_matricula) = k.cod_tabla
    WHERE
    b.cod_periodo = ('{}') 
    order by 3'''.format(periodo, periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    info = result.fetchall()
    return info

def correccion_notas_programas(periodos, num_identificacion):
  # periodo= '20232'
  # num_identificacion= '72222244'
  # programa= '13011'
  query = '''
    select 
      sg.cod_periodo,sg.cod_unidad, sua.nom_unidad nom_programa, sg.id_vinculacion, bt.nom_largo, bt.num_identificacion
    from 
      sinu.src_grupo sg 
    left join sinu.src_uni_academica sua on sg.cod_unidad = sua.cod_unidad
    left join sinu.src_mat_pensum smp on sg.cod_unidad = smp.cod_unidad and sg.cod_materia = smp.cod_materia and sg.cod_pensum = smp.cod_pensum
    left join sinu.src_vinculacion sv on sg.id_vinculacion = sv.id_vinculacion
    left join sinu.bas_tercero bt on sv.id_tercero = bt.id_tercero
    where cod_periodo in ({}) --and --sg.cod_unidad = '11051' and 
      and sg.id_vinculacion is not null
      and bt.num_identificacion = '{}'
    --sg.usu_creacion = 156949
    group by sg.cod_periodo,sg.cod_unidad, sua.nom_unidad, sg.id_vinculacion, bt.nom_largo, bt.num_identificacion
    order by 6
  '''.format(periodos, num_identificacion)
  conn = connect_oracle()
  result = conn.execute(query)
  return result.fetchall()


def matriculados_hep(periodo):
    query = '''
    WITH q AS (
        SELECT
            a.id_alum_programa id_alum_programa_2,
            g.ID_TERCERO,
            g.num_identificacion identificacion,
            g.nom_largo,
            d.cod_periodo periodo,
            b.cod_unidad,
            h.nom_unidad programa,
            b.cod_pensum pensum,
            a.cod_materia,
            c.nom_materia,
            c.num_nivel,
            c.int_horaria,
            c.uni_teorica creditos,
            a.cod_uni_e Cod_Programa_Equivalente,
            a.cod_pen_e,
            a.cod_materia_e Cod_Asignatura_Equivalente,
            (SELECT nom_materia FROM sinu.src_materia
            WHERE cod_materia = a.cod_materia_e) Asignatura_Equivalente,
            DECODE(tip_periodo,'N','Normal','Vacacional') tipo_periodo,
            v.pro_nivel, 
            v.pro_acumulado,
            a.tip_nota,
            e.nom_tabla tipo_nota,
            d.num_niv_cursa sem_cursada,
            f.nom_tabla est_materia,
            a.def_historia,
            a.ind_aprobada,
            DECODE(a.ind_aprobada,1,'Si','No') aprobada,
            v.tot_uni_matricular,
            v.tot_uni_matriculadas,
            (v.tot_uni_matriculadas-v.tot_uni_pierde) TOT_UNI_APROBADAS,
            v.tot_uni_matriculadas "TOT_UNI_CURSADAS",
            NVL(c.val_posibles,
                (SELECT DECODE(c.tip_nota,'N',x.val_posibles,x.val_posibles_alfa)
                FROM sinu.SRC_REGLAMENTO x,
                      sinu.SRC_PENSUM y
                WHERE x.id_reglamento = y.id_reglamento
                AND y.cod_pensum      = c.cod_pensum
                AND y.cod_unidad      = c.cod_unidad)) val_posibles,
            DECODE(b.est_alumno,0,'INACTIVO',1,'ACTIVO',2,'EGRESADO',3,'MOVILIDAD',4,'TRASLADO',5,'CANCELADO',8,'EXCLUIDO',9,'GRADUADO',10,'ANULADO',12,'GRADUADO TEMPORAL') "ESTADO"
        FROM  sinu.SRC_HIS_ACADEMICA a
        LEFT JOIN sinu.SRC_ALUM_PROGRAMA b ON a.id_alum_programa = b.id_alum_programa
        LEFT JOIN sinu.SRC_MAT_PENSUM c ON b.cod_unidad = c.cod_unidad 
                                    AND b.cod_pensum = c.cod_pensum 
                                    AND a.cod_materia = c.cod_materia
        LEFT JOIN sinu.BAS_TERCERO g ON b.id_tercero = g.id_tercero
        LEFT JOIN sinu.SRC_UNI_ACADEMICA h ON b.cod_unidad = h.cod_unidad
        LEFT JOIN sinu.SRC_GENERICA e ON e.tip_tabla = 'TIPNOT' 
                                AND e.cod_tabla <> e.tip_tabla 
                                AND e.cod_tabla = a.tip_nota
        LEFT JOIN sinu.SRC_GENERICA f ON f.tip_tabla = 'ESTMAT' 
                                AND f.cod_tabla <> f.tip_tabla 
                                AND f.cod_tabla = a.est_materia
        LEFT JOIN sinu.SRC_ALUM_PERIODO d ON a.id_alum_programa = d.id_alum_programa 
                                    AND a.per_acumula = d.cod_periodo
        LEFT JOIN sinu.src_vis_alum_per_est_web v ON b.id_alum_programa = v.id_alum_programa
        WHERE h.cod_est_metodologica = 'ESTMET' 
          AND h.est_metodologica = 4
          AND a.cod_periodo in '{periodo}'
          and v.cod_periodo in '{periodo}'
    ),
    total_creditos AS (
        SELECT 
            A1.ID_ALUM_PROGRAMA,
            SUM(M.UNI_TEORICA) AS total_creditos
        FROM sinu.SRC_ALUM_PROGRAMA A1
        JOIN sinu.SRC_MAT_PENSUM M ON A1.COD_PENSUM = M.COD_PENSUM AND A1.COD_UNIDAD = M.COD_UNIDAD
        JOIN sinu.SRC_HIS_ACADEMICA H ON A1.ID_ALUM_PROGRAMA = H.ID_ALUM_PROGRAMA AND M.COD_MATERIA = H.COD_MATERIA
        JOIN sinu.BAS_TERCERO B1 ON A1.ID_TERCERO = B1.ID_TERCERO
        JOIN sinu.SRC_UNI_ACADEMICA U ON A1.COD_UNIDAD = U.COD_UNIDAD
        WHERE H.DEF_HISTORIA >= 3.0
          AND U.NOM_UNIDAD NOT LIKE '%CURSO%'
          AND U.NOM_UNIDAD NOT LIKE '%DIPLOMA%'
          AND U.NOM_UNIDAD NOT LIKE '%ESPECIALIZAC%'
          AND U.NOM_UNIDAD NOT LIKE '%DIPIPLOMA%'
          AND U.NOM_UNIDAD NOT LIKE '%MAESTRIA%'
        GROUP BY A1.ID_ALUM_PROGRAMA
    ),
    cantidad_periodos AS (
        SELECT 
            id_alum_programa,
            COUNT(DISTINCT cod_periodo) AS cantidad_periodos
        FROM sinu.src_his_academica
        GROUP BY id_alum_programa
    )
    SELECT DISTINCT
          a.id_alum_programa,
          d.id_tercero,
          d.num_identificacion,
          d.nom_tercero || ' ' || d.seg_nombre AS Nombres,
          d.pri_apellido || ' ' || d.seg_apellido AS Apellidos,
          d.gen_tercero,
          d.fec_nacimiento,
          d.tel_cecular celular,
          d.DIR_EMAIL EMAIL_INSTITUCIONAL, 
          d.DIR_EMAIL_PER EMAIL_PERSONAL,
          b.cod_unidad cod_programa,
          b.nom_unidad programa,
          c.num_niv_cursa semestre,
          c.cod_periodo periodo_Actual,
          a.cod_periodo periodo_ingreso,
          c.EST_MAT_ACA Matrícula_Academica,
          c.est_mat_fin Matricula_Financiera,
          a.cod_pensum,
          DECODE(a.EST_ALUMNO, 0, 'INACTIVO', 1, 'ACTIVO', 2, 'EGRESADO', 3, 'MOVILIDAD', 4, 'TRASLADO', 5, 'CANCELADO', 8, 'EXCLUIDO', 9, 'GRADUADO', 10, 'ANULADO') "ESTADO_ALUMNO",
          c.tot_uni_matricular,
          c.tot_uni_matriculadas,
          DECODE(b.cod_modalidad,1,'Pregrado',2,'Posgrado',3,'Edu Continuada') Modalidad,
          total_creditos.total_creditos AS total_creditos_cursados,
          B.tot_uni_aprobacion tot_unidades_programa,
          cantidad_periodos.cantidad_periodos
    FROM sinu.src_alum_programa a
    LEFT JOIN sinu.src_uni_academica b ON a.cod_unidad = b.cod_unidad 
    LEFT JOIN sinu.src_alum_periodo c ON a.id_alum_programa = c.id_alum_programa
    LEFT JOIN sinu.bas_tercero d ON a.id_tercero = d.id_tercero
    LEFT JOIN sinu.src_generica h ON d.eps_tercero = h.cod_tabla AND h.tip_tabla = 'CODEPS' 
    LEFT JOIN sinu.bas_geopolitica e ON d.id_ubi_nac = e.id_geopolitica
    LEFT JOIN sinu.bas_geopolitica f ON d.id_ubi_res = f.id_geopolitica
    LEFT JOIN sinu.SRC_ENC_LIQUIDACION g ON a.id_alum_programa = g.id_alum_programa
    LEFT JOIN sinu.total_creditos ON a.id_alum_programa = total_creditos.ID_ALUM_PROGRAMA
    LEFT JOIN sinu.cantidad_periodos ON a.id_alum_programa = cantidad_periodos.id_alum_programa
    WHERE c.cod_periodo = '{periodo}'
      AND g.COD_PERIODO = '{periodo}'
      AND c.est_mat_fin = 1
      AND g.est_liquidacion = 2
      AND g.tip_liquidacion = 1
    ORDER BY 5
    '''.format(periodo=periodo)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()


def validar_nuevo_estudiante(identificacion):
    query = '''
      select id_alum_programa,id_tercero,num_identificacion , cantidad_periodos
      from (
        select distinct
        a.id_alum_programa id_alum_programa,
        d.id_tercero id_tercero,
        d.num_identificacion num_identificacion,
        (select count(distinct(cod_periodo))  from sinu.src_his_academica y where y.id_alum_programa = a.id_alum_programa and y.cod_periodo <> c.cod_periodo) cantidad_periodos
        from sinu.src_alum_programa a, sinu.src_uni_academica b, sinu.src_alum_periodo c, sinu.bas_tercero d, sinu.bas_geopolitica e, sinu.bas_geopolitica f, sinu.SRC_ENC_LIQUIDACION g
        where a.id_tercero = d.id_tercero
            and a.id_alum_programa = c.id_alum_programa
            and a.cod_unidad = b.cod_unidad
            and d.id_ubi_nac=e.id_geopolitica
            and d.id_ubi_res=f.id_geopolitica
            and c.cod_periodo = '20241'
            and g.COD_PERIODO = '20241'
            and b.cod_modalidad in ('1','3')
            and a.est_alumno IN (1,7)
            and c.est_mat_fin=1
            and g.est_liquidacion = 2
            and g.tip_liquidacion = 1
            and a.id_alum_programa = g.id_alum_programa
            and  b.cod_unidad not in ('19028','24009','32121','32123','32144','32160','32168','50015','60016',
        '60022','21071','32178','19002','19038','50017','21018','22088','32149','32153','19073','24082','32124',
        '32125','32142','32143','60019','22079','23029','40503','17034','32163','22038','22069','22087','32147',
        '32148','32209','32122','32162','60014','160B1','32177','32194','17033','24068','24073','32118','32126',
        '32131','60018','B0009','22086','22106','18000','19001','32150','32204','19043','24062','31132','32133',
        '32140','32145','32154','22012','22039','32183','13035','24012','24019','32128','32130','32132','32135',
        '32165','21015','40065','17099','32179','32186','32300','60017','32174','23071','60024','50016','60021',
        '11001','60023','60001','19039','23035','17007','90005','23047','60002','24084','90001','90002','32206') 
        )  WHERE cantidad_periodos = 0 
        and num_identificacion = '{}'
    '''.format(identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()



def ListarAsignaturaSisef(identificacion, periodo):
    query = '''
          SELECT DISTINCT
              C.num_identificacion,
              C.nom_largo alumno,
              b.cod_periodo,
              E.nom_materia,
              D.cod_materia,
              NVL(D.num_grupo,0) num_grupo,
              DECODE (i.num_dia,2,'Lunes',3,'Martes',4,'Miercoles',5,'Jueves',6,'Viernes',7,'Sabado',1,'Domingo') dia,
              i.num_dia,
              sinu.funb_hora_militar (i.hor_inicio) hor_inicio,
              sinu.funb_hora_militar(i.hor_fin) hor_fin,
              F.nom_largo profesor,
              A.cod_unidad,
              DECODE(e.cod_tip_materia,1,'TEORICA',2,'PRACTICA',3,'TEORICO-PRACTICA') TIPO_ASIGNATURA,
              e.uni_teorica creditos,
              e.int_horaria,
              g.nom_aula,
              ( select LISTAGG (l.cod_requisito, ',') WITHIN GROUP (order by l.cod_requisito)
              from sinu.src_req_materia l
              where l.cod_materia = d.cod_materia
              and l.cod_pensum = d.cod_pensum
              and l.cod_unidad = d.cod_unidad) pre_requisito
              FROM sinu.SRC_ALUM_PROGRAMA A
              LEFT JOIN sinu.SRC_ENC_MATRICULA B
              ON B.id_alum_programa = A.id_alum_programa
              LEFT JOIN sinu.BAS_TERCERO C
              ON A.id_tercero = C.id_tercero
              LEFT JOIN sinu.SRC_GRUPO D
              ON B.id_grupo = D.id_grupo
              LEFT JOIN sinu.SRC_MAT_PENSUM E
              ON d.cod_unidad = E.cod_unidad AND d.cod_pensum = E.cod_pensum AND D.cod_materia = E.cod_materia
              LEFT JOIN sinu.SRC_AULA G
              ON D.id_aula = G.id_aula
              LEFT JOIN sinu.SRC_VINCULACION H
              ON D.id_vinculacion = H.id_vinculacion
              LEFT JOIN sinu.BAS_TERCERO F
              ON H.id_tercero = F.id_tercero
              LEFT JOIN sinu.SRC_UNI_ACADEMICA J
              ON A.cod_unidad = J.cod_unidad
              LEFT JOIN sinu.src_hor_grupo I
              ON D.id_grupo = i.id_grupo
              WHERE
              b.cod_periodo = '{}'
              AND j.cod_modalidad = '1'
              AND C.num_identificacion = '{}'
              and b.est_matricula <> 5
              order by 8, 9
          '''.format(periodo, identificacion)
    conn = connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

def validarpagomatricula(periodo,num_identificacion):
    query='''
          SELECT
              d.num_identificacion,
              d.nom_largo nombres,
              d.dir_email_per correo_personal,
              d.dir_email correo_institucional,
              d.dir_residencia,
              d.tel_cecular,
              d.tel_residencia,
              c.cod_unidad cod_programa,
              e.nom_unidad,
              a.cod_periodo,
              a.num_documento liquidacion,
              f.nom_concepto,
              DECODE(a.tip_liquidacion,1,'Matricula',2,'Pecunario') tip_liquidacion,
              TO_DATE(TO_CHAR(a.fec_pago, 'YYYY/MM/DD HH24:MI:SS'), 'YYYY/MM/DD HH24:MI:SS') fecha_pago,
              a.fec_liquidacion,
              TO_CHAR(NVL(TO_CHAR(CASE WHEN f.tip_concepto = 1 THEN b.val_liquidado ELSE 0 END), '0')) AS val_cobros,
              TO_CHAR(NVL(TO_CHAR(CASE WHEN f.tip_concepto = 2 THEN b.val_liquidado ELSE 0 END), '0')) AS val_descuentos,
              TO_CHAR(NVL(TO_CHAR(CASE WHEN f.tip_concepto = 1 THEN CASE WHEN a.val_pagado < 0 THEN 0 ELSE a.val_pagado END ELSE 0 END), '0')) AS val_Pago,
              g.est_mat_aca,
              g.est_mat_fin,
              CASE WHEN f.tip_concepto = 1 THEN
                  CASE WHEN a.est_liquidacion = 1 THEN 'Sin pago' ELSE 'Pagada' END
              ELSE TO_CHAR(f.tip_concepto) END AS est_pago,
              TO_CHAR(f.tip_concepto) AS tip_concepto
              FROM
              SINU.SRC_ENC_LIQUIDACION a
              JOIN SINU.SRC_DET_LIQUIDACION b ON a.id_enc_liquidacion = b.id_enc_liquidacion
              JOIN SINU.SRC_ALUM_PROGRAMA c ON a.id_alum_programa = c.id_alum_programa
              JOIN SINU.BAS_TERCERO d ON c.id_tercero = d.id_tercero
              JOIN SINU.SRC_UNI_ACADEMICA e ON c.cod_unidad = e.cod_unidad
              JOIN SINU.FIN_CONCEPTO f ON b.id_concepto = f.id_concepto
              JOIN SINU.SRC_ALUM_PERIODO g ON a.id_alum_programa = g.id_alum_programa AND a.cod_periodo = g.cod_periodo
              JOIN SINU.SRC_SEDE h ON e.id_sede = h.id_sede
              JOIN SINU.SRC_SECCIONAL i ON h.id_seccional = i.id_seccional
              WHERE
                (a.cod_periodo = '{}' OR a.cod_periodo like '24G%')
                  AND e.cod_modalidad = '1' AND a.tip_liquidacion = 1   AND d.num_identificacion = '{}'
              ORDER BY 1

'''.format(periodo, num_identificacion)
    conn=connect_oracle()
    result = conn.execute(query)
    return result.fetchall()

def MatriculaCursosFormacion(periodo):
    query='''
      SELECT DISTINCT 
    a.id_alum_programa,
    d.id_tercero,
    d.num_identificacion,
    d.nom_tercero || ' ' || d.seg_nombre AS Nombres,
    d.pri_apellido || ' ' || d.seg_apellido AS Apellidos,
    d.tel_cecular telefono,
    d.gen_tercero,
    b.cod_unidad AS cod_programa,
    b.nom_unidad AS programa,
    c.num_niv_cursa AS semestre,
    c.cod_periodo,
    (SELECT MAX(ma.fec_matricula) 
    FROM sinu.SRC_ENC_MATRICULA ma 
    WHERE ma.id_alum_programa = A.id_alum_programa
    AND (ma.cod_periodo LIKE '{}%' OR ma.cod_periodo LIKE '{}%')) AS fec_matricula,
    c.est_mat_aca AS Matricula_Academica,
    c.est_mat_fin AS Matricula_Financiera,
    
    DECODE(b.cod_modalidad, 1, 'Pregrado', 2, 'Posgrado', 3, 'Edu Continuada') AS Modalidad
FROM 
    sinu.src_alum_programa a
    JOIN sinu.src_uni_academica b ON a.cod_unidad = b.cod_unidad 
    JOIN sinu.src_alum_periodo c ON a.id_alum_programa = c.id_alum_programa
    JOIN sinu.bas_tercero d ON a.id_tercero = d.id_tercero    
WHERE 
    (c.cod_periodo LIKE '{}%' OR c.cod_periodo LIKE '{}%')
    AND a.est_alumno IN (1, 7)
    AND (c.est_mat_aca = 0 OR c.est_mat_aca = 1)
    AND c.est_mat_fin = 1
    AND EXISTS (
        SELECT 1
        FROM sinu.src_alum_programa ap
        WHERE ap.id_tercero = a.id_tercero
          AND ap.cod_unidad = '25070'
    )
ORDER BY 
    3
'''.format(periodo.valora, periodo.valorb, periodo.valora, periodo.valorb)
    conn=connect_oracle()
    result = conn.execute(query)
    return result.fetchall()
