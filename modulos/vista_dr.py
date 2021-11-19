import datetime as dt

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.constants import TRUE
from tkcalendar import DateEntry

from modulos import busqueda_dr
from apoyo.elementos_de_GUI import Cuadro, Ventana, Hovertip_Sefa, Vitrina_vista 
from apoyo.manejo_de_bases import Base_de_datos
import apoyo.datos_frecuentes as dfrec
from modulos import menus


# Prueba rama
# Valores de lista desplegable
id_b_ospa = '13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4'
id_parametros = '1NPg8Q0O_NqQ6bkRhy4ow17x2XJ08r6Ev3R6X80WmZ3c'

base_parametros = Base_de_datos(id_parametros, 'PARAMETROS')
tabla_parametros = base_parametros.generar_dataframe()
agente_conta = list(set(tabla_parametros['AGENTE CALCULADORA']))
componente_amb = list(set(tabla_parametros['COMPONENTE CALCULADORA']))
actividad_eco = list(set(tabla_parametros['ACTIVIDAD CALCULADORA']))
extension = list(set(tabla_parametros['EXTENSION CALCULADORA']))
ubicacion = list(set(tabla_parametros['UBICACION CALCULADORA']))
ocurrencia = list(set(tabla_parametros['OCURRENCIA CALCULADORA']))

tabla_parametros_dep = tabla_parametros.loc[1:30,['DEPARTAMENTO', 'SIGLAS_DEPARTAMENTO']]
departamento =  list(set(tabla_parametros_dep['DEPARTAMENTO']))

tipo_afectacion = ('Agente contaminante', 'Extracción de recursos')
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



# 0. Tablas relacionales
base_relacion_docs = Base_de_datos(id_b_ospa, 'RELACION_DOCS')
base_relacion_d_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_D')
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



# 2. Bases de datos complementarias
id_b_efa = '1pjHXiz15Zmw-49Nr4o1YdXJnddUX74n7Tbdf5SH7Lb0'
b_efa = Base_de_datos(id_b_efa, 'Directorio')
tabla_directorio = b_efa.generar_dataframe()
lista_efa = list(set(tabla_directorio['Entidad u oficina']))

b_efa_inei = Base_de_datos(id_b_efa, 'ID_INEI')
tabla_ubigeo_completo = b_efa_inei.generar_dataframe()
tabla_ubigeo = tabla_ubigeo_completo.loc[:,['Departamento', 'Provincia']]
departamento_inei = list(set(tabla_ubigeo['Departamento']))

