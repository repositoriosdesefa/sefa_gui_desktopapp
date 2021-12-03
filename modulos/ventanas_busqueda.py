from tkinter import Message, messagebox
import datetime as dt
import pandas as pd
from apoyo.elementos_de_GUI import Cuadro, Ventana, Vitrina_busqueda, Vitrina_busquedaep, Vitrina_pendientes
from apoyo.manejo_de_bases import Base_de_datos
from modulos import ventanas_vista, menus
from modulos import variables_globales as vg
from modulos.funcionalidades_ospa import funcionalidades_ospa


id_b_ospa = '13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4'

# 1. Bases
b_dr = vg.b_dr
b_dr_tabla = b_dr.generar_dataframe()
b_dr_cod = vg.b_dr_cod
b_dr_hist = vg.b_dr_hist
b_de = vg.b_de
b_de_tabla = b_de.generar_dataframe()
b_de_cod = vg.b_de_cod
b_de_hist = vg.b_de_hist
b_ep = vg.b_ep
b_ep_tabla = b_ep.generar_dataframe()
b_ep_cod = vg.b_ep_cod
b_ep_hist = vg.b_ep_hist
b_mp = vg.b_mp
b_mp_tabla = b_mp.generar_dataframe()
b_mp_cod = vg.b_mp_cod
b_mp_hist = vg.b_mp_hist
b_adm = vg.b_adm
b_adm_tabla = b_adm.generar_dataframe()
tabla_lista_efa = vg.tabla_lista_efa


# 2. Tablas relacionales
base_relacion_docs = vg.base_relacion_docs
base_relacion_d_hist = vg.base_relacion_docs_hist
base_relacion_dr_ep =  vg.base_relacion_dr_ep
base_relacion_dr_ep_hist =  vg.base_relacion_dr_ep_hist
base_relacion_de_ep =  vg.base_relacion_de_ep
base_relacion_de_ep_hist =  vg.base_relacion_de_ep_hist
b_relacion_mp_ep =  vg.base_relacion_mp_ep
b_relacion_mp_ep_tabla = b_relacion_mp_ep.generar_dataframe()
base_relacion_mp_ep_hist =  vg.base_relacion_mp_ep_hist



class Doc_recibidos_busqueda(funcionalidades_ospa):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.id_objeto_ingresado = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_0 = self.tabla_inicial0.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['NRO DOC','REMITENTE','HT INGRESO','FECHA INGRESO SEFA','INDICACION','ESPECIALISTA_1','FECHA ULTIMO MOV.','ASUNTO']]
        
        # Información para las listas desplegables
        self.listatipodoc = sorted(list(set(self.tabla_0['TIPO DOC'])))
        self.listaremitente = sorted(list(set(self.tabla_0['REMITENTE'])))

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
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.c15 = Cuadro(self)
        self.c15.agregar_rejilla(self.rejilla_b)

        self.frame_vitrina_dr = Cuadro(self)

        # Creando vitrina
        self.v1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_dr, 
                                   self.asociar_dr_de, height=250, width=1080)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.c1.eliminar_cuadro()
        self.v1.Eliminar_vitrina()
        self.c15.eliminar_cuadro()
        self.frame_vitrina_dr.eliminar_cuadro()
        # Actualizando data
        b_dr = vg.b_dr
        b_dr_tabla = b_dr.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_0 = self.tabla_inicial0.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['NRO DOC','REMITENTE','HT INGRESO','FECHA INGRESO SEFA','INDICACION','ESPECIALISTA_1','FECHA ULTIMO MOV.','ASUNTO']]
      
        # Información para las listas desplegables
        self.listatipodoc = sorted(list(set(self.tabla_0['TIPO DOC'])))
        self.listaremitente = sorted(list(set(self.tabla_0['REMITENTE'])))

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
        self.c15 = Cuadro(self)
        self.c15.agregar_rejilla(self.rejilla_b)
        self.frame_vitrina_dr = Cuadro(self)
        # Creando vitrina
        self.v1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_dr, 
                                   self.asociar_dr_de, height=250, width=1080)


    def Buscardr(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro = self.c1.obtener_lista_de_datos()
        self.ht = self.listas_filtro[0]
        self.tipodoc = self.listas_filtro[1]
        self.remitente = self.listas_filtro[2]
        self.nrodoc = self.listas_filtro[3]

        self.filtro0 = self.tabla_0
        self.filtro0['NUM_DOC']=self.filtro0['NUM_DOC'].apply(str)

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodoc)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodoc+"' "

        if len(self.nrodoc)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"NUM_DOC=="+"'"+self.nrodoc+"' "
        
        self.mostrarDatosdr(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatosdr(self, filtro):

        self.filtro0 = self.tabla_0
        
        if len(self.remitente)>0: # Filtro por palabra clave
            self.v1.Eliminar_vitrina()
            self.filtro0 = self.tabla_0[self.tabla_0['REMITENTE'].str.contains(self.remitente)]
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

        tabla_filtro2 = filtro0.loc[:, ['NRO DOC','REMITENTE','HT INGRESO','FECHA INGRESO SEFA','INDICACION','ESPECIALISTA_1','FECHA ULTIMO MOV.','ASUNTO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_dr.eliminar_cuadro()
            self.frame_vitrina_dr = Cuadro(self)
            self.v1 = Vitrina_busqueda(self, tabla_filtro3, self.ver_dr, 
                                   self.asociar_dr_de, height=250, width=1080)
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
                                   self.asociar_dr_de, height=250, width=1080)

    #----------------------------------------------------------------------
    def ver_dr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x

        lb1 = b_dr.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], lb1[9], lb1[10],
                                 lb1[11], lb1[12], lb1[13], lb1[14], lb1[15], lb1[16], lb1[17], lb1[18]]
        
        self.desaparecer()
        subframe = ventanas_vista.Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                                lista=lista_para_insertar, id_objeto = x)

    #----------------------------------------------------------------------
    def asociar_dr_de(self, x):
        """"""
        self.x = x

        if self.nuevo == True:
            messagebox.showinfo("Error", "No tiene antecedente que pueda asociarse")
        else:
            
            #OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
            self.IDDR = b_dr.listar_datos_de_fila(self.x)
            self.IDDR_FINAL = self.IDDR[0]

            #OBTENER EL ID USUARIO DEL DOCUMENTO EMITIDO
            codigode = self.id_objeto_ingresado
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
                    
            # Asociación de extremos de problema de DR con DE
            # 1. Obtengo la tabla de relación entre DE y EP
            tabla_de_dr_ep = base_relacion_dr_ep.generar_dataframe()
            # 2. Filtro las relaciones que tiene el DE
            # Filtro para obtener las relaciones activas
            tabla_relacion_activos = tabla_de_dr_ep[tabla_de_dr_ep['ESTADO']=="ACTIVO"]
            # Con ese ID, filtro la tabla de relacion
            tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos['ID_DR']==self.IDDR_FINAL]
            # 3. Obtengo el ID de los EP que están relacionados al DE
            # Me quedo con el vector a filtrar en forma de lista
            lista_ep = list(tabla_relacion_filtrada['ID_EP'].unique())
            # 4. Concateno los ID de los EP relacionados al DE con el ID del DR
            if len(lista_ep) > 0:
                for indice in range(len(lista_ep)):
                    cod_relacion = id_interno_de + "/" + lista_ep[indice]
                    datos_insertar = [cod_relacion, id_interno_de, lista_ep[indice], 'ACTIVO', hora_de_modificacion] 
                    base_relacion_de_ep.agregar_datos(datos_insertar)
            else:
                messagebox.showinfo("¡Atención!", "El registro ha sido asociado con éxito")
        
    #----------------------------------------------------------------------     
    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

