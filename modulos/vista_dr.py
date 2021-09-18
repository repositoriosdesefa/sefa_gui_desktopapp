import datetime as dt
from PIL.Image import ImagePointHandler
import pandas as pd
from tkinter import Tk
from modulos import busqueda_dr
import gspread
from apoyo.elementos_de_GUI import Cuadro, Ventana, CustomHovertip
from apoyo.manejo_de_bases import Base_de_datos
from apoyo.vsf import Vitrina_vista
from tkinter import messagebox
import apoyo.datos_frecuentes as dfrec

# Prueba rama
# Valores de lista desplegable
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

id_b_ospa = '13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4'

# 0. Tablas relacionales
base_relacion_docs = Base_de_datos(id_b_ospa, 'RELACION_DOCS')
base_relacion_d_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_D')
# 1. Bases de datos principales
# Documentos recibidos
b_dr_cod = Base_de_datos(id_b_ospa, 'DOCS_R')
b_dr = Base_de_datos(id_b_ospa, 'DOC_RECIBIDOS_FINAL')
b_dr_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_DR')
# Documentos emitidos
b_de_cod = Base_de_datos(id_b_ospa, 'DOCS_E')
b_de = Base_de_datos(id_b_ospa, 'DOC_EMITIDOS_FINAL')
b_de_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_DE')
# Extremo de problemas
b_ep = Base_de_datos(id_b_ospa, 'EXTREMOS')

# 2. Bases de datos complementarias
id_b_efa = '1pjHXiz15Zmw-49Nr4o1YdXJnddUX74n7Tbdf5SH7Lb0'
b_efa = Base_de_datos(id_b_efa, 'Directorio')