class inicio_app_OSPA(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 2,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_button(3, 1, "DR", self.vista_dr)
        c1.agregar_button(3, 2, "BDR", self.busqueda_dr)
        c1.agregar_label(4, 1,' ')
        c1.agregar_button(5, 1, "DE", self.vista_de)
        c1.agregar_button(5, 2, "BDE", self.busqueda_de)
        c1.agregar_label(6, 1,' ')
        c1.agregar_button(7, 1, "EP", self.vista_ep)
        c1.agregar_button(7, 2, "BEP", self.busqueda_ep)
        c1.agregar_label(8, 1,' ')
        c1.agregar_button(9, 1, "JPF", self.pendientes_jefe_firma)
        c1.agregar_button(9, 2, "BMC", self.busqueda_mc)
        c1.agregar_label(10, 1,' ')
        c1.agregar_button(11, 1, "JPA", self.pendientes_jefe_asignar)
        c1.agregar_button(11, 2, "BAD", self.busqueda_ad)
        c1.agregar_label(12, 1,' ')

    #----------------------------------------------------------------------
    def vista_dr(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Doc_recibidos_vista(self, 650, 1150, "Documentos recibidos")
    
    #----------------------------------------------------------------------
    def busqueda_dr(self):


        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, "Búsqueda de documentos recibidos")

    #----------------------------------------------------------------------
    def vista_de(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Doc_emitidos_vista(self, 650, 1150, "Documentos emitidos")
    
    #----------------------------------------------------------------------
    def busqueda_de(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, "Búsqueda de documentos emitidos")
    
    #----------------------------------------------------------------------
    def vista_ep(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Extremo_problemas_vista(self, 650, 1150, "Extremo de problemas")
     
     #----------------------------------------------------------------------
    def busqueda_ep(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Extremos(self, 600, 1300, 
                    "Búsqueda de extremos")
    
    #----------------------------------------------------------------------
    def vista_mp(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Macroproblemas_vista(self, 650, 1150, "Extremo de problemas")
     
     #----------------------------------------------------------------------
    def busqueda_mp(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = Macroproblemas_vista(self, 600, 1300, 
                    "Búsqueda de extremos")

     #----------------------------------------------------------------------
    def busqueda_mc(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Macroproblemas(self, 600, 1300, 
                    "Búsqueda de macroproblemas")

     #----------------------------------------------------------------------
    def busqueda_ad(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Administrados(self, 600, 1300, 
                    "Búsqueda de administrados")

     #----------------------------------------------------------------------
    def pendientes_jefe_firma(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Pendientes_jefe_firma(self, 600, 1300, 
                    "Pendientes por firmar")

     #----------------------------------------------------------------------
    def pendientes_jefe_asignar(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Pendientes_jefe_asignar(self, 600, 1300, 
                    "Pendientes por firmar")

class Doc_recibidos_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        if self.nuevo != True: # En caso exista
            self.lista_para_insertar = lista
            self.cod_usuario_dr = id_doc

        # I. Labels and Entries
        rejilla_dr = [
            ('L', 0, 0, 'Tipo de documento'),
            ('CX', 0, 1, tipo_documento),

            ('L', 0, 2, 'N° de documento'),
            ('E', 0, 3),

            ('L', 1, 0, 'Fecha de recepción OEFA'),
            ('D', 1, 1),

            ('L', 1, 2, 'Fecha de recepción SEFA'),
            ('D', 1, 3),

            ('L', 2, 0, 'Vía de recepción'),
            ('CX', 2, 1, tipo_ingreso),

            ('L', 2, 2, 'HT de documento'),
            ('E', 2, 3),

            ('L', 3, 0, 'Asunto'),
            ('EL', 3, 1, 112, 3),

            ('L', 4, 0, 'Remitente'),
            ('CX', 4, 1, lista_efa),

            ('L', 4, 2, '¿Es respuesta?'),
            ('CX', 4, 3, si_no),

            ('L', 5, 0, 'Indicación'),
            ('CX', 5, 1, tipo_indicacion),

            ('L', 5, 2, 'Especialista asignado'),
            ('CX', 5, 3, especialista),

            ('L', 6, 0, 'Aporte del documento'),
            ('ST', 6, 1),

            ('L', 7, 0, 'Respuesta'),
            ('CX', 7, 1, tipo_respuesta),
            
            ('L', 8, 0, 'Departamento'),
            ('CXD', 8, 1, 39, departamento_inei, tabla_ubigeo, 'Departamento', 29),

            ('L', 8, 2, 'Provincia'),
            ('CXR', 8, 3, especialista)
        ]

        # II. Tablas en ventana
        # II.1 Lista de DE
        tabla_de_de_completa = b_de.generar_dataframe()
        self.tabla_de_de =  tabla_de_de_completa.drop(['HT_SALIDA', 'COD_PROBLEMA', 'FECHA_PROYECTO_FINAL',
                                                    'FECHA_FIRMA', 'TIPO_DOC', 'SE_EMITIO',
                                                    'MARCO_PEDIDO', 'FECHA_ULTIMO_MOV', 'FECHA_ASIGNACION',
                                                    'DOCUMENTO_ELABORADO', 'DOCUMENTO_FIRMADO', 'DOCUMENTO_NOTIFICADO',
                                                    'PLAZO', 'ESTADO_DOCE', 'ESPECIALISTA'], axis=1)

        # II.2 Lista de EP
        tabla_de_ep_completa = b_ep.generar_dataframe()
        tabla_de_ep_id = tabla_de_ep_completa
        self.tabla_de_ep = tabla_de_ep_id.drop(['OCURRENCIA', 'EXTENSION', 'TIPO DE AFECTACION',
                                                'PROVINCIA', 'DISTRITO', 'DESCRIPCION', 'TIPO DE UBICACION',
                                                'CARACTERISTICA 1', 'CARACTERISTICA 2', 'TIPO CAUSA',
                                                'PRIORIDAD', 'PUNTAJE', 
                                                'CODIGO SINADA', 'ACTIVIDAD', 'FECHA_ULTIMO_MOV'], axis=1)
        
        # III. Ubicaciones
        # III.1 Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        titulos.agregar_titulo(0,1,'                             ')
        titulos.agregar_titulo(0,2,'Detalle de documento recibido')
        titulos.agregar_titulo(0,3,'                             ')
        titulos.agregar_titulo(0,4,'                             ')

        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_dr)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo != True:
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.enviar_dr)
        f_boton.agregar_button(0, 2, 'Inicio', self.inicio_app) # Botón provisional
        # III.4 Frame de botón y títulos de vitrina 1
        self.boton_vitrina_1 = Cuadro(self)
        self.boton_vitrina_1.agregar_button(0, 0,'(+) Agregar', self.busqueda_de)
        self.boton_vitrina_1.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_1.agregar_titulo(0, 2, 'Documentos emitidos asociados')
        self.boton_vitrina_1.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_1.agregar_titulo(0, 4,'                              ')

        # III.5 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        # En caso exista precedente, se busca en la tabla de Documentos emitidos
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_1,
                                 b_dr_cod, self.tabla_de_de, base_relacion_docs, 
                                 "ID_DR", "ID_DE", self.ver_de, self.eliminar_de)
        else:
            self.frame_vitrina_1.agregar_label(1, 2, '                  0 documentos emitidos asociados')


        # III.6 Frame de botón y títulos de vitrina 2
        self.boton_vitrina_2 = Cuadro(self)
        self.boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_ep)
        self.boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_2.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        self.boton_vitrina_2.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_2.agregar_titulo(0, 4,'                              ')

        # III.7 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_2,
                                 b_dr_cod, self.tabla_de_ep, base_relacion_dr_ep, 
                                 "ID_DR", "ID_EP", self.ver_ep, self.eliminar_ep)
        else:
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 extremos de problemas asociados') 

    #----------------------------------------------------------------------
    def generar_vitrina(self, frame_vitrina,
                        tabla_codigo_entrada, tabla_salida, base_relacion, 
                        id_entrada, id_salida, funcion_ver, funcion_eliminar):
        """"""
        # Obtengo el código del usuario que heredo
        cod_usuario = self.cod_usuario_dr
        # Genero las tablas para el filtrado 
        tabla_de_codigo = tabla_codigo_entrada.generar_dataframe() # Tabla de códigos
        tabla_de_relacion = base_relacion.generar_dataframe() # Tabla de relación
        # Filtro la tabla para obtener el código interno 
        tabla_de_codigo_filtrada = tabla_de_codigo[tabla_de_codigo['COD_DR']==cod_usuario]
        cod_interno = tabla_de_codigo_filtrada.iloc[0,0]
        # Filtro para obtener las relaciones activas
        tabla_relacion_activos = tabla_de_relacion[tabla_de_relacion['ESTADO']=="ACTIVO"]
        # Con ese ID, filtro la tabla de relacion
        tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos[id_entrada]==cod_interno]
        # Me quedo con el vector a filtrar en forma de lista
        lista_dr = list(tabla_relacion_filtrada[id_salida].unique())
        # Filtro la tabla de documentos recibidos
        tabla_filtrada = tabla_salida[tabla_salida[id_salida].isin(lista_dr)]
        # Tabla de documentos emitidos filtrada
        tabla_vitrina = tabla_filtrada.drop([id_salida], axis=1)
        if len(tabla_vitrina.index) > 0:
            self.vitrina = Vitrina_vista(self, tabla_vitrina, funcion_ver, funcion_eliminar, 
                                        height=80, width=1050) 
        else:
            frame_vitrina.agregar_label(1, 2, '                  0 documentos emitidos asociados')

    #----------------------------------------------------------------------
    def actualizar_vitrina(self, vitrina, frame_vitrina,
                            tabla_codigo_entrada, tabla_salida, tabla_relacion, 
                            id_entrada, id_salida, funcion_ver, funcion_eliminar):
        """"""
        vitrina.eliminar_vitrina()
        # Generar vitrina de documentos recibidos asociados
        self.generar_vitrina(frame_vitrina,
                            tabla_codigo_entrada, tabla_salida, tabla_relacion, 
                            id_entrada, id_salida, funcion_ver, funcion_eliminar)

    #----------------------------------------------------------------------
    def enviar_dr(self):
        """"""
        datos_ingresados = self.frame_rejilla.obtener_lista_de_datos()
        # Genero la tablas de código de DE
        tabla_de_codigo_dr = b_dr_cod.generar_dataframe()
        # Guardo el código de usuario que llega
        if self.nuevo != True:
            # En caso exista ID insertado en la rejilla
            cod_usuario_existente = self.cod_usuario_dr
            valor_de_comprobacion = self.comprobar_id(b_dr_cod, cod_usuario_existente)
            if valor_de_comprobacion == True:
                self.cod_usuario_dr = cod_usuario_existente
                # A partir del código comprobado
                tabla_codigo_dr_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr['COD_DR']==self.cod_usuario_dr]
                cod_interno_dr = tabla_codigo_dr_filtrada.iloc[0,0]

                # Pestaña 1: Código Único
                # Obtengo los datos ingresados
                lista_descargada_codigo = b_dr_cod.listar_datos_de_fila(cod_interno_dr) # Se trae la info   
                # Obtengo el ID interno
                self.cod_usuario_dr = lista_descargada_codigo[3]
                nuevo_cod_usuario_dr = datos_ingresados[0] + " " + datos_ingresados[1]
                # Actualizo las tablas en la web
                hora_de_modificacion = str(dt.datetime.now())
                #b_dr_cod.cambiar_un_dato_de_una_fila(cod_interno_dr, 2, hora_de_modificacion) # Se actualiza código interno
                b_dr_cod.cambiar_un_dato_de_una_fila(cod_interno_dr, 4, nuevo_cod_usuario_dr) # Se actualiza código interno

                # Pestaña 2:       
                # Cambio los datos de una fila
                # Código interno del aplicativo + Código del usuario del DR + Hora de modificación
                lista_a_sobreescribir = [cod_interno_dr] + [nuevo_cod_usuario_dr] + datos_ingresados + [hora_de_modificacion]
                b_dr.cambiar_los_datos_de_una_fila(cod_interno_dr, lista_a_sobreescribir) # Se sobreescribe la información
            
                # Pestaña 3
                lista_historial = lista_a_sobreescribir
                b_dr_hist.agregar_datos(lista_historial) # Se sube la info

                messagebox.showinfo("¡Excelente!", "Se ha actualizado el registro")
                self.actualizar_vista_dr(nuevo_cod_usuario_dr)


        else:
            # Comprobación de que no se ingresa un código de usuario repetido
            cod_dr_ingresado = datos_ingresados[0] + " " + datos_ingresados[1]
            valor_de_comprobacion = self.comprobar_id(b_dr_cod, cod_dr_ingresado) # Comprobar si el id de usuario ya existe
            if valor_de_comprobacion == True: # Verifico que lo ingresado no exista
                messagebox.showerror("Error", "Este documento ya existe")
            else:
                # Timestamp
                ahora = str(dt.datetime.now())
                # Pestaña 1: Código Único
                cod_dr_ingresado = datos_ingresados[0] + " " + datos_ingresados[1]
                # Creo el código único
                b_dr_cod.agregar_codigo(cod_dr_ingresado, ahora)
                # Descargo el código único
                lista_descargada_codigo = b_dr_cod.listar_datos_de_fila(ahora) # Se trae la info
        
                # Pestaña 2:       
                # Obtengo el ID interno
                cod_interno_dr = lista_descargada_codigo[0]
                cod_usuario_dr = lista_descargada_codigo[3]
                # Creo el vector a subir
                lista_a_cargar = [cod_interno_dr] + [cod_usuario_dr] + datos_ingresados + [ahora]
                b_dr.agregar_datos(lista_a_cargar) # Se sube la info

                # Pestaña 3
                hora_de_creacion = str(ahora) # De lo creado en la pestaña 1
                lista_historial = lista_a_cargar + [hora_de_creacion] # Lo subido a la pestaña 2 + hora
                b_dr_hist.agregar_datos(lista_historial) # Se sube la info

                # Confirmación de registro
                messagebox.showinfo("¡Excelente!", "Se ha ingresado un nuevo registro")
                self.actualizar_vista_dr(cod_usuario_dr) 
    
    #----------------------------------------------------------------------
    def actualizar_vista_dr(self, id_usuario):

        texto_documento = 'Documento recibido: ' +  id_usuario

        lb1 = b_dr.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8],
                                lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], lb1[14]]
        
        self.desaparecer()
        subframe = Doc_recibidos_vista(self, 650, 1150, texto_documento, 
                                        nuevo=False, lista=lista_para_insertar, id_doc = id_usuario)
    
    #----------------------------------------------------------------------
    def busqueda_de(self):
        """"""
        if self.nuevo != True:
            # En caso exista un código insertado en la rejilla
            cod_usuario_dr = self.cod_usuario_dr 
            texto_pantalla = "Documento emitido que se asociará: " + cod_usuario_dr
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, texto_pantalla,
                                                           nuevo=False, id_doc = cod_usuario_dr)

        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar un documento emitido, por favor guarde la información registrada")


    #----------------------------------------------------------------------
    def ver_de(self, id_usuario):
        """"""
        texto_documento = 'Documento emitido: ' + id_usuario

        lb1 = b_de.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6]]
                        #, lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = Doc_emitidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_doc = id_usuario)

    #----------------------------------------------------------------------
    def eliminar_de(self, id_usuario_de):
        """"""
        # Obtengo los ID del usuario
        codigo_de = id_usuario_de
        codigo_dr = self.cod_usuario_dr
        # Genero las tablas de código 
        tabla_de_codigo_dr = b_dr_cod.generar_dataframe()
        tabla_de_codigo_de = b_de_cod.generar_dataframe()
        # Filtro las tablas para obtener el ID interno
        tabla_codigo_dr_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr['COD_DR']==codigo_dr]
        id_interno_dr = tabla_codigo_dr_filtrada.iloc[0,0]
        tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de['COD_DE']==codigo_de]
        id_interno_de = tabla_codigo_de_filtrada.iloc[0,0]
        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" + id_interno_de
        # Se cambia dato en tabla de relación
        base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4,'ELIMINADO')
        # Elimino los frame para insertar el cuadro actualizado
        self.boton_vitrina_1.eliminar_cuadro()
        self.frame_vitrina_2.eliminar_cuadro()

        # Situo la ventana actualizada
        self.actualizar_vitrina(self.vitrina, self.frame_vitrina_1,
                                b_dr_cod, self.tabla_de_de, base_relacion_docs, 
                                "ID_DR", "ID_DE", self.ver_de, self.eliminar_de)
        # Vuelvo a crear los cuadros luego de la vitrina 1
        self.boton_vitrina_2 = Cuadro(self) # Se vuelve a crear (Provisional)
        self.boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_ep)
        self.boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_2.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        self.boton_vitrina_2.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_2.agregar_titulo(0, 4,'                              ')
        self.frame_vitrina_2 = Cuadro(self) # Se vuelve a crear (Provisional)
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_2,
                                 b_dr_cod, self.tabla_de_ep, base_relacion_dr_ep, 
                                 "ID_DR", "ID_EP", self.ver_ep, self.eliminar_ep)
        else:
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 extremos de problemas asociados') 

        # Actualización de historial
        datos_modificados = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
        hora = str(dt.datetime.now())
        datos_a_cargar_hist = datos_modificados + [hora]
        base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
        # Confirmación de eliminación de documento emitido
        messagebox.showinfo("¡Documento emitido eliminado!", "El registro se ha desasociado correctamente")
    
    #----------------------------------------------------------------------
    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

    #----------------------------------------------------------------------
    def busqueda_ep(self):
        """"""
        print("Pantalla de búsqueda de extremo de problemas")
    
    #----------------------------------------------------------------------
    def ver_ep(self, id_usuario):
        """"""
        texto_documento = 'Extremo de problema: ' + id_usuario

        lb1 = b_ep.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], 
                                lb1[8], lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], 
                                lb1[14], lb1[15], lb1[16], lb1[17], lb1[18], lb1[19]]

        self.desaparecer()
        subframe = Extremo_problemas_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_problema = id_usuario)

    #----------------------------------------------------------------------
    def eliminar_ep(self, x):
        """"""
        print("Eliminar extremo de problema asociado")
    
    #----------------------------------------------------------------------
    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

