from tkinter import Message, messagebox
import datetime as dt
import pandas as pd
from apoyo.elementos_de_GUI import Cuadro, Ventana, Vitrina_busqueda, Vitrina_busquedaep, Vitrina_pendientes_jefe_firma
from apoyo.manejo_de_bases import Base_de_datos
import apoyo.datos_frecuentes as dfrec
from modulos import vista_dr
from modulos import menus

# BASES DE DATOS:
#----------------------------------------------------------------------
id_b_ospa = '13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4'

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
#b_de_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_EP')
# Macroproblemas
b_mc = Base_de_datos(id_b_ospa, 'MACROPROBLEMA')
# Administrados
b_ad = Base_de_datos(id_b_ospa, 'ADMINISTRADOS')

# 2. Bases de datos complementarias
id_b_efa = '1pjHXiz15Zmw-49Nr4o1YdXJnddUX74n7Tbdf5SH7Lb0'
b_efa = Base_de_datos(id_b_efa, 'Directorio')
#----------------------------------------------------------------------

class Doc_recibidos_busqueda(Ventana):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_de = id_doc

        # Generamos el dataframe a filtrar
        self.tabla_inicial = b_dr.generar_dataframe()
        self.tabla_0 = self.tabla_inicial.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['NRO DOC','REMITENTE','HT INGRESO','FECHA INGRESO SEFA','INDICACION','ESPECIALISTA','FECHA ULTIMO MOV.','ASUNTO']]
        
        # Información para las listas desplegables
        self.listatipodoc = list(set(self.tabla_0['TIPO DOC']))
        self.listaremitente = list(set(self.tabla_0['REMITENTE']))

        # Agregando logo del ospa a la ventana y título
        self.c0 = Cuadro(self)
        self.c0.agregar_label(0,0,' ')
        self.c0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)
        c2 = Cuadro(self)
        c2.agregar_titulo(2, 0, 'Búsqueda de documentos recibidos')

        # Armando rejilla con los filtros
        self.rejilla_dr = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 39, self.listatipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 39, self.listaremitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3)

        )


        # Agregando rejilla a la ventana
        self.c1 = Cuadro(self)
        self.c1.agregar_rejilla(self.rejilla_dr)

        # Generando rejilla para botones
        self.rejilla_b = (
            ('B', 5, 4, 'Buscar', self.Buscardr),
            ('B', 5, 5, 'Limpiar', self.limpiar),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.c15 = Cuadro(self)
        self.c15.agregar_rejilla(self.rejilla_b)

        self.frame_vitrina_dr = Cuadro(self)

        # Creando vitrina
        self.v1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_dr, 
                                   self.asociar_dr_de, height=200, width=1080)
    
    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")


    #----------------------------------------------------------------------

    def Buscardr(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro = self.c1.obtener_lista_de_datos()
        self.ht = self.listas_filtro[0]
        self.tipodoc = self.listas_filtro[1]
        self.remitente = self.listas_filtro[2]
        self.nrodoc = self.listas_filtro[3]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodoc)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodoc+"' "
        
        self.mostrarDatosdr(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatosdr(self, filtro):

        self.filtro0 = self.tabla_0
        
        if len(self.remitente)>0: # Filtro por palabra clave
            self.v1.Eliminar_vitrina()
            self.filtro0 = self.tabla_0[self.tabla_0['REMITENTE'].str.contains(self.remitente)]
            self.Complementodr(self.filtro0)

        if len(self.nrodoc)>0: # Filtro por palabra clave
            self.v1.Eliminar_vitrina()
            self.filtro0['NRO DOC']=self.filtro0['NRO DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOC'].str.contains(self.nrodoc)]
            self.Complementodr(self.filtro0)

        if len(self.ht)>0: # Filtro por palabra clave
            self.v1.Eliminar_vitrina()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.ht)]
            self.Complementodr(self.filtro0)

        if len(filtro)>0:

            self.v1.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementodr(self.filtro1)

        else:
            self.v1.Eliminar_vitrina()
            self.Complementodr(self.filtro0)

    #----------------------------------------------------------------------

    def Complementodr(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['NRO DOC','REMITENTE','HT INGRESO','FECHA INGRESO SEFA','INDICACION','ESPECIALISTA','FECHA ULTIMO MOV.','ASUNTO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_dr.eliminar_cuadro()
            self.frame_vitrina_dr = Cuadro(self)
            self.v1 = Vitrina_busqueda(self, tabla_filtro3, self.ver_dr, 
                                   self.asociar_dr_de, height=200, width=1080)
        else:
            self.frame_vitrina_dr.eliminar_cuadro()
            self.frame_vitrina_dr = Cuadro(self)
            self.frame_vitrina_dr.agregar_label(1, 2, '                  0 documentos encontrados')

    #----------------------------------------------------------------------
    def limpiar(self):
        
        # Eliminando campos
        self.c1.eliminar_cuadro()
        self.v1.Eliminar_vitrina()
        self.c15.eliminar_cuadro()
        self.frame_vitrina_dr.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.c1 = Cuadro(self)
        self.c1.agregar_rejilla(self.rejilla_dr)
        self.c15 = Cuadro(self)
        self.c15.agregar_rejilla(self.rejilla_b)
        self.frame_vitrina_dr = Cuadro(self)
        # Creando vitrina
        self.v1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_dr, 
                                   self.asociar_dr_de, height=200, width=1080)

    #----------------------------------------------------------------------

    def volver(self):
        """"""
        codigode = self.cod_doc_de

        lb1 = b_de.listar_datos_de_fila(codigode)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6]]
        #,                       lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, 
                                                nuevo=False, lista=lista_para_insertar, id_doc=codigode)

    #----------------------------------------------------------------------
    def ver_dr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x
        #print(x)
        lb1 = b_dr.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], lb1[11], lb1[12], lb1[13]]
        
        self.desaparecer()
        subframe = vista_dr.Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                                lista=lista_para_insertar, id_doc = x)

    #----------------------------------------------------------------------
    def asociar_dr_de(self, x):
        """"""
        self.x = x
        
        #OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
        self.IDDR = b_dr.listar_datos_de_fila(self.x)
        self.IDDR_FINAL = self.IDDR[0]

        #OBTENER EL ID USUARIO DEL DOCUMENTO EMITIDO
        codigode = self.cod_doc_de
        # OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
        tabla_de_codigo_de = b_de.generar_dataframe()
        tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de.COD_DE == codigode]
        id_interno_de = tabla_codigo_de_filtrada.iloc[0,0]
        
        # Definición de ID de relación
        id_relacion_doc = self.IDDR_FINAL + "/" + id_interno_de

        # BUSCAR COINCIDENCIAS
        valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)

        # BUSCAR ESTADO DE ID RELACION SI EXISTE
        if valor_repetido != False:  # si hay coincidencias de ese id_relacion_doc
            tabla_de_relaciones = base_relacion_docs.generar_dataframe()
            tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_doc]
            estado_rela = tabla_relaciones_filtrada.iloc[0,3]

        hora_de_modificacion = str(dt.datetime.now())

        if valor_repetido != True:
            
            # GUARDAR RELACION
            b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'RELACION_DOCS')

            # Pestaña 1: Código Único
            datos_insertar = [id_relacion_doc,self.IDDR_FINAL,id_interno_de,'ACTIVO',hora_de_modificacion]
            b0.agregar_datos(datos_insertar)
            datos_a_cargar_hist = [id_relacion_doc,self.IDDR_FINAL,id_interno_de,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
            base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
            messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        else:
            if estado_rela == 'ACTIVO':
                messagebox.showinfo("Error", "Ya se encuentra asociado")
            else:
                datos_iniciales = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
                hora = str(dt.datetime.now())
                datos_a_cargar_hist = datos_iniciales + [hora]
                estado_a_sobreescribir = 'ACTIVO'
                datos_a_cargar_hist[3] = estado_a_sobreescribir
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 5, hora)
                base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
                base_relacion_d_hist.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
    
    #----------------------------------------------------------------------     
    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

