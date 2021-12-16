#####################################################
# VARIABLES GLOBALES - ACCESIBLES DESDE TODA LA APP #
#####################################################

from apoyo.manejo_de_bases import Base_de_datos

cod_usuario = None
usuario = None
oficina = None
texto_bienvenida = None

# 0. Tablas relacionales
id_b_ospa = '13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4'
id_usuarios = '12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY'
base_usuario = Base_de_datos(id_usuarios, 'Usuario')
base_datos_usuario = Base_de_datos(id_usuarios, 'Datos_de_usuario')
base_relacion_docs = Base_de_datos(id_b_ospa, 'RELACION_DOCS')
base_relacion_docs_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_D')
base_relacion_dr_ep =  Base_de_datos(id_b_ospa, 'RELACION_DR-EP')
base_relacion_dr_ep_hist =  Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_DR-EP')
base_relacion_de_ep =  Base_de_datos(id_b_ospa, 'RELACION_DE-EP')
base_relacion_de_ep_hist =  Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_DE-EP')
base_relacion_mp_ep =  Base_de_datos(id_b_ospa, 'RELACION_MP-EP')
base_relacion_mp_ep_hist =  Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_MP-EP')
base_parametros_dep = Base_de_datos(id_b_ospa, 'PARAMETROS')
       
tabla_parametros_dep = base_parametros_dep.generar_dataframe()

# 1. Bases de datos principales
# Documentos recibidos
b_dr_cod = Base_de_datos(id_b_ospa, 'DOCS_R')
b_dr = Base_de_datos(id_b_ospa, 'DOC_RECIBIDOS')
b_dr_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_DR')
# Documentos emitidos
b_de_cod = Base_de_datos(id_b_ospa, 'DOCS_E')
b_de = Base_de_datos(id_b_ospa, 'DOC_EMITIDOS')
b_de_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_DE')
# Extremo de problemas
b_ep_cod = Base_de_datos(id_b_ospa, 'EXT_P')
b_ep = Base_de_datos(id_b_ospa, 'EXT_PROBLEMA')
b_ep_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_EP')
# Macro problemas
b_mp_cod = Base_de_datos(id_b_ospa, 'MC_P')
b_mp = Base_de_datos(id_b_ospa, 'MACROPROBLEMA')
b_mp_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_MP')
# Administrados
b_adm = Base_de_datos(id_b_ospa, 'ADMINISTRADOS')

# 2. Bases de datos complementarias
# 2.1 Directorio de Oficinas
id_b_efa = '1pjHXiz15Zmw-49Nr4o1YdXJnddUX74n7Tbdf5SH7Lb0'
b_efa = Base_de_datos(id_b_efa, 'Directorio')
tabla_directorio = b_efa.generar_dataframe()
tabla_directorio_efa = tabla_directorio[tabla_directorio['TIPO_OFICINA']!="OTRO"]
tabla_directorio_efa_final = tabla_directorio_efa[tabla_directorio_efa['Tipo de entidad u oficina']!="T_EFA_DIR"]
# 2.1 Ubigeo
id_lista_efa = "1ephi7hS0tHRQQq5nlkV141ZCY54FUfkw13EeKn310Y4"
b_lista_efa = Base_de_datos(id_lista_efa, 'Lista de EFA')
tabla_lista_efa = b_lista_efa.generar_dataframe()

# 3. Listas dependientes
# 21. Lista de EFA
lista_efa_dependiente = tabla_directorio.loc[:,['Tipo de entidad u oficina', 'EFA ABREVIADO', 'Departamento', 'Entidad u oficina', 'EFA_OSPA']]
lista_efa_ospa = sorted(list(lista_efa_dependiente['EFA_OSPA'].unique()))
# 3.2 Ubigeo
tabla_departamento_efa = tabla_lista_efa.loc[:, ['DEP_OSPA', 'PROV_DIST_OSPA']]
departamento_ospa = sorted(list(tabla_lista_efa['DEP_OSPA'].unique()))

# 4. Parámetros
ancho_v_vista = 1025
alto_v_vista = 600
ancho_v_vista_vitrina = 950
alto_v_vista_vitrina = 120

ancho_v_busqueda = 1300
alto_v_busqueda = 568
ancho_v_busqueda_vitrina = 950
ancho_v_busqueda_de_vitrina = 1065
ancho_v_busqueda_ep_vitrina = 1210
ancho_v_busqueda_peq1_vitrina = 1040
ancho_v_busqueda_pf_vitrina = 900
ancho_v_busqueda_mp_vitrina = 800
ancho_v_busqueda_mpf_vitrina = 800
alto_v_busqueda_vitrina = 240
ancho_v_busqueda_prei_vitrina = 1065
ancho_v_busqueda_peq2_vitrina = 1180

alto_logo = 50
ancho_logo = 280

alto_ventana_secundaria = 413
ancho_ventana_secundaria = 403

alto_franja_inferior_1 = 52
ancho_franja_inferior_1 = 400

