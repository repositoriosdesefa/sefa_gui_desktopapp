#########################################################
# DATOS DE USO FRECUENTES (LISTA, TUPLAS, DICCIONARIOS) #
# VARIABLES GLOBALES - ACCESIBLES DESDE TODA LA APP     #
#########################################################
import pandas as pd
from apoyo.manejo_de_bases import Base_de_datos

TodasBases = pd.read_excel('BasesDatos.xlsx', sheet_name='bases')

valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"
#pruebaaaaaaaa

oficinas = [
    'ODE Amazonas',
    'ODE Áncash',
    'ODE Apurímac',
    'ODE Arequipa',
    'ODE Ayacucho',
    'ODE Cajamarca',
    'ODE Cusco',
    'ODE Huancavelica',
    'ODE Huánuco',
    'ODE Ica',
    'ODE Junín',
    'ODE La Libertad',
    'ODE Lambayeque',
    'ODE Loreto',
    'ODE Madre de Dios',
    'ODE Moquegua',
    'ODE Pasco',
    'ODE Piura',
    'ODE Puno',
    'ODE San Martín',
    'ODE Tacna',
    'ODE Tumbes',
    'ODE Ucayali',
    'ODE VRAEM',
    'OE Chimbote',
    'OE Cotabambas',
    'OE Espinar',
    'OE La Convención',
    'OE Pichanaki',
    'SEFA'
]

# I. Tamaño de las pantallas de vista
ancho_v_vista = 1025
alto_v_vista = 600
ancho_v_vista_vitrina = 895
alto_v_vista_vitrina = 120
# PARA PROBLEMAS AMBIENTALES
ancho_v_vista_vitrinapr = 885
# PARA EXTREMOS
ancho_v_vista_vitrinaep = 920
# II. Tamaño de las pantallas de búsqueda
ancho_v_busqueda = 1300
ancho_v_busqueda_franja = ancho_v_busqueda - 3
alto_v_busqueda_franja = 78
alto_v_busqueda = 568
ancho_v_busqueda_vitrina = 950
ancho_v_busqueda_de_vitrina = 1065
ancho_v_busqueda_ep_vitrina = 810
ancho_v_busqueda_peq1_vitrina = 1040
ancho_v_busqueda_pf_vitrina = 900
ancho_v_busqueda_mp_vitrina = 800
ancho_v_busqueda_mpf_vitrina = 800
alto_v_busqueda_mpf_vitrina = 245
alto_v_busqueda_vitrina = 240
ancho_v_busqueda_prei_vitrina = 1065
ancho_v_busqueda_peq2_vitrina = 1180
ancho_v_busqueda_progr_vitrina = 710

# III. Tamaño del logo, franja
alto_logo = 50
ancho_logo = 280
alto_ventana_secundaria = 600
ancho_ventana_secundaria = 403
alto_franja_inferior_1 = 52
ancho_franja_inferior_1 = 400

# IV. Otras variables
cod_usuario = None
usuario = None
oficina = None
texto_bienvenida = None

# V. ID de Bases de Datos
id_usuarios = TodasBases.query("TIPO_DE_BASE=='usuarios'").iloc[0, 1]
id_b_docs = TodasBases.query("TIPO_DE_BASE=='documentos'").iloc[0, 1]
id_b_problemas = TodasBases.query("TIPO_DE_BASE=='problemas'").iloc[0, 1]
id_b_parametros = TodasBases.query("TIPO_DE_BASE=='parametros-relaciones'").iloc[0, 1]
id_b_directorio_efa = TodasBases.query("TIPO_DE_BASE=='directorio'").iloc[0, 1]
id_b_lista_efa = TodasBases.query("TIPO_DE_BASE=='listadoefa'").iloc[0, 1]


# VI. Bases de datos complementarias
# 6.0 Usuarios y parámetros

base_parametros = Base_de_datos(id_b_parametros, 'PARAMETROS')


# VIII. Bases de datos parámetros
tabla_parametros = base_parametros.generar_dataframe()
# 8.0 Desplegables en Drive
combo_vacio = ()
agente_conta = list(set(tabla_parametros['AGENTE CALCULADORA']))
componente_amb = list(set(tabla_parametros['COMPONENTE CALCULADORA']))
actividad_eco = list(set(tabla_parametros['ACTIVIDAD CALCULADORA']))
extension = list(set(tabla_parametros['EXTENSION CALCULADORA']))
ubicacion = list(set(tabla_parametros['UBICACION CALCULADORA']))
ocurrencia = list(set(tabla_parametros['OCURRENCIA CALCULADORA']))
tipo_afectacion = list(set(tabla_parametros['T_AFECTACION']))
tipo_administrado = list(set(tabla_parametros['T_ADMINISTRADO']))
estado_problemas = list(set(tabla_parametros['ESTADO_PROBLEMAS']))
tipo_causa = list(set(tabla_parametros['T_CAUSA']))
tipo_ingreso = list(set(tabla_parametros['T_INGRESO']))
tipo_documento = list(set(tabla_parametros['T_DOC']))
especialista_1 = list(set(tabla_parametros['ESPECIALISTA_1']))
tipo_accion_1 = list(set(tabla_parametros['T_ACCION_1']))
especialista_2 = list(set(tabla_parametros['ESPECIALISTA_2']))
tipo_accion_2 = list(set(tabla_parametros['T_ACCION_2']))
si_no = list(set(tabla_parametros['SI_NO']))
tipo_respuesta = list(set(tabla_parametros['T_RPTA']))
categorias = list(set(tabla_parametros['CATEGORIAS_PEDIDO']))
marco_pedido = list(set(tabla_parametros['MARCO_PEDIDO']))

b_lista_efa = Base_de_datos(id_b_lista_efa, 'Lista de EFA')
tabla_lista_efa = b_lista_efa.generar_dataframe()

b_efa = Base_de_datos(id_b_directorio_efa, 'Directorio')
tabla_directorio = b_efa.generar_dataframe()