class Doc_emitidos_busqueda(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_dr = id_doc

        # Generamos el dataframe a filtrar
        self.tabla_inicial = b_de.generar_dataframe()
        self.tabla_0 = self.tabla_inicial.rename(columns={'COD_DE':'DOC EMITIDO','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['DOC EMITIDO','DESTINATARIO','HT SALIDA','FECHA FIRMA','FECHA NOTIFICACION','ESTADO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.listacategoria = list(set(self.tabla_0['CATEGORIA']))
        self.listadestinatario = list(set(self.tabla_0['DESTINATARIO']))
        self.listatipodocemit = list(set(self.tabla_0['TIPO DOC']))
        self.listaestado = list(set(self.tabla_0['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        self.cde0 = Cuadro(self)
        self.cde0.agregar_label(0, 0,' ')
        self.cde0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        cde2 = Cuadro(self)
        cde2.agregar_titulo(2, 0, 'Búsqueda de documentos emitidos')

        # Armando rejilla con los filtros

        self.rejilla_de = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 39, self.listacategoria, '', 'readonly'),

            ('L', 1, 0, 'Nro registro Siged'),
            ('EE', 1, 1),

            ('L', 0, 2, 'Destinatario'),
            ('CXE', 0, 3, 39, self.listadestinatario, '', 'normal'),

            ('L', 1, 2, 'Estado'),
            ('CXE', 1, 3, 39, self.listaestado, '', 'normal'),

            ('L', 2, 0, 'Tipo de documento'),
            ('CXP', 2, 1, 39, self.listatipodocemit, '', 'readonly'),

            ('L', 2, 2, 'Nro de documento'),
            ('EE', 2, 3)

        )
        
        # Agregando rejilla a la ventana
        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)

        # Generando rejilla para botones
        self.rejilla_bde = (
            ('B', 5, 4, 'Buscar', self.Buscar_de),
            ('B', 5, 5, 'Limpiar', self.limpiar_de),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.cde15 = Cuadro(self)
        self.cde15.agregar_rejilla(self.rejilla_bde)
        self.frame_vitrina_1 = Cuadro(self)

        # Creando vitrina
        self.vde1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_de, 
                                    self.asociar_de_dr, height=200, width=1080)

    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

    #----------------------------------------------------------------------

    def Buscar_de(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtrode = self.cde1.obtener_lista_de_datos()
        self.decate = self.listas_filtrode[0] #
        self.deid = self.listas_filtrode[1]
        self.dedestin = self.listas_filtrode[2]
        self.deestado = self.listas_filtrode[3]
        self.detipodoc = self.listas_filtrode[4] #
        self.dedoc = self.listas_filtrode[5]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.decate)>0 :
            filtro="CATEGORIA=="+"'"+self.decate+"' "
    
        if len(self.detipodoc)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO DOC`=="+"'"+self.detipodoc+"' "
        
        self.mostrarDatosde(filtro)

    #----------------------------------------------------------------------

    def mostrarDatosde(self, filtro):

        self.filtro0 = self.tabla_0
        
        if len(self.deid)>0: # Filtro por palabra clave
            self.vde1.Eliminar_vitrina()
            self.filtro0['HT SALIDA']=self.filtro0['HT SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT SALIDA'].str.contains(self.deid)]
            self.Complementode(self.filtro0)

        if len(self.dedoc)>0: # Filtro por palabra clave
            self.vde1.Eliminar_vitrina()
            self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOCUMENTO'].str.contains(self.dedoc)]
            self.Complementode(self.filtro0)

        if len(self.dedestin)>0: # Filtro por palabra clave
            self.vde1.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.dedestin)]
            self.Complementode(self.filtro0)

        if len(self.deestado)>0: # Filtro por palabra clave
            self.vde1.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['ESTADO'].str.contains(self.deestado)]
            self.Complementode(self.filtro0)
  
        if len(filtro)>0:

            self.vde1.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementode(self.filtro1)

        else:
            self.vde1.Eliminar_vitrina()
            self.Complementode(self.filtro0)

    #----------------------------------------------------------------------
    def Complementode(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['DOC EMITIDO','DESTINATARIO','HT SALIDA','FECHA FIRMA','FECHA NOTIFICACION','ESTADO','CATEGORIA','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.vde1 = Vitrina_busqueda(self, tabla_filtro3, self.ver_de, self.asociar_de_dr, height=200, width=1080)
        else:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.frame_vitrina_1.agregar_label(1, 2, '                  0 documentos encontrados')

    #----------------------------------------------------------------------

    def limpiar_de(self):

        # Eliminando campos
        self.cde1.eliminar_cuadro()
        self.vde1.Eliminar_vitrina()
        self.cde15.eliminar_cuadro()
        self.frame_vitrina_1.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)
        self.cde15 = Cuadro(self)
        self.cde15.agregar_rejilla(self.rejilla_bde)
        self.frame_vitrina_1 = Cuadro(self)
        # Creando vitrina
        self.vde1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_de, self.asociar_de_dr, height=200, width=1080)

    #----------------------------------------------------------------------

    def volver(self):
        """"""
        codigodr = self.cod_doc_dr

        lb1 = b_dr.listar_datos_de_fila(codigodr)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
                                                nuevo=False, lista=lista_para_insertar, id_doc=codigodr)

    #----------------------------------------------------------------------
    def ver_de(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento emitido: ' + x

        lb1 = b_de.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                                nuevo=False, lista=lista_para_insertar, id_doc=x)

    #----------------------------------------------------------------------
    def asociar_de_dr(self, x):
        """"""
        self.x = x

        #OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
        self.IDDE = b_de.listar_datos_de_fila(self.x)
        self.IDDE_FINAL = self.IDDE[0]

        #OBTENER EL ID USUARIO DEL DOCUMENTO RECIBIDO
        codigodr = self.cod_doc_dr
        # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
        tabla_de_codigo_dr = b_dr.generar_dataframe()
        tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == codigodr]
        id_interno_dr = tabla_codigo_de_filtrada.iloc[0,0]

        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" +  self.IDDE_FINAL

        # BUSCAR COINCIDENCIAS
        valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)

        # BUSCAR ESTADO DE ID RELACION SI EXISTE
        if valor_repetido != False:  # si hay coincidencias de ese id_relacion_doc
            tabla_de_relaciones = base_relacion_docs.generar_dataframe()
            tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_doc]
            estado_rela = tabla_relaciones_filtrada.iloc[0,3]

        hora_de_modificacion = str(dt.datetime.now())

        if valor_repetido != True:
            
            # GUARDAR RELACION
            b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'RELACION_DOCS')

            # Pestaña 1: Código Único
            datos_insertar = [id_relacion_doc,id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion]
            b0.agregar_datos(datos_insertar)
            datos_a_cargar_hist = [id_relacion_doc, id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
            base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
            messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        else:
            if estado_rela == 'ACTIVO':
                messagebox.showinfo("Error", "Ya se encuentra asociado")
            else:
                datos_iniciales = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
                hora = str(dt.datetime.now())
                datos_a_cargar_hist = datos_iniciales + [hora]
                estado_a_sobreescribir = 'ACTIVO'
                datos_a_cargar_hist[3] = estado_a_sobreescribir
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 5, hora)
                base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
                base_relacion_d_hist.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        
        # Asociación de extremos de problema de DR con DE
        # 1. Obtengo la tabla de relación entre DE y EP
        tabla_de_ep_de = base_relacion_de_ep.generar_dataframe()
        # 2. Filtro las relaciones que tiene el DE
        # Filtro para obtener las relaciones activas
        tabla_relacion_activos = tabla_de_ep_de[tabla_de_ep_de['ESTADO']=="ACTIVO"]
        # Con ese ID, filtro la tabla de relacion
        tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos['ID_DE']==self.IDDE_FINAL]
        # 3. Obtengo el ID de los EP que están relacionados al DE
        # Me quedo con el vector a filtrar en forma de lista
        lista_ep = list(tabla_relacion_filtrada['ID_EP'].unique())
        # 4. Concateno los ID de los EP relacionados al DE con el ID del DR
        if len(lista_ep) > 0:
            for indice in range(len(lista_ep)):
                cod_relacion = self.IDDE_FINAL + "/" + lista_ep[indice]
                datos_insertar = [cod_relacion, self.IDDE_FINAL, lista_ep[indice], 'ACTIVO', hora_de_modificacion] 
                base_relacion_de_ep.agregar_datos(datos_insertar)
        else:
            messagebox.showinfo("¡Atención!", "El registro ha sido asociado con éxito")
        

    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

class Extremos(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_dr = id_doc
        
        # Renombramos los encabezados
        self.ep = b_ep.generar_dataframe()
        self.tabla_ep = self.ep.rename(columns={'ID_EP':'ID EXTREMO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','AGENTE CONTAMINANTE':'AGENT. CONTAMI.','COMPONENTE AMBIENTAL':'COMPONEN. AMBIE.'})
        self.tabla_deF = self.tabla_ep.loc[0:99, ['ID EXTREMO','AGENT. CONTAMI.','COMPONEN. AMBIE.','ACTIVIDAD','DEPARTAMENTO','EFA','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
        
        # Listas para desplegables
        self.listaAG = list(set(self.tabla_ep['AGENT. CONTAMI.']))
        self.listaCA = list(set(self.tabla_ep['COMPONEN. AMBIE.']))
        self.listaACT = list(set(self.tabla_ep['ACTIVIDAD']))
        self.listaDEPAR = list(set(self.tabla_ep['DEPARTAMENTO']))
        self.listaPROV = list(set(self.tabla_ep['PROVINCIA']))
        self.listaDISTR = list(set(self.tabla_ep['DISTRITO']))
        self.listaTIPOUBI = list(set(self.tabla_ep['TIPO DE UBICACION']))
        self.listaOCURR = list(set(self.tabla_ep['OCURRENCIA']))
        self.listaEFA = list(set(self.tabla_ep['EFA']))

        # Agregando logo del ospa a la ventana y título
        self.ep0 = Cuadro(self)
        self.ep0.agregar_label(0, 0,' ')
        self.ep0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        ep3 = Cuadro(self)
        ep3.agregar_titulo(2, 0, 'Búsqueda de extremos')
    
        # Armando rejilla con los filtros
        self.rejilla_ep = (

            ('L', 0, 0, 'Agente contaminante'),
            ('CXP', 0, 1, 39, self.listaAG, '', "readonly"),

            ('L', 0, 2, 'Componente ambiental'),
            ('CXP', 0, 3, 39, self.listaCA, '', "readonly"),

            ('L', 0, 4, 'Actividad'),
            ('CXP', 0, 5, 39, self.listaACT, '', "readonly"),

            ('L', 1, 0, 'Departamento'),
            ('CXP', 1, 1, 39, self.listaDEPAR, '', "readonly"),

            ('L', 1, 2, 'Provincia'),
            ('CXP', 1, 3, 39, self.listaPROV, '', "readonly"),

            ('L', 1, 4, 'Distrito'),
            ('CXP', 1, 5, 39, self.listaDISTR, '', "readonly"),

            ('L', 2, 0, 'Tipo de ubicación'),
            ('CXP', 2, 1, 39, self.listaTIPOUBI, '', "readonly"),

            ('L', 2, 2, 'Ocurrencia'),
            ('CXP', 2, 3, 39, self.listaOCURR, '', "readonly"),

            ('L', 2, 4, 'EFA'),
            ('CXE', 2, 5, 39, self.listaEFA, '', "normal"),

            ('L', 3, 0, 'Palabra clave en descripción'),
            ('EE', 3, 1)

        )
        
        # Agregando rejilla a la ventana
        self.ep1 = Cuadro(self)
        self.ep1.agregar_rejilla(self.rejilla_ep)

        # Generando rejilla para botones
        self.rejilla_ep2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_ep),
            ('B', 5, 5, 'Limpiar', self.limpiar_ep),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ep2 = Cuadro(self)
        self.ep2.agregar_rejilla(self.rejilla_ep2)
        self.frame_vitrina_ep = Cuadro(self)

        # Creando vitrina
        self.vep = Vitrina_busquedaep(self, self.tabla_deF, self.ver_ep, self.asociar_dr_de_ep, height=200, width=1230)

#----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

#----------------------------------------------------------------------
    
    def Buscar_ep(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtroep = self.ep1.obtener_lista_de_datos()
        self.AG = self.listas_filtroep[0]
        self.CA = self.listas_filtroep[1]
        self.ACTIVIDAD = self.listas_filtroep[2]
        self.DEPART = self.listas_filtroep[3]
        self.PROVI = self.listas_filtroep[4]
        self.DISTR = self.listas_filtroep[5]
        self.TIPOUBI = self.listas_filtroep[6]
        self.OCURRE = self.listas_filtroep[7]
        self.EFA = self.listas_filtroep[8]
        self.CLAVE = self.listas_filtroep[9]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.AG)>0 :
            filtro="`AGENT. CONTAMI.`=="+"'"+self.AG+"' "
    
        if len(self.CA)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`COMPONEN. AMBIE.`=="+"'"+self.CA+"' "

        if len(self.ACTIVIDAD)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ACTIVIDAD=="+"'"+self.ACTIVIDAD+"' "

        if len(self.DEPART)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"DEPARTAMENTO=="+"'"+self.DEPART+"' "

        if len(self.PROVI)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"PROVINCIA=="+"'"+self.PROVI+"' "

        if len(self.DISTR)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"DISTRITO=="+"'"+self.DISTR+"' "

        if len(self.TIPOUBI)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO DE UBICACION`=="+"'"+self.TIPOUBI+"' "

        if len(self.OCURRE)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"OCURRENCIA=="+"'"+self.OCURRE+"' "
        
        self.mostrarDatosep(filtro)       

#----------------------------------------------------------------------

    def mostrarDatosep(self, filtro):

        self.filtro0 = self.tabla_ep
        
        if len(self.EFA)>0: # Filtro por palabra clave
            self.vep.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['EFA'].str.contains(self.EFA)]
            self.Complementoep(self.filtro0)

        if len(self.CLAVE)>0: # Filtro por palabra clave
            self.vep.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['DESCRIPCION'].str.contains(self.CLAVE)]
            self.Complementoep(self.filtro0)
  
        if len(filtro)>0:

            self.vep.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementoep(self.filtro1)

        else:
            self.vep.Eliminar_vitrina()
            self.Complementoep(self.filtro0)

    #----------------------------------------------------------------------

    def Complementoep(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['ID EXTREMO','AGENT. CONTAMI.','COMPONEN. AMBIE.','ACTIVIDAD','DEPARTAMENTO','EFA','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ep.eliminar_cuadro()
            self.frame_vitrina_ep = Cuadro(self)
            self.vep = Vitrina_busquedaep(self, tabla_filtro3, self.ver_ep, self.asociar_dr_de_ep, height=200, width=1230)
        else:
            self.frame_vitrina_ep.eliminar_cuadro()
            self.frame_vitrina_ep = Cuadro(self)
            self.frame_vitrina_ep.agregar_label(1, 2, '                  0 extremos encontrados')

    #----------------------------------------------------------------------
    def limpiar_ep(self):
     
         # Eliminando campos
        self.ep1.eliminar_cuadro()
        self.vep.Eliminar_vitrina()
        self.ep2.eliminar_cuadro()
        self.frame_vitrina_ep.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.ep1 = Cuadro(self)
        self.ep1.agregar_rejilla(self.rejilla_ep)
        self.ep2 = Cuadro(self)
        self.ep2.agregar_rejilla(self.rejilla_ep2)

        self.frame_vitrina_ep = Cuadro(self)
        # Creando vitrina
        self.vep = Vitrina_busquedaep(self, self.tabla_deF, self.ver_ep, self.asociar_dr_de_ep, height=200, width=1230)

    #----------------------------------------------------------------------
    def volver(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

    #----------------------------------------------------------------------
    def ver_ep(self, x):
        """"""
        #self.x = x
        #texto_documento = 'Documento emitido: ' + x
        print("hola")
        #bde = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS_FINAL')
        #lb1 = bde.listar_datos_de_fila(self.x)
        #lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                #lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        #self.desaparecer()
        #subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                 #               nuevo=False, lista=lista_para_insertar, id_doc=x)

    #----------------------------------------------------------------------
    def asociar_dr_de_ep(self, x):
        """"""
        self.x = x

        #OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
        self.IDDE = b_de.listar_datos_de_fila(self.x)
        self.IDDE_FINAL = self.IDDE[0]

        #OBTENER EL ID USUARIO DEL DOCUMENTO RECIBIDO
        codigodr = self.cod_doc_dr
        # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
        tabla_de_codigo_dr = b_dr.generar_dataframe()
        tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == codigodr]
        id_interno_dr = tabla_codigo_de_filtrada.iloc[0,0]

        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" +  self.IDDE_FINAL

        # BUSCAR COINCIDENCIAS
        valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)

        # BUSCAR ESTADO DE ID RELACION SI EXISTE
        if valor_repetido != False:  # si hay coincidencias de ese id_relacion_doc
            tabla_de_relaciones = base_relacion_docs.generar_dataframe()
            tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_doc]
            estado_rela = tabla_relaciones_filtrada.iloc[0,3]

        hora_de_modificacion = str(dt.datetime.now())

        if valor_repetido != True:
            
            # GUARDAR RELACION
            b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'RELACION_DOCS')

            # Pestaña 1: Código Único
            datos_insertar = [id_relacion_doc,id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion]
            b0.agregar_datos(datos_insertar)
            datos_a_cargar_hist = [id_relacion_doc, id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
            base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
            messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        else:
            if estado_rela == 'ACTIVO':
                messagebox.showinfo("Error", "Ya se encuentra asociado")
            else:
                datos_iniciales = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
                hora = str(dt.datetime.now())
                datos_a_cargar_hist = datos_iniciales + [hora]
                estado_a_sobreescribir = 'ACTIVO'
                datos_a_cargar_hist[3] = estado_a_sobreescribir
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 5, hora)
                base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
                base_relacion_d_hist.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        
        # Asociación de extremos de problema de DR con DE
        # 1. Obtengo la tabla de relación entre DE y EP
        tabla_de_ep_de = base_relacion_de_ep.generar_dataframe()
        # 2. Filtro las relaciones que tiene el DE
        # Filtro para obtener las relaciones activas
        tabla_relacion_activos = tabla_de_ep_de[tabla_de_ep_de['ESTADO']=="ACTIVO"]
        # Con ese ID, filtro la tabla de relacion
        tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos['ID_DE']==self.IDDE_FINAL]
        # 3. Obtengo el ID de los EP que están relacionados al DE
        # Me quedo con el vector a filtrar en forma de lista
        lista_ep = list(tabla_relacion_filtrada['ID_EP'].unique())
        # 4. Concateno los ID de los EP relacionados al DE con el ID del DR
        if len(lista_ep) > 0:
            for indice in range(len(lista_ep)):
                cod_relacion = self.IDDE_FINAL + "/" + lista_ep[indice]
                datos_insertar = [cod_relacion, self.IDDE_FINAL, lista_ep[indice], 'ACTIVO', hora_de_modificacion] 
                base_relacion_de_ep.agregar_datos(datos_insertar)
        else:
            messagebox.showinfo("¡Atención!", "El registro ha sido asociado con éxito")
        

    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

