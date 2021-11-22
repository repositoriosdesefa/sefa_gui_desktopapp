#####################################################
# VARIABLES GLOBALES - ACCESIBLES DESDE TODA LA APP #
#####################################################

from apoyo.manejo_de_bases import Base_de_datos

cod_usuario = None
usuario = None
oficina = None

# 0. Tablas relacionales
id_b_ospa = '13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4'
base_relacion_docs = Base_de_datos(id_b_ospa, 'RELACION_DOCS')
base_relacion_docs_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_D')
base_relacion_dr_ep =  Base_de_datos(id_b_ospa, 'RELACION_DR-EP')
base_relacion_dr_ep_hist =  Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_DR-EP')
base_relacion_de_ep =  Base_de_datos(id_b_ospa, 'RELACION_DE-EP')
base_relacion_de_ep_hist =  Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_DE-EP')
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

# 2. Bases de datos complementarias
# 2.1 Directorio de Oficinas
id_b_efa = '1pjHXiz15Zmw-49Nr4o1YdXJnddUX74n7Tbdf5SH7Lb0'
b_efa = Base_de_datos(id_b_efa, 'Directorio')
tabla_directorio = b_efa.generar_dataframe()
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
# 4.1 Bases de datos
id_parametros = '1NPg8Q0O_NqQ6bkRhy4ow17x2XJ08r6Ev3R6X80WmZ3c'
base_parametros = Base_de_datos(id_parametros, 'PARAMETROS')
tabla_parametros = base_parametros.generar_dataframe()
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
# 5.1 Documentos recibidos
tabla_de_dr_cod = b_dr_cod.generar_dataframe()
tabla_de_dr_completa = b_dr.generar_dataframe()
tabla_de_dr_resumen = tabla_de_dr_completa.drop(['VIA_RECEPCION', 'HT_ENTRANTE', 'EFA_CATEGORIA',
                                            'F_ING_OEFA', 'TIPO_DOC', 'ESPECIALISTA',
                                            'INDICACION', 'TIPO_RESPUESTA', 'RESPUESTA',
                                            'FECHA_ULTIMO_MOV', 'FECHA_ASIGNACION'], axis=1)

# 5.2 Documentos emitidos
tabla_de_de_cod = b_de_cod.generar_dataframe()
tabla_de_de_completa = b_de.generar_dataframe()
tabla_de_de_resumen =  tabla_de_de_completa.drop(['HT_SALIDA', 'COD_PROBLEMA', 'FECHA_PROYECTO_FINAL',
                                                    'FECHA_FIRMA', 'TIPO_DOC', 'CATEGORIA_DESTINATARIO',
                                                    'MARCO_PEDIDO', 'FECHA_ULTIMO_MOV', 'FECHA_ASIGNACION',
                                                    'DOCUMENTO_ELABORADO', 'DOCUMENTO_FIRMADO', 'DOCUMENTO_NOTIFICADO',
                                                    'PLAZO', 'ESTADO_DOCE', 'ESPECIALISTA'], axis=1)
# 5.3 Extremos de problema
tabla_de_ep_cod = b_ep_cod.generar_dataframe()
tabla_de_ep_completa = b_ep.generar_dataframe()
tabla_de_ep_resumen = tabla_de_ep_completa.drop(['OCURRENCIA', 'EXTENSION', 'TIPO DE AFECTACION',
                                                'PROVINCIA', 'DESCRIPCION', 'TIPO DE UBICACION',
                                                'CARACTERISTICA 1', 'CARACTERISTICA 2', 'TIPO CAUSA',
                                                'PRIORIDAD', 'PUNTAJE', 
                                                'CODIGO SINADA', 'ACTIVIDAD', 'FECHA_ULTIMO_MOV'], axis=1)

