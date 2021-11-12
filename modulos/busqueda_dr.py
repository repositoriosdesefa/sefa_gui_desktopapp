from tkinter import messagebox
import datetime as dt

from apoyo.elementos_de_GUI import Cuadro, Ventana, Vitrina_busqueda, Vitrina_busquedaep
from apoyo.manejo_de_bases import Base_de_datos
import apoyo.datos_frecuentes as dfrec
from modulos import vista_dr

# BASES DE DATOS:
#----------------------------------------------------------------------
id_b_ospa = '13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4'

# 0. Tablas relacionales
base_relacion_docs = Base_de_datos(id_b_ospa, 'RELACION_DOCS')
base_relacion_d_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_RELACION_D')

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
b_de_hist = Base_de_datos(id_b_ospa, 'HISTORIAL_EP')


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
        self.tabla_0 = self.tabla_inicial.rename(columns={'COD_DR':'ID DOC RECIBIDO','COD_PROBLEMA':'CODIGO','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['ID DOC RECIBIDO','FECHA INGRESO SEFA','CODIGO','REMITENTE','TIPO DOC','INDICACION','FECHA ULTIMO MOV.','ASUNTO']]
 
        # Información para las listas desplegables
        self.listatipodoc = list(set(self.tabla_0['TIPO DOC']))
        self.listadestina = list(set(self.tabla_0['REMITENTE']))

        # Agregando logo del ospa a la ventana y título
        self.c0 = Cuadro(self)
        self.c0.agregar_label(0,0,' ')
        self.c0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)
        c2 = Cuadro(self)
        c2.agregar_titulo(2, 0, 'Búsqueda de documentos recibidos')

        # Armando rejilla con los filtros
        self.rejilla_dr = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('E', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CX', 1, 1, self.listatipodoc),

            ('L', 0, 2, 'Código'),
            ('E', 0, 3),

            ('L', 1, 2, 'Remitente'),
            ('CX', 1, 3, self.listadestina)

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

        self.frame_vitrina_1 = Cuadro(self)

        # Creando vitrina
        self.v1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_dr, 
                                   self.funcion_de_asociar, height=200, width=1070)
    
    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = vista_dr.inicio_app_OSPA(self, 400, 400, "Inicio")

    #----------------------------------------------------------------------

    def Buscardr(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro = self.c1.obtener_lista_de_datos()
        self.ht = self.listas_filtro[0]
        self.tipodoc = self.listas_filtro[1]
        self.codigo = self.listas_filtro[2]
        self.remitente = self.listas_filtro[3]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodoc)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodoc+"' "
        if len(self.codigo)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"CODIGO=="+"'"+self.codigo+"' "
        if len(self.remitente)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"REMITENTE=="+"'"+self.remitente+"' "
        
        self.mostrarDatosdr(filtro)

    #----------------------------------------------------------------------

    def Complementodr(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['ID DOC RECIBIDO','FECHA INGRESO SEFA','CODIGO','REMITENTE','TIPO DOC','INDICACION','FECHA ULTIMO MOV.','ASUNTO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.v1 = Vitrina_busqueda(self, tabla_filtro3, self.ver_dr, 
                                   self.funcion_de_asociar, height=200, width=1070)
        else:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.frame_vitrina_1.agregar_label(1, 2, '                  0 documentos encontrados')
    #----------------------------------------------------------------------  

    def mostrarDatosdr(self, filtro):

        self.filtro0 = self.tabla_0

        if len(self.ht)>0: # Filtro por palabra clave
            self.v1.Eliminar_vitrina()
            self.filtro0 = self.tabla_0[self.tabla_0['ID DOC RECIBIDO'].str.contains(self.ht.upper())]
            self.Complementodr(self.filtro0)

        if len(filtro)>0:

            self.v1.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementodr(self.filtro1)

        else:
            self.v1.Eliminar_vitrina()
            self.Complementodr(self.filtro0)

    #----------------------------------------------------------------------
    def limpiar(self):
        
        # Eliminando campos
        self.c1.eliminar_cuadro()
        self.v1.Eliminar_vitrina()
        self.c15.eliminar_cuadro()
        self.frame_vitrina_1.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.c1 = Cuadro(self)
        self.c1.agregar_rejilla(self.rejilla_dr)
        self.c15 = Cuadro(self)
        self.c15.agregar_rejilla(self.rejilla_b)
        self.frame_vitrina_1 = Cuadro(self)
        # Creando vitrina
        self.v1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_dr, 
                                   self.funcion_de_asociar, height=200, width=1070)

    #----------------------------------------------------------------------

    def volver(self):
        """"""
        codigode = self.cod_doc_de

        lb1 = b_de.listar_datos_de_fila(codigode)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, 
                                                nuevo=False, lista=lista_para_insertar, id_doc=codigode)

    #----------------------------------------------------------------------
    def ver_dr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x

        lb1 = b_dr.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], 
                                lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], lb1[14]]
        
        self.desaparecer()
        subframe = vista_dr.Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                                lista=lista_para_insertar, id_doc = x)

    #----------------------------------------------------------------------
    def funcion_de_asociar(self, x):
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
        self.tabla_0 = self.tabla_inicial.rename(columns={'COD_DE':'ID DOC EMITIDO','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','COD_PROBLEMA':'CODIGO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['ID DOC EMITIDO','CODIGO','DESTINATARIO','NRO DOCUMENTO','TIPO DOC','ESTADO','FECHA ULTIMO MOV.','DETALLE']]
 
        # Información para las listas desplegables
        self.listacategoria = list(set(self.tabla_0['CATEGORIA']))
        self.listadestinatario = list(set(self.tabla_0['DESTINATARIO']))
        self.listatipodocemit = list(set(self.tabla_0['TIPO DOC']))

        # Agregando logo del ospa a la ventana y título
        self.cde0 = Cuadro(self)
        self.cde0.agregar_label(0, 0,' ')
        self.cde0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        cde2 = Cuadro(self)
        cde2.agregar_titulo(2, 0, 'Búsqueda de documentos emitidos')

        # Armando rejilla con los filtros

        self.rejilla_de = (

            ('L', 0, 0, 'Categoría'),
            ('CX', 0, 1, self.listacategoria),

            ('L', 1, 0, 'Nro registro Siged'),
            ('E', 1, 1),

            ('L', 0, 2, 'Destinatario'),
            ('CX', 0, 3, self.listadestinatario),

            ('L', 1, 2, 'Código'),
            ('E', 1, 3),

            ('L', 2, 0, 'Tipo de documento'),
            ('CX', 2, 1, self.listatipodocemit),

            ('L', 2, 2, 'Nro de documento'),
            ('E', 2, 3)

        )
        
        # Agregando rejilla a la ventana
        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)

        # Generando rejilla para botones
        rejilla_bde = (
            ('B', 5, 4, 'Buscar', self.Buscar_de),
            ('B', 5, 5, 'Limpiar', self.limpiar_de),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.cde15 = Cuadro(self)
        self.cde15.agregar_rejilla(rejilla_bde)

        self.frame_vitrina_1 = Cuadro(self)

        # Creando vitrina
        self.vde1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)

    #----------------------------------------------------------------------

    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = vista_dr.inicio_app_OSPA(self, 400, 400, "Inicio")

    #----------------------------------------------------------------------

    def Buscar_de(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtrode = self.cde1.obtener_lista_de_datos()
        self.decate = self.listas_filtrode[0] #
        self.deht = self.listas_filtrode[1]
        self.dedestin = self.listas_filtrode[2]
        self.decodigo = self.listas_filtrode[3]
        self.detipodoc = self.listas_filtrode[4] #
        self.dedoc = self.listas_filtrode[5]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.decate)>0 :
            filtro="CATEGORIA=="+"'"+self.decate+"' "
        if len(self.dedestin)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"DESTINATARIO=="+"'"+self.dedestin+"' "
        if len(self.decodigo)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"CODIGO=="+"'"+self.decodigo+"' "
        if len(self.detipodoc)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO DOC`=="+"'"+self.detipodoc+"' "
        if len(self.dedoc)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`NRO DOCUMENTO`=="+"'"+self.dedoc+"' "
        
        self.mostrarDatosde(filtro)

    #----------------------------------------------------------------------
    def Complementode(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['ID DOC EMITIDO','CODIGO','DESTINATARIO','NRO DOCUMENTO','TIPO DOC','ESTADO','FECHA ULTIMO MOV.','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.vde1 = Vitrina_busqueda(self, tabla_filtro3, self.ver_de, self.funcion_de_asociar_de, height=200, width=1070)
        else:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.frame_vitrina_1.agregar_label(1, 2, '                  0 documentos encontrados')
    #----------------------------------------------------------------------  

    def mostrarDatosde(self, filtro):

        self.filtro0 = self.tabla_0

        if len(self.deht)>0: # Filtro por palabra clave
            self.vde1.Eliminar_vitrina()
            self.filtro0 = self.tabla_0[self.tabla_0['ID DOC EMITIDO'].str.contains(self.ht.upper())]
            self.Complementode(self.filtro0)

        if len(filtro)>0:

            self.vde1.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementode(self.filtro1)

        else:
            self.vde1.Eliminar_vitrina()
            self.Complementode(self.filtro0)

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
        self.cde15.agregar_rejilla(self.rejilla_de)
        self.frame_vitrina_1 = Cuadro(self)
        # Creando vitrina
        self.vde1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_de, self.funcion_de_asociar_de, height=200, width=1070)

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
    def funcion_de_asociar_de(self, x):
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
        self.tabla_ep = self.ep.rename(columns={'ID_EP':'ID EXTREMO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.'})
        self.tabla_ep2 = self.tabla_ep.loc[:, ['ID EXTREMO','AGENTE CONTAMINANTE','COMPONENTE AMBIENTAL','ACTIVIDAD','DEPARTAMENTO','EFA','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
        self.tabla_ep3 = self.tabla_ep2.loc[0:70, ['ID EXTREMO','AGENTE CONTAMINANTE','COMPONENTE AMBIENTAL','ACTIVIDAD','DEPARTAMENTO','EFA','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
        
        # Listas para desplegables
        self.listaAG = list(set(self.tabla_ep['AGENTE CONTAMINANTE']))
        self.listaCA = list(set(self.tabla_ep['COMPONENTE AMBIENTAL']))
        self.listaACT = list(set(self.tabla_ep['ACTIVIDAD']))
        self.listaDEPAR = list(set(self.tabla_ep['DEPARTAMENTO']))
        self.listaPROV = list(set(self.tabla_ep['PROVINCIA']))
        self.listaDISTR = list(set(self.tabla_ep['DISTRITO']))
        self.listaTIPOUBI = list(set(self.tabla_ep['TIPO DE UBICACION']))
        #self.listaOCURR = list(set(self.tabla_ep['OCURRENCIA']))
        self.listaEFA = list(set(self.tabla_ep['EFA']))


        self.rejilla_ep = (

            ('L', 0, 0, 'Agente contaminante'),
            ('CX', 0, 1, self.listaAG),

            ('L', 0, 2, 'Componente ambiental'),
            ('CX', 0, 3, self.listaCA),

            ('L', 0, 4, 'Actividad'),
            ('CX', 0, 5, self.listaACT),

            ('L', 1, 0, 'Departamento'),
            ('CX', 1, 1, self.listaDEPAR),

            ('L', 1, 2, 'Provincia'),
            ('CX', 1, 3, self.listaPROV),

            ('L', 1, 4, 'Distrito'),
            ('CX', 1, 5, self.listaDISTR),

            ('L', 2, 0, 'Tipo de ubicación'),
            ('CX', 2, 1, self.listaTIPOUBI),

            #('L', 2, 2, 'Ocurrencia'),
            #('CX', 2, 3, self.listaOCURR),

            ('L', 2, 4, 'EFA'),
            ('CX', 2, 5, self.listaEFA),

            ('L', 3, 0, 'Palabra clave en descripción'),
            ('E', 3, 1)

        )
        
        self.ep0 = Cuadro(self)
        self.ep0.agregar_label(0, 0,' ')
        self.ep0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)

        self.ep1 = Cuadro(self)
        self.ep1.agregar_rejilla(self.rejilla_ep)

        rejilla_ep2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_ep),
            ('B', 5, 5, 'Limpiar', self.limpiar_ep),
            ('B', 5, 6, 'Volver', self.volver)
        )
        

        ep2 = Cuadro(self)
        ep2.agregar_rejilla(rejilla_ep2)

        ep3 = Cuadro(self)
        ep3.agregar_titulo(2, 0, 'Búsqueda de extremos')


        self.vep = Vitrina_busquedaep(self, self.tabla_ep3, self.ver_ep, self.funcion_de_asociar_ep, height=200, width=1200)
    
#----------------------------------------------------------------------
    def Buscar_ep(self):

        self.listas_filtroep = self.ep1.obtener_lista_de_datos()
        self.palabraclave = self.listas_filtroep[8]
        self.efa = self.listas_filtroep[7]

        
        if self.palabraclave != "":
            self.vep.Eliminar_vitrina()
            self.tabla_filtradade = self.tabla_ep2[self.tabla_ep2['DESCRIPCION'].str.contains(self.palabraclave.upper())]
            self.vep = Vitrina_busquedaep(self, self.tabla_filtradade, self.ver_ep, self.funcion_de_asociar_ep, height=200, width=1200)
            if self.efa != "":
                self.vep.Eliminar_vitrina()
                self.tabla_filtradade2 = self.tabla_filtradade[self.tabla_filtradade['EFA']==self.efa]
                self.vep = Vitrina_busqueda(self, self.tabla_filtradade2, self.ver_ep, self.funcion_de_asociar_ep, height=200, width=1200)
           

#----------------------------------------------------------------------
    def limpiar_ep(self):
        self.vep.Eliminar_vitrina()

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
    def funcion_de_asociar_ep(self, x):
        """"""
        print("hola")