class Doc_emitidos_busqueda(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.id_objeto_ingresado = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_de_tabla
        self.tabla_0 = self.tabla_inicial0.rename(columns={'COD_DE':'DOC EMITIDO','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['DOC EMITIDO','DESTINATARIO','TIPO DOC','NRO DOCUMENTO','FECHA FIRMA','FECHA NOTIFICACION','ESTADO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.listacategoria = sorted(list(set(self.tabla_0['CATEGORIA'])))
        self.listadestinatario = sorted(list(set(self.tabla_0['DESTINATARIO'])))
        self.listatipodocemit = sorted(list(set(self.tabla_0['TIPO DOC'])))
        self.listaestado = sorted(list(set(self.tabla_0['ESTADO'])))

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

            ('L', 0, 2, 'Nro registro Siged'),
            ('EE', 0, 3),

            ('L', 0, 4, 'Destinatario'),
            ('CXE', 0, 5, 39, self.listadestinatario, '', 'normal'),

            ('L', 1, 0, 'Estado'),
            ('CXE', 1, 1, 39, self.listaestado, '', 'normal'),

            ('L', 1, 2, 'Tipo de documento'),
            ('CXP', 1, 3, 39, self.listatipodocemit, '', 'readonly'),

            ('L', 1, 4, 'Nro de documento'),
            ('EE', 1, 5)

        )
        
        # Agregando rejilla a la ventana
        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)

        # Generando rejilla para botones
        self.rejilla_bde = (
            ('B', 5, 4, 'Buscar', self.Buscar_de),
            ('B', 5, 5, 'Limpiar', self.limpiar_de),
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app),
            ('B', 5, 9, 'Emitir doc', self.doc_emitido)
        )
        
        # Agregando rejilla de botones a la ventana
        self.cde15 = Cuadro(self)
        self.cde15.agregar_rejilla(self.rejilla_bde)
        self.frame_vitrina_1 = Cuadro(self)

        # Creando vitrina
        self.vde1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_de, 
                                    self.asociar_de_dr, height=250, width=1190)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.cde1.eliminar_cuadro()
        self.vde1.Eliminar_vitrina()
        self.cde15.eliminar_cuadro()
        self.frame_vitrina_1.eliminar_cuadro()
        # Actualizando data
        b_de = vg.b_de
        b_de_tabla = b_de.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_de_tabla
        self.tabla_0 = self.tabla_inicial0.rename(columns={'COD_DE':'DOC EMITIDO','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION'})
        self.tabla_drF = self.tabla_0.loc[0:99, ['DOC EMITIDO','DESTINATARIO','TIPO DOC','NRO DOCUMENTO','FECHA FIRMA','FECHA NOTIFICACION','ESTADO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.listacategoria = sorted(list(set(self.tabla_0['CATEGORIA'])))
        self.listadestinatario = sorted(list(set(self.tabla_0['DESTINATARIO'])))
        self.listatipodocemit = sorted(list(set(self.tabla_0['TIPO DOC'])))
        self.listaestado = sorted(list(set(self.tabla_0['ESTADO'])))

        # Armando rejilla con los filtros

        self.rejilla_de = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 39, self.listacategoria, '', 'readonly'),

            ('L', 0, 2, 'Nro registro Siged'),
            ('EE', 0, 3),

            ('L', 0, 4, 'Destinatario'),
            ('CXE', 0, 5, 39, self.listadestinatario, '', 'normal'),

            ('L', 1, 0, 'Estado'),
            ('CXE', 1, 1, 39, self.listaestado, '', 'normal'),

            ('L', 1, 2, 'Tipo de documento'),
            ('CXP', 1, 3, 39, self.listatipodocemit, '', 'readonly'),

            ('L', 1, 4, 'Nro de documento'),
            ('EE', 1, 5)

        )

        # Agregando rejilla a la ventana
        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)
        self.cde15 = Cuadro(self)
        self.cde15.agregar_rejilla(self.rejilla_bde)
        self.frame_vitrina_1 = Cuadro(self)
        # Creando vitrina
        self.vde1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_de, 
                                    self.asociar_de_dr, height=250, width=1190)

    #----------------------------------------------------------------------

    def doc_emitido(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subframe = ventanas_vista.Doc_emitidos_vista(self, 550, 1090, "Registro Documento Emitido")

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

        self.filtro0 = self.tabla_0
        self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)

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

        if len(self.dedoc)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`NRO DOCUMENTO`=="+"'"+self.dedoc+"' "
        
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

        tabla_filtro2 = filtro0.loc[:, ['DOC EMITIDO','DESTINATARIO','TIPO DOC','NRO DOCUMENTO','FECHA FIRMA','FECHA NOTIFICACION','ESTADO','CATEGORIA','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.vde1 = Vitrina_busqueda(self, tabla_filtro3, self.ver_de, self.asociar_de_dr, height=250, width=1190)
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
        self.vde1 = Vitrina_busqueda(self, self.tabla_drF, self.ver_de, 
                                    self.asociar_de_dr, height=250, width=1190)

    #----------------------------------------------------------------------
    def ver_dr(self, id_usuario):
        """"""
        texto_documento = 'Documento recibido: ' + id_usuario

        lb1 = b_dr.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], lb1[9], lb1[10],
                                lb1[11], lb1[12], lb1[13], lb1[14], lb1[15], lb1[16], lb1[17], lb1[18]]
        
        self.desaparecer()
        subframe = ventanas_vista.Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_objeto = id_usuario)

    #----------------------------------------------------------------------
    def asociar_de_dr(self, x):
        """"""
        self.x = x

        if self.nuevo == True:
            messagebox.showinfo("Error", "No tiene antecedente que pueda asociarse")
        else:

            #OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
            self.IDDE = b_de.listar_datos_de_fila(self.x)
            self.IDDE_FINAL = self.IDDE[0]

            #OBTENER EL ID USUARIO DEL DOCUMENTO RECIBIDO
            codigodr = self.id_objeto_ingresado
            # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
            tabla_de_codigo_dr = b_dr.generar_dataframe()
            tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == codigodr]
            id_interno_dr = tabla_codigo_de_filtrada.iloc[0,0]

            # Definición de ID de relación
            id_relacion_doc = id_interno_dr + "/" +  self.IDDE_FINAL

            # BUSCAR COINCIDENCIAS
            valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)
            hora_de_modificacion = str(dt.datetime.now())

            if valor_repetido == False:
            
                # GUARDAR RELACION
                b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'RELACION_DOCS')

                # Pestaña 1: Código Único
                datos_insertar = [id_relacion_doc,id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion]
                b0.agregar_datos(datos_insertar)
                datos_a_cargar_hist = [id_relacion_doc, id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
                base_relacion_d_hist.agregar_datos(datos_a_cargar_hist)
                messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
                
            else:
                # BUSCAR ESTADO DE ID RELACION SI EXISTE
                tabla_de_relaciones = base_relacion_docs.generar_dataframe()
                tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_doc]
                estado_rela = tabla_relaciones_filtrada.iloc[0,3]
                
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