class Doc_emitidos_vista(Ventana):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc=None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        if self.nuevo != True: # En caso exista
            self.lista_para_insertar = lista
            self.cod_usuario_de = id_doc

        # I. Labels and Entries
        rejilla_de = [
            ('L', 0, 0, 'HT de documento'),
            ('E', 0, 1),

            ('L', 0, 2, 'Categoría'),
            ('CX', 0, 3, categorias),

            ('L', 1, 0, 'Tipo de documento'),
            ('CX', 1, 1, tipo_documento),

            ('L', 1, 2, 'N° de documento'),
            ('E', 1, 3),

            ('L', 2, 0, 'Destinatario'),
            ('CX', 2, 1, lista_efa),

            ('L', 2, 2, 'Marco de pedido'),
            ('CX', 2, 3, marco_pedido),

            ('L', 3, 0, 'Detalle de requerimiento'),
            ('ST', 3, 1)

        ]


        # II. Tablas en ventana
        # II.1 Lista de DR
        tabla_de_dr = b_dr.generar_dataframe()
        self.tabla_de_dr = tabla_de_dr.drop(['VIA_RECEPCION', 'HT_ENTRANTE',
                                            'F_ING_OEFA', 'TIPO_DOC', 'ESPECIALISTA',
                                            'INDICACION', 'TIPO_RESPUESTA', 'RESPUESTA',
                                            'FECHA_ULTIMO_MOV', 'FECHA_ASIGNACION'], axis=1)
        # II.2 Lista de EP
        tabla_de_ep = b_ep.generar_dataframe()
        self.tabla_de_ep = tabla_de_ep.drop(['ID_EP'], axis=1)

        # III. Ubicaciones
        # III.1 Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_imagen(0, 0, 'Logo_OSPA.png', 202, 49)
        titulos.agregar_titulo(0, 1, '                             ')
        titulos.agregar_titulo(0, 2, 'Detalle de documento emitido ')
        titulos.agregar_titulo(0, 3, '                             ')
        titulos.agregar_titulo(0, 4, '                             ')

        # III.2 Frame de rejilla
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_de)

        #self.frame_rejilla_decisores_fecha = Cuadro(self)
        #self.valordecisor = StringVar(name="vacio")
        #self.valordecisor.trace("w", lambda name, index, mode, valor=self.valordecisor: self.cambio_valor(valor))
        #self.frame_rejilla_decisores_fecha.agregar_combobox(1,1, si_no)
        #self.fecha = DateEntry(self.frame_rejilla_decisores_fecha)
        #self.existe = True
        #self.lastupdated = None

        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo != True: 
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.enviar_de)
        f_boton.agregar_button(0, 2, 'Inicio', self.inicio_app) # Botón provisional

        # III.4 Frame de botón y títulos de vitrina 1
        self.boton_vitrina_1 = Cuadro(self)
        self.boton_vitrina_1.agregar_button(0, 0,'(+) Agregar', self.busqueda_dr)
        self.boton_vitrina_1.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_1.agregar_titulo(0, 2, 'Documentos recibidos asociados')
        self.boton_vitrina_1.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_1.agregar_titulo(0, 4,'                              ')

        # III.5 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        # En caso exista precedente, se busca en la tabla de Extremo de problemas
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_1,
                                 b_de_cod, self.tabla_de_dr, base_relacion_docs, 
                                 "ID_DE", "ID_DR", self.ver_dr, self.eliminar_dr)
       # Etiqueta de 0 problemas asociados
        else:
            self.frame_vitrina_1.agregar_label(1, 2, '                0 extremos de problemas asociados')

        # III.6 Frame de botón y títulos de vitrina 2
        self.boton_vitrina_2 = Cuadro(self)
        self.boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_ep)
        self.boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_2.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        self.boton_vitrina_2.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_2.agregar_titulo(0, 4,'                              ')
        
        # III.7 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
        # En caso exista precedente, se busca en la tabla de Documentos recibidos
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_2,
                                 b_de_cod, self.tabla_de_ep, base_relacion_de_ep, 
                                 "ID_DE", "ID_EP", self.ver_ep, self.eliminar_ep)
        else:
            self.frame_vitrina_2.agregar_label(1, 2, '                  0 documentos recibidos asociados')
        
        #self.after(10, self.update)

    #----------------------------------------------------------------------
    def generar_vitrina(self, frame_vitrina,
                        tabla_codigo_entrada, tabla_salida, base_relacion, 
                        id_entrada, id_salida, funcion_ver, funcion_eliminar):
        """"""
        # Obtengo el código del usuario que heredo
        cod_usuario = self.cod_usuario_de
        # Genero las tablas para el filtrado 
        tabla_de_codigo = tabla_codigo_entrada.generar_dataframe() # Tabla de códigos
        tabla_de_relacion = base_relacion.generar_dataframe() # Tabla de relación
        # Filtro la tabla para obtener el código interno 
        tabla_de_codigo_filtrada = tabla_de_codigo[tabla_de_codigo['COD_DE']==cod_usuario]
        cod_interno = tabla_de_codigo_filtrada.iloc[0,0]
        # Filtro para obtener las relaciones activas
        tabla_relacion_activos = tabla_de_relacion[tabla_de_relacion['ESTADO']=="ACTIVO"]
        # Con ese ID, filtro la tabla de relacion
        tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos[id_entrada]==cod_interno]
        # Me quedo con el vector a filtrar en forma de lista
        lista_dr = list(tabla_relacion_filtrada[id_salida].unique())
        # Filtro la tabla de documentos recibidos
        tabla_filtrada = tabla_salida[tabla_salida[id_salida].isin(lista_dr)]
        # Tabla de documentos emitidos filtrada
        tabla_vitrina = tabla_filtrada.drop([id_salida], axis=1)
        if len(tabla_vitrina.index) > 0:
            self.vitrina = Vitrina_vista(self, tabla_vitrina, funcion_ver, funcion_eliminar, 
                                        height=80, width=1050) 
        else:
            frame_vitrina.agregar_label(1, 2, '                  0 documentos recibidos asociados')

    #----------------------------------------------------------------------
    def actualizar_vitrina(self, vitrina, frame_vitrina,
                            tabla_codigo_entrada, tabla_salida, tabla_relacion, 
                            id_entrada, id_salida, funcion_ver, funcion_eliminar):
        """"""
        vitrina.eliminar_vitrina()
        # Generar vitrina de documentos recibidos asociados
        self.generar_vitrina(frame_vitrina,
                            tabla_codigo_entrada, tabla_salida, tabla_relacion, 
                            id_entrada, id_salida, funcion_ver, funcion_eliminar)

    #----------------------------------------------------------------------
    def enviar_de(self):
        """"""
        datos_ingresados = self.frame_rejilla.obtener_lista_de_datos()
        # Genero la tablas de código de DE
        tabla_de_codigo_de = b_de_cod.generar_dataframe()
        # Guardo el código de usuario que llega
        if self.nuevo != True:
            # En caso exista ID insertado en la rejilla
            cod_usuario_de = self.cod_usuario_de # Compruebo si son iguales
            valor_de_comprobacion = self.comprobar_id(b_de_cod, cod_usuario_de)

        else:
            # Comprobación de que no se ingresa un ID de usuario repetido
            ht = datos_ingresados[0]
            valor_de_comprobacion = self.comprobar_id(b_de_cod, ht) # Comprobar si el id de usuario ya existe
       
        # Modifico o creo, según exista
        if valor_de_comprobacion == True:
            # A partir del código comprobado
            tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de['COD_DE']==cod_usuario_de]
            cod_interno_de = tabla_codigo_de_filtrada.iloc[0,0]

            # Pestaña 1: Código Único
            # Obtengo los datos ingresados
            lista_descargada_codigo = b_de_cod.listar_datos_de_fila(cod_interno_de) # Se trae la info   
            # Obtengo el ID interno
            cod_usuario_de = lista_descargada_codigo[3]
            correlativo = cod_interno_de[7:20]
            nuevo_cod_usuario_de = correlativo + "/" + datos_ingresados[0]
            # Actualizo las tablas en la web
            hora_de_modificacion = str(dt.datetime.now())
            b_de_cod.cambiar_un_dato_de_una_fila(cod_interno_de, 2, hora_de_modificacion) # Se actualiza código interno
            b_de_cod.cambiar_un_dato_de_una_fila(cod_interno_de, 4, nuevo_cod_usuario_de) # Se actualiza código interno

            # Pestaña 2:       
            # Cambio los datos de una fila
            lista_a_sobreescribir = [cod_interno_de] + [nuevo_cod_usuario_de] + datos_ingresados
            b_de.cambiar_los_datos_de_una_fila(cod_interno_de, lista_a_sobreescribir) # Se sobreescribe la información
            
            # Pestaña 3
            lista_historial = lista_a_sobreescribir + [hora_de_modificacion] # Lo subido a la pestaña 2 + hora
            b_de_hist.agregar_datos(lista_historial) # Se sube la info

            messagebox.showinfo("¡Excelente!", "Se ha actualizado el registro")
            self.actualizar_vista_de(nuevo_cod_usuario_de)
        
        else:
            # Timestamp
            ahora = str(dt.datetime.now())
            # Pestaña 1: Código Único
            ht = datos_ingresados[0]
            # Creo el código único
            b_de_cod.agregar_nuevo_codigo(ht, ahora)
            # Descargo el código único
            lista_descargada_codigo = b_de_cod.listar_datos_de_fila(ahora) # Se trae la info
        
            # Pestaña 2:       
            # Obtengo el ID interno
            cod_interno_de = lista_descargada_codigo[0]
            cod_usuario_de = lista_descargada_codigo[3]
            # Creo el vector a subir
            lista_a_cargar = [cod_interno_de] + [cod_usuario_de] + datos_ingresados
            b_de.agregar_datos(lista_a_cargar) # Se sube la info

            # Pestaña 3
            hora_de_creacion = str(ahora) # De lo creado en la pestaña 1
            lista_historial = lista_a_cargar + [hora_de_creacion] # Lo subido a la pestaña 2 + hora
            b_de_hist.agregar_datos(lista_historial) # Se sube la info
        
            # Confirmación de registro
            messagebox.showinfo("¡Excelente!", "Se ha ingresado un nuevo registro")
            self.actualizar_vista_de(cod_usuario_de) 
    
    #----------------------------------------------------------------------
    def actualizar_vista_de(self, id_usuario):

        texto_documento = 'Documento emitido: ' +  id_usuario

        lb1 = b_de.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6]]
        #, lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        
        self.desaparecer()
        subframe = Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                        nuevo=False, lista=lista_para_insertar, id_doc = id_usuario)
    
    #----------------------------------------------------------------------
    def busqueda_ep(self):
        """"""
        
        if self.nuevo != True:
            # En caso exista un código insertado en la rejilla
            cod_usuario_de = self.cod_usuario_de 
            texto_pantalla = "Documento emitido que se asociará: " + cod_usuario_de
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla,
                                                           nuevo=False, id_doc = cod_usuario_de)

        else:
            # En caso fuera una nueva ventana
            texto_pantalla = "Búsqueda de extremos de problemas"
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Extremos(self, 600, 1300, 
                    "Búsqueda de extremos")

    #----------------------------------------------------------------------
    def ver_ep(self, x):
        """"""
        y = x + "Ver extremo de problema"
        print(y)

    #----------------------------------------------------------------------
    def eliminar_ep(self, x):
        """"""
        y = x + "Eliminar extremo de problema"
        print(y)

    #----------------------------------------------------------------------
    def busqueda_dr(self):
        """"""
        if self.nuevo != True:
            # En caso exista un código insertado en la rejilla
            cod_usuario_de = self.cod_usuario_de 
            texto_pantalla = "Documento emitido que se asociará: " + cod_usuario_de
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla,
                                                           nuevo=False, id_doc = cod_usuario_de)

        else:
            # En caso fuera una nueva ventana
            texto_pantalla = "Búsqueda de documentos recibidos"
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla)

    #----------------------------------------------------------------------
    def ver_dr(self, id_usuario):
        """"""
        texto_documento = 'Documento recibido: ' + id_usuario

        lb1 = b_dr.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], 
                                lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], lb1[14]]
        
        self.desaparecer()
        subframe = Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_doc = id_usuario)

    #----------------------------------------------------------------------
    def eliminar_dr(self, id_usuario_dr):
        """"""
        # Obtengo los ID del usuario
        codigo_dr = id_usuario_dr
        codigo_de = self.cod_usuario_de
        # Genero las tablas de código 
        tabla_de_codigo_dr = b_dr_cod.generar_dataframe()
        tabla_de_codigo_de = b_de_cod.generar_dataframe()
        # Filtro las tablas para obtener el ID interno
        tabla_codigo_dr_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr['COD_DR']==codigo_dr]
        id_interno_dr = tabla_codigo_dr_filtrada.iloc[0,0]
        tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de['COD_DE']==codigo_de]
        id_interno_de = tabla_codigo_de_filtrada.iloc[0,0]
        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" + id_interno_de
        # Se cambia dato en tabla de relación
        base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4,'ELIMINADO')
        # Elimino los frame para insertar el cuadro actualizado
        self.boton_vitrina_2.eliminar_cuadro()
        self.frame_vitrina_2.eliminar_cuadro()

        # Le paso el frame de DR
        self.actualizar_vitrina(self.vitrina, self.frame_vitrina_2, 
                                b_de_cod, self.tabla_de_dr, base_relacion_docs, 
                                "ID_DE", "ID_DR", self.ver_dr, self.eliminar_dr)
        
        # Vuelvo a crear los cuadros luego de la vitrina 1
        self.boton_vitrina_2 = Cuadro(self) # Se vuelve a crear (Provisional)
        self.boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_ep)
        self.boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_2.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        self.boton_vitrina_2.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_2.agregar_titulo(0, 4,'                              ')
        self.frame_vitrina_2 = Cuadro(self) # Se vuelve a crear (Provisional)
        if self.nuevo != True:
            # Provisional
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 extremos de problemas asociados') 
        else:
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 extremos de problemas asociados') 


        # Actualización de historial
        datos_modificados = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
        hora = str(dt.datetime.now())
        datos_a_cargar_hist = datos_modificados + [hora]
        base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)

        # Confirmación de eliminación de documento emitido
        messagebox.showinfo("¡Documento recibido eliminado!", "El registro se ha desasociado correctamente")
    
    #----------------------------------------------------------------------
    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False
    
    #----------------------------------------------------------------------
    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")
    
    #----------------------------------------------------------------------
    def cambio_valor(self, ultimo_valor):
        print(ultimo_valor)
        #self.lastupdated = str(ultimo_valor)
    
    #----------------------------------------------------------------------
    def actualizar(self):
        #if self.lastupdated != None:
        #    if self.lastupdated == "vacio" and self.valordecisor.get() == "Si":
        #        if self.existe == False:
        #            self.fecha = DateEntry(self.frame_rejilla_decisores_fecha)
        #        
        #        self.fecha.grid(row = 1, column = 2, pady=4, padx=8)
        #        self.fecha.update()
        #        self.lastupdated = None

        #    elif self.lastupdated == "vacio" and self.valordecisor.get() == "No":
        #        self.fecha.destroy()
        #        self.lastupdated = None
        #        self.existe = False

        #self.after(10, self.actualizar)
        print("Actualización")
    
    #----------------------------------------------------------------------
    def dependiente_1(self, valor_combobox_1):
        # 1. Obtener dataframe con valores de Dpto, Prov, Distrito
        tabla_valores_dependientes = b_efa_inei.generar_dataframe()
        # 2. Filtrar la información
        tabla_val_dep_filtrada = tabla_valores_dependientes[tabla_valores_dependientes['Departamento']==valor_combobox_1]
        # 3. Seleccionar columna y convertirla en lista
        valores_filtrados = list(set(tabla_val_dep_filtrada.loc[:,['Provincia', 'Departamento']]))
        print(valores_filtrados)
        # 4. Valores filtrados pasan a ser parte del combobox siguiente 
    
    #---------------------------------------------------------------------
    def cambiar_lista(self, rejilla_a_mod, posicion):
        print("Hola")

        

class Extremo_problemas_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_problema = None):
        """Constructor"""

        Ventana.__init__(self, *args)
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo

        if self.nuevo != True: # En caso exista
            self.lista_para_insertar = lista
            self.id_problema = id_problema
            lista_id_codigo = b_ep_cod.listar_datos_de_fila(self.id_problema) 
            cod_problema = lista_id_codigo[3]

            # I. Labels and Entries
            rejilla_ep = [
                ('L', 0, 0, 'Código de problema'),
                ('L', 0, 1, str(cod_problema)),

                ('L', 0, 2, 'Departamento'),
                ('EL', 0, 3, 30, 1),

                ('L', 0, 4, 'Ocurrencia'),
                ('EL', 0, 5, 30, 1),

                ('L', 1, 0, 'Componente ambiental'),
                ('EL', 1, 1, 30, 1),

                ('L', 1, 2, 'Provincia'),
                ('EL', 1, 3, 30, 1),

                ('L', 1, 4, 'Descripción'),
                ('STP', 1, 5, 28, 2),

                ('L', 2, 0, 'Tipo de afectación'),
                ('CXP', 2, 1, 27, tipo_afectacion, "readonly"),

                ('L', 2, 2, 'Distrito'),
                ('EL', 2, 3, 30, 1),

                ('L', 3, 0, 'Agente contaminante'),
                ('CXP', 3, 1, 27, agente_conta, "readonly"),

                ('L', 3, 2, 'Tipo de ubicación'),
                ('CXP', 3, 3, 27, ubicacion, "readonly"),

                ('L', 3, 4, 'EFA'),
                ('CXP', 3, 5, 27, lista_efa, "readonly"),

                ('L', 4, 0, 'Actividad'),
                ('CXP', 4, 1, 27, actividad_eco, "readonly"),

                ('L', 4, 2, 'Extensión'),
                ('CXP', 4, 3, 27, extension, "readonly"),
                
                ('L', 4, 4, 'Estado'),
                ('EL', 4, 5, 30, 1),

                ('L', 5, 0, 'Característica 1'),
                ('EL', 5, 1, 30, 1),

                ('L', 5, 2, 'Tipo de causa'),
                ('EL', 5, 3, 30, 1),

                ('L', 5, 4, 'Código SINADA'),
                ('EL', 5, 5, 30, 1),

                ('L', 6, 0, 'Característica 2'),
                ('EL', 6, 1, 30, 1),

                ('L', 6, 2, '¿Es prioridad?'),
                ('CXP', 6, 3, 27, si_no, "readonly"),

                ('L', 6, 4, 'Puntaje'),
                ('EL', 6, 5, 30, 1)

            ]

        # Rejilla nuevo
        rejilla_ep_nuevo = [
            #('L', 0, 0, 'Código de problema'),
            #('L', 0, 1, str(cod_problema)),

            ('L', 0, 2, 'Departamento'),
            ('CXP', 0, 3, 27, departamento, "readonly"),

            ('L', 0, 4, 'Ocurrencia'),
            ('CXP', 0, 5, 27, ocurrencia, "readonly"),

            ('L', 1, 0, 'Componente ambiental'),
            ('CXP', 1, 1, 27, componente_amb, "readonly"),

            ('L', 1, 2, 'Provincia'),
            ('EL', 1, 3, 30, 1),

            ('L', 1, 4, 'Descripción'),
            ('STP', 1, 5, 28, 2),

            ('L', 2, 0, 'Tipo de afectación'),
            ('CXP', 2, 1, 27, tipo_afectacion, "readonly"),

            ('L', 2, 2, 'Distrito'),
            ('EL', 2, 3, 30, 1),

            ('L', 3, 0, 'Agente contaminante'),
            ('CXP', 3, 1, 27, agente_conta, "readonly"),

            ('L', 3, 2, 'Tipo de ubicación'),
            ('CXP', 3, 3, 27, ubicacion, "readonly"),

            ('L', 3, 4, 'EFA'),
            ('CXP', 3, 5, 27, lista_efa, "readonly"),

            ('L', 4, 0, 'Actividad'),
            ('CXP', 4, 1, 27, actividad_eco, "readonly"),

            ('L', 4, 2, 'Extensión'),
            ('CXP', 4, 3, 27, extension, "readonly"),
            
            ('L', 4, 4, 'Estado'),
            ('EL', 4, 5, 30, 1),

            ('L', 5, 0, 'Característica 1'),
            ('EL', 5, 1, 30, 1),

            ('L', 5, 2, 'Tipo de causa'),
            ('EL', 5, 3, 30, 1),

            ('L', 5, 4, 'Código SINADA'),
            ('EL', 5, 5, 30, 1),

            ('L', 6, 0, 'Característica 2'),
            ('EL', 6, 1, 30, 1),

            ('L', 6, 2, '¿Es prioridad?'),
            ('CXP', 6, 3, 27, si_no, "readonly")

            #('L', 6, 4, 'Puntaje'),
            #('EL', 6, 5, 30, 1)

        ]

        # II. Tablas en ventana
        # II.1 Lista de DE
        tabla_de_de_completa = b_de.generar_dataframe()
        self.tabla_de_de =  tabla_de_de_completa.drop(['HT_SALIDA', 'COD_PROBLEMA', 'FECHA_PROYECTO_FINAL',
                                                    'FECHA_FIRMA', 'TIPO_DOC', 'SE_EMITIO',
                                                    'MARCO_PEDIDO', 'FECHA_ULTIMO_MOV', 'FECHA_ASIGNACION',
                                                    'PLAZO', 'ESTADO_DOCE', 'ESPECIALISTA'], axis=1)

        # II.2 Lista de EP
        tabla_de_ep_completa = b_ep.generar_dataframe()
        tabla_de_ep_id = tabla_de_ep_completa
        tabla_de_ep = tabla_de_ep_id.drop(['ID_EP'], axis=1)
        
        # III. Ubicaciones
        # III.1 Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        titulos.agregar_titulo(0,1,'                             ')
        titulos.agregar_titulo(0,2,'Detalle de extremo de problema')
        titulos.agregar_titulo(0,3,'                             ')
        titulos.agregar_titulo(0,4,'                             ')

        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo != True:
            self.frame_rejilla.agregar_rejilla(rejilla_ep)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)
        else:
            self.frame_rejilla.agregar_rejilla(rejilla_ep_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.enviar_ep)
        f_boton.agregar_button(0, 2, 'Inicio', self.inicio_app) # Botón provisional
        
        # III.4 Frame de botón y títulos de vitrina 1
        self.boton_vitrina_1 = Cuadro(self)
        self.boton_vitrina_1.agregar_button(0, 0,'(+) Agregar', self.busqueda_dr)
        self.boton_vitrina_1.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_1.agregar_titulo(0, 2, 'Documentos recibidos asociados')
        self.boton_vitrina_1.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_1.agregar_titulo(0, 4,'                              ')

        # III.5 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        # En caso exista precedente, se busca en la tabla de Documentos emitidos
        if self.nuevo != True:
            self.frame_vitrina_1.agregar_label(1, 2, '                  0 documentos recibidos asociados')
        else:
            self.frame_vitrina_1.agregar_label(1, 2, '                  0 documentos recibidos asociados')


        # III.6 Frame de botón y títulos de vitrina 2
        self.boton_vitrina_2 = Cuadro(self)
        self.boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_de)
        self.boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_2.agregar_titulo(0, 2, 'Documentos emitidos asociados')
        self.boton_vitrina_2.agregar_titulo(0, 3, '                              ')
        self.boton_vitrina_2.agregar_titulo(0, 4, '                              ')

        # III.7 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
        if self.nuevo != True:
            # Provisional
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 documentos emitidos asociados') 
        else:
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 documentos emitidos asociados') 

    #----------------------------------------------------------------------
    def generar_vitrina(self, frame_vitrina,
                        tabla_codigo_entrada, tabla_salida, base_relacion, 
                        id_entrada, id_salida, funcion_ver, funcion_eliminar):
        """"""
        # Obtengo el código del usuario que heredo
        cod_usuario = self.id_problema
        # Genero las tablas para el filtrado 
        tabla_de_codigo = tabla_codigo_entrada.generar_dataframe() # Tabla de códigos
        tabla_de_relacion = base_relacion.generar_dataframe() # Tabla de relación
        # Filtro la tabla para obtener el código interno 
        tabla_de_codigo_filtrada = tabla_de_codigo[tabla_de_codigo['COD_EP']==cod_usuario]
        cod_interno = tabla_de_codigo_filtrada.iloc[0,0]
        # Filtro para obtener las relaciones activas
        tabla_relacion_activos = tabla_de_relacion[tabla_de_relacion['ESTADO']=="ACTIVO"]
        # Con ese ID, filtro la tabla de relacion
        tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos[id_entrada]==cod_interno]
        # Me quedo con el vector a filtrar en forma de lista
        lista_dr = list(tabla_relacion_filtrada[id_salida].unique())
        # Filtro la tabla de documentos recibidos
        tabla_filtrada = tabla_salida[tabla_salida[id_salida].isin(lista_dr)]
        # Tabla de documentos emitidos filtrada
        tabla_vitrina = tabla_filtrada.drop([id_salida], axis=1)
        if len(tabla_vitrina.index) > 0:
            self.vitrina = Vitrina_vista(self, tabla_vitrina, funcion_ver, funcion_eliminar, 
                                        height=80, width=1050) 
        else:
            frame_vitrina.agregar_label(1, 2, '                  0 documentos emitidos asociados')

    #----------------------------------------------------------------------
    def actualizar_vitrina(self, vitrina, frame_vitrina,
                            tabla_codigo_entrada, tabla_salida, tabla_relacion, 
                            id_entrada, id_salida, funcion_ver, funcion_eliminar):
        """"""
        vitrina.eliminar_vitrina()
        # Generar vitrina de documentos recibidos asociados
        self.generar_vitrina(frame_vitrina,
                            tabla_codigo_entrada, tabla_salida, tabla_relacion, 
                            id_entrada, id_salida, funcion_ver, funcion_eliminar)

    #----------------------------------------------------------------------
    def enviar_ep(self):
        """"""
        datos_ingresados = self.frame_rejilla.obtener_lista_de_datos()
        # Genero la tablas de código de DE
        tabla_de_codigo_ep = b_ep_cod.generar_dataframe()
        # Guardo el código de usuario que llega
        if self.nuevo != True:
            # En caso exista ID insertado en la rejilla
            cod_usuario_ep = self.id_problema
            valor_de_comprobacion = self.comprobar_id(b_ep_cod, cod_usuario_ep)

        else:
            # Comprobación de que no se ingresa un código de usuario repetido
            combinatoria = datos_ingresados[0] + datos_ingresados[1] # Mejorar a comprobación de combinación
            valor_de_comprobacion = self.comprobar_id(b_ep_cod, combinatoria) # Comprobar si el id de usuario ya existe
       
        # Modifico o creo, según exista
        # Modificación
        if valor_de_comprobacion == True:
            # A partir del código comprobado
            tabla_codigo_ep_filtrada = tabla_de_codigo_ep[tabla_de_codigo_ep['COD_EP']==cod_usuario_ep]
            cod_interno_ep = tabla_codigo_ep_filtrada.iloc[0,0]

            # Pestaña 1: Código Único
            # Obtengo los datos ingresados
            lista_descargada_codigo = b_ep_cod.listar_datos_de_fila(cod_interno_ep) # Se trae la info   
            # Obtengo el ID interno
            cod_usuario_ep = lista_descargada_codigo[3]
            correlativo = cod_interno_ep[7:20]
            nuevo_cod_usuario_ep = correlativo + "/" + datos_ingresados[0]
            # Actualizo las tablas en la web
            hora_de_modificacion = str(dt.datetime.now())
            b_dr_cod.cambiar_un_dato_de_una_fila(cod_interno_ep, 2, hora_de_modificacion) # Se actualiza código interno
            b_dr_cod.cambiar_un_dato_de_una_fila(cod_interno_ep, 4, nuevo_cod_usuario_ep) # Se actualiza código interno

            # Pestaña 2:       
            # Cambio los datos de una fila
            lista_a_sobreescribir = [cod_interno_ep] + [nuevo_cod_usuario_ep] + datos_ingresados
            b_ep.cambiar_los_datos_de_una_fila(cod_interno_ep, lista_a_sobreescribir) # Se sobreescribe la información
            
            # Pestaña 3
            lista_historial = lista_a_sobreescribir + [hora_de_modificacion] # Lo subido a la pestaña 2 + hora
            b_ep_hist.agregar_datos(lista_historial) # Se sube la info

            messagebox.showinfo("¡Excelente!", "Se ha actualizado el registro")
            self.actualizar_vista_dr(nuevo_cod_usuario_ep)

        # Creación
        else:
            # Timestamp
            ahora = str(dt.datetime.now())
            hora_de_creacion = str(ahora) # De lo creado en la pestaña 1
            # Pestaña 1: Código Único
            departamento = datos_ingresados[0]
            # Obtención de sigla de departamento
            tabla_siglas_filtrada = tabla_parametros_dep[tabla_parametros_dep['DEPARTAMENTO']==departamento]
            sigla_cod_interno = tabla_siglas_filtrada.iloc[0,1]
            # Obtención de número de extremo
            tabla_codigo_ep_filtrada = tabla_de_codigo_ep[tabla_de_codigo_ep['DEPARTAMENTO']==departamento]
            numero_problemas = len(tabla_codigo_ep_filtrada.index) + 1
            if numero_problemas < 10:
                numero_codigo = "-00" + str(numero_problemas)
            elif numero_problemas < 100:
                numero_codigo = "-0" + str(numero_problemas)
            else:
                numero_codigo = "-" + str(numero_problemas)
            
            cod_interno_ep = sigla_cod_interno + numero_codigo
            # Creo el código único
            b_ep_cod.agregar_codigo(cod_interno_ep, ahora, departamento)
            # Descargo el código único
            lista_descargada_codigo = b_ep_cod.listar_datos_de_fila(ahora) # Se trae la info
        
            # Pestaña 2:       
            # Obtengo el ID interno
            cod_interno_ep = lista_descargada_codigo[0]
            cod_usuario_ep = lista_descargada_codigo[3]
            # Creo el vector a subir
            lista_a_cargar = [cod_interno_ep] + [cod_usuario_ep] + datos_ingresados + [hora_de_creacion]
            b_ep.agregar_datos(lista_a_cargar) # Se sube la info

            # Pestaña 3
            # Lo subido a la pestaña 2 + Hora de último movimiento
            lista_historial = lista_a_cargar + [hora_de_creacion]
            b_ep_hist.agregar_datos(lista_historial) # Se sube la info
        
            # Confirmación de registro
            messagebox.showinfo("¡Excelente!", "Se ha ingresado un nuevo registro")
            self.actualizar_vista_ep(cod_usuario_ep) 
    
    #----------------------------------------------------------------------
    def actualizar_vista_ep(self, id_usuario):

        texto_documento = 'Extremo de problema: ' +  id_usuario

        lb1 = b_ep.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], 
                                lb1[8], lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], 
                                lb1[14], lb1[15], lb1[16], lb1[17], lb1[18], lb1[19]]
        
        self.desaparecer()
        subframe = Extremo_problemas_vista(self, 650, 1150, texto_documento, 
                                        nuevo=False, lista=lista_para_insertar, id_problema = id_usuario)
    
    #----------------------------------------------------------------------
    def busqueda_de(self):
        """"""
        if self.nuevo != True:
            # En caso exista un código insertado en la rejilla
            cod_usuario_dr = self.cod_usuario_dr 
            texto_pantalla = "Documento emitido que se asociará: " + cod_usuario_dr
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, texto_pantalla,
                                                           nuevo=False, id_doc = cod_usuario_dr)

        else:
            # En caso fuera una nueva ventana
            texto_pantalla = "Búsqueda de documentos emitidos"
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, texto_pantalla)


    #----------------------------------------------------------------------
    def ver_de(self, id_usuario):
        """"""
        texto_documento = 'Documento emitido: ' + id_usuario

        lb1 = b_de.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6]]
                    #, lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = Doc_emitidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_doc = id_usuario)

    #----------------------------------------------------------------------
    def eliminar_de(self, id_usuario_de):
        """"""
        # Obtengo los ID del usuario
        codigo_de = id_usuario_de
        codigo_dr = self.cod_usuario_dr
        # Genero las tablas de código 
        tabla_de_codigo_dr = b_dr_cod.generar_dataframe()
        tabla_de_codigo_de = b_de_cod.generar_dataframe()
        # Filtro las tablas para obtener el ID interno
        tabla_codigo_dr_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr['COD_DR']==codigo_dr]
        id_interno_dr = tabla_codigo_dr_filtrada.iloc[0,0]
        tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de['COD_DE']==codigo_de]
        id_interno_de = tabla_codigo_de_filtrada.iloc[0,0]
        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" + id_interno_de
        # Se cambia dato en tabla de relación
        base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4,'ELIMINADO')
        # Elimino los frame para insertar el cuadro actualizado
        self.boton_vitrina_2.eliminar_cuadro()
        self.frame_vitrina_2.eliminar_cuadro()

        # Situo la ventana actualizada
        self.actualizar_vitrina(self.vitrina, self.frame_vitrina_1,
                                b_dr_cod, self.tabla_de_de, base_relacion_docs, 
                                "ID_DR", "ID_DE", self.ver_de, self.eliminar_de)
        # Vuelvo a crear los cuadros luego de la vitrina 1
        self.boton_vitrina_2 = Cuadro(self) # Se vuelve a crear (Provisional)
        self.boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_ep)
        self.boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_2.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        self.boton_vitrina_2.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_2.agregar_titulo(0, 4,'                              ')
        self.frame_vitrina_2 = Cuadro(self) # Se vuelve a crear (Provisional)
        if self.nuevo != True:
            # Provisional
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 extremos de problemas asociados') 
        else:
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 extremos de problemas asociados') 

        # Actualización de historial
        datos_modificados = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
        hora = str(dt.datetime.now())
        datos_a_cargar_hist = datos_modificados + [hora]
        base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
        # Confirmación de eliminación de documento emitido
        messagebox.showinfo("¡Documento emitido eliminado!", "El registro se ha desasociado correctamente")
    
    #----------------------------------------------------------------------
    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

    #----------------------------------------------------------------------
    def busqueda_dr(self):
        """"""
        if self.nuevo != True:
            # En caso exista un código insertado en la rejilla
            cod_usuario_de = self.cod_usuario_de 
            texto_pantalla = "Documento emitido que se asociará: " + cod_usuario_de
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla,
                                                           nuevo=False, id_doc = cod_usuario_de)

        else:
            # En caso fuera una nueva ventana
            texto_pantalla = "Búsqueda de documentos recibidos"
            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla)
    
    #----------------------------------------------------------------------
    def ver_dr(self, id_usuario):
        """"""
        texto_documento = 'Documento recibido: ' + id_usuario

        lb1 = b_dr.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], 
                                lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], lb1[14]]
        
        self.desaparecer()
        subframe = Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_doc = id_usuario)

    #----------------------------------------------------------------------
    def eliminar_dr(self, id_usuario_dr):
        """"""
        # Obtengo los ID del usuario
        codigo_dr = id_usuario_dr
        codigo_de = self.cod_usuario_de
        # Genero las tablas de código 
        tabla_de_codigo_dr = b_dr_cod.generar_dataframe()
        tabla_de_codigo_de = b_de_cod.generar_dataframe()
        # Filtro las tablas para obtener el ID interno
        tabla_codigo_dr_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr['COD_DR']==codigo_dr]
        id_interno_dr = tabla_codigo_dr_filtrada.iloc[0,0]
        tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de['COD_DE']==codigo_de]
        id_interno_de = tabla_codigo_de_filtrada.iloc[0,0]
        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" + id_interno_de
        # Se cambia dato en tabla de relación
        base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4,'ELIMINADO')
        # Le paso el frame de DR
        self.actualizar_vitrina(self.vitrina, self.frame_vitrina_2, 
                                b_de_cod, self.tabla_de_dr, base_relacion_docs, 
                                "ID_DE", "ID_DR", self.ver_dr, self.eliminar_dr)

        # Actualización de historial
        datos_modificados = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
        hora = str(dt.datetime.now())
        datos_a_cargar_hist = datos_modificados + [hora]
        base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)

        # Confirmación de eliminación de documento emitido
        messagebox.showinfo("¡Documento recibido eliminado!", "El registro se ha desasociado correctamente")
    
    
    #----------------------------------------------------------------------
    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

class Macroproblemas_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_mp = None):
        """Constructor"""

        Ventana.__init__(self, *args)
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        if self.nuevo != True: # En caso exista
            self.lista_para_insertar = lista
            self.cod_usuario_mp = id_mp

        # I. Labels and Entries
        rejilla_mp = [
            ('L', 0, 0, 'Nombre del problema'),
            ('ST', 0, 1),

            ('L', 1, 0, 'Descripción'),
            ('ST', 1, 1),

            ('L', 2, 0, 'Observaciones'),
            ('ST', 2, 1),

            ('L', 3, 0, 'Estado'),
            ('E', 3, 1)
        ]

        # II. Tablas en ventana
        # II.1 Lista de DE
        tabla_de_ep_completa = b_ep.generar_dataframe()
        tabla_de_ep_id = tabla_de_ep_completa
        self.tabla_de_ep = tabla_de_ep_id.drop(['OCURRENCIA', 'EXTENSION', 'TIPO DE AFECTACION',
                                                'PROVINCIA', 'DISTRITO', 'DESCRIPCION', 'TIPO DE UBICACION',
                                                'CARACTERISTICA 1', 'CARACTERISTICA 2', 'TIPO CAUSA',
                                                'CODIGO SINADA', 'ACTIVIDAD', 'FECHA_ULTIMO_MOV'], axis=1)
        
        # III. Ubicaciones
        # III.1 Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        titulos.agregar_titulo(0,1,'                             ')
        titulos.agregar_titulo(0,2,'Detalle del macroproblema')
        titulos.agregar_titulo(0,3,'                             ')
        titulos.agregar_titulo(0,4,'                             ')

        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_mp)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo != True:
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.enviar_mp)
        f_boton.agregar_button(0, 2, 'Inicio', self.inicio_app) # Botón provisional
        
        # III.4 Frame de botón y títulos de vitrina 1
        self.boton_vitrina_1 = Cuadro(self)
        self.boton_vitrina_1.agregar_button(0, 0,'(+) Agregar', self.busqueda_de)
        self.boton_vitrina_1.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_1.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        self.boton_vitrina_1.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_1.agregar_titulo(0, 4,'                              ')

        # III.5 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_1,
                                 b_dr_cod, self.tabla_de_ep, base_relacion_dr_ep, 
                                 "ID_DR", "ID_EP", self.ver_ep, self.eliminar_ep)
        else:
            self.frame_vitrina_1.agregar_label(1, 2,'                  0 extremos de problemas asociados') 

    #----------------------------------------------------------------------
    def enviar_mp(self, x):
        """"""
        print("Guardar macroproblemas")
    

    #----------------------------------------------------------------------
    def eliminar_ep(self, x):
        """"""
        print("Eliminar extremo de problema asociado")
    
    #----------------------------------------------------------------------
    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")