class Macroproblemas(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_mc = id_doc
        
        # Renombramos los encabezados
        self.mc = b_mc.generar_dataframe()
        self.tabla_mc = self.mc.rename(columns={'ID_MC':'ID MACROPROBLEMA','COD_MC':'COD. MACROPROBLEMA','NOMBRE_DEL_PROBLEMA':'NOMBRE PROBLEMA','TIPO_DE_CAUSA':'TIPO CAUSA','TIPO_DE_AFECTACION':'TIPO AFECTACION','FECHA_DE_CREACION':'FECHA CREACION'})
        self.tabla_mcF = self.tabla_mc.loc[0:99, ['ID MACROPROBLEMA','COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','TIPO CAUSA','TIPO AFECTACION','ESTADO','DESCRIPCION']]
        
        # Listas para desplegables
        self.listaTC = list(set(self.tabla_mc['TIPO CAUSA']))
        self.listaTA = list(set(self.tabla_mc['TIPO AFECTACION']))
        self.listaestado = list(set(self.tabla_mc['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        self.mc0 = Cuadro(self)
        self.mc0.agregar_label(0, 0,' ')
        self.mc0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        mc3 = Cuadro(self)
        mc3.agregar_titulo(2, 0, 'Búsqueda de macroproblemas')
    
        # Armando rejilla con los filtros
        self.rejilla_mc = (

            ('L', 0, 0, 'Código de Macroproblema'),
            ('EE', 0, 1),
            
            ('L', 1, 0, 'Tipo de causa'),
            ('CXP', 1, 1, 39, self.listaTC, '', "readonly"),

            ('L', 0, 2, 'Tipo de afectación'),
            ('CXP', 0, 3, 39, self.listaTA, '', "readonly"),

            ('L', 1, 2, 'Estado'),
            ('CXP', 1, 3, 39, self.listaestado, '', "readonly"),

            ('L', 2, 0, 'Nombre del problema'),
            ('EE', 2, 1),

            ('L', 2, 2, 'Palabra clave en descripción'),
            ('EE', 2, 3),
        )
        
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mc)

        # Generando rejilla para botones
        self.rejilla_mc2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_mc),
            ('B', 5, 5, 'Limpiar', self.limpiar_mc),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mc2)
        self.frame_vitrina_mc = Cuadro(self)

        # Creando vitrina
        self.vmc = Vitrina_busqueda(self, self.tabla_mcF, self.ver_mc, self.funcion_de_asociar_mc, height=200, width=1080)

#----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

#----------------------------------------------------------------------
    
    def Buscar_mc(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtromc = self.mc1.obtener_lista_de_datos()
        self.CODIGO = self.listas_filtromc[0]
        self.TC = self.listas_filtromc[1]
        self.TA = self.listas_filtromc[2]
        self.ESTADO = self.listas_filtromc[3]
        self.NOMBRE = self.listas_filtromc[4]
        self.DESCRIP = self.listas_filtromc[5]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.CODIGO)>0 :
            filtro="`COD. MACROPROBLEMA`=="+"'"+self.CODIGO+"' "
    
        if len(self.TC)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO CAUSA`=="+"'"+self.TC+"' "

        if len(self.TA)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO AFECTACION`=="+"'"+self.TA+"' "

        if len(self.ESTADO)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESTADO=="+"'"+self.ESTADO+"' "
        
        self.mostrarDatosmc(filtro)       

#----------------------------------------------------------------------

    def mostrarDatosmc(self, filtro):

        self.filtro0 = self.tabla_mc
        
        if len(self.NOMBRE)>0: # Filtro por palabra clave
            self.vmc.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['NOMBRE PROBLEMA'].str.contains(self.NOMBRE)]
            self.Complementomc(self.filtro0)

        if len(self.DESCRIP)>0: # Filtro por palabra clave
            self.vmc.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['DESCRIPCION'].str.contains(self.DESCRIP)]
            self.Complementomc(self.filtro0)
  
        if len(filtro)>0:

            self.vmc.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementomc(self.filtro1)

        else:
            self.vmc.Eliminar_vitrina()
            self.Complementomc(self.filtro0)

    #----------------------------------------------------------------------

    def Complementomc(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['ID MACROPROBLEMA','COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','TIPO CAUSA','TIPO AFECTACION','ESTADO','DESCRIPCION']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_mc.eliminar_cuadro()
            self.frame_vitrina_mc = Cuadro(self)
            self.vmc = Vitrina_busqueda(self, tabla_filtro3, self.ver_mc, self.funcion_de_asociar_mc, height=200, width=1080)
        else:
            self.frame_vitrina_mc.eliminar_cuadro()
            self.frame_vitrina_mc = Cuadro(self)
            self.frame_vitrina_mc.agregar_label(1, 2, '                  0 macroproblemas encontrados')

    #----------------------------------------------------------------------
    def limpiar_mc(self):
     
         # Eliminando campos
        self.mc1.eliminar_cuadro()
        self.vmc.Eliminar_vitrina()
        self.mc2.eliminar_cuadro()
        self.frame_vitrina_mc.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mc)
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mc2)

        self.frame_vitrina_mc = Cuadro(self)
        # Creando vitrina
        self.vmc = Vitrina_busqueda(self, self.tabla_mcF, self.ver_mc, self.funcion_de_asociar_mc, height=200, width=1080)

    #----------------------------------------------------------------------
    def volver(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

    #----------------------------------------------------------------------
    def ver_mc(self, x):
        """"""
        #self.x = x
        #texto_documento = 'Documento emitido: ' + x
        print("hola")
        #bde = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS_FINAL')
        #lb1 = bde.listar_datos_de_fila(self.x)
        #lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                #lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        #self.desaparecer()
        #subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                 #               nuevo=False, lista=lista_para_insertar, id_doc=x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_mc(self, x):
        """"""
        print("hola")

class Administrados(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_ad = id_doc
        
        # Renombramos los encabezados
        self.ad = b_ad.generar_dataframe()
        self.tabla_ad = self.ad.rename(columns={'ID_AD':'ID ADMINISTRADO','NOMBRE_O_RAZON_SOCIAL':'NOMBRE / RAZON SOCIAL','CATEGORÍA':'TIPO','DNI_RUC':'DNI / RUC','INCUMPLIMIENTO_1':'INCUMPLIMIENTO 1','INCUMPLIMIENTO_2':'INCUMPLIMIENTO 2'})
        self.tabla_adF = self.tabla_ad.loc[0:99, ['ID ADMINISTRADO','NOMBRE / RAZON SOCIAL','TIPO','DNI / RUC','INCUMPLIMIENTO 1','INCUMPLIMIENTO 2']]
        
        # Listas para desplegables
        self.listaAD = list(set(self.tabla_ad['NOMBRE / RAZON SOCIAL']))
        self.listaTIPO= list(set(self.tabla_ad['TIPO']))

        # Agregando logo del ospa a la ventana y título
        self.ad0 = Cuadro(self)
        self.ad0.agregar_label(0, 0,' ')
        self.ad0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        ad3 = Cuadro(self)
        ad3.agregar_titulo(2, 0, 'Búsqueda de administrados')
    
        # Armando rejilla con los filtros
        self.rejilla_ad = (

            ('L', 0, 0, 'Administrado'),
            ('CXP', 0, 1, 39, self.listaAD, '', "normal"),

            ('L', 1, 0, 'Tipo'),
            ('CXP', 1, 1, 39, self.listaTIPO, '', "normal"),

            ('L', 0, 2, 'DNI / RUC'),
            ('E', 0, 3),

            ('L', 1, 2, 'Palabra clave en incumplimiento'),
            ('E', 1, 3)
        )
        
        # Agregando rejilla a la ventana
        self.ad1 = Cuadro(self)
        self.ad1.agregar_rejilla(self.rejilla_ad)

        # Generando rejilla para botones
        self.rejilla_ad2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_ad),
            ('B', 5, 5, 'Limpiar', self.limpiar_ad),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ad2 = Cuadro(self)
        self.ad2.agregar_rejilla(self.rejilla_ad2)
        self.frame_vitrina_ad = Cuadro(self)

        # Creando vitrina
        self.vad = Vitrina_busqueda(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, height=200, width=850)

#----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = vista_dr.inicio_app_OSPA(self, 400, 400, "Inicio")

#----------------------------------------------------------------------
    
    def Buscar_ad(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtroad = self.ad1.obtener_lista_de_datos()
        self.ADMINI = self.listas_filtroad[0]
        self.Tipo = self.listas_filtroad[1]
        self.ruc = self.listas_filtroad[2]
        self.incum = self.listas_filtroad[3]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.Tipo)>0 :
            filtro="TIPO=="+"'"+self.Tipo+"' "
    
        if len(self.ruc)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`DNI / RUC`=="+"'"+self.ruc+"' "
        
        self.mostrarDatosad(filtro)       

#----------------------------------------------------------------------

    def mostrarDatosad(self, filtro):

        self.filtro0 = self.tabla_ad
        
        if len(self.ADMINI)>0: # Filtro por palabra clave
            self.vad.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['NOMBRE / RAZON SOCIAL'].str.contains(self.ADMINI)]
            self.Complementoad(self.filtro0)

        if len(self.incum)>0: # Filtro por palabra clave
            self.vad.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['INCUMPLIMIENTO 1'].str.contains(self.incum)]
            self.Complementoad(self.filtro0)
  
        if len(filtro)>0:

            self.vad.Eliminar_vitrina()
            self.filtro0['DNI / RUC']=self.filtro0['DNI / RUC'].apply(str)
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementoad(self.filtro1)

        else:
            self.vad.Eliminar_vitrina()
            self.Complementoad(self.filtro0)

    #----------------------------------------------------------------------

    def Complementoad(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['ID ADMINISTRADO','NOMBRE / RAZON SOCIAL','TIPO','DNI / RUC','INCUMPLIMIENTO 1','INCUMPLIMIENTO 2']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ad.eliminar_cuadro()
            self.frame_vitrina_ad = Cuadro(self)
            self.vad = Vitrina_busqueda(self, tabla_filtro3, self.ver_ad, self.funcion_de_asociar_ad, height=200, width=850)
        else:
            self.frame_vitrina_ad.eliminar_cuadro()
            self.frame_vitrina_ad = Cuadro(self)
            self.frame_vitrina_ad.agregar_label(1, 2, '                  0 administrados encontrados')

    #----------------------------------------------------------------------
    def limpiar_ad(self):
     
         # Eliminando campos
        self.ad1.eliminar_cuadro()
        self.vad.Eliminar_vitrina()
        self.ad2.eliminar_cuadro()
        self.frame_vitrina_ad.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.ad1 = Cuadro(self)
        self.ad1.agregar_rejilla(self.rejilla_ad)
        self.ad2 = Cuadro(self)
        self.ad2.agregar_rejilla(self.rejilla_ad2)

        self.frame_vitrina_ad = Cuadro(self)
        # Creando vitrina
        self.vad = Vitrina_busqueda(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, height=200, width=850)

    #----------------------------------------------------------------------
    def volver(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

    #----------------------------------------------------------------------
    def ver_ad(self, x):
        """"""
        #self.x = x
        #texto_documento = 'Documento emitido: ' + x
        print("hola")
        #bde = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS_FINAL')
        #lb1 = bde.listar_datos_de_fila(self.x)
        #lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                #lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        #self.desaparecer()
        #subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                 #               nuevo=False, lista=lista_para_insertar, id_doc=x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_ad(self, x):
        """"""
        print("hola")

class Pendientes_jefe_firma(Ventana):
    """"""

#----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_dr = id_doc

        # Generamos el dataframe a filtrar
        self.tabla_inicial = b_de.generar_dataframe()
        self.tabla_inicial = self.tabla_inicial[self.tabla_inicial['FECHA_FIRMA']=='']
        self.tabla_0_pfirma = self.tabla_inicial.rename(columns={'COD_DE':'DOC EMITIDO','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
        self.tabla_pfirmaF = self.tabla_0_pfirma.loc[0:99, ['DOC EMITIDO','DESTINATARIO','HT SALIDA','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.categoria = list(set(self.tabla_0_pfirma['CATEGORIA']))
        self.destinatario = list(set(self.tabla_0_pfirma['DESTINATARIO']))
        self.tipodocemitpfirma = list(set(self.tabla_0_pfirma['TIPO DOC']))
        self.especialista = list(set(self.tabla_0_pfirma['ESPECIALISTA']))

        # Agregando logo del ospa a la ventana y título
        self.pfirma0 = Cuadro(self)
        self.pfirma0.agregar_label(0, 0,' ')
        self.pfirma0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        pfirma2 = Cuadro(self)
        pfirma2.agregar_titulo(2, 0, 'Documentos pendientes de firma')

        # Armando rejilla con los filtros

        self.rejilla_pfirma = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 39, self.categoria, '', 'readonly'),

            ('L', 1, 0, 'Nro registro Siged'),
            ('EE', 1, 1),

            ('L', 0, 2, 'Destinatario'),
            ('CXE', 0, 3, 39, self.destinatario, '', 'normal'),

            ('L', 1, 2, 'Especialista'),
            ('CXP', 1, 3, 39, self.especialista, '', 'readonly'),

            ('L', 2, 0, 'Tipo de documento'),
            ('CXP', 2, 1, 39, self.tipodocemitpfirma, '', 'readonly'),

            ('L', 2, 2, 'Nro de documento'),
            ('EE', 2, 3)

        )
        
        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)

        # Generando rejilla para botones
        self.rejilla_2_pfirma = (
            ('B', 5, 4, 'Buscar', self.Buscar_pfirma),
            ('B', 5, 5, 'Limpiar', self.limpiar_pfirma),
            ('B', 5, 6, 'Volver', self.volver_pfirma),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)

        # Creando vitrina
        self.vpfirma = Vitrina_pendientes_jefe_firma(self, self.tabla_pfirmaF, self.ver_pfirma, self.funcion_de_asociar_pfirma, height=200, width=1050)

    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

    #----------------------------------------------------------------------

    def Buscar_pfirma(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtropfirma = self.pfirma1.obtener_lista_de_datos()
        self.decatepfirma = self.listas_filtropfirma[0] #
        self.htpfirma = self.listas_filtropfirma[1]
        self.destinpfirma = self.listas_filtropfirma[2]
        self.espepfirma = self.listas_filtropfirma[3]
        self.tipodocpfirma = self.listas_filtropfirma[4] #
        self.docpfirma = self.listas_filtropfirma[5]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.decatepfirma)>0 :
            filtro="CATEGORIA=="+"'"+self.decatepfirma+"' "
    
        if len(self.tipodocpfirma)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO DOC`=="+"'"+self.tipodocpfirma+"' "
        
        self.mostrarDatospfirma(filtro)

    #----------------------------------------------------------------------

    def mostrarDatospfirma(self, filtro):

        self.filtro0 = self.tabla_0_pfirma
        
        if len(self.htpfirma)>0: # Filtro por palabra clave
            self.vpfirma.Eliminar_vitrina()
            self.filtro0['HT SALIDA']=self.filtro0['HT SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT SALIDA'].str.contains(self.htpfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.docpfirma)>0: # Filtro por palabra clave
            self.vpfirma.Eliminar_vitrina()
            self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOCUMENTO'].str.contains(self.docpfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.destinpfirma)>0: # Filtro por palabra clave
            self.vpfirma.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.destinpfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.espepfirma)>0: # Filtro por palabra clave
            self.vpfirma.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['ESPECIALISTA'].str.contains(self.espepfirma)]
            self.Complementopfirma(self.filtro0)
  
        if len(filtro)>0:

            self.vpfirma.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopfirma(self.filtro1)

        else:
            self.vpfirma.Eliminar_vitrina()
            self.Complementopfirma(self.filtro0)

    #----------------------------------------------------------------------
    def Complementopfirma(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['DOC EMITIDO','DESTINATARIO','HT SALIDA','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_pfirma.eliminar_cuadro()
            self.frame_vitrina_pfirma = Cuadro(self)
            self.vpfirma = Vitrina_pendientes_jefe_firma(self, tabla_filtro3, self.ver_pfirma, self.funcion_de_asociar_pfirma, height=200, width=1050)
        else:
            self.frame_vitrina_pfirma.eliminar_cuadro()
            self.frame_vitrina_pfirma = Cuadro(self)
            self.frame_vitrina_pfirma.agregar_label(1, 2, '                  0 documentos encontrados')

    #----------------------------------------------------------------------

    def limpiar_pfirma(self):

        # Eliminando campos
        self.pfirma1.eliminar_cuadro()
        self.vpfirma.Eliminar_vitrina()
        self.pfirma15.eliminar_cuadro()
        self.frame_vitrina_pfirma.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)
        # Creando vitrina
        self.vpfirma = Vitrina_pendientes_jefe_firma(self, self.tabla_pfirmaF, self.ver_pfirma, self.funcion_de_asociar_pfirma, height=200, width=1050)

    #----------------------------------------------------------------------

    def volver_pfirma(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

    #----------------------------------------------------------------------
    def ver_pfirma(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento emitido: ' + x

        lb1 = b_de.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                                nuevo=False, lista=lista_para_insertar, id_doc=x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_pfirma(self, x):
        """"""
        self.x = x

        #OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
        self.bdee = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS')
        self.IDDE = self.bdee.listar_datos_de_fila(self.x)
        self.IDDE_FINAL = self.IDDE[0]

        #OBTENER EL ID USUARIO DEL DOCUMENTO RECIBIDO
        codigodr = self.cod_doc_dr
        # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
        tabla_de_codigo_dr = b_dr.generar_dataframe()
        tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == codigodr]
        id_interno_dr = tabla_codigo_de_filtrada.iloc[0,0]

        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" +  self.IDDE_FINAL

        # BUSCAR COINCIDENCIAS
        valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)

        # BUSCAR ESTADO DE ID RELACION SI EXISTE
        if valor_repetido != False:  # si hay coincidencias de ese id_relacion_doc
            tabla_de_relaciones = base_relacion_docs.generar_dataframe()
            tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_doc]
            estado_rela = tabla_relaciones_filtrada.iloc[0,3]

        hora_de_modificacion = str(dt.datetime.now())

        if valor_repetido != True:
            
            # GUARDAR RELACION
            b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'RELACION_DOCS')

            # Pestaña 1: Código Único
            datos_insertar = [id_relacion_doc,id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion]
            b0.agregar_datos(datos_insertar)
            datos_a_cargar_hist = [id_relacion_doc, id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
            base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
            messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        else:
            if estado_rela == 'ACTIVO':
                messagebox.showinfo("Error", "Ya se encuentra asociado")
            else:
                datos_iniciales = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
                hora = str(dt.datetime.now())
                datos_a_cargar_hist = datos_iniciales + [hora]
                estado_a_sobreescribir = 'ACTIVO'
                datos_a_cargar_hist[3] = estado_a_sobreescribir
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 5, hora)
                base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
                base_relacion_d_hist.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        
        

    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False
    
class Pendientes_jefe_asignar(Ventana):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_jpa = id_doc

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_dr.generar_dataframe()
        self.tabla_inicial1 = self.tabla_inicial0[self.tabla_inicial0['TIPO_RESPUESTA']!='Si']
        self.tabla_inicial2 = self.tabla_inicial1[self.tabla_inicial1['ESPECIALISTA']=='']
        #self.tabla_inicial2['F_ING_SEFA'] = pd.to_datetime(self.tabla_inicial2['F_ING_SEFA'], dayfirst=True)
        #self.tabla_inicial = self.tabla_inicial2.sort_values(["F_ING_SEFA"])
        self.tabla_jpa = self.tabla_inicial2.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_jpaF = self.tabla_jpa.loc[0:99, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','ASUNTO']]
 
        # Información para las listas desplegables
        self.jpatipodoc = list(set(self.tabla_jpa['TIPO DOC']))
        self.jparemitente = list(set(self.tabla_jpa['REMITENTE']))

        # Agregando logo del ospa a la ventana y título
        self.jpa0 = Cuadro(self)
        self.jpa0.agregar_label(0,0,' ')
        self.jpa0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)
        jpa2 = Cuadro(self)
        jpa2.agregar_titulo(2, 0, 'Documentos pendientes de asignar')

        # Armando rejilla con los filtros
        self.rejilla_jpa = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 39, self.jpatipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 39, self.jparemitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3)

        )

        # Agregando rejilla a la ventana
        self.jpa1 = Cuadro(self)
        self.jpa1.agregar_rejilla(self.rejilla_jpa)

        # Generando rejilla para botones
        self.rejilla_jpa2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_jpa),
            ('B', 5, 5, 'Limpiar', self.limpiar_jpa),
            ('B', 5, 6, 'Volver', self.volver_jpa),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.jpa15 = Cuadro(self)
        self.jpa15.agregar_rejilla(self.rejilla_jpa2)

        self.frame_vitrina_jpa = Cuadro(self)

        # Creando vitrina
        self.vjpa = Vitrina_pendientes_jefe_firma(self, self.tabla_jpaF, self.ver_jpa, 
                                   self.funcion_de_asociar_jpa, height=200, width=800)
    
    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

    #----------------------------------------------------------------------

    def Buscar_jpa(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro_jpa = self.jpa1.obtener_lista_de_datos()
        self.htjpa = self.listas_filtro_jpa[0]
        self.tipodocjpa = self.listas_filtro_jpa[1]
        self.remitentejpa = self.listas_filtro_jpa[2]
        self.nrodocjpa = self.listas_filtro_jpa[3]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodocjpa)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodocjpa+"' "
        
        self.mostrarDatosjpa(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatosjpa(self, filtro):

        self.filtro0 = self.tabla_jpa
        
        if len(self.remitentejpa)>0: # Filtro por palabra clave
            self.vjpa.Eliminar_vitrina()
            self.filtro0 = self.tabla_jpa[self.tabla_jpa['REMITENTE'].str.contains(self.remitentejpa)]
            self.Complementojpa(self.filtro0)

        if len(self.nrodocjpa)>0: # Filtro por palabra clave
            self.vjpa.Eliminar_vitrina()
            self.filtro0['NRO DOC']=self.filtro0['NRO DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOC'].str.contains(self.nrodocjpa)]
            self.Complementojpa(self.filtro0)

        if len(self.htjpa)>0: # Filtro por palabra clave
            self.vjpa.Eliminar_vitrina()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.htjpa)]
            self.Complementojpa(self.filtro0)

        if len(filtro)>0:

            self.vjpa.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementojpa(self.filtro1)

        else:
            self.vjpa.Eliminar_vitrina()
            self.Complementojpa(self.filtro0)

    #----------------------------------------------------------------------

    def Complementojpa(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','ASUNTO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_jpa.eliminar_cuadro()
            self.frame_vitrina_jpa = Cuadro(self)
            self.vjpa = Vitrina_pendientes_jefe_firma(self, tabla_filtro3, self.ver_jpa, 
                                   self.funcion_de_asociar_jpa, height=200, width=800)
        else:
            self.frame_vitrina_jpa.eliminar_cuadro()
            self.frame_vitrina_jpa = Cuadro(self)
            self.frame_vitrina_jpa.agregar_label(1, 2, '                  0 documentos encontrados')

    #----------------------------------------------------------------------
    def limpiar_jpa(self):
        
        # Eliminando campos
        self.jpa1.eliminar_cuadro()
        self.vjpa.Eliminar_vitrina()
        self.jpa15.eliminar_cuadro()
        self.frame_vitrina_jpa.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.jpa1 = Cuadro(self)
        self.jpa1.agregar_rejilla(self.rejilla_jpa)
        self.jpa15 = Cuadro(self)
        self.jpa15.agregar_rejilla(self.rejilla_jpa2)
        self.frame_vitrina_jpa = Cuadro(self)
        # Creando vitrina
        self.vjpa = Vitrina_pendientes_jefe_firma(self, self.tabla_jpaF, self.ver_jpa, 
                                   self.funcion_de_asociar_jpa, height=200, width=800)

    #----------------------------------------------------------------------

    def volver_jpa(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

    #----------------------------------------------------------------------
    def ver_jpa(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x
        #print(x)
        lb1 = b_dr.listar_datos_de_fila(self.x)
        # PARA EL CASO DE ESTA PANTALLA SOLO LLEVARA LOS DATOS INGRESADOS HASTA APORTE DEL DOC O ASUNTO (CAMPOS OBLIGATORIO)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8]]
        
        self.desaparecer()
        subframe = vista_dr.Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                                lista=lista_para_insertar, id_doc = x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_jpa(self, x):
        """"""
        print('hola')

class Pendientes_por_reiterar(Ventana):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_ppr = id_doc

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_de.generar_dataframe()
        self.tabla_inicial1 = self.tabla_inicial0.query("ESTADO_DOCE=='Enviar reiterativo' or ESTADO_DOCE=='Eviar OCI'")
        self.tabla_ppr = self.tabla_inicial1.rename(columns={'COD_DE':'DOC EMITIDO','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
        self.tabla_pprF = self.tabla_ppr.loc[0:99, ['DOC EMITIDO','DESTINATARIO','HT SALIDA','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.categoriappr = list(set(self.tabla_ppr['CATEGORIA']))
        self.destinatarioppr = list(set(self.tabla_ppr['DESTINATARIO']))
        self.tipodocemitpfirmappr = list(set(self.tabla_ppr['TIPO DOC']))
        self.especialistappr = list(set(self.tabla_ppr['ESPECIALISTA']))

        # Agregando logo del ospa a la ventana y título
        self.ppr0 = Cuadro(self)
        self.ppr0.agregar_label(0,0,' ')
        self.ppr0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)
        ppr2 = Cuadro(self)
        ppr2.agregar_titulo(2, 0, 'Documentos pendientes de reiterar/comunicación al OCI')

        self.rejilla_ppr = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 39, self.categoriappr, '', 'readonly'),

            ('L', 1, 0, 'Nro registro Siged'),
            ('EE', 1, 1),

            ('L', 0, 2, 'Destinatario'),
            ('CXE', 0, 3, 39, self.destinatarioppr, '', 'normal'),

            ('L', 1, 2, 'Especialista'),
            ('CXP', 1, 3, 39, self.especialistappr, '', 'readonly'),

            ('L', 2, 0, 'Tipo de documento'),
            ('CXP', 2, 1, 39, self.tipodocemitpfirmappr, '', 'readonly'),

            ('L', 2, 2, 'Nro de documento'),
            ('EE', 2, 3)

        )
        
        # Agregando rejilla a la ventana
        self.ppr1 = Cuadro(self)
        self.ppr1.agregar_rejilla(self.rejilla_ppr)

        # Generando rejilla para botones
        self.rejilla_2_ppr = (
            ('B', 5, 4, 'Buscar', self.Buscar_ppr),
            ('B', 5, 5, 'Limpiar', self.limpiar_ppr),
            ('B', 5, 6, 'Volver', self.volver_ppr),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ppr15 = Cuadro(self)
        self.ppr15.agregar_rejilla(self.rejilla_2_ppr)
        self.frame_vitrina_ppr = Cuadro(self)

        # Creando vitrina
        self.vppr = Vitrina_pendientes_jefe_firma(self, self.tabla_pprF, self.ver_ppr, self.funcion_de_asociar_ppr, height=200, width=1050)

    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

    #----------------------------------------------------------------------

    def Buscar_ppr(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtroppr = self.ppr1.obtener_lista_de_datos()
        self.decateppr = self.listas_filtroppr[0] #
        self.htppr = self.listas_filtroppr[1]
        self.destinppr = self.listas_filtroppr[2]
        self.espeppr = self.listas_filtroppr[3]
        self.tipodocppr = self.listas_filtroppr[4] #
        self.docppr = self.listas_filtroppr[5]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.decateppr)>0 :
            filtro="CATEGORIA=="+"'"+self.decateppr+"' "
    
        if len(self.tipodocppr)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO DOC`=="+"'"+self.tipodocppr+"' "
        
        self.mostrarDatosppr(filtro)

    #----------------------------------------------------------------------

    def mostrarDatosppr(self, filtro):

        self.filtro0 = self.tabla_ppr
        
        if len(self.htppr)>0: # Filtro por palabra clave
            self.vprr.Eliminar_vitrina()
            self.filtro0['HT SALIDA']=self.filtro0['HT SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT SALIDA'].str.contains(self.htppr)]
            self.Complementoppr(self.filtro0)

        if len(self.docppr)>0: # Filtro por palabra clave
            self.vppr.Eliminar_vitrina()
            self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOCUMENTO'].str.contains(self.docppr)]
            self.Complementoppr(self.filtro0)

        if len(self.destinppr)>0: # Filtro por palabra clave
            self.vppr.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.destinppr)]
            self.Complementoppr(self.filtro0)

        if len(self.espeppr)>0: # Filtro por palabra clave
            self.vppr.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['ESPECIALISTA'].str.contains(self.espeppr)]
            self.Complementoppr(self.filtro0)
  
        if len(filtro)>0:

            self.vppr.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementoppr(self.filtro1)

        else:
            self.vppr.Eliminar_vitrina()
            self.Complementoppr(self.filtro0)

    #----------------------------------------------------------------------
    def Complementoppr(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['DOC EMITIDO','DESTINATARIO','HT SALIDA','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ppr.eliminar_cuadro()
            self.frame_vitrina_ppr = Cuadro(self)
            self.vppr = Vitrina_pendientes_jefe_firma(self, tabla_filtro3, self.ver_ppr, self.funcion_de_asociar_ppr, height=200, width=1050)
        else:
            self.frame_vitrina_ppr.eliminar_cuadro()
            self.frame_vitrina_ppr = Cuadro(self)
            self.frame_vitrina_ppr.agregar_label(1, 2, '                  0 documentos encontrados')

    #----------------------------------------------------------------------

    def limpiar_ppr(self):

        # Eliminando campos
        self.ppr1.eliminar_cuadro()
        self.vppr.Eliminar_vitrina()
        self.ppr15.eliminar_cuadro()
        self.frame_vitrina_ppr.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.ppr1 = Cuadro(self)
        self.ppr1.agregar_rejilla(self.rejilla_ppr)
        self.ppr15 = Cuadro(self)
        self.ppr15.agregar_rejilla(self.rejilla_2_ppr)
        self.frame_vitrina_ppr = Cuadro(self)
        # Creando vitrina
        self.vppr = Vitrina_pendientes_jefe_firma(self, self.tabla_pprF, self.ver_ppr, self.funcion_de_asociar_ppr, height=200, width=1050)

    #----------------------------------------------------------------------

    def volver_ppr(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

    #----------------------------------------------------------------------
    def ver_ppr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento emitido: ' + x

        lb1 = b_de.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                                nuevo=False, lista=lista_para_insertar, id_doc=x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_ppr(self, x):
        """"""
        self.x = x

        #OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
        self.bdee = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS')
        self.IDDE = self.bdee.listar_datos_de_fila(self.x)
        self.IDDE_FINAL = self.IDDE[0]

        #OBTENER EL ID USUARIO DEL DOCUMENTO RECIBIDO
        codigodr = self.cod_doc_ppr
        # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
        tabla_de_codigo_dr = b_dr.generar_dataframe()
        tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == codigodr]
        id_interno_dr = tabla_codigo_de_filtrada.iloc[0,0]

        # Definición de ID de relación
        id_relacion_doc = id_interno_dr + "/" +  self.IDDE_FINAL

        # BUSCAR COINCIDENCIAS
        valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)

        # BUSCAR ESTADO DE ID RELACION SI EXISTE
        if valor_repetido != False:  # si hay coincidencias de ese id_relacion_doc
            tabla_de_relaciones = base_relacion_docs.generar_dataframe()
            tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_doc]
            estado_rela = tabla_relaciones_filtrada.iloc[0,3]

        hora_de_modificacion = str(dt.datetime.now())

        if valor_repetido != True:
            
            # GUARDAR RELACION
            b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'RELACION_DOCS')

            # Pestaña 1: Código Único
            datos_insertar = [id_relacion_doc,id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion]
            b0.agregar_datos(datos_insertar)
            datos_a_cargar_hist = [id_relacion_doc, id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
            base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
            messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        else:
            if estado_rela == 'ACTIVO':
                messagebox.showinfo("Error", "Ya se encuentra asociado")
            else:
                datos_iniciales = base_relacion_docs.listar_datos_de_fila(id_relacion_doc)
                hora = str(dt.datetime.now())
                datos_a_cargar_hist = datos_iniciales + [hora]
                estado_a_sobreescribir = 'ACTIVO'
                datos_a_cargar_hist[3] = estado_a_sobreescribir
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                base_relacion_docs.cambiar_un_dato_de_una_fila(id_relacion_doc, 5, hora)
                base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
                base_relacion_d_hist.cambiar_un_dato_de_una_fila(id_relacion_doc, 4, estado_a_sobreescribir)
                messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        
        

    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

class Pendientes_eq1_trabajar(Ventana):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_doc = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_peq1t = id_doc

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_dr.generar_dataframe()
        self.tabla_inicial1 = self.tabla_inicial0[self.tabla_inicial0['ESPECIALISTA']!='']
        self.tabla_peq1t = self.tabla_inicial1.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_peq1tF = self.tabla_peq1t.loc[0:99, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','INDICACION','ASUNTO']]
 
        # Información para las listas desplegables
        self.peq1ttipodoc = list(set(self.tabla_peq1tF['TIPO DOC']))
        self.peq1tremitente = list(set(self.tabla_peq1tF['REMITENTE']))

        # Agregando logo del ospa a la ventana y título
        self.peq1t0 = Cuadro(self)
        self.peq1t0.agregar_label(0,0,' ')
        self.peq1t0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)
        peq1t2 = Cuadro(self)
        peq1t2.agregar_titulo(2, 0, 'Documentos pendientes de trabajar - Equipo 1')

        # Armando rejilla con los filtros
        self.rejilla_peq1t = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 39, self.peq1ttipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 39, self.peq1tremitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3)

        )

        # Agregando rejilla a la ventana
        self.peq1t1 = Cuadro(self)
        self.peq1t1.agregar_rejilla(self.rejilla_peq1t)

        # Generando rejilla para botones
        self.rejilla_peq1t2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_peq1t),
            ('B', 5, 5, 'Limpiar', self.limpiar_peq1t),
            ('B', 5, 6, 'Volver', self.volver_peq1t),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.peq1t15 = Cuadro(self)
        self.peq1t15.agregar_rejilla(self.rejilla_peq1t2)

        self.frame_vitrina_peq1t = Cuadro(self)

        # Creando vitrina 
        self.vpeq1t = Vitrina_pendientes_jefe_firma(self, self.tabla_peq1tF, self.ver_peq1t, 
                                   self.funcion_de_asociar_peq1t, height=200, width=800)
    
    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")

    #----------------------------------------------------------------------

    def Buscar_peq1t(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro_peq1t = self.peq1t1.obtener_lista_de_datos()
        self.htpeq1t = self.listas_filtro_peq1t[0]
        self.tipodocpeq1t = self.listas_filtro_peq1t[1]
        self.remitentepeq1t = self.listas_filtro_peq1t[2]
        self.nrodocpeq1t = self.listas_filtro_peq1t[3]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodocpeq1t)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodocpeq1t+"' "
        
        self.mostrarDatospeq1t(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatospeq1t(self, filtro):

        self.filtro0 = self.tabla_peq1t
        
        if len(self.remitentepeq1t)>0: # Filtro por palabra clave
            self.vpeq1t.Eliminar_vitrina()
            self.filtro0 = self.tabla_peq1t[self.tabla_peq1t['REMITENTE'].str.contains(self.remitentepeq1t)]
            self.Complementopeq1t(self.filtro0)

        if len(self.nrodocpeq1t)>0: # Filtro por palabra clave
            self.vpeq1t.Eliminar_vitrina()
            self.filtro0['NRO DOC']=self.filtro0['NRO DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOC'].str.contains(self.nrodocpeq1t)]
            self.Complementopeq1t(self.filtro0)

        if len(self.htpeq1t)>0: # Filtro por palabra clave
            self.vpeq1t.Eliminar_vitrina()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.htpeq1t)]
            self.Complementopeq1t(self.filtro0)

        if len(filtro)>0:

            self.vpeq1t.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopeq1t(self.filtro1)

        else:
            self.vpeq1t.Eliminar_vitrina()
            self.Complementopeq1t(self.filtro0)

    #----------------------------------------------------------------------

    def Complementopeq1t(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','INDICACION','ASUNTO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_peq1t.eliminar_cuadro()
            self.frame_vitrina_peq1t = Cuadro(self)
            self.vpeq1t = Vitrina_pendientes_jefe_firma(self, tabla_filtro3, self.ver_peq1t, 
                                   self.funcion_de_asociar_peq1t, height=200, width=800)
        else:
            self.frame_vitrina_peq1t.eliminar_cuadro()
            self.frame_vitrina_peq1t = Cuadro(self)
            self.frame_vitrina_peq1t.agregar_label(1, 2, '                  0 documentos encontrados')

    #----------------------------------------------------------------------
    def limpiar_peq1t(self):
        
        # Eliminando campos
        self.peq1t1.eliminar_cuadro()
        self.vpeq1t.Eliminar_vitrina()
        self.peq1t15.eliminar_cuadro()
        self.frame_vitrina_peq1t.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.peq1t1 = Cuadro(self)
        self.peq1t1.agregar_rejilla(self.rejilla_peq1t)
        self.peq1t15 = Cuadro(self)
        self.peq1t15.agregar_rejilla(self.rejilla_peq1t2)
        self.frame_vitrina_peq1t = Cuadro(self)
        # Creando vitrina
        self.vpeq1t = Vitrina_pendientes_jefe_firma(self, self.tabla_peq1tF, self.ver_peq1t, 
                                   self.funcion_de_asociar_peq1t, height=200, width=800)

    #----------------------------------------------------------------------

    def volver_peq1t(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

    #----------------------------------------------------------------------
    def ver_peq1t(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x
        #print(x)
        lb1 = b_dr.listar_datos_de_fila(self.x)
        # PARA EL CASO DE ESTA PANTALLA SOLO LLEVARA LOS DATOS INGRESADOS HASTA APORTE DEL DOC O ASUNTO (CAMPOS OBLIGATORIO)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8]]
        
        self.desaparecer()
        subframe = vista_dr.Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                                lista=lista_para_insertar, id_doc = x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_peq1t(self, x):
        """"""
        print('hola')