class Extremos(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, x = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.id_objeto_ingresado = id_objeto
        self.x = x #Código de extremo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
        
        # Renombramos los encabezados
        self.ep = b_ep_tabla
        self.tabla_ep = self.ep.rename(columns={'COD_EP':'CODIGO EXTREMO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','AGENTE CONTAMINANTE':'AGENT. CONTAMI.','COMPONENTE AMBIENTAL':'COMPONEN. AMBIE.'})
        self.tabla_deF = self.tabla_ep.loc[0:99, ['CODIGO EXTREMO','AGENT. CONTAMI.','COMPONEN. AMBIE.','ACTIVIDAD','DEPARTAMENTO','EFA','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
        
        # Listas para desplegables
        self.listaAG = sorted(list(set(self.tabla_ep['AGENT. CONTAMI.'])))
        self.listaCA = sorted(list(set(self.tabla_ep['COMPONEN. AMBIE.'])))
        self.listaACT = sorted(list(set(self.tabla_ep['ACTIVIDAD'])))
        self.listaDEPAR = sorted(list(set(self.tabla_ep['DEPARTAMENTO'])))
        self.listaPROV = sorted(list(set(self.tabla_ep['PROVINCIA'])))
        #self.listaDISTR = list(set(self.tabla_ep['DISTRITO']))
        self.listaTIPOUBI = sorted(list(set(self.tabla_ep['TIPO DE UBICACION'])))
        self.listaOCURR = sorted(list(set(self.tabla_ep['OCURRENCIA'])))
        self.listaEFA = sorted(list(set(self.tabla_ep['EFA'])))

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
            ('CXDEP3', 1, 1, 37, tabla_lista_efa, "Triple",
            'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

            ('L', 2, 0, 'Tipo de ubicación'),
            ('CXP', 2, 1, 39, self.listaTIPOUBI, '', "readonly"),

            ('L', 2, 2, 'Ocurrencia'),
            ('CXP', 2, 3, 39, self.listaOCURR, '', "readonly"),

            ('L', 2, 4, 'EFA'),
            ('CXE', 2, 5, 39, self.listaEFA, '', "normal"),

            ('L', 3, 0, 'Palabra clave en descripción'),
            ('EE', 3, 1),

            ('L', 3, 2, 'Código extremo'),
            ('EE', 3, 3)

        )
        
        # Agregando rejilla a la ventana
        self.ep1 = Cuadro(self)
        self.ep1.agregar_rejilla(self.rejilla_ep)

        # Generando rejilla para botones
        self.rejilla_ep2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_ep),
            ('B', 5, 5, 'Limpiar', self.limpiar_ep),
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app),
            ('B', 5, 9, 'Crear extremo', self.crear_extremo)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ep2 = Cuadro(self)
        self.ep2.agregar_rejilla(self.rejilla_ep2)
        self.frame_vitrina_ep = Cuadro(self)

        # Creando vitrina
        self.vep = Vitrina_busquedaep(self, self.tabla_deF, self.ver_ep_cod, 
                                     self.asociar_ep, self.ver_mp_ep, height=250, width=1220)

    #----------------------------------------------------------------------

    def crear_extremo(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_vista.Extremo_problemas_vista(self, 550, 1090, "Registro Extremo de Problema")

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
        self.codigo = self.listas_filtroep[10]

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

        if len(self.codigo)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`CODIGO EXTREMO`=="+"'"+self.codigo+"' "
        
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

        tabla_filtro2 = filtro0.loc[:, ['CODIGO EXTREMO','AGENT. CONTAMI.','COMPONEN. AMBIE.','ACTIVIDAD','DEPARTAMENTO','EFA','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ep.eliminar_cuadro()
            self.frame_vitrina_ep = Cuadro(self)
            self.vep = Vitrina_busquedaep(self, tabla_filtro3, self.ver_ep_cod, self.asociar_ep, self.ver_mp_ep, height=250, width=1220)
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
        self.vep = Vitrina_busquedaep(self, self.tabla_deF, self.ver_ep_cod, self.asociar_ep, self.ver_mp_ep, height=250, width=1220)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.ep1.eliminar_cuadro()
        self.vep.Eliminar_vitrina()
        self.ep2.eliminar_cuadro()
        self.frame_vitrina_ep.eliminar_cuadro()
        # Actualizando data
        b_ep = vg.b_ep
        b_ep_tabla = b_ep.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.ep = b_ep_tabla
        self.tabla_ep = self.ep.rename(columns={'COD_EP':'CODIGO EXTREMO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','AGENTE CONTAMINANTE':'AGENT. CONTAMI.','COMPONENTE AMBIENTAL':'COMPONEN. AMBIE.'})
        self.tabla_deF = self.tabla_ep.loc[0:99, ['CODIGO EXTREMO','AGENT. CONTAMI.','COMPONEN. AMBIE.','ACTIVIDAD','DEPARTAMENTO','EFA','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
     

        # Información para las listas desplegables
        self.listaAG = sorted(list(set(self.tabla_ep['AGENT. CONTAMI.'])))
        self.listaCA = sorted(list(set(self.tabla_ep['COMPONEN. AMBIE.'])))
        self.listaACT = sorted(list(set(self.tabla_ep['ACTIVIDAD'])))
        self.listaDEPAR = sorted(list(set(self.tabla_ep['DEPARTAMENTO'])))
        self.listaPROV = sorted(list(set(self.tabla_ep['PROVINCIA'])))
        #self.listaDISTR = list(set(self.tabla_ep['DISTRITO']))
        self.listaTIPOUBI = sorted(list(set(self.tabla_ep['TIPO DE UBICACION'])))
        self.listaOCURR = sorted(list(set(self.tabla_ep['OCURRENCIA'])))
        self.listaEFA = sorted(list(set(self.tabla_ep['EFA'])))

        # Armando rejilla con los filtros
        self.rejilla_ep = (

            ('L', 0, 0, 'Agente contaminante'),
            ('CXP', 0, 1, 39, self.listaAG, '', "readonly"),

            ('L', 0, 2, 'Componente ambiental'),
            ('CXP', 0, 3, 39, self.listaCA, '', "readonly"),

            ('L', 0, 4, 'Actividad'),
            ('CXP', 0, 5, 39, self.listaACT, '', "readonly"),

            ('L', 1, 0, 'Departamento'),
            ('CXDEP3', 1, 1, 37, tabla_lista_efa, "Triple",
            'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

            ('L', 2, 0, 'Tipo de ubicación'),
            ('CXP', 2, 1, 39, self.listaTIPOUBI, '', "readonly"),

            ('L', 2, 2, 'Ocurrencia'),
            ('CXP', 2, 3, 39, self.listaOCURR, '', "readonly"),

            ('L', 2, 4, 'EFA'),
            ('CXE', 2, 5, 39, self.listaEFA, '', "normal"),

            ('L', 3, 0, 'Palabra clave en descripción'),
            ('EE', 3, 1),

            ('L', 3, 2, 'Código extremo'),
            ('EE', 3, 3)

        )
        
        # Agregando rejilla a la ventana
        self.ep1 = Cuadro(self)
        self.ep1.agregar_rejilla(self.rejilla_ep)
        self.ep2 = Cuadro(self)
        self.ep2.agregar_rejilla(self.rejilla_ep2)
        # Creando vitrina
        self.frame_vitrina_ep = Cuadro(self)
        # Creando vitrina
        self.vep = Vitrina_busquedaep(self, self.tabla_deF, self.ver_ep_cod, self.asociar_ep, self.ver_mp_ep, height=250, width=1220)

    #----------------------------------------------------------------------
    def ver_ep_cod(self, id_objeto):
        """"""
        texto_documento = 'Extremo de problema: ' + id_objeto

        tabla_codigo_de_filtrada = self.tabla_ep.query("`CODIGO EXTREMO`==@id_objeto")
        self.id_interno_ep = tabla_codigo_de_filtrada.iloc[0,0]

        lb1 = b_ep.listar_datos_de_fila(id_objeto)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], 
                                lb1[8], lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], 
                                lb1[14], lb1[15], lb1[16], lb1[17], lb1[18], lb1[19], lb1[20]]
        self.desaparecer()

        subframe = ventanas_vista.Extremo_problemas_vista(self, 750, 1350, texto_documento, 
                                        nuevo=False, lista=lista_para_insertar, id_objeto = id_objeto)


    #----------------------------------------------------------------------
    def ver_mp_ep(self, x):
        """"""
        self.x = x
        texto_documento = 'Extremo de problema: ' + x

        tabla_codigo_de_filtrada = self.tabla_ep.query("`CODIGO EXTREMO`==@self.x")
        self.id_interno_ep = tabla_codigo_de_filtrada.iloc[0,0]
        tabla_codigo_de_filtrada2 = tabla_codigo_de_filtrada['ID_EP'].tolist()
        self.relacion_mp_ep = b_relacion_mp_ep.generar_dataframe()
        relacion_activos = self.relacion_mp_ep[self.relacion_mp_ep.ID_EP.isin(tabla_codigo_de_filtrada2)]
        relacion_activos2 = relacion_activos['ID_MP'].tolist()


        if len(relacion_activos) == 0:
            messagebox.showinfo("Error", "No tiene macroproblemas asociados")
        else:
            self.desaparecer()
            subframe = Macroproblemas_filtrada(self, 500, 1200,texto_documento, nuevo=False, id_objeto = self.id_interno_ep, x = x, listamc = relacion_activos2)


    #----------------------------------------------------------------------
    def asociar_ep(self, x):
        """"""

        self.x = x
        hora_de_modificacion = str(dt.datetime.now())
        
        if self.nuevo == True:
            messagebox.showinfo("Error", "No tiene antecedente que pueda asociarse")
        else:
            #OBTENER EL ID INTERNO DEL EXTREMO DE PROBLEMA
            self.IDEP = b_ep.listar_datos_de_fila(self.x)
            self.IDEP_FINAL = self.IDEP[0]

            #OBTENER EL ID USUARIO DEL OBJETO A ASOCIAR
            id_objeto_anterior = self.id_objeto_ingresado
            # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
            if self.tipo_objeto_anterior == "DR":
                tabla_de_codigo_dr = b_dr.generar_dataframe()
                tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == id_objeto_anterior]
                base_relacion_objetos = base_relacion_dr_ep 
                base_relacion_objetos_hist = base_relacion_dr_ep_hist
            elif self.tipo_objeto_anterior == "MP":
                tabla_de_codigo_dr = b_mp.generar_dataframe()
                tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_MP == id_objeto_anterior]
                base_relacion_objetos = b_relacion_mp_ep
                base_relacion_objetos_hist = base_relacion_mp_ep_hist
            else:
                raise messagebox.showinfo("Error", "No puede asociar extremos de problema desde esta vista")
            
            id_interno = tabla_codigo_de_filtrada.iloc[0,0]

            # Definición de ID de relación
            id_relacion_objetos = id_interno + "/" +  self.IDEP_FINAL

            # BUSCAR COINCIDENCIAS
            valor_repetido = self.comprobar_id(base_relacion_objetos, id_relacion_objetos)

            # BUSCAR ESTADO DE ID RELACION SI EXISTE
            if valor_repetido == True:  # si hay coincidencias de ese id_relacion_doc
                tabla_de_relaciones = base_relacion_objetos.generar_dataframe()
                tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_objetos]
                estado_rela = tabla_relaciones_filtrada.iloc[0,3]
                if estado_rela == 'ACTIVO':
                    messagebox.showinfo("Error", "Ya se encuentra asociado")
                else:
                    datos_iniciales = base_relacion_objetos.listar_datos_de_fila(id_relacion_objetos)
                    hora = str(dt.datetime.now())
                    datos_a_cargar_hist = datos_iniciales + [hora]
                    estado_a_sobreescribir = 'ACTIVO'
                    datos_a_cargar_hist[3] = estado_a_sobreescribir
                    base_relacion_objetos.cambiar_un_dato_de_una_fila(id_relacion_objetos, 4, estado_a_sobreescribir)
                    base_relacion_objetos.cambiar_un_dato_de_una_fila(id_relacion_objetos, 5, hora)
                    base_relacion_objetos_hist.agregar_datos(datos_a_cargar_hist)
                    base_relacion_objetos_hist.cambiar_un_dato_de_una_fila(id_relacion_objetos, 4, estado_a_sobreescribir)
                    messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        
            else:
                # Pestaña 1: Código Único
                datos_insertar = [id_relacion_objetos, id_interno, self.IDEP_FINAL,'ACTIVO',hora_de_modificacion]
                base_relacion_objetos.agregar_datos(datos_insertar)
                datos_a_cargar_hist = [id_relacion_objetos, id_interno, self.IDEP_FINAL,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
                base_relacion_objetos_hist.agregar_datos(datos_a_cargar_hist)
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

class Macroproblemas(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, x = None, listamc = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.x2 = x
        self.listamc = listamc
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_mp = id_objeto
            self.x2 = x

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_mp_tabla

        self.tabla_mp = self.tabla_inicial0.rename(columns={'COD_MP':'COD. MACROPROBLEMA','NOMBRE_DEL_PROBLEMA':'NOMBRE PROBLEMA','FECHA_DE_CREACION':'FECHA CREACION'})
        self.tabla_mpF = self.tabla_mp.loc[0:99, ['COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
        
        # Listas para desplegables
        self.listaestado = list(set(self.tabla_mp['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        self.mc0 = Cuadro(self)
        self.mc0.agregar_label(0, 0,' ')
        self.mc0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        mc3 = Cuadro(self)
        mc3.agregar_titulo(2, 0, 'Búsqueda de macroproblemas')
    
        # Armando rejilla con los filtros
        self.rejilla_mp = (

            ('L', 0, 0, 'Código de Macroproblema'),
            ('EE', 0, 1),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 39, self.listaestado, '', "readonly"),

            ('L', 1, 0, 'Nombre del problema'),
            ('EE', 1, 1),

            ('L', 1, 2, 'Palabra clave en descripción'),
            ('EE', 1, 3),
        )
        
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)

        # Generando rejilla para botones
        self.rejilla_mp2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_mp),
            ('B', 5, 5, 'Limpiar', self.limpiar_mp),
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app),
            ('B', 5, 9, 'Crear macrop.', self.crear_macroproblema)
        )
        
        # Agregando rejilla de botones a la ventana
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)
        self.frame_vitrina_mp = Cuadro(self)

        # Creando vitrina
        self.vmc = Vitrina_busqueda(self, self.tabla_mpF, self.ver_mp, self.funcion_de_asociar_mp, height=200, width=780)

     #----------------------------------------------------------------------

    def crear_macroproblema(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_vista.Macroproblemas_vista(self, 550, 1090, "Creación de macroproblemas")

    #----------------------------------------------------------------------
    
    def Buscar_mp(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtromc = self.mc1.obtener_lista_de_datos()
        self.CODIGO = self.listas_filtromc[0]
        self.ESTADO = self.listas_filtromc[1]
        self.NOMBRE = self.listas_filtromc[2]
        self.DESCRIP = self.listas_filtromc[3]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.CODIGO)>0 :
            filtro="`COD. MACROPROBLEMA`=="+"'"+self.CODIGO+"' "

        if len(self.ESTADO)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESTADO=="+"'"+self.ESTADO+"' "
        
        self.mostrarDatosmc(filtro)       

    #----------------------------------------------------------------------

    def mostrarDatosmc(self, filtro):

        self.filtro0 = self.tabla_mp
        
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

        tabla_filtro2 = filtro0.loc[:, ['COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.vmc = Vitrina_busqueda(self, tabla_filtro3, self.ver_mp, self.funcion_de_asociar_mp, height=200, width=780)
        else:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.frame_vitrina_mp.agregar_label(1, 2, '                  0 macroproblemas encontrados')

    #----------------------------------------------------------------------
    def limpiar_mp(self):
     
         # Eliminando campos
        self.mc1.eliminar_cuadro()
        self.vmc.Eliminar_vitrina()
        self.mc2.eliminar_cuadro()
        self.frame_vitrina_mp.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)

        self.frame_vitrina_mp = Cuadro(self)
        # Creando vitrina
        self.vmc = Vitrina_busqueda(self, self.tabla_mpF, self.ver_mp, self.funcion_de_asociar_mp, height=200, width=780)

        #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.mc1.eliminar_cuadro()
        self.vmc.Eliminar_vitrina()
        self.mc2.eliminar_cuadro()
        self.frame_vitrina_mp.eliminar_cuadro()
        # Actualizando data
        b_mp = vg.b_mp
        b_mp_tabla = b_mp.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_mp_tabla
        self.tabla_mp = self.tabla_inicial0.rename(columns={'COD_MP':'COD. MACROPROBLEMA','NOMBRE_DEL_PROBLEMA':'NOMBRE PROBLEMA','FECHA_DE_CREACION':'FECHA CREACION'})
        self.tabla_mpF = self.tabla_mp.loc[0:99, ['COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
        
        # Información para las listas desplegables
        self.listaestado = list(set(self.tabla_mp['ESTADO']))

        # Armando rejilla con los filtros

        self.rejilla_mp = (

            ('L', 0, 0, 'Código de Macroproblema'),
            ('EE', 0, 1),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 39, self.listaestado, '', "readonly"),

            ('L', 1, 0, 'Nombre del problema'),
            ('EE', 1, 1),

            ('L', 1, 2, 'Palabra clave en descripción'),
            ('EE', 1, 3),
        )

        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)

        self.frame_vitrina_mp = Cuadro(self)
        # Creando vitrina
        self.vmc = Vitrina_busqueda(self, self.tabla_mpF, self.ver_mp, self.funcion_de_asociar_mp, height=200, width=780)
    
    #----------------------------------------------------------------------
    def funcion_de_asociar_mp(self, x):
        """"""
        print("hola")

class Macroproblemas_filtrada(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, x = None, listamc = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.x2 = x
        self.tipo_objeto_anterior = tipo_objeto_anterior
        self.listamc = listamc
        if self.nuevo != True: #en caso exista
            self.listamp = lista
            self.id_usuario= id_objeto
            self.x2 = x

        # Renombramos los encabezados
        self.mc = b_mp_tabla

        self.mc = self.mc[self.mc.ID_MP.isin(self.listamc)]

        self.tabla_mp = self.mc.rename(columns={'COD_MP':'COD. MACROPROBLEMA','NOMBRE_DEL_PROBLEMA':'NOMBRE PROBLEMA','FECHA_DE_CREACION':'FECHA CREACION'})
        self.tabla_mpF = self.tabla_mp.loc[0:99, ['COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
        
        # Listas para desplegables
        self.listaestado = list(set(self.tabla_mp['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        self.mc0 = Cuadro(self)
        self.mc0.agregar_label(0, 0,' ')
        self.mc0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        mc3 = Cuadro(self)
        mc3.agregar_titulo(2, 0, 'Macroproblemas asociados')
    
        # Armando rejilla con los filtros
        self.rejilla_mp = (

            ('L', 0, 0, 'Código de Macroproblema'),
            ('EE', 0, 1),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 39, self.listaestado, '', "readonly"),

            ('L', 1, 0, 'Nombre del problema'),
            ('EE', 1, 1),

            ('L', 1, 2, 'Palabra clave en descripción'),
            ('EE', 1, 3),
        )
        
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)

        # Generando rejilla para botones
        self.rejilla_mp2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_mpf),
            ('B', 5, 5, 'Limpiar', self.limpiar_mp),
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)
        self.frame_vitrina_mp = Cuadro(self)

        # Creando vitrina
        self.vmc = Vitrina_pendientes(self, self.tabla_mpF, self.ver_mp, height=200, width=800)

    #----------------------------------------------------------------------
    
    def Buscar_mpf(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtromcF = self.mc1.obtener_lista_de_datos()
        self.CODIGOf = self.listas_filtromcF[0]
        self.ESTADOf = self.listas_filtromcF[1]
        self.NOMBREf = self.listas_filtromcF[2]
        self.DESCRIPf = self.listas_filtromcF[3]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.CODIGOf)>0 :
            filtro="`COD. MACROPROBLEMA`=="+"'"+self.CODIGOf+"' "

        if len(self.ESTADOf)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESTADO=="+"'"+self.ESTADOf+"' "
        
        self.mostrarDatosmcf(filtro)       

    #----------------------------------------------------------------------

    def mostrarDatosmcf(self, filtro):

        self.filtro0 = self.tabla_mp
        
        if len(self.NOMBREf)>0: # Filtro por palabra clave
            self.vmc.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['NOMBRE PROBLEMA'].str.contains(self.NOMBREf)]
            self.Complementomcf(self.filtro0)

        if len(self.DESCRIPf)>0: # Filtro por palabra clave
            self.vmc.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['DESCRIPCION'].str.contains(self.DESCRIPf)]
            self.Complementomcf(self.filtro0)
  
        if len(filtro)>0:

            self.vmc.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementomcf(self.filtro1)

        else:
            self.vmc.Eliminar_vitrina()
            self.Complementomcf(self.filtro0)

    #----------------------------------------------------------------------

    def Complementomcf(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.vmc = Vitrina_pendientes(self, tabla_filtro3, self.ver_mp, height=200, width=800)
        else:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.frame_vitrina_mp.agregar_label(1, 2, '                  0 macroproblemas encontrados')

    #----------------------------------------------------------------------
    def limpiar_mp(self):
     
         # Eliminando campos
        self.mc1.eliminar_cuadro()
        self.vmc.Eliminar_vitrina()
        self.mc2.eliminar_cuadro()
        self.frame_vitrina_mp.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)

        self.frame_vitrina_mp = Cuadro(self)
        # Creando vitrina
        self.vmc = Vitrina_pendientes(self, self.tabla_mpF, self.ver_mp, height=200, width=800)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.mc1.eliminar_cuadro()
        self.vmc.Eliminar_vitrina()
        self.mc2.eliminar_cuadro()
        self.frame_vitrina_mp.eliminar_cuadro()
        # Actualizando data
        b_mp = vg.b_mp
        b_mp_tabla = b_mp.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_mp_tabla
        self.mc = self.tabla_inicial0[self.tabla_inicial0.ID_MP.isin(self.listamc)]
        self.tabla_mp = self.mc.rename(columns={'COD_MP':'COD. MACROPROBLEMA','NOMBRE_DEL_PROBLEMA':'NOMBRE PROBLEMA','FECHA_DE_CREACION':'FECHA CREACION'})
        self.tabla_mpF = self.tabla_mp.loc[0:99, ['COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
        
        # Información para las listas desplegables
        self.listaestado = list(set(self.tabla_mp['ESTADO']))
        # Armando rejilla con los filtros

        self.rejilla_mp = (

            ('L', 0, 0, 'Código de Macroproblema'),
            ('EE', 0, 1),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 39, self.listaestado, '', "readonly"),

            ('L', 1, 0, 'Nombre del problema'),
            ('EE', 1, 1),

            ('L', 1, 2, 'Palabra clave en descripción'),
            ('EE', 1, 3),
        )

        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)

        self.frame_vitrina_mp = Cuadro(self)
        # Creando vitrina
        self.vmc = Vitrina_pendientes(self, self.tabla_mpF, self.ver_mp, height=200, width=800)

class Administrados(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_ad = id_objeto
        
        # Renombramos los encabezados
        self.ad = b_adm_tabla
        self.tabla_ad = self.ad.rename(columns={'ID_AD':'ID ADMINISTRADO','NOMBRE_O_RAZON_SOCIAL':'NOMBRE / RAZON SOCIAL','CATEGORÍA':'TIPO','DNI_RUC':'DNI / RUC'})
        self.tabla_adF = self.tabla_ad.loc[0:99, ['ID ADMINISTRADO','NOMBRE / RAZON SOCIAL','TIPO','DNI / RUC']]
        
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
            ('E', 0, 3)
        )
        
        # Agregando rejilla a la ventana
        self.ad1 = Cuadro(self)
        self.ad1.agregar_rejilla(self.rejilla_ad)

        # Generando rejilla para botones
        self.rejilla_ad2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_ad),
            ('B', 5, 5, 'Limpiar', self.limpiar_ad),
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Crear admin.', self.crear_adm),
            ('B', 5, 9, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ad2 = Cuadro(self)
        self.ad2.agregar_rejilla(self.rejilla_ad2)
        self.frame_vitrina_ad = Cuadro(self)

        # Creando vitrina
        self.vad = Vitrina_busqueda(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, height=200, width=590)

    #----------------------------------------------------------------------
    
    def Buscar_ad(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtroad = self.ad1.obtener_lista_de_datos()
        self.ADMINI = self.listas_filtroad[0]
        self.Tipo = self.listas_filtroad[1]
        self.ruc = self.listas_filtroad[2]

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

        tabla_filtro2 = filtro0.loc[:, ['ID ADMINISTRADO','NOMBRE / RAZON SOCIAL','TIPO','DNI / RUC']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ad.eliminar_cuadro()
            self.frame_vitrina_ad = Cuadro(self)
            self.vad = Vitrina_busqueda(self, tabla_filtro3, self.ver_ad, self.funcion_de_asociar_ad, height=200, width=590)
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
        self.vad = Vitrina_busqueda(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, height=200, width=590)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.ad1.eliminar_cuadro()
        self.vad.Eliminar_vitrina()
        self.ad2.eliminar_cuadro()
        self.frame_vitrina_ad.eliminar_cuadro()
        # Actualizando data
        b_adm = vg.b_adm
        b_adm_tabla = b_adm.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.ad = b_adm_tabla
        self.tabla_ad = self.ad.rename(columns={'ID_AD':'ID ADMINISTRADO','NOMBRE_O_RAZON_SOCIAL':'NOMBRE / RAZON SOCIAL','CATEGORÍA':'TIPO','DNI_RUC':'DNI / RUC'})
        self.tabla_adF = self.tabla_ad.loc[0:99, ['ID ADMINISTRADO','NOMBRE / RAZON SOCIAL','TIPO','DNI / RUC']]
        
        # Información para las listas desplegables
        self.listaAD = list(set(self.tabla_ad['NOMBRE / RAZON SOCIAL']))
        self.listaTIPO= list(set(self.tabla_ad['TIPO']))
        # Armando rejilla con los filtros

        self.rejilla_ad = (

            ('L', 0, 0, 'Administrado'),
            ('CXP', 0, 1, 39, self.listaAD, '', "normal"),

            ('L', 1, 0, 'Tipo'),
            ('CXP', 1, 1, 39, self.listaTIPO, '', "normal"),

            ('L', 0, 2, 'DNI / RUC'),
            ('E', 0, 3)
        )
        
        # Agregando rejilla a la ventana
        self.ad1 = Cuadro(self)
        self.ad1.agregar_rejilla(self.rejilla_ad)
        self.ad2 = Cuadro(self)
        self.ad2.agregar_rejilla(self.rejilla_ad2)

        self.frame_vitrina_ad = Cuadro(self)
        # Creando vitrina
        self.vad = Vitrina_busqueda(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, height=200, width=590)

    #----------------------------------------------------------------------
    def ver_ad(self, x):
        """"""
        #self.x = x
        #texto_documento = 'Documento emitido: ' + x
        print("Administrado")
        #bde = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS_FINAL')
        #lb1 = bde.listar_datos_de_fila(self.x)
        #lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], 
                                #lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        #self.desaparecer()
        #subframe = ventanas_vista.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                 #               nuevo=False, lista=lista_para_insertar, id_objeto=x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_ad(self, x):
        """"""
        print("hola")

    #----------------------------------------------------------------------
    def crear_adm(self, x):
        """"""
        print("hola")

class Pendientes_jefe_firma(funcionalidades_ospa):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.id_objeto_ingresado = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("FECHA_FIRMA=='' or FECHA_FIRMA==' '")
        self.tabla_0_pfirma = self.tabla_inicial1.rename(columns={'COD_DE':'HT','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
        self.tabla_pfirmaF = self.tabla_0_pfirma.loc[0:99, ['HT','DESTINATARIO','TIPO DOC','NRO DOCUMENTO','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.categoria = sorted(list(set(self.tabla_0_pfirma['CATEGORIA'])))
        self.destinatario = sorted(list(set(self.tabla_0_pfirma['DESTINATARIO'])))
        self.tipodocemitpfirma = sorted(list(set(self.tabla_0_pfirma['TIPO DOC'])))
        self.especialista = sorted(list(set(self.tabla_0_pfirma['ESPECIALISTA'])))

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

            ('L', 0, 2, 'Nro registro Siged'),
            ('EE', 0, 3),

            ('L', 0, 4, 'Destinatario'),
            ('CXE', 0, 5, 39, self.destinatario, '', 'normal'),

            ('L', 1, 0, 'Especialista'),
            ('CXP', 1, 1, 39, self.especialista, '', 'readonly'),

            ('L', 1, 2, 'Tipo de documento'),
            ('CXP', 1, 3, 39, self.tipodocemitpfirma, '', 'readonly'),

            ('L', 1, 4, 'Nro de documento'),
            ('EE', 1, 5)

        )
        
        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)

        # Generando rejilla para botones
        self.rejilla_2_pfirma = (
            ('B', 5, 4, 'Buscar', self.Buscar_pfirma),
            ('B', 5, 5, 'Limpiar', self.limpiar_pfirma),
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)

        # Creando vitrina
        self.vpfirma = Vitrina_pendientes(self, self.tabla_pfirmaF, 
                                                    self.ver_de, height=250, width=1190)

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

        self.filtro0 = self.tabla_0_pfirma
        self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)
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

        if len(self.espepfirma)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESPECIALISTA=="+"'"+self.espepfirma+"' "

        if len(self.docpfirma)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`NRO DOCUMENTO`=="+"'"+self.docpfirma+"' "
        
        self.mostrarDatospfirma(filtro)

    #----------------------------------------------------------------------

    def mostrarDatospfirma(self, filtro):

        self.filtro0 = self.tabla_0_pfirma
        
        if len(self.htpfirma)>0: # Filtro por palabra clave
            self.vpfirma.Eliminar_vitrina()
            self.filtro0['HT SALIDA']=self.filtro0['HT SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT SALIDA'].str.contains(self.htpfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.destinpfirma)>0: # Filtro por palabra clave
            self.vpfirma.Eliminar_vitrina()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.destinpfirma)]
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

        tabla_filtro2 = filtro0.loc[:, ['HT','DESTINATARIO','TIPO DOC','NRO DOCUMENTO','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_pfirma.eliminar_cuadro()
            self.frame_vitrina_pfirma = Cuadro(self)
            self.vpfirma = Vitrina_pendientes(self, tabla_filtro3, self.ver_de, height=250, width=1190)
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
        self.vpfirma = Vitrina_pendientes(self, self.tabla_pfirmaF, self.ver_de, height=250, width=1190)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.pfirma1.eliminar_cuadro()
        self.vpfirma.Eliminar_vitrina()
        self.pfirma15.eliminar_cuadro()
        self.frame_vitrina_pfirma.eliminar_cuadro()
        # Actualizando data
        b_de = vg.b_de
        b_de_tabla = b_de.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("FECHA_FIRMA=='' or FECHA_FIRMA==' '")
        self.tabla_0_pfirma = self.tabla_inicial1.rename(columns={'COD_DE':'HT','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
        self.tabla_pfirmaF = self.tabla_0_pfirma.loc[0:99, ['HT','DESTINATARIO','TIPO DOC','NRO DOCUMENTO','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.categoria = sorted(list(set(self.tabla_0_pfirma['CATEGORIA'])))
        self.destinatario = sorted(list(set(self.tabla_0_pfirma['DESTINATARIO'])))
        self.tipodocemitpfirma = sorted(list(set(self.tabla_0_pfirma['TIPO DOC'])))
        self.especialista = sorted(list(set(self.tabla_0_pfirma['ESPECIALISTA'])))

        # Armando rejilla con los filtros

        self.rejilla_pfirma = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 39, self.categoria, '', 'readonly'),

            ('L', 0, 2, 'Nro registro Siged'),
            ('EE', 0, 3),

            ('L', 0, 4, 'Destinatario'),
            ('CXE', 0, 5, 39, self.destinatario, '', 'normal'),

            ('L', 1, 0, 'Especialista'),
            ('CXP', 1, 1, 39, self.especialista, '', 'readonly'),

            ('L', 1, 2, 'Tipo de documento'),
            ('CXP', 1, 3, 39, self.tipodocemitpfirma, '', 'readonly'),

            ('L', 1, 4, 'Nro de documento'),
            ('EE', 1, 5)

        )

        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)
        # Creando vitrina
        self.vpfirma = Vitrina_pendientes(self, self.tabla_pfirmaF, self.ver_de, height=250, width=1190)
    
class Pendientes_jefe_asignar(funcionalidades_ospa):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_jpa = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_dr.generar_dataframe()
        #self.tabla_inicial1 = self.tabla_inicial0[self.tabla_inicial0['TIPO_RESPUESTA']!='Si']
        self.tabla_inicial2 = self.tabla_inicial0.query("ESPECIALISTA_1=='' or ESPECIALISTA_1==' '")
        self.tabla_jpa = self.tabla_inicial2.rename(columns={'COD_DR':'NRO DOCUMENTO','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_jpaF = self.tabla_jpa.loc[0:99, ['NRO DOCUMENTO','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','ASUNTO']]


        # Información para las listas desplegables
        self.jpatipodoc = sorted(list(set(self.tabla_jpa['TIPO DOC'])))
        self.jparemitente = sorted(list(set(self.tabla_jpa['REMITENTE'])))


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
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app),
        )
        
        # Agregando rejilla de botones a la ventana
        self.jpa15 = Cuadro(self)
        self.jpa15.agregar_rejilla(self.rejilla_jpa2)

        self.frame_vitrina_jpa = Cuadro(self)

        # Creando vitrina
        self.vjpa = Vitrina_pendientes(self, self.tabla_jpaF, self.ver_dr, height=200, width=770)
    
    #----------------------------------------------------------------------

    def Buscar_jpa(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro_jpa = self.jpa1.obtener_lista_de_datos()
        self.htjpa = self.listas_filtro_jpa[0]
        self.tipodocjpa = self.listas_filtro_jpa[1]
        self.remitentejpa = self.listas_filtro_jpa[2]
        self.nrodocjpa = self.listas_filtro_jpa[3]

        self.filtro0 = self.tabla_jpa
        self.filtro0['NUM_DOC']=self.filtro0['NUM_DOC'].apply(str)
        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodocjpa)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodocjpa+"' "

        if len(self.nrodocjpa)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"NUM_DOC=="+"'"+self.nrodocjpa+"' "
        
        self.mostrarDatosjpa(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatosjpa(self, filtro):

        self.filtro0 = self.tabla_jpa
        
        if len(self.remitentejpa)>0: # Filtro por palabra clave
            self.vjpa.Eliminar_vitrina()
            self.filtro0 = self.tabla_jpa[self.tabla_jpa['REMITENTE'].str.contains(self.remitentejpa)]
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

        tabla_filtro2 = filtro0.loc[:, ['NRO DOCUMENTO','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','ASUNTO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_jpa.eliminar_cuadro()
            self.frame_vitrina_jpa = Cuadro(self)
            self.vjpa = Vitrina_pendientes(self, tabla_filtro3, self.ver_dr, height=200, width=770)
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
        self.vjpa = Vitrina_pendientes(self, self.tabla_jpaF, self.ver_dr, height=200, width=770)


    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.jpa1.eliminar_cuadro()
        self.vjpa.Eliminar_vitrina()
        self.jpa15.eliminar_cuadro()
        self.frame_vitrina_jpa.eliminar_cuadro()
        # Actualizando data
        b_dr = vg.b_dr
        b_dr_tabla = b_dr.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_inicial2 = self.tabla_inicial0.query("ESPECIALISTA_1=='' or ESPECIALISTA_1==' '")
        self.tabla_jpa = self.tabla_inicial2.rename(columns={'COD_DR':'NRO DOCUMENTO','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_jpaF = self.tabla_jpa.loc[0:99, ['NRO DOCUMENTO','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','ASUNTO']]

        # Información para las listas desplegables
        self.jpatipodoc = sorted(list(set(self.tabla_jpa['TIPO DOC'])))
        self.jparemitente = sorted(list(set(self.tabla_jpa['REMITENTE'])))

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
        self.jpa15 = Cuadro(self)
        self.jpa15.agregar_rejilla(self.rejilla_jpa2)
        self.frame_vitrina_jpa = Cuadro(self)
        # Creando vitrina
        self.vjpa = Vitrina_pendientes(self, self.tabla_jpaF, self.ver_dr, height=200, width=770)

class Pendientes_por_reiterar(funcionalidades_ospa):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_ppr = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("ESTADO_DOCE=='Enviar reiterativo' or ESTADO_DOCE=='Eviar OCI'")
        self.tabla_ppr = self.tabla_inicial1.rename(columns={'COD_DE':'HT SALIDA','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
        self.tabla_pprF = self.tabla_ppr.loc[0:99, ['HT SALIDA','DESTINATARIO','NRO DOCUMENTO','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
 
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
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ppr15 = Cuadro(self)
        self.ppr15.agregar_rejilla(self.rejilla_2_ppr)
        self.frame_vitrina_ppr = Cuadro(self)

        # Creando vitrina
        self.vppr = Vitrina_pendientes(self, self.tabla_pprF, self.ver_de, height=200, width=1050)

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
        self.filtro0 = self.tabla_ppr
        self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)

        filtro=""
        if len(self.decateppr)>0 :
            filtro="CATEGORIA=="+"'"+self.decateppr+"' "
    
        if len(self.tipodocppr)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`TIPO DOC`=="+"'"+self.tipodocppr+"' "

        if len(self.docppr)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`NRO DOCUMENTO`=="+"'"+self.docppr+"' "
        
        self.mostrarDatosppr(filtro)

    #----------------------------------------------------------------------

    def mostrarDatosppr(self, filtro):

        self.filtro0 = self.tabla_ppr
        
        if len(self.htppr)>0: # Filtro por palabra clave
            self.vppr.Eliminar_vitrina()
            self.filtro0['HT_SALIDA']=self.filtro0['HT_SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT_SALIDA'].str.contains(self.htppr)]
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

        tabla_filtro2 = filtro0.loc[:, ['HT SALIDA','DESTINATARIO','NRO DOCUMENTO','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ppr.eliminar_cuadro()
            self.frame_vitrina_ppr = Cuadro(self)
            self.vppr = Vitrina_pendientes(self, tabla_filtro3, self.ver_de, height=200, width=1050)
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
        self.vppr = Vitrina_pendientes(self, self.tabla_pprF, self.ver_de, height=200, width=1050)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.ppr1.eliminar_cuadro()
        self.vppr.Eliminar_vitrina()
        self.ppr15.eliminar_cuadro()
        self.frame_vitrina_ppr.eliminar_cuadro()
        # Actualizando data
        b_de = vg.b_de
        b_de_tabla = b_de.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("ESTADO_DOCE=='Enviar reiterativo' or ESTADO_DOCE=='Eviar OCI'")
        self.tabla_ppr = self.tabla_inicial1.rename(columns={'COD_DE':'HT SALIDA','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
        self.tabla_pprF = self.tabla_ppr.loc[0:99, ['HT SALIDA','DESTINATARIO','NRO DOCUMENTO','ESPECIALISTA','FECHA PROYECTO','CATEGORIA','DETALLE']]
 
        # Información para las listas desplegables
        self.categoriappr = list(set(self.tabla_ppr['CATEGORIA']))
        self.destinatarioppr = list(set(self.tabla_ppr['DESTINATARIO']))
        self.tipodocemitpfirmappr = list(set(self.tabla_ppr['TIPO DOC']))
        self.especialistappr = list(set(self.tabla_ppr['ESPECIALISTA']))

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
        self.ppr15 = Cuadro(self)
        self.ppr15.agregar_rejilla(self.rejilla_2_ppr)
        self.frame_vitrina_ppr = Cuadro(self)
        # Creando vitrina
        self.vppr = Vitrina_pendientes(self, self.tabla_pprF, self.ver_de, height=200, width=1050)


    #----------------------------------------------------------------------

class Pendientes_eq1_trabajar(funcionalidades_ospa):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_peq1t = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("TIPO_RESPUESTA!='No'")
        self.tabla_peq1t = self.tabla_inicial1.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_peq1tF = self.tabla_peq1t.loc[0:99, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','INDICACION','ASUNTO']]
 
        # Información para las listas desplegables
        self.peq1ttipodoc = list(set(self.tabla_peq1t['TIPO DOC']))
        self.peq1tremitente = list(set(self.tabla_peq1t['REMITENTE']))

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
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.peq1t15 = Cuadro(self)
        self.peq1t15.agregar_rejilla(self.rejilla_peq1t2)

        self.frame_vitrina_peq1t = Cuadro(self)

        # Creando vitrina 
        self.vpeq1t = Vitrina_pendientes(self, self.tabla_peq1tF, self.ver_dr, height=200, width=1080)
    
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
            self.vpeq1t = Vitrina_pendientes(self, tabla_filtro3, self.ver_dr, height=200, width=1080)
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
        self.vpeq1t = Vitrina_pendientes(self, self.tabla_peq1tF, self.ver_dr, height=200, width=1080)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.peq1t1.eliminar_cuadro()
        self.vpeq1t.Eliminar_vitrina()
        self.peq1t15.eliminar_cuadro()
        self.frame_vitrina_peq1t.eliminar_cuadro()
        # Actualizando data
        b_dr = vg.b_dr
        b_dr_tabla = b_dr.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("TIPO_RESPUESTA!='No'")
        self.tabla_peq1t = self.tabla_inicial1.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_peq1tF = self.tabla_peq1t.loc[0:99, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','INDICACION','ASUNTO']]
 
        # Información para las listas desplegables
        self.peq1ttipodoc = list(set(self.tabla_peq1t['TIPO DOC']))
        self.peq1tremitente = list(set(self.tabla_peq1t['REMITENTE']))

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
        self.peq1t15 = Cuadro(self)
        self.peq1t15.agregar_rejilla(self.rejilla_peq1t2)
        self.frame_vitrina_peq1t = Cuadro(self)
        # Creando vitrina
        self.vpeq1t = Vitrina_pendientes(self, self.tabla_peq1tF, self.ver_dr, height=200, width=1080)
    #----------------------------------------------------------------------

class Pendientes_eq2_calificarrpta(funcionalidades_ospa):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_peq2t = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("TIPO_RESPUESTA=='Si'")
        #self.tabla_inicial2 = self.tabla_inicial1.query("RESPUESTA==' ' or RESPUESTA==''")
        self.tabla_peq2t = self.tabla_inicial1.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_peq2tF = self.tabla_peq2t.loc[0:99, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','ESPECIALISTA_1','INDICACION','ASUNTO']]
 
        # Información para las listas desplegables
        self.peq2ttipodoc = list(set(self.tabla_peq2t['TIPO DOC']))
        self.peq2tremitente = list(set(self.tabla_peq2t['REMITENTE']))
        self.peq2tespecialista = list(set(self.tabla_peq2t['ESPECIALISTA_1']))

        # Agregando logo del ospa a la ventana y título
        self.peq2t0 = Cuadro(self)
        self.peq2t0.agregar_label(0,0,' ')
        self.peq2t0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)
        peq2t2 = Cuadro(self)
        peq2t2.agregar_titulo(2, 0, 'Documentos pendientes de calificar respuesta')

        # Armando rejilla con los filtros
        self.rejilla_peq2t = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 39, self.peq2ttipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 39, self.peq2tremitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3),

            ('L', 2, 0, 'Especialista'),
            ('CXP', 2, 1, 39, self.peq2tespecialista, '', 'readonly')

        )

        # Agregando rejilla a la ventana
        self.peq2t1 = Cuadro(self)
        self.peq2t1.agregar_rejilla(self.rejilla_peq2t)

        # Generando rejilla para botones
        self.rejilla_peq2t2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_peq2t),
            ('B', 5, 5, 'Limpiar', self.limpiar_peq2t),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Actualizar', self.actualizar),
            ('B', 5, 8, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.peq2t15 = Cuadro(self)
        self.peq2t15.agregar_rejilla(self.rejilla_peq2t2)

        self.frame_vitrina_peq2t = Cuadro(self)

        # Creando vitrina 
        self.vpeq2t = Vitrina_pendientes(self, self.tabla_peq2tF, self.ver_dr, height=200, width=1170)


    #----------------------------------------------------------------------

    def Buscar_peq2t(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro_peq2t = self.peq2t1.obtener_lista_de_datos()
        self.htpeq2t = self.listas_filtro_peq2t[0]
        self.tipodocpeq2t = self.listas_filtro_peq2t[1]
        self.remitentepeq2t = self.listas_filtro_peq2t[2]
        self.nrodocpeq2t = self.listas_filtro_peq2t[3]
        self.especialistapeq2t = self.listas_filtro_peq2t[4]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodocpeq2t)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodocpeq2t+"' "

        if len(self.especialistapeq2t)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESPECIALISTA_1=="+"'"+self.especialistapeq2t+"' "
        
        self.mostrarDatospeq2t(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatospeq2t(self, filtro):

        self.filtro0 = self.tabla_peq2t
        
        if len(self.remitentepeq2t)>0: # Filtro por palabra clave
            self.vpeq2t.Eliminar_vitrina()
            self.filtro0 = self.tabla_peq2t[self.tabla_peq2t['REMITENTE'].str.contains(self.remitentepeq2t)]
            self.Complementopeq2t(self.filtro0)

        if len(self.nrodocpeq2t)>0: # Filtro por palabra clave
            self.vpeq2t.Eliminar_vitrina()
            self.filtro0['NRO DOC']=self.filtro0['NRO DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOC'].str.contains(self.nrodocpeq2t)]
            self.Complementopeq2t(self.filtro0)

        if len(self.htpeq2t)>0: # Filtro por palabra clave
            self.vpeq2t.Eliminar_vitrina()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.htpeq2t)]
            self.Complementopeq2t(self.filtro0)

        if len(filtro)>0:

            self.vpeq2t.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopeq2t(self.filtro1)

        else:
            self.vpeq2t.Eliminar_vitrina()
            self.Complementopeq2t(self.filtro0)

    #----------------------------------------------------------------------

    def Complementopeq2t(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','ESPECIALISTA_1','INDICACION','ASUNTO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_peq2t.eliminar_cuadro()
            self.frame_vitrina_peq2t = Cuadro(self)
            self.vpeq2t = Vitrina_pendientes(self, tabla_filtro3, self.ver_dr, height=200, width=1170)
        else:
            self.frame_vitrina_peq2t.eliminar_cuadro()
            self.frame_vitrina_peq2t = Cuadro(self)
            self.frame_vitrina_peq2t.agregar_label(1, 2, '                  0 documentos encontrados')

    #----------------------------------------------------------------------
    def limpiar_peq2t(self):
        
        # Eliminando campos
        self.peq2t1.eliminar_cuadro()
        self.vpeq2t.Eliminar_vitrina()
        self.peq2t15.eliminar_cuadro()
        self.frame_vitrina_peq2t.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.peq2t1 = Cuadro(self)
        self.peq2t1.agregar_rejilla(self.rejilla_peq2t)
        self.peq2t15 = Cuadro(self)
        self.peq2t15.agregar_rejilla(self.rejilla_peq2t2)
        self.frame_vitrina_peq2t = Cuadro(self)
        # Creando vitrina
        self.vpeq2t = Vitrina_pendientes(self, self.tabla_peq2tF, self.ver_dr, height=200, width=1270)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.peq2t1.eliminar_cuadro()
        self.vpeq2t.Eliminar_vitrina()
        self.peq2t15.eliminar_cuadro()
        self.frame_vitrina_peq2t.eliminar_cuadro()
        # Actualizando data
        b_dr = vg.b_dr
        b_dr_tabla = b_dr.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("TIPO_RESPUESTA=='Si'")
        #self.tabla_inicial2 = self.tabla_inicial1.query("RESPUESTA=='' or RESPUESTA==' '")
        self.tabla_peq2t = self.tabla_inicial1.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO'})
        self.tabla_peq2tF = self.tabla_peq2t.loc[0:99, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','ESPECIALISTA_1','INDICACION','ASUNTO']]
 
        # Información para las listas desplegables
        self.peq2ttipodoc = list(set(self.tabla_peq2t['TIPO DOC']))
        self.peq2tremitente = list(set(self.tabla_peq2t['REMITENTE']))
        self.peq2tespecialista = list(set(self.tabla_peq2t['ESPECIALISTA_1']))

        self.rejilla_peq2t = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 39, self.peq2ttipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 39, self.peq2tremitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3),

            ('L', 2, 0, 'Especialista'),
            ('CXP', 2, 1, 39, self.peq2tespecialista, '', 'readonly')

        )
        
        # Agregando rejilla a la ventana
        self.peq2t1 = Cuadro(self)
        self.peq2t1.agregar_rejilla(self.rejilla_peq2t)
        self.peq2t15 = Cuadro(self)
        self.peq2t15.agregar_rejilla(self.rejilla_peq2t2)
        self.frame_vitrina_peq2t = Cuadro(self)
        # Creando vitrina
        self.vpeq2t = Vitrina_pendientes(self, self.tabla_peq2tF, self.ver_dr, height=200, width=1270)

class Pendientes_eq2_programaciones(funcionalidades_ospa):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto_anterior = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # Almacenamos información herededa
        self.nuevo = nuevo
        self.tipo_objeto_anterior = tipo_objeto_anterior
        if self.nuevo != True: #en caso exista
            self.id_usuario = lista
            self.cod_doc_peq2pr = id_objeto

        # Generamos el dataframe a filtrar
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0[self.tabla_inicial0['CATEGORIA']=='Programación'] 
        self.tabla_peq2pr = self.tabla_inicial1.rename(columns={'COD_DE':'DOC EMITIDO','FECHA_PROYECTO_FINAL':'FECHA ACCION','FECHA_FIRMA':'FECHA PROGRAMACION','TIPO_DOC':'TIPO DOC','ESTADO_DOCE':'ESTADO','DOCUMENTO_ELABORADO':'¿SE EJECUTO?'})
        self.tabla_peq2prF = self.tabla_peq2pr.loc[0:99, ['DESTINATARIO','FECHA ACCION','FECHA PROGRAMACION','ESPECIALISTA','ESTADO','¿SE EJECUTO?']]
 
        # Información para las listas desplegables
        self.peq2prremitente = list(set(self.tabla_peq2pr['DESTINATARIO']))
        self.peq2prespecialista = list(set(self.tabla_peq2pr['ESPECIALISTA']))
        self.peq2prestado = list(set(self.tabla_peq2pr['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        self.peq2pr0 = Cuadro(self)
        self.peq2pr0.agregar_label(0,0,' ')
        self.peq2pr0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)
        peq2pr2 = Cuadro(self)
        peq2pr2.agregar_titulo(2, 0, 'Revisión de programaciones')

        # Armando rejilla con los filtros
        self.rejilla_peq2pr = (

            ('L', 0, 0, 'Remitente'),
            ('CXE', 0, 1, 39, self.peq2prremitente, '', 'normal'),

            ('L', 1, 0, 'Especialista'),
            ('CXP', 1, 1, 39, self.peq2prespecialista, '', 'readonly'),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 39, self.peq2prestado, '', 'readonly')

        )

        # Agregando rejilla a la ventana
        self.peq2pr1 = Cuadro(self)
        self.peq2pr1.agregar_rejilla(self.rejilla_peq2pr)

        # Generando rejilla para botones
        self.rejilla_peq2pr2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_peq2pr),
            ('B', 5, 5, 'Limpiar', self.limpiar_peq2pr),
            ('B', 5, 6, 'Actualizar', self.actualizar),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 8, 'Inicio', self.inicio_app)
        )
        
        # Agregando rejilla de botones a la ventana
        self.peq2pr15 = Cuadro(self)
        self.peq2pr15.agregar_rejilla(self.rejilla_peq2pr2)

        self.frame_vitrina_peq2pr = Cuadro(self)

        # Creando vitrina 
        self.vpeq2pr = Vitrina_pendientes(self, self.tabla_peq2prF, self.ver_de, height=200, width=900)

    #----------------------------------------------------------------------

    def Buscar_peq2pr(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro_peq2pr = self.peq2pr1.obtener_lista_de_datos()
        self.remitentepeq2pr = self.listas_filtro_peq2pr[0]
        self.especialistapeq2pr = self.listas_filtro_peq2pr[1]
        self.estadopeq2pr = self.listas_filtro_peq2pr[2]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.especialistapeq2pr)>0 :
            filtro="ESPECIALISTA=="+"'"+self.especialistapeq2pr+"' "

        if len(self.estadopeq2pr)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESTADO=="+"'"+self.estadopeq2pr+"' "
        
        self.mostrarDatospeq2pr(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatospeq2pr(self, filtro):

        self.filtro0 = self.tabla_peq2pr
        
        if len(self.remitentepeq2pr)>0: # Filtro por palabra clave
            self.vpeq2pr.Eliminar_vitrina()
            self.filtro0 = self.tabla_peq2pr[self.tabla_peq2pr['DESTINATARIO'].str.contains(self.remitentepeq2pr)]
            self.Complementopeq2pr(self.filtro0)

        if len(filtro)>0:

            self.vpeq2pr.Eliminar_vitrina()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopeq2pr(self.filtro1)

        else:
            self.vpeq2pr.Eliminar_vitrina()
            self.Complementopeq2pr(self.filtro0)

    #----------------------------------------------------------------------

    def Complementopeq2pr(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['DESTINATARIO','FECHA ACCION','FECHA PROGRAMACION','ESPECIALISTA','ESTADO','¿SE EJECUTO?']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_peq2pr.eliminar_cuadro()
            self.frame_vitrina_peq2pr = Cuadro(self)
            self.vpeq2pr = Vitrina_pendientes(self, tabla_filtro3, self.ver_de, height=200, width=900)
        else:
            self.frame_vitrina_peq2pr.eliminar_cuadro()
            self.frame_vitrina_peq2pr = Cuadro(self)
            self.frame_vitrina_peq2pr.agregar_label(1, 2, '                  0 programaciones encontradas')

    #----------------------------------------------------------------------
    def limpiar_peq2pr(self):
        
        # Eliminando campos
        self.peq2pr1.eliminar_cuadro()
        self.vpeq2pr.Eliminar_vitrina()
        self.peq2pr15.eliminar_cuadro()
        self.frame_vitrina_peq2pr.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.peq2pr1 = Cuadro(self)
        self.peq2pr1.agregar_rejilla(self.rejilla_peq2pr)
        self.peq2pr15 = Cuadro(self)
        self.peq2pr15.agregar_rejilla(self.rejilla_peq2pr2)
        self.frame_vitrina_peq2pr = Cuadro(self)
        # Creando vitrina
        self.vpeq2pr = Vitrina_pendientes(self, self.tabla_peq2prF, self.ver_de, height=200, width=900)

        #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.peq2pr1.eliminar_cuadro()
        self.vpeq2pr.Eliminar_vitrina()
        self.peq2pr15.eliminar_cuadro()
        self.frame_vitrina_peq2pr.eliminar_cuadro()
        # Actualizando data
        b_de = vg.b_de
        b_de_tabla = b_de.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0[self.tabla_inicial0['CATEGORIA']=='Programación'] 
        self.tabla_peq2pr = self.tabla_inicial1.rename(columns={'COD_DE':'DOC EMITIDO','FECHA_PROYECTO_FINAL':'FECHA ACCION','FECHA_FIRMA':'FECHA PROGRAMACION','TIPO_DOC':'TIPO DOC','ESTADO_DOCE':'ESTADO','DOCUMENTO_ELABORADO':'¿SE EJECUTO?'})
        self.tabla_peq2prF = self.tabla_peq2pr.loc[0:99, ['DESTINATARIO','FECHA ACCION','FECHA PROGRAMACION','ESPECIALISTA','ESTADO','¿SE EJECUTO?']]
 
        # Información para las listas desplegables
        self.peq2prremitente = list(set(self.tabla_peq2pr['DESTINATARIO']))
        self.peq2prespecialista = list(set(self.tabla_peq2pr['ESPECIALISTA']))
        self.peq2prestado = list(set(self.tabla_peq2pr['ESTADO']))

        self.rejilla_peq2pr = (

            ('L', 0, 0, 'Remitente'),
            ('CXE', 0, 1, 39, self.peq2prremitente, '', 'normal'),

            ('L', 1, 0, 'Especialista'),
            ('CXP', 1, 1, 39, self.peq2prespecialista, '', 'readonly'),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 39, self.peq2prestado, '', 'readonly')

        )
        
        # Agregando rejilla a la ventana
        self.peq2pr1 = Cuadro(self)
        self.peq2pr1.agregar_rejilla(self.rejilla_peq2pr)
        self.peq2pr15 = Cuadro(self)
        self.peq2pr15.agregar_rejilla(self.rejilla_peq2pr2)
        self.frame_vitrina_peq2pr = Cuadro(self)
        # Creando vitrina
        self.vpeq2pr = Vitrina_pendientes(self, self.tabla_peq2prF, self.ver_de, height=200, width=900)