# 4.1 Bases de datos
id_parametros = '1NPg8Q0O_NqQ6bkRhy4ow17x2XJ08r6Ev3R6X80WmZ3c'
base_parametros = Base_de_datos(id_parametros, 'PARAMETROS')
tabla_parametros = base_parametros.generar_dataframe()
base_parametros_act = Base_de_datos(id_parametros, 'Datos de actividad')
tabla_parametros_act = base_parametros_act.generar_dataframe()
# 4.2 Desplegables en Drive
agente_conta = list(set(tabla_parametros['AGENTE CALCULADORA']))
componente_amb = list(set(tabla_parametros['COMPONENTE CALCULADORA']))
actividad_eco = list(set(tabla_parametros['ACTIVIDAD CALCULADORA']))
extension = list(set(tabla_parametros['EXTENSION CALCULADORA']))
ubicacion = list(set(tabla_parametros['UBICACION CALCULADORA']))
ocurrencia = list(set(tabla_parametros['OCURRENCIA CALCULADORA']))
# 4.4 Desplegables en Local
combo_vacio = ()
tipo_afectacion = ('AGENTE CONTAMINANTE', 'EXTRACCIÓN DE RECURSOS')
estado_problemas = ('ABIERTA', 'CERRADO')
tipo_causa = ('CAUSA DESCONOCIDA', 'CAUSA NATURAL', 'CAUSA HUMANA')
tipo_ingreso = ('DIRECTO', 'DERIVACION-SUBDIRECCION', 
                'DERIVACION-SUPERVISION', 'DERIVACION-SINADA')
tipo_documento = ('OFICIO', 'MEMORANDO', 'CARTA', 'OFICIO CIRCULAR','MEMORANDO CIRCULAR', 'CARTA CIRCULAR',
                  'INFORME', 'RESOLUCIÓN', 'CÉDULA DE NOTIFICACIÓN', 'INFORME MÚLTIPLE', 'OTROS')
especialista = ('Zurita, Carolina', 'López, José')
tipo_indicacion = ('No corresponde', 'Archivar', 'Actualizar', 'Crear')
si_no = ('Si', 'No')
tipo_respuesta = ('Ejecutó supervisión','Solicitó información a administrado',
                  'Ejecutó acción de evaluación', 'Inició PAS', 'Administrado en adecuación / formalización',
                  'Programó supervisión', 'Programó acción de evaluación', 'No es competente',
                  'No corresponde lo solicitado', 'En evaluación de la EFA', 'Otros')
categorias = ('Pedido de información', 'Pedido de información adicional', 'Pedido de información urgente',
              'Reiterativo', 'Oficio a OCI')
marco_pedido = ('EFA', 'OEFA',
                'Colaboración', 'Delegación', 'Conocimiento')

# 5. Tablas resumen
# 5.0 Relaciones
tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
tabla_relacion_mp_ep = base_relacion_mp_ep.generar_dataframe()
# 5.1 Documentos recibidos
tabla_de_dr_cod = b_dr_cod.generar_dataframe()
tabla_de_dr_completa = b_dr.generar_dataframe()
tabla_de_dr_resumen = tabla_de_dr_completa.drop(['VIA_RECEPCION', 'HT_ENTRANTE', 'TIPO_REMITENTE', 'CATEGORIA_REMITENTE',
                                            'F_ING_OEFA', 'TIPO_DOC', 'ESPECIALISTA_1', 'ESPECIALISTA_2',
                                            'ACCION_1', 'F_ASIGNACION_1', 'F_ASIGNACION_2', 'TIPO_RESPUESTA', 'RESPUESTA',
                                            'F_EJECUCION_1', 'F_EJECUCION_2',
                                            'FECHA_ULTIMO_MOV', 'USUARIO'], axis=1)

# 5.2 Documentos emitidos
tabla_de_de_cod = b_de_cod.generar_dataframe()
tabla_de_de_completa = b_de.generar_dataframe()
tabla_de_de_resumen =  tabla_de_de_completa.drop(['HT_SALIDA', 'FECHA_PROYECTO_FINAL', 
                                                    'FECHA_FIRMA', 'TIPO_DOC', 'CATEGORIA_DESTINATARIO',
                                                    'MARCO_PEDIDO', 'FECHA_ULTIMO_MOV', 'TIPO_DESTINATARIO',
                                                    'PLAZO', 'ESTADO_DOCE', 'ESPECIALISTA', 'USUARIO',
                                                    'FECHA_PROYECTO_REIT',	'SE_EMITIO_REIT', 	'TIPO_DOC_REIT',
                                                    'NUM_DOC_REIT', 'FECHA_FIRMA_REIT', 'FECHA_NOTIFICACION_REIT',
                                                    'FECHA_PROYECTO_OCI', 'SE_EMITIO_OCI', 'TIPO_DOC_OCI', 'NUM_DOC_OCI',
                                                    'FECHA_FIRMA_OCI', 'FECHA_NOTIFICACION_OCI'], axis=1)

# 5.3 Extremos de problema
tabla_de_ep_cod = b_ep_cod.generar_dataframe()
tabla_de_ep_completa = b_ep.generar_dataframe()
tabla_de_ep_resumen = tabla_de_ep_completa.drop(['OCURRENCIA', 'EXTENSION', 'TIPO DE AFECTACION',
                                                'PROVINCIA', 'DESCRIPCION', 'TIPO DE UBICACION', 'DISTRITO', 
                                                'TIPO_EFA', 'CATEGORIA_EFA',
                                                'CARACTERISTICA 1', 'CARACTERISTICA 2', 'TIPO CAUSA',
                                                'PRIORIDAD', 'PUNTAJE',  'USUARIO',
                                                'CODIGO SINADA', 'ACTIVIDAD', 'FECHA_ULTIMO_MOV', 'USUARIO'], axis=1)

# 5.4 Macroproblemas
tabla_de_mp_cod = b_mp_cod.generar_dataframe()
tabla_de_mp_completa = b_mp.generar_dataframe()
tabla_de_mp_resumen = tabla_de_mp_completa.drop(['FECHA_ULTIMO_MOV'], axis=1)