class inicio_app_OSPA(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_button(3, 1, "DR", self.vista_dr)
        c1.agregar_label(4, 1,' ')
        c1.agregar_button(5, 1, "BDR", self.busqueda_dr)
        c1.agregar_label(6, 1,' ')
        c1.agregar_button(7, 1, "DE", self.vista_de)
        c1.agregar_label(8, 1,' ')
        c1.agregar_button(9, 1, "BDE", self.busqueda_de)
        c1.agregar_label(10, 1,' ')

    #----------------------------------------------------------------------
    def vista_dr(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Doc_recibidos_vista(self, 650, 1200, "Documentos recibidos")
    
    #----------------------------------------------------------------------
    def busqueda_dr(self):


        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, "Búsqueda de documentos recibidos")

    #----------------------------------------------------------------------
    def vista_de(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Doc_emitidos_vista(self, 650, 1200, "Documentos emitidos")
    
    #----------------------------------------------------------------------
    def busqueda_de(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, "Búsqueda de documentos emitidos")



class Doc_recibidos_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        self.nuevo = nuevo

        # Lista de DE
        tabla_de_de_completa = b_de.generar_dataframe()
        tabla_de_de_id =  tabla_de_de_completa.drop(['HT_SALIDA', 'COD_PROBLEMA', 'FECHA_PROYECTO_FINAL',
                                                    'FECHA_FIRMA', 'TIPO_DOC', 'SE_EMITIO',
                                                    'MARCO_PEDIDO', 'FECHA_ULTIMO_MOV', 'FECHA_ASIGNACION',
                                                    'PLAZO', 'ESTADO_DOCE', 'ESPECIALISTA'], axis=1)
        # Lista de DE asociados
        tabla_de_de = tabla_de_de_id.drop(['ID_DE'], axis=1)

        # Lista de EP
        tabla_de_ep_completa = b_ep.generar_dataframe()
        tabla_de_ep_id = tabla_de_ep_completa
        tabla_de_ep = tabla_de_ep_id.drop(['ID_DE', 'ID_DR', 'ID_EP'], axis=1)

        # Desplegable EFA
        tabla_directorio = b_efa.generar_dataframe()
        lista_efa = list(set(tabla_directorio['Entidad u oficina']))

        # Labels and Entries
        rejilla_dr = (
            ('L', 0, 0, 'HT entrante'),
            ('E', 0, 1),

            ('L', 0, 2, 'Vía de recepción'),
            ('CX', 0, 3, tipo_ingreso),

            ('L', 1, 0, 'Fecha de recepción OEFA'),
            ('D', 1, 1),

            ('L', 1, 2, 'Fecha de recepción SEFA'),
            ('D', 1, 3),

            ('L', 2, 0, 'Tipo de documento'),
            ('CX', 2, 1, tipo_documento),

            ('L', 2, 2, 'N° de documento'),
            ('E', 2, 3),

            ('L', 3, 0, 'Remitente'),
            ('CX', 3, 1, lista_efa),

            ('L', 3, 2, 'Especialista asignado'),
            ('CX', 3, 3, especialista),

            ('L', 4, 0, 'Asunto'),
            ('EL', 4, 1, 112),

            ('L', 5, 0, 'Aporte del documento'),
            ('ST', 5, 1),

            ('L', 6, 0, 'Indicación'),
            ('CX', 6, 1, tipo_indicacion),

            ('L', 6, 2, '¿Es respuesta?'),
            ('CX', 6, 3, si_no),

            ('L', 7, 0, 'Respuesta'),
            ('CX', 7, 1, tipo_respuesta)
        )

        # Ubicaiones

        # 1. Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        titulos.agregar_titulo(0,1,'                             ')
        titulos.agregar_titulo(0,2,'Detalle de documento recibido')
        titulos.agregar_titulo(0,3,'                             ')
        titulos.agregar_titulo(0,4,'                             ')

        # 2. Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_dr)

        if self.nuevo != True:
            self.lista_para_insertar = lista
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        # 3. Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.enviar_dr)
        f_boton.agregar_button(0, 2, 'Inicio', self.inicio_app) # Botón provisional
        
        # 4. Frame de botón y títulos de vitrina 1
        boton_vitrina_1 = Cuadro(self)
        boton_vitrina_1.agregar_button(0, 0,'(+) Agregar', self.busqueda_de)
        boton_vitrina_1.agregar_titulo(0, 1,'                                                       ')
        boton_vitrina_1.agregar_titulo(0, 2, 'Documentos emitidos asociados')
        boton_vitrina_1.agregar_titulo(0, 3,'                              ')
        boton_vitrina_1.agregar_titulo(0, 4,'                              ')

        # 5. Frame de vitrina 1
        self.vitrina_1 = Cuadro(self)
        # Generar vitrina de documentos emitidos asociados
        if self.nuevo != True:
            # Uso la lista que hereda
            lista_para_filtrar = lista
            # Obtengo el ID del usuario
            id_doc = lista_para_filtrar[0]
            # Generación de tabla de relación
            tabla_de_relacion = base_relacion_docs.generar_dataframe()
            # Con ese ID, filtro la tabla de relacion
            tabla_filtrada = tabla_de_relacion[tabla_de_relacion['ID_DR']==id_doc]
            # Me quedo con el vector a filtrar
            vector_de = tabla_filtrada['ID_DE']
            valor_prueba = 'DOCS_E-2021-2'
            # Filtro con el vector de documentos emitidos asociados
            tabla_de_de_vinculada = tabla_de_de_id[tabla_de_de_id['ID_DE']==valor_prueba]
            # Tabla de documentos emitidos filtrada
            tabla_de_de = tabla_de_de_vinculada.drop(['ID_DE'], axis=1)
            if len(tabla_de_de.index) > 0:
                v1 = Vitrina_vista(self, tabla_de_de, self.ver_de, 
                                   self.eliminar_de, height=80, width=1050) 
            else:
                self.vitrina_1.agregar_label(1, 2, '                  0 documentos emitidos asociados')
        else:
            self.vitrina_1.agregar_label(1, 2, '                  0 documentos emitidos asociados') 

        # 6. Frame de botón y títulos de vitrina 2
        boton_vitrina_2 = Cuadro(self)
        boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_ep)
        boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        boton_vitrina_2.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        boton_vitrina_2.agregar_titulo(0, 3,'                              ')
        boton_vitrina_2.agregar_titulo(0, 4,'                              ')

        # 7. Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
        if self.nuevo != True:
            v2 = Vitrina_vista(self, tabla_de_ep, self.ver_ep, 
                               self.eliminar_ep, height=80, width=1050)
        else:
            self.frame_vitrina_2.agregar_label(1, 2,'                  0 extremos de problemas asociados') 

    #----------------------------------------------------------------------
    def enviar_dr(self):
        """"""
        datos_ingresados = self.frame_rejilla.obtener_lista_de_datos()

        # Pestaña 1: Código Único
        codigo_ht = datos_ingresados[0]
        b_dr_cod.agregar_dato_generando_id(codigo_ht)
        
        # Pestaña 2: 
        lista_descargada_codigo = b_dr_cod.listar_datos_de_fila(codigo_ht)
        codigo_dr = lista_descargada_codigo[0]
        lista_a_cargar = datos_ingresados + [codigo_dr]
        b_dr.agregar_datos(lista_a_cargar)

        # Pestaña 3
        hora_de_creacion = lista_descargada_codigo[1]
        lista_historial = lista_a_cargar + [hora_de_creacion]
        b_dr_hist.agregar_datos(lista_historial)
        
        # Confirmación de registro
        messagebox.showinfo("¡Excelente!", "El registro se ha ingresado correctamente")

    #----------------------------------------------------------------------
    def busqueda_de(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, "Pantalla de búsqueda")

    #----------------------------------------------------------------------
    def ver_de(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento emitido: ' + x

        bde = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS_FINAL')
        lb1 = bde.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = Doc_emitidos_vista(self, 600, 1100, texto_documento, nuevo=False, lista=lista_para_insertar)

    #----------------------------------------------------------------------
    def eliminar_de(self, x):
        """"""
        print("Eliminar documento emitido asociado")
    
    #----------------------------------------------------------------------
    def busqueda_ep(self):
        """"""
        print("Pantalla de búsqueda de extremo de problemas")
    
    #----------------------------------------------------------------------
    def ver_ep(self, x):
        """"""
        print("Ver extremo de problema asociado")

    #----------------------------------------------------------------------
    def eliminar_ep(self, x):
        """"""
        print("Eliminar extremo de problema asociado")
    
    #----------------------------------------------------------------------
    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = inicio_app_OSPA(self, 400, 400, "Inicio")



class Doc_emitidos_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc=None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información heredada
        self.nuevo = nuevo
        if self.nuevo != True: # En caso exista
            self.lista_para_insertar = lista

        # Desplegable EFA
        tabla_directorio = b_efa.generar_dataframe()
        lista_efa = list(set(tabla_directorio['Entidad u oficina']))

        # Labels and Entries
        rejilla_dr = (
            ('L', 0, 0, 'HT de salida'),
            ('E', 0, 1),

            ('L', 0, 2, 'Categoría'),
            ('CX', 0, 3, categorias),

            ('L', 1, 0, 'Fecha de proyecto final'),
            ('D', 1, 1),

            ('L', 1, 2, 'Fecha de firma'),
            ('D', 1, 3),

            ('L', 2, 0, 'Tipo de documento'),
            ('CX', 2, 1, tipo_documento),

            ('L', 2, 2, 'N° de documento'),
            ('E', 2, 3),

            ('L', 3, 0, 'Destinatario'),
            ('CX', 3, 1, lista_efa),

            ('L', 3, 2, '¿Se emitió documento?'),
            ('CX', 3, 3, si_no),

            ('L', 4, 0, 'Detalle de requerimiento'),
            ('ST', 4, 1),

            ('L', 5, 0, 'Marco de pedido'),
            ('CX', 5, 1, marco_pedido),

            ('L', 5, 2, 'Fecha de notificación'),
            ('D', 5, 3)

        )

        # Lista de DR
        tabla_de_dr = b_dr.generar_dataframe()
        self.tabla_de_dr = tabla_de_dr.drop(['COD_PROBLEMA', 'VIA_RECEPCION', 'HT_ENTRANTE',
                                        'F_ING_OEFA', 'TIPO_DOC', 'ESPECIALISTA',
                                        'INDICACION', 'TIPO_RESPUESTA', 'RESPUESTA',
                                        'FECHA_ULTIMO_MOV', 'FECHA_ASIGNACION'], axis=1)
        # Lista de EP
        tabla_de_ep = b_ep.generar_dataframe()
        tabla_de_ep = tabla_de_ep.drop(['ID_DE', 'ID_DR', 'ID_EP'], axis=1)

        # Ubicaciones

        # 1. Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        titulos.agregar_titulo(0,1,'                             ')
        titulos.agregar_titulo(0,2,'Detalle de documento emitido ')
        titulos.agregar_titulo(0,3,'                             ')
        titulos.agregar_titulo(0,4,'                             ')

        # 2. Frame de rejilla
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_dr)

        if self.nuevo != True: # En caso exista se inserta en las rejillas
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)
            self.id_usuario = id_doc

        # 3. Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.enviar_de)
        f_boton.agregar_button(0, 2, 'Inicio', self.inicio_app) # Botón provisional

        # 4. Frame de botón y títulos de vitrina 1
        boton_vitrina_1 = Cuadro(self)
        boton_vitrina_1.agregar_button(0, 0,'(+) Agregar', self.busqueda_ep)
        boton_vitrina_1.agregar_titulo(0, 1,'                                                       ')
        boton_vitrina_1.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        boton_vitrina_1.agregar_titulo(0, 3,'                              ')
        boton_vitrina_1.agregar_titulo(0, 4,'                              ')

        # 5. Frame de vitrina 1
        self.vitrina_1 = Cuadro(self)

        if self.nuevo != True:
            # Agregar condicional para filtrar los problemas relacionados
            self.vitrina_1.agregar_label(1, 2, '                0 extremos de problemas asociados')

        else:
            self.vitrina_1.agregar_label(1, 2, '                0 extremos de problemas asociados')

        # 6. Frame de botón y títulos de vitrina 2
        boton_vitrina_2 = Cuadro(self)
        boton_vitrina_2.agregar_button(0, 0,'(+) Agregar', self.busqueda_dr)
        boton_vitrina_2.agregar_titulo(0, 1,'                                                       ')
        boton_vitrina_2.agregar_titulo(0, 2, 'Documentos recibidos asociados')
        boton_vitrina_2.agregar_titulo(0, 3,'                              ')
        boton_vitrina_2.agregar_titulo(0, 4,'                              ')
        
        # 7. Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_2,
                                 b_de_cod, self.tabla_de_dr, base_relacion_docs, 
                                 "ID_DE", "ID_DR", self.ver_dr, self.eliminar_dr)
        else:
            self.frame_vitrina_2.agregar_label(1, 2, '                  0 documentos emitidos asociados')

        
    #----------------------------------------------------------------------
    def generar_vitrina(self, frame_vitrina,
                        tabla_codigo_entrada, tabla_salida, base_relacion, 
                        id_entrada, id_salida, funcion_ver, funcion_eliminar):
        """"""
        # Obtengo el ID del usuario que heredo
        id_usuario = self.id_usuario
        # Genero las tablas para el filtrado 
        tabla_de_codigo = tabla_codigo_entrada.generar_dataframe() # Tabla de códigos
        tabla_de_relacion = base_relacion.generar_dataframe() # Tabla de relación
        # Filtro la tabla para obtener el ID de la 
        tabla_de_codigo_filtrada = tabla_de_codigo[tabla_de_codigo['HT_ID']==id_usuario]
        id_interno = tabla_de_codigo_filtrada.iloc[0,0]
        # Filtro para obtener las relaciones activas
        tabla_relacion_activos = tabla_de_relacion[tabla_de_relacion['ESTADO']=="ACTIVO"]
        # Con ese ID, filtro la tabla de relacion
        tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos[id_entrada]==id_interno]
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
    def enviar_de(self):
        """"""

        datos_ingresados = self.frame_rejilla.obtener_lista_de_datos()
        # Genero la tablas de código de DE
        tabla_de_codigo_de = b_de_cod.generar_dataframe()
        # Guardo el ID de usuario que llega
        if self.nuevo != True:
            # En caso exista ID insertado en la rejilla
            id_usuario_insertado = self.id_usuario # Compruebo si son iguales
            valor_de_comprobacion = self.comprobar_id(b_de_cod, id_usuario_insertado)
            id_usuario = id_usuario_insertado

        else:
            # ID ingresado en la rejilla
            id_usuario_ingresado = datos_ingresados[0]
            valor_de_comprobacion = self.comprobar_id(b_de_cod, id_usuario_ingresado) # Comprobar si el id de usuario ya existe
            id_usuario = id_usuario_ingresado
       
        # Modifico o creo, según exista
        if valor_de_comprobacion == True:
            # A partir del código comprobado
            tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de['HT_ID']==id_usuario]
            id_interno_de = tabla_codigo_de_filtrada.iloc[0,0]
            # Pestaña 1: Código Único
            # Obtengo los datos ingresados
            id_usuario_ingresado = datos_ingresados[0]
            id_usuario = id_usuario_ingresado
            # Actualizo las tablas en la web
            hora_de_modificacion = str(dt.datetime.now())
            b_de_cod.cambiar_un_dato_de_una_fila(id_interno_de, 4, id_usuario) # Se actualiza código interno
            b_de_cod.cambiar_un_dato_de_una_fila(id_interno_de, 2, hora_de_modificacion) # Se actualiza código interno

            # Pestaña 2:       
            # Cambio los datos de una fila
            lista_a_sobreescribir = [id_interno_de] + datos_ingresados
            b_de.cambiar_los_datos_de_una_fila(id_interno_de, lista_a_sobreescribir) # Se sobreescribe la información
            
            # Pestaña 3
            lista_historial = lista_a_sobreescribir + [hora_de_modificacion] # Lo subido a la pestaña 2 + hora
            b_de_hist.agregar_datos(lista_historial) # Se sube la info

            messagebox.showinfo("¡Excelente!", "Se ha actualizado el registro")
            self.actualizar_doc_vista(id_usuario)
        
        else:
            # Timestamp
            ahora = str(dt.datetime.now())
            # Pestaña 1: Código Único
            b_de_cod.agregar_dato_generando_id(id_usuario, ahora)
            # Obtengo el ID creado por el momento de ingreso
            lista_descargada_codigo = b_de_cod.listar_datos_de_fila(ahora) # Se trae la info
        
            # Pestaña 2:       
            # Obtengo el ID interno
            cod_interno = lista_descargada_codigo[0]
            cod_usuario = lista_descargada_codigo[3]
            # Creo el vector a subir
            lista_a_cargar = [cod_interno] + [cod_usuario] + datos_ingresados
            b_de.agregar_datos(lista_a_cargar) # Se sube la info

            # Pestaña 3
            hora_de_creacion = str(ahora) # De lo creado en la pestaña 1
            lista_historial = lista_a_cargar + [hora_de_creacion] # Lo subido a la pestaña 2 + hora
            b_de_hist.agregar_datos(lista_historial) # Se sube la info
        
            # Confirmación de registro
            messagebox.showinfo("¡Excelente!", "Se ha ingresado un nuevo registro")
            self.actualizar_doc_vista(cod_usuario) 
    
    #----------------------------------------------------------------------
    def actualizar_doc_vista(self, id_usuario):

        texto_documento = 'Documento emitido: ' +  id_usuario

        lb1 = b_de.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        
        self.desaparecer()
        subframe = Doc_emitidos_vista(self, 650, 1100, texto_documento, 
                                        nuevo=False, lista=lista_para_insertar, id_doc = id_usuario)
    
    #----------------------------------------------------------------------
    def busqueda_ep(self):
        """"""
        print("Búsqueda de extremo de problema")

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
        # Obtengo el ID usuario
        id_usuario = "2021-1/2018-E01-014945"
        texto_pantalla = "Documento emitido: " + id_usuario
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla,
                                                    nuevo=False, dato=id_usuario)

    #----------------------------------------------------------------------
    def ver_dr(self, id_usuario):
        """"""
        self.x = id_usuario
        texto_documento = 'Documento recibido: ' + id_usuario

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS')
        lb1 = b1.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[1], lb1[2],lb1[3], lb1[4], lb1[5], 
                               lb1[6], lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12], lb1[13]]
        
        self.desaparecer()
        subframe = Doc_recibidos_vista(self, 650, 1200, texto_documento, nuevo=False, lista=lista_para_insertar)

    #----------------------------------------------------------------------
    def eliminar_dr(self, id_usuario_dr):
        """"""
        # Obtengo los ID del usuario
        codigo_dr = id_usuario_dr
        codigo_de = self.id_usuario
        # Genero las tablas de código 
        tabla_de_codigo_dr = b_dr_cod.generar_dataframe()
        tabla_de_codigo_de = b_de_cod.generar_dataframe()
        # Filtro las tablas para obtener el ID interno
        tabla_codigo_dr_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr['HT_ID']==codigo_dr]
        id_interno_dr = tabla_codigo_dr_filtrada.iloc[0,0]
        tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de['HT_ID']==codigo_de]
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
        messagebox.showinfo("¡Documento desasociado!", "El registro se ha desasociado correctamente")
    
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
        subFrame = inicio_app_OSPA(self, 400, 400, "Inicio")

