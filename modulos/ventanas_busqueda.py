from tkinter import Message, messagebox
import datetime as dt
import pandas as pd
import numpy as np
from apoyo.elementos_de_GUI import Cuadro, Ventana, Vitrina
from apoyo.manejo_de_bases import Base_de_datos
from modulos import ventanas_vista, menus
import apoyo.datos_frecuentes as df
from apoyo.funcionalidades_ospa import funcionalidades_ospa


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
        b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
        b_dr_tabla = b_dr.generar_dataframe()
        self.tabla_inicial = b_dr_tabla
        self.tabla_renombrada = self.renombrar_encabezados(self.tabla_inicial, tipo_base = 'dr')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'dr')
        self.tabla_drF = self.tabla_seleccionada.head(100)
        
        # Información para las listas desplegables
        self.listatipodoc = sorted(list(set(self.tabla_renombrada['TIPO DOC'])))
        self.listaremitente = sorted(list(set(self.tabla_renombrada['REMITENTE'])))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Búsqueda de documentos recibidos', 
                                            self.inicio_app, self.cerrar_sesion)

        # Armando rejilla con los filtros
        self.rejilla_dr = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 44, self.listatipodoc, '', 'readonly'),

            ('L', 1, 2, 'Nro de documento'),
            ('EE', 1, 3),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 44, self.listaremitente, '', 'normal'),

            ('L', 0, 4, 'Palabra clave asunto doc.'),
            ('EE', 0, 5)

        )

        # Agregando rejilla a la ventana
        self.rejilla_1 = Cuadro(self)
        self.rejilla_1.agregar_rejilla(self.rejilla_dr)

        # Generando rejilla para botones
        self.rejilla_b = (
            ('B', 5, 4, 'Buscar', self.Buscardr),
            ('B', 5, 5, 'Limpiar', self.limpiar),
            ('B', 5, 6, 'Actualizar', self.actualizar_dr),
            ('B', 5, 7, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.rejilla_2 = Cuadro(self)
        self.rejilla_2.agregar_rejilla(self.rejilla_b)
        self.frame_vitrina_dr = Cuadro(self)

        # Creando vitrina
        self.vdr = Vitrina(self, self.tabla_drF, self.ver_dr, 
                                   self.asociar_dr_de, funcion3 =None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_vitrina)
        
        # Franja inferior
        self.franjai = Cuadro(self)
        self.franjai.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

    #----------------------------------------------------------------------  
    def Buscardr(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro = self.rejilla_1.obtener_lista_de_datos()
        self.ht = self.listas_filtro[0]
        self.tipodoc = self.listas_filtro[1]
        self.nrodoc = self.listas_filtro[2]
        self.remitente = self.listas_filtro[3]
        self.aporte = self.listas_filtro[4]

        self.filtro0 = self.tabla_renombrada
        self.filtro0['NUM_DOC']=self.filtro0['NUM_DOC'].apply(str)

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodoc)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodoc+"' "

        
        self.mostrarDatosdr(filtro)

    #----------------------------------------------------------------------  
    def mostrarDatosdr(self, filtro):

        self.filtro0 = self.tabla_renombrada
        
        if len(self.remitente)>0: # Filtro por palabra clave
            self.vdr.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['REMITENTE'].str.contains(self.remitente)]
            self.Complementodr(self.filtro0)

        if len(self.ht)>0: # Filtro por palabra clave
            self.vdr.eliminar_vitrina2()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.ht)]
            self.Complementodr(self.filtro0)

        if len(self.nrodoc)>0: # Filtro por palabra clave
            self.vdr.eliminar_vitrina2()
            self.filtro0['NUM_DOC']=self.filtro0['NUM_DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NUM_DOC'].str.contains(self.nrodoc)]
            self.Complementodr(self.filtro0)
            
        if len(self.aporte)>0: # Filtro por palabra clave
            self.vdr.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['ASUNTO'].str.contains(self.aporte)]
            self.Complementodr(self.filtro0)

        if len(filtro)>0:

            self.vdr.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementodr(self.filtro1)

        else:
            self.vdr.eliminar_vitrina2()
            self.Complementodr(self.filtro0)

    #----------------------------------------------------------------------

    def Complementodr(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'dr')
        self.tabla = self.tabla_seleccionada.loc[:]

        if len(self.tabla.index) > 100:
            tabla_final = self.tabla.head(100)
        else:
            tabla_final = self.tabla
        if len(tabla_final.index) > 0:
            self.frame_vitrina_dr.eliminar_cuadro()
            self.frame_vitrina_dr = Cuadro(self)
            self.vdr = Vitrina(self, tabla_final, self.ver_dr, 
                                   self.asociar_dr_de, funcion3 =None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_vitrina)
        else:
            self.frame_vitrina_dr.eliminar_cuadro()
            self.frame_vitrina_dr = Cuadro(self)
            self.frame_vitrina_dr.agregar_label(1, 2, '                  0 documentos encontrados')
            self.frame_vitrina_dr.agregar_label(2, 2, ' ')
            self.frame_vitrina_dr.agregar_label(3, 2, ' ')
            self.frame_vitrina_dr.agregar_label(4, 2, ' ')
            self.frame_vitrina_dr.agregar_label(5, 2, ' ')
    #----------------------------------------------------------------------
    def limpiar(self):

        # Eliminando campos
        self.rejilla_1.eliminar_cuadro()
        self.vdr.eliminar_vitrina2()
        self.rejilla_2.eliminar_cuadro()
        self.frame_vitrina_dr.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.rejilla_1 = Cuadro(self)
        self.rejilla_1.agregar_rejilla(self.rejilla_dr)
        self.rejilla_2 = Cuadro(self)
        self.rejilla_2.agregar_rejilla(self.rejilla_b)
        self.frame_vitrina_dr = Cuadro(self)
        # Creando vitrina
        self.vdr = Vitrina(self, self.tabla_drF, self.ver_dr, 
                                   self.asociar_dr_de, funcion3 =None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_vitrina)

    #----------------------------------------------------------------------
    def asociar_dr_de(self, x):
        """"""
        self.x = x

        if self.nuevo == True:
            messagebox.showinfo("Error", "No tiene antecedente que pueda asociarse")
        else:
            
            #OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
            b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
            self.IDDR = b_dr.listar_datos_de_fila(self.x)
            self.IDDR_FINAL = self.IDDR[0]

            #OBTENER EL ID USUARIO DEL DOCUMENTO EMITIDO
            codigode = self.id_objeto_ingresado
            # OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO.
            b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
            tabla_de_codigo_de = b_de.generar_dataframe()
            tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de.COD_DE == codigode]
            id_interno_de = tabla_codigo_de_filtrada.iloc[0,0]
        
            # Definición de ID de relación
            id_relacion_doc = self.IDDR_FINAL + "/" + id_interno_de

            # BUSCAR COINCIDENCIAS
            base_relacion_docs = Base_de_datos(df.id_b_parametros, 'RELACION_DOCS')
            valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)

            # BUSCAR ESTADO DE ID RELACION SI EXISTE
            if valor_repetido != False:  # si hay coincidencias de ese id_relacion_doc
                tabla_de_relaciones = base_relacion_docs.generar_dataframe()
                tabla_relaciones_filtrada = tabla_de_relaciones[tabla_de_relaciones['ID_DOCS_R'] == id_relacion_doc]
                estado_rela = tabla_relaciones_filtrada.iloc[0,3]

            hora_de_modificacion = str(dt.datetime.now())

            if valor_repetido != True:
            
                # GUARDAR RELACION
                b0 = Base_de_datos('1wDGtiCiT92K1lP62SQ0nBr_nuBQiHlJ17CPysdVMPM8', 'RELACION_DOCS')

                # Pestaña 1: Código Único
                datos_insertar = [id_relacion_doc,self.IDDR_FINAL,id_interno_de,'ACTIVO',hora_de_modificacion]
                b0.agregar_datos(datos_insertar)
                datos_a_cargar_hist = [id_relacion_doc,self.IDDR_FINAL,id_interno_de,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
                base_relacion_d_hist = Base_de_datos(df.id_b_parametros, 'HISTORIAL_RELACION_D')
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
            base_relacion_dr_pr =  Base_de_datos(df.id_b_parametros, 'RELACION_DR-PR')
            tabla_de_dr_ep = base_relacion_dr_pr.generar_dataframe()
            # 2. Filtro las relaciones que tiene el DE
            # Filtro para obtener las relaciones activas
            tabla_relacion_activos = tabla_de_dr_ep[tabla_de_dr_ep['ESTADO']=="ACTIVO"]
            # Con ese ID, filtro la tabla de relacion
            tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos['ID_DR']==self.IDDR_FINAL]
            # 3. Obtengo el ID de los EP que están relacionados al DE
            # Me quedo con el vector a filtrar en forma de lista
            lista_ep = list(tabla_relacion_filtrada['ID_PR'].unique())
            # 4. Concateno los ID de los EP relacionados al DE con el ID del DR
            if len(lista_ep) > 0:
                for indice in range(len(lista_ep)):
                    cod_relacion = id_interno_de + "/" + lista_ep[indice]
                    datos_insertar = [cod_relacion, id_interno_de, lista_ep[indice], 'ACTIVO', hora_de_modificacion] 
                    base_relacion_de_pr =  Base_de_datos(df.id_b_parametros, 'RELACION_DE-PR')
                    base_relacion_de_pr.agregar_datos(datos_insertar)
            #else:
            #    messagebox.showinfo("¡Atención!", "El registro ha sido asociado con éxito")

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
        b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
        b_de_tabla = b_de.generar_dataframe()
        self.tabla_inicial = b_de_tabla
        self.tabla_renombrada = self.renombrar_encabezados(self.tabla_inicial, tipo_base = 'de')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'de')
        self.tabla_deF = self.tabla_seleccionada.head(100)
       
        # Información para las listas desplegables
        self.listacategoria = sorted(list(set(self.tabla_renombrada['CATEGORIA'])))
        self.listadestinatario = sorted(list(set(self.tabla_renombrada['DESTINATARIO'])))
        self.listatipodocemit = sorted(list(set(self.tabla_renombrada['TIPO DOC'])))
        self.listaestado = sorted(list(set(self.tabla_renombrada['ESTADO'])))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Búsqueda de documentos emitidos', 
                                            self.inicio_app, self.cerrar_sesion)

        # Armando rejilla con los filtros

        self.rejilla_de = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 44, self.listacategoria, '', 'readonly'),

            ('L', 0, 2, 'Nro registro Siged'),
            ('EE', 0, 3),

            ('L', 0, 4, 'Destinatario'),
            ('CXE', 0, 5, 44, self.listadestinatario, '', 'normal'),

            ('L', 1, 0, 'Estado'),
            ('CXE', 1, 1, 44, self.listaestado, '', 'normal'),

            ('L', 1, 2, 'Tipo de documento'),
            ('CXP', 1, 3, 44, self.listatipodocemit, '', 'readonly'),

            ('L', 1, 4, 'Nro de documento'),
            ('EE', 1, 5),

            ('L', 2, 0, 'Palabra clave detalle doc.'),
            ('EE', 2, 1)

        )
        
        # Agregando rejilla a la ventana
        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)

        # Generando rejilla para botones
        self.rejilla_bde = (
            ('B', 5, 4, 'Buscar', self.Buscar_de),
            ('B', 5, 5, 'Limpiar', self.limpiar_de),
            ('B', 5, 6, 'Actualizar', self.actualizar_de),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 9, 'Emitir doc', self.nuevo_de)
        )
        
        # Agregando rejilla de botones a la ventana
        self.cde15 = Cuadro(self)
        self.cde15.agregar_rejilla(self.rejilla_bde)
        self.frame_vitrina_1 = Cuadro(self)

        # Creando vitrina
        self.vde1 = Vitrina(self, self.tabla_deF, self.ver_de, 
                                    self.asociar_de_dr, funcion3 =None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_de_vitrina)
        
        # Franja inferior
        self.cde16 = Cuadro(self)
        self.cde16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

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
        self.detalle = self.listas_filtrode[6]

        self.filtro0 = self.tabla_renombrada
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

        self.filtro0 = self.tabla_renombrada
        
        if len(self.deid)>0: # Filtro por palabra clave
            self.vde1.eliminar_vitrina2()
            self.filtro0['HT SALIDA']=self.filtro0['HT SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT SALIDA'].str.contains(self.deid)]
            self.Complementode(self.filtro0)

        if len(self.dedoc)>0: # Filtro por palabra clave
            self.vde1.eliminar_vitrina2()
            self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOCUMENTO'].str.contains(self.dedoc)]
            self.Complementode(self.filtro0)

        if len(self.dedestin)>0: # Filtro por palabra clave
            self.vde1.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.dedestin)]
            self.Complementode(self.filtro0)

        if len(self.deestado)>0: # Filtro por palabra clave
            self.vde1.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['ESTADO'].str.contains(self.deestado)]
            self.Complementode(self.filtro0)

        if len(self.detalle)>0: # Filtro por palabra clave
            self.vde1.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DETALLE'].str.contains(self.detalle)]
            self.Complementode(self.filtro0)
  
        if len(filtro)>0:

            self.vde1.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementode(self.filtro1)

        else:
            self.vde1.eliminar_vitrina2()
            self.Complementode(self.filtro0)

    #----------------------------------------------------------------------
    def Complementode(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'de')
        self.tabla = self.tabla_seleccionada.loc[:]
        if len(self.tabla.index) > 100:
            tabla_filtro3 = self.tabla.head(100)
        else:
            tabla_filtro3 = self.tabla
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.vde1 = Vitrina(self, tabla_filtro3, self.ver_de, self.asociar_de_dr, funcion3 =None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_de_vitrina)
           
        else:
            self.frame_vitrina_1.eliminar_cuadro()
            self.frame_vitrina_1 = Cuadro(self)
            self.frame_vitrina_1.agregar_label(1, 2, '                  0 documentos encontrados')
        
    #----------------------------------------------------------------------

    def limpiar_de(self):

        # Eliminando campos
        self.cde1.eliminar_cuadro()
        self.vde1.eliminar_vitrina2()
        self.cde15.eliminar_cuadro()
        self.frame_vitrina_1.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)
        self.cde15 = Cuadro(self)
        self.cde15.agregar_rejilla(self.rejilla_bde)
        self.frame_vitrina_1 = Cuadro(self)
        # Creando vitrina
        self.vde1 = Vitrina(self, self.tabla_deF, self.ver_de, 
                                    self.asociar_de_dr, funcion3 =None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_de_vitrina)
        
    #----------------------------------------------------------------------
    def asociar_de_dr(self, x):
        """"""
        self.x = x

        if self.nuevo == True:
            messagebox.showinfo("Error", "No tiene antecedente que pueda asociarse")
        else:

            #OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
            b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
            self.IDDE = b_de.listar_datos_de_fila(self.x)
            self.IDDE_FINAL = self.IDDE[0]

            #OBTENER EL ID USUARIO DEL DOCUMENTO RECIBIDO
            codigodr = self.id_objeto_ingresado
            # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
            b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
            tabla_de_codigo_dr = b_dr.generar_dataframe()
            tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == codigodr]
            id_interno_dr = tabla_codigo_de_filtrada.iloc[0,0]

            # Definición de ID de relación
            id_relacion_doc = id_interno_dr + "/" +  self.IDDE_FINAL

            # BUSCAR COINCIDENCIAS
            base_relacion_docs = Base_de_datos(df.id_b_parametros, 'RELACION_DOCS')
            valor_repetido = self.comprobar_id(base_relacion_docs, id_relacion_doc)
            hora_de_modificacion = str(dt.datetime.now())

            if valor_repetido == False:
            
                # GUARDAR RELACION
                b0 = Base_de_datos('1wDGtiCiT92K1lP62SQ0nBr_nuBQiHlJ17CPysdVMPM8', 'RELACION_DOCS')

                # Pestaña 1: Código Único
                datos_insertar = [id_relacion_doc,id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion]
                b0.agregar_datos(datos_insertar)
                datos_a_cargar_hist = [id_relacion_doc, id_interno_dr, self.IDDE_FINAL,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
                base_relacion_d_hist = Base_de_datos(df.id_b_parametros, 'HISTORIAL_RELACION_D')
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
        b_pr = Base_de_datos(df.id_b_problemas, 'PROBLEMA')
        b_ep_tabla = b_pr.generar_dataframe()
        self.tabla_renombrada = self.renombrar_encabezados(b_ep_tabla, tipo_base = 'ep')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'ep')
        self.tabla_epF = self.tabla_seleccionada.head(100)

        # Listas para desplegables
        #self.listaAG = sorted(list(set(self.tabla_renombrada['AGENT. CONTAMI.'])))
        #self.listaCA = sorted(list(set(self.tabla_renombrada['COMPONEN. AMBIE.'])))
        #self.listaACT = sorted(list(set(self.tabla_renombrada['ACTIVIDAD'])))
        #self.listaTIPOUBI = sorted(list(set(self.tabla_renombrada['TIPO DE UBICACION'])))
        #self.listaOCURR = sorted(list(set(self.tabla_renombrada['OCURRENCIA'])))
        #self.listaEFA = sorted(list(set(self.tabla_renombrada['EFA'])))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Búsqueda de problemas', 
                                            self.inicio_app, self.cerrar_sesion)
    
        b_lista_efa = Base_de_datos(df.id_b_lista_efa, 'Lista de EFA')
        tabla_lista_efa = b_lista_efa.generar_dataframe()
        # Armando rejilla con los filtros
        self.rejilla_ep = (

            #('L', 0, 0, 'Agente contaminante'),
            #('CXP', 0, 1, 44, self.listaAG, '', "readonly"),

            #('L', 0, 2, 'Componente ambiental'),
            #('CXP', 0, 3, 44, self.listaCA, '', "readonly"),

            #('L', 0, 4, 'Actividad'),
            #('CXP', 0, 5, 44, self.listaACT, '', "readonly"),

            ('L', 0, 0, 'Departamento'),
            ('CXDEP3', 0, 1, 44, tabla_lista_efa, "Triple",
            'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

            #('L', 2, 0, 'Tipo de ubicación'),
            #('CXP', 2, 1, 44, self.listaTIPOUBI, '', "readonly"),

            #('L', 2, 2, 'Ocurrencia'),
            #('CXP', 2, 3, 44, self.listaOCURR, '', "readonly"),

            #('L', 2, 4, 'EFA'),
            #('CXE', 2, 5, 44, self.listaEFA, '', "normal"),

            ('L', 1, 0, 'Palabra clave en descripción'),
            ('EE', 1, 1),

            ('L', 1, 2, 'Código problema'),
            ('EE', 1, 3)

        )
        
        # Agregando rejilla a la ventana
        self.ep1 = Cuadro(self)
        self.ep1.agregar_rejilla(self.rejilla_ep)

        # Generando rejilla para botones
        self.rejilla_ep2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_ep),
            ('B', 5, 5, 'Limpiar', self.limpiar_ep),
            ('B', 5, 6, 'Actualizar', self.actualizar_ep),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 9, 'Crear extremo', self.nuevo_ep)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ep2 = Cuadro(self)
        self.ep2.agregar_rejilla(self.rejilla_ep2)
        self.frame_vitrina_ep = Cuadro(self)

        # Creando vitrina
        self.vep = Vitrina(self, self.tabla_epF, self.ver_ep, self.asociar_ep, self.ver_mp_ep, tipo_vitrina = "Modelo4", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_ep_vitrina)
        
        # Franja inferior
        self.ep3 = Cuadro(self)
        self.ep3.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

    #----------------------------------------------------------------------
    
    def Buscar_ep(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtroep = self.ep1.obtener_lista_de_datos()
        #self.AG = self.listas_filtroep[0]
        #self.CA = self.listas_filtroep[1]
        #self.ACTIVIDAD = self.listas_filtroep[2]
        self.DEPART = self.listas_filtroep[0]
        self.PROVI = self.listas_filtroep[1]
        self.DISTR = self.listas_filtroep[2]
        #self.TIPOUBI = self.listas_filtroep[6]
        #self.OCURRE = self.listas_filtroep[7]
        #self.EFA = self.listas_filtroep[8]
        self.CLAVE = self.listas_filtroep[3]
        self.codigo = self.listas_filtroep[4]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.DEPART)>0 :
            filtro="DEPARTAMENTO=="+"'"+self.DEPART+"' "
    
        #if len(self.CA)>0 :
        #    if len(filtro)>0 :
        #        filtro = filtro+" & "
        #    else:
        #        filtro
        #    filtro=filtro+"`COMPONEN. AMBIE.`=="+"'"+self.CA+"' "

        #if len(self.ACTIVIDAD)>0 :
        #    if len(filtro)>0 :
        #        filtro = filtro+" & "
        #    else:
        #        filtro
        #    filtro=filtro+"ACTIVIDAD=="+"'"+self.ACTIVIDAD+"' "

        #if len(self.DEPART)>0 :
        #    if len(filtro)>0 :
        #        filtro = filtro+" & "
        #    else:
        #        filtro
        #    filtro=filtro+"DEPARTAMENTO=="+"'"+self.DEPART+"' "

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

        #if len(self.TIPOUBI)>0 :
        #    if len(filtro)>0 :
        #        filtro = filtro+" & "
        #    else:
        #        filtro
        #    filtro=filtro+"`TIPO DE UBICACION`=="+"'"+self.TIPOUBI+"' "

        #if len(self.OCURRE)>0 :
        #    if len(filtro)>0 :
        #        filtro = filtro+" & "
        #    else:
        #        filtro
        #    filtro=filtro+"OCURRENCIA=="+"'"+self.OCURRE+"' "

        if len(self.codigo)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"`CODIGO EXTREMO`=="+"'"+self.codigo+"' "
        
        self.mostrarDatosep(filtro)       

    #----------------------------------------------------------------------

    def mostrarDatosep(self, filtro):

        self.filtro0 = self.tabla_renombrada
        
        #if len(self.EFA)>0: # Filtro por palabra clave
        #    self.vep.eliminar_vitrina2()
        #    self.filtro0 = self.filtro0[self.filtro0['EFA'].str.contains(self.EFA)]
        #    self.Complementoep(self.filtro0)

        if len(self.CLAVE)>0: # Filtro por palabra clave
            self.vep.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESCRIPCION'].str.contains(self.CLAVE)]
            self.Complementoep(self.filtro0)
  
        if len(filtro)>0:

            self.vep.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementoep(self.filtro1)

        else:
            self.vep.eliminar_vitrina2()
            self.Complementoep(self.filtro0)

    #----------------------------------------------------------------------

    def Complementoep(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'ep')
        self.tabla = self.tabla_seleccionada.loc[:]
        if len(self.tabla.index) > 100:
            tabla_filtro3 = self.tabla.head(100)
        else:
            tabla_filtro3 = self.tabla
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ep.eliminar_cuadro()
            self.frame_vitrina_ep = Cuadro(self)
            self.vep = Vitrina(self, tabla_filtro3, self.ver_ep, self.asociar_ep, self.ver_mp_ep, tipo_vitrina = "Modelo4", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_ep_vitrina)
        else:
            self.frame_vitrina_ep.eliminar_cuadro()
            self.frame_vitrina_ep = Cuadro(self)
            self.frame_vitrina_ep.agregar_label(1, 2, '                  0 extremos encontrados')
           
    #----------------------------------------------------------------------
    def limpiar_ep(self):
     
         # Eliminando campos
        self.ep1.eliminar_cuadro()
        self.vep.eliminar_vitrina2()
        self.ep2.eliminar_cuadro()
        self.frame_vitrina_ep.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.ep1 = Cuadro(self)
        self.ep1.agregar_rejilla(self.rejilla_ep)
        self.ep2 = Cuadro(self)
        self.ep2.agregar_rejilla(self.rejilla_ep2)
        self.frame_vitrina_ep = Cuadro(self)
        self.vep = Vitrina(self, self.tabla_epF, self.ver_ep, self.asociar_ep, self.ver_mp_ep, tipo_vitrina = "Modelo4", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_ep_vitrina)
          
    #----------------------------------------------------------------------
    def ver_mp_ep(self, x):
        """"""
        self.x = x
        texto_documento = 'Problema: ' + x

        tabla_codigo_de_filtrada = self.tabla_renombrada.query("`CODIGO EXTREMO`==@self.x")
        self.id_interno_ep = tabla_codigo_de_filtrada.iloc[0,0]
        tabla_codigo_de_filtrada2 = tabla_codigo_de_filtrada['ID_PR'].tolist()
        b_relacion_mp_pr =  Base_de_datos(df.id_b_parametros, 'RELACION_MP-PR')
        self.relacion_mp_ep = b_relacion_mp_pr.generar_dataframe()
        relacion_activos = self.relacion_mp_ep[self.relacion_mp_ep.ID_PR.isin(tabla_codigo_de_filtrada2)]
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
            b_pr = Base_de_datos(df.id_b_problemas, 'PROBLEMA')
            self.IDEP = b_pr.listar_datos_de_fila(self.x)
            self.IDEP_FINAL = self.IDEP[0]

            #OBTENER EL ID USUARIO DEL OBJETO A ASOCIAR
            id_objeto_anterior = self.id_objeto_ingresado
            # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
            if self.tipo_objeto_anterior == "DR":
                b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
                tabla_de_codigo_dr = b_dr.generar_dataframe()
                tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_DR == id_objeto_anterior]
                base_relacion_dr_pr =  Base_de_datos(df.id_b_parametros, 'RELACION_DR-PR')
                base_relacion_objetos = base_relacion_dr_pr
                base_relacion_dr_pr_hist =  Base_de_datos(df.id_b_parametros, 'HISTORIAL_RELACION_DR-PR')
                base_relacion_objetos_hist = base_relacion_dr_pr_hist
            elif self.tipo_objeto_anterior == "MP":
                b_mp = Base_de_datos(df.id_b_problemas, 'MACROPROBLEMA')
                tabla_de_codigo_dr = b_mp.generar_dataframe()
                tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.COD_MP == id_objeto_anterior]
                b_relacion_mp_pr =  Base_de_datos(df.id_b_parametros, 'RELACION_MP-PR')
                base_relacion_objetos = b_relacion_mp_pr
                base_relacion_mp_pr_hist =  Base_de_datos(df.id_b_parametros, 'HISTORIAL_RELACION_MP-PR')
                base_relacion_objetos_hist = base_relacion_mp_pr_hist
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
        b_mp = Base_de_datos(df.id_b_problemas, 'MACROPROBLEMA')
        b_mp_tabla = b_mp.generar_dataframe()
        self.tabla_renombrada = self.renombrar_encabezados(b_mp_tabla, tipo_base = 'mp')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'mp')
        self.tabla_mpF = self.tabla_seleccionada.head(100)

        # Listas para desplegables
        self.listaestado = list(set(self.tabla_renombrada['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Búsqueda de Macroproblemas', 
                                            self.inicio_app, self.cerrar_sesion)
    
        # Armando rejilla con los filtros
        self.rejilla_mp = (

            ('L', 0, 0, 'Código de Macroproblema'),
            ('EE', 0, 1),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 44, self.listaestado, '', "readonly"),

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
            ('B', 5, 6, 'Actualizar', self.actualizar_bmp),
            ('B', 5, 7, 'Volver', self.volver),
            ('B', 5, 9, 'Crear macrop.', self.crear_macroproblema)
        )
        
        # Agregando rejilla de botones a la ventana
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)
        self.frame_vitrina_mp = Cuadro(self)

        # Creando vitrina
        self.vmc = Vitrina(self, self.tabla_mpF, self.ver_mp, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)

        # Franja inferior
        self.mc3 = Cuadro(self)
        self.mc3.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

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

        self.filtro0 = self.tabla_renombrada
        
        if len(self.NOMBRE)>0: # Filtro por palabra clave
            self.vmc.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['NOMBRE PROBLEMA'].str.contains(self.NOMBRE)]
            self.Complementomc(self.filtro0)

        if len(self.DESCRIP)>0: # Filtro por palabra clave
            self.vmc.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESCRIPCION'].str.contains(self.DESCRIP)]
            self.Complementomc(self.filtro0)
  
        if len(filtro)>0:

            self.vmc.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementomc(self.filtro1)

        else:
            self.vmc.eliminar_vitrina2()
            self.Complementomc(self.filtro0)

    #----------------------------------------------------------------------

    def Complementomc(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'mp')
        self.tabla = self.tabla_seleccionada.loc[:]

        if len(self.tabla.index) > 100:
            tabla_filtro3 = self.tabla.head(100)
        else:
            tabla_filtro3 = self.tabla

        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.vmc = Vitrina(self, tabla_filtro3, self.ver_mp, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)
            
        else:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.frame_vitrina_mp.agregar_label(1, 2, '                  0 macroproblemas encontrados')
            
    #----------------------------------------------------------------------
    def limpiar_mp(self):
     
         # Eliminando campos
        self.mc1.eliminar_cuadro()
        self.vmc.eliminar_vitrina2()
        self.mc2.eliminar_cuadro()
        self.frame_vitrina_mp.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)
        self.frame_vitrina_mp = Cuadro(self)
        # Creando vitrina
        self.vmc = Vitrina(self, self.tabla_mpF, self.ver_mp, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)
        
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
        b_mp = Base_de_datos(df.id_b_problemas, 'MACROPROBLEMA')
        b_mp_tabla = b_mp.generar_dataframe()
        self.mc = b_mp_tabla

        self.mc = self.mc[self.mc.ID_MP.isin(self.listamc)]

        self.tabla_renombrada = self.renombrar_encabezados(self.mc, tipo_base = 'mp')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'mp')
        self.tabla_mpF = self.tabla_seleccionada.head(100)

        #self.tabla_mp = self.mc.rename(columns={'COD_MP':'COD. MACROPROBLEMA','NOMBRE_DEL_PROBLEMA':'NOMBRE PROBLEMA','FECHA_DE_CREACION':'FECHA CREACION'})
        #self.tabla_mpF = self.tabla_mp.loc[0:99, ['COD. MACROPROBLEMA','FECHA CREACION','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
        
        # Listas para desplegables
        self.listaestado = list(set(self.tabla_renombrada['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Búsqueda de Macroproblemas filtrada', 
                                            self.inicio_app, self.cerrar_sesion)
    
        # Armando rejilla con los filtros
        self.rejilla_mp = (

            ('L', 0, 0, 'Código de Macroproblema'),
            ('EE', 0, 1),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 44, self.listaestado, '', "readonly"),

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
            ('B', 5, 6, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)
        self.frame_vitrina_mp = Cuadro(self)

        # Creando vitrina
        self.vmc = Vitrina(self, self.tabla_mpF, self.ver_mp, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mpf_vitrina)

        # Franja inferior
        self.mc3 = Cuadro(self)
        self.mc3.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

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

        self.filtro0 = self.tabla_renombrada
        
        if len(self.NOMBREf)>0: # Filtro por palabra clave
            self.vmc.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['NOMBRE PROBLEMA'].str.contains(self.NOMBREf)]
            self.Complementomcf(self.filtro0)

        if len(self.DESCRIPf)>0: # Filtro por palabra clave
            self.vmc.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESCRIPCION'].str.contains(self.DESCRIPf)]
            self.Complementomcf(self.filtro0)
  
        if len(filtro)>0:

            self.vmc.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementomcf(self.filtro1)

        else:
            self.vmc.eliminar_vitrina2()
            self.Complementomcf(self.filtro0)

    #----------------------------------------------------------------------

    def Complementomcf(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'mp')
        self.tabla = self.tabla_seleccionada.loc[:]

        if len(self.tabla.index) > 100:
            tabla_filtro3 = self.tabla.head(100)
        else:
            tabla_filtro3 = self.tabla
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.vmc = Vitrina(self, tabla_filtro3, self.ver_mp, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mpf_vitrina)
            
        else:
            self.frame_vitrina_mp.eliminar_cuadro()
            self.frame_vitrina_mp = Cuadro(self)
            self.frame_vitrina_mp.agregar_label(1, 2, '                  0 macroproblemas encontrados')
            
    #----------------------------------------------------------------------
    def limpiar_mp(self):
     
         # Eliminando campos
        self.mc1.eliminar_cuadro()
        self.vmc.eliminar_vitrina2()
        self.mc2.eliminar_cuadro()
        self.frame_vitrina_mp.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.mc1 = Cuadro(self)
        self.mc1.agregar_rejilla(self.rejilla_mp)
        self.mc2 = Cuadro(self)
        self.mc2.agregar_rejilla(self.rejilla_mp2)

        self.frame_vitrina_mp = Cuadro(self)
        # Creando vitrina
        self.vmc = Vitrina(self, self.tabla_mpF, self.ver_mp, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mpf_vitrina)
      
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
        #self.ad = b_adm_tabla
        #self.tabla_ad = self.ad.rename(columns={'ID_AD':'ID ADMINISTRADO','NOMBRE_O_RAZON_SOCIAL':'NOMBRE / RAZON SOCIAL','CATEGORÍA':'TIPO','DNI_RUC':'DNI / RUC'})
        #self.tabla_adF = self.tabla_ad.loc[0:99, ['ID ADMINISTRADO','NOMBRE / RAZON SOCIAL','TIPO','DNI / RUC']]
        
        # Listas para desplegables
        #self.listaAD = list(set(self.tabla_ad['NOMBRE / RAZON SOCIAL']))
        #self.listaTIPO= list(set(self.tabla_ad['TIPO']))

        # Agregando logo del ospa a la ventana y título
        self.ad0 = Cuadro(self)
        self.ad0.agregar_label(0, 0,' ')
        self.ad0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)
        ad3 = Cuadro(self)
        ad3.agregar_titulo(2, 0, 'Búsqueda de administrados')
    
        # Armando rejilla con los filtros
        self.rejilla_ad = (

            ('L', 0, 0, 'Administrado'),
            ('CXP', 0, 1, 44, self.listaAD, '', "normal"),

            ('L', 1, 0, 'Tipo'),
            ('CXP', 1, 1, 44, self.listaTIPO, '', "normal"),

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
        self.vad = Vitrina(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, funcion3=None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)

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
            self.vad.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['NOMBRE / RAZON SOCIAL'].str.contains(self.ADMINI)]
            self.Complementoad(self.filtro0)
  
        if len(filtro)>0:

            self.vad.eliminar_vitrina2()
            self.filtro0['DNI / RUC']=self.filtro0['DNI / RUC'].apply(str)
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementoad(self.filtro1)

        else:
            self.vad.eliminar_vitrina2()
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
            self.vad = Vitrina(self, tabla_filtro3, self.ver_ad, self.funcion_de_asociar_ad, funcion3=None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)
        else:
            self.frame_vitrina_ad.eliminar_cuadro()
            self.frame_vitrina_ad = Cuadro(self)
            self.frame_vitrina_ad.agregar_label(1, 2, '                  0 administrados encontrados')

    #----------------------------------------------------------------------
    def limpiar_ad(self):
     
         # Eliminando campos
        self.ad1.eliminar_cuadro()
        self.vad.eliminar_vitrina2()
        self.ad2.eliminar_cuadro()
        self.frame_vitrina_ad.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.ad1 = Cuadro(self)
        self.ad1.agregar_rejilla(self.rejilla_ad)
        self.ad2 = Cuadro(self)
        self.ad2.agregar_rejilla(self.rejilla_ad2)

        self.frame_vitrina_ad = Cuadro(self)
        # Creando vitrina
        self.vad = Vitrina(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, funcion3=None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)

    #----------------------------------------------------------------------
    def actualizar(self):
        
        # Eliminando campos
        self.ad1.eliminar_cuadro()
        self.vad.eliminar_vitrina2()
        self.ad2.eliminar_cuadro()
        self.frame_vitrina_ad.eliminar_cuadro()
        # Actualizando data
        #b_adm = df.b_adm
        #b_adm_tabla = b_adm.generar_dataframe()
        
        # Generamos el dataframe a filtrar 
        #self.ad = b_adm_tabla
        #self.tabla_ad = self.ad.rename(columns={'ID_AD':'ID ADMINISTRADO','NOMBRE_O_RAZON_SOCIAL':'NOMBRE / RAZON SOCIAL','CATEGORÍA':'TIPO','DNI_RUC':'DNI / RUC'})
        #self.tabla_adF = self.tabla_ad.loc[0:99, ['ID ADMINISTRADO','NOMBRE / RAZON SOCIAL','TIPO','DNI / RUC']]
        
        # Información para las listas desplegables
        #self.listaAD = list(set(self.tabla_ad['NOMBRE / RAZON SOCIAL']))
        #self.listaTIPO= list(set(self.tabla_ad['TIPO']))
        # Armando rejilla con los filtros

        self.rejilla_ad = (

            ('L', 0, 0, 'Administrado'),
            ('CXP', 0, 1, 44, self.listaAD, '', "normal"),

            ('L', 1, 0, 'Tipo'),
            ('CXP', 1, 1, 44, self.listaTIPO, '', "normal"),

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
        self.vad = Vitrina(self, self.tabla_adF, self.ver_ad, self.funcion_de_asociar_ad, funcion3=None, tipo_vitrina = "Modelo3", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)

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
        b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
        self.b_de_tabla = b_de.generar_dataframe()
        conditionlist = [(self.b_de_tabla['FECHA_FIRMA'] == '') & (self.b_de_tabla['FECHA_PROYECTO_FINAL'] != ''),
        (self.b_de_tabla['FECHA_FIRMA_REIT'] == '') & (self.b_de_tabla['FECHA_PROYECTO_REIT'] != ''),
        (self.b_de_tabla['FECHA_FIRMA_OCI'] == '') & (self.b_de_tabla['FECHA_PROYECTO_OCI'] != '')]
        choicelist = ['CUENTA', 'CUENTA', 'CUENTA']
        self.b_de_tabla['AUXILIAR'] = np.select(conditionlist, choicelist, default='NO CUENTA')
        self.tabla_inicial1 =  self.b_de_tabla.query("AUXILIAR=='CUENTA'")
        self.tabla_inicial2 =  self.tabla_inicial1.query("FECHA_PROYECTO_FINAL!=''")
        self.tabla_renombrada = self.renombrar_encabezados(self.tabla_inicial2, tipo_base = 'de')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'pf')
        self.tabla_pfirmaF = self.tabla_seleccionada.head(100)

        # Información para las listas desplegables
        self.categoria = sorted(list(set(self.tabla_renombrada['CATEGORIA'])))
        self.destinatario = sorted(list(set(self.tabla_renombrada['DESTINATARIO'])))
        self.tipodocemitpfirma = sorted(list(set(self.tabla_renombrada['TIPO DOC'])))
        self.especialista = sorted(list(set(self.tabla_renombrada['ESPECIALISTA'])))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Documentos pendientes de firma', 
                                            self.inicio_app, self.cerrar_sesion)

        # Armando rejilla con los filtros

        self.rejilla_pfirma = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 44, self.categoria, '', 'readonly'),

            ('L', 0, 2, 'Nro registro Siged'),
            ('EE', 0, 3),

            ('L', 0, 4, 'Destinatario'),
            ('CXE', 0, 5, 44, self.destinatario, '', 'normal'),

            ('L', 1, 0, 'Especialista'),
            ('CXP', 1, 1, 44, self.especialista, '', 'readonly'),

            ('L', 1, 2, 'Palabra clave del detalle'),
            ('EE', 1, 3)

        )
        
        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)

        # Generando rejilla para botones
        self.rejilla_2_pfirma = (
            ('B', 5, 4, 'Buscar', self.Buscar_pfirma),
            ('B', 5, 5, 'Limpiar', self.limpiar_pfirma),
            ('B', 5, 6, 'Actualizar', self.actualizar_pf),
            ('B', 5, 7, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)


        if len(self.tabla_pfirmaF.index) > 0:
            self.vpfirma = Vitrina(self, self.tabla_pfirmaF, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_vitrina) 
            return self.vpfirma
        else:
            self.frame_vitrina_pfirma = Cuadro(self)
            self.frame_vitrina_pfirma.agregar_label(1, 2, '                  0 documentos pendientes de firmar')

             # Franja inferior
            self.pfirma16 = Cuadro(self)
            self.pfirma16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

    #----------------------------------------------------------------------

    def Buscar_pfirma(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtropfirma = self.pfirma1.obtener_lista_de_datos()
        self.decatepfirma = self.listas_filtropfirma[0] #
        self.htpfirma = self.listas_filtropfirma[1]
        self.destinpfirma = self.listas_filtropfirma[2]
        self.espepfirma = self.listas_filtropfirma[3]
        self.detallepfirma = self.listas_filtropfirma[4] #
        self.filtro0 = self.tabla_renombrada
        self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)
        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.decatepfirma)>0 :
            filtro="CATEGORIA=="+"'"+self.decatepfirma+"' "

        if len(self.espepfirma)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESPECIALISTA=="+"'"+self.espepfirma+"' "
        
        self.mostrarDatospfirma(filtro)

    #----------------------------------------------------------------------

    def mostrarDatospfirma(self, filtro):

        self.filtro0 = self.tabla_renombrada
        
        if len(self.htpfirma)>0: # Filtro por palabra clave
            self.vpfirma.eliminar_vitrina2()
            self.filtro0['HT SALIDA']=self.filtro0['HT SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT SALIDA'].str.contains(self.htpfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.detallepfirma)>0: # Filtro por palabra clave
            self.vpfirma.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DETALLE'].str.contains(self.detallepfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.destinpfirma)>0: # Filtro por palabra clave
            self.vpfirma.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.destinpfirma)]
            self.Complementopfirma(self.filtro0)
  
        if len(filtro)>0:

            self.vpfirma.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopfirma(self.filtro1)

        else:
            self.vpfirma.eliminar_vitrina2()
            self.Complementopfirma(self.filtro0)

    #----------------------------------------------------------------------
    def Complementopfirma(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'pf')
        self.tabla = self.tabla_seleccionada.loc[:]
        if len(self.tabla.index) > 100:
            tabla_filtro3 = self.tabla.head(100)
        else:
            tabla_filtro3 = self.tabla
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_pfirma.eliminar_cuadro()
            self.frame_vitrina_pfirma = Cuadro(self)
            self.vpfirma = Vitrina(self, tabla_filtro3, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_pf_vitrina)
            
        else:
            self.frame_vitrina_pfirma.eliminar_cuadro()
            self.frame_vitrina_pfirma = Cuadro(self)
            self.frame_vitrina_pfirma.agregar_label(1, 2, '                  0 documentos encontrados')
            
    #----------------------------------------------------------------------

    def limpiar_pfirma(self):

        # Eliminando campos
        self.pfirma1.eliminar_cuadro()
        self.vpfirma.eliminar_vitrina2()
        self.pfirma15.eliminar_cuadro()
        self.frame_vitrina_pfirma.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)
       
        # Creando vitrina
        self.vpfirma = Vitrina(self, self.tabla_pfirmaF, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_pf_vitrina)
        
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
        b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
        self.tabla_inicial0 = b_dr.generar_dataframe()
        self.tabla_inicial1 = self.tabla_inicial0.query("F_ASIGNACION_1=='' or ESPECIALISTA_1==' ' or ESPECIALISTA_1==''")
        self.tabla_renombrada = self.renombrar_encabezados( self.tabla_inicial1, tipo_base = 'dr')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'paj')
        self.tabla_jpaF = self.tabla_seleccionada.head(100)

        # Información para las listas desplegables
        self.jpatipodoc = sorted(list(set(self.tabla_inicial1['TIPO_DOC'])))
        self.jparemitente = sorted(list(set(self.tabla_inicial1['REMITENTE'])))


        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Documentos pendientes de asignar', 
                                            self.inicio_app, self.cerrar_sesion)


        # Armando rejilla con los filtros
        self.rejilla_jpa = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 44, self.jpatipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 44, self.jparemitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3),

            ('L', 0, 4, 'Palabra clave asunto doc.'),
            ('EE', 0, 5)

        )

        # Agregando rejilla a la ventana
        self.jpa1 = Cuadro(self)
        self.jpa1.agregar_rejilla(self.rejilla_jpa)

        # Generando rejilla para botones
        self.rejilla_jpa2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_jpa),
            ('B', 5, 5, 'Limpiar', self.limpiar_jpa),
            ('B', 5, 6, 'Actualizar', self.actualizar_pasignar),
            ('B', 5, 7, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.jpa15 = Cuadro(self)
        self.jpa15.agregar_rejilla(self.rejilla_jpa2)

        self.frame_vitrina_jpa = Cuadro(self)

        if len(self.tabla_jpaF.index) > 0:
            self.vjpa = Vitrina(self, self.tabla_jpaF, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_vitrina) 
            return self.vjpa
        else:
            self.frame_vitrina_jpa = Cuadro(self)
            self.frame_vitrina_jpa.agregar_label(1, 2, '                  0 documentos pendientes de asignar')

        # Franja inferior
            self.jpa16 = Cuadro(self)
            self.jpa16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)
  
    #----------------------------------------------------------------------

    def Buscar_jpa(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro_jpa = self.jpa1.obtener_lista_de_datos()
        self.htjpa = self.listas_filtro_jpa[0]
        self.tipodocjpa = self.listas_filtro_jpa[1]
        self.remitentejpa = self.listas_filtro_jpa[2]
        self.nrodocjpa = self.listas_filtro_jpa[3]
        self.aporte = self.listas_filtro_jpa[4]

        self.filtro0 = self.tabla_renombrada
        self.filtro0['NUM_DOC']=self.filtro0['NUM_DOC'].apply(str)
        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodocjpa)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodocjpa+"' "

        
        self.mostrarDatosjpa(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatosjpa(self, filtro):

        self.filtro0 = self.tabla_renombrada
        
        if len(self.remitentejpa)>0: # Filtro por palabra clave
            self.vjpa.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['REMITENTE'].str.contains(self.remitentejpa)]
            self.Complementojpa(self.filtro0)

        if len(self.htjpa)>0: # Filtro por palabra clave
            self.vjpa.eliminar_vitrina2()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.htjpa)]
            self.Complementojpa(self.filtro0)

        if len(self.nrodocjpa)>0: # Filtro por palabra clave
            self.vjpa.eliminar_vitrina2()
            self.filtro0['NRO DOC']=self.filtro0['NRO DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOC'].str.contains(self.nrodocjpa)]
            self.Complementojpa(self.filtro0)

        if len(self.aporte)>0: # Filtro por palabra clave
            self.vjpa.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['ASUNTO'].str.contains(self.aporte)]
            self.Complementojpa(self.filtro0)

        if len(filtro)>0:

            self.vjpa.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementojpa(self.filtro1)

        else:
            self.vjpa.eliminar_vitrina2()
            self.Complementojpa(self.filtro0)

    #----------------------------------------------------------------------

    def Complementojpa(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'paj')
        tabla_filtro2 = self.tabla_seleccionada.loc[:]

        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_jpa.eliminar_cuadro()
            self.frame_vitrina_jpa = Cuadro(self)
            self.vjpa = Vitrina(self, tabla_filtro3, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_vitrina)
            
        else:
            self.frame_vitrina_jpa.eliminar_cuadro()
            self.frame_vitrina_jpa = Cuadro(self)
            self.frame_vitrina_jpa.agregar_label(1, 2, '                  0 documentos encontrados')
            
    #----------------------------------------------------------------------
    def limpiar_jpa(self):
        
        # Eliminando campos
        self.jpa1.eliminar_cuadro()
        self.vjpa.eliminar_vitrina2()
        self.jpa15.eliminar_cuadro()
        self.frame_vitrina_jpa.eliminar_cuadro()

        # Agregando rejilla a la ventana
        self.jpa1 = Cuadro(self)
        self.jpa1.agregar_rejilla(self.rejilla_jpa)
        self.jpa15 = Cuadro(self)
        self.jpa15.agregar_rejilla(self.rejilla_jpa2)
        self.frame_vitrina_jpa = Cuadro(self)
        # Creando vitrina
        self.vjpa = Vitrina(self, self.tabla_jpaF, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_vitrina)
        
    
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
        b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
        b_de_tabla = b_de.generar_dataframe()
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("ESTADO_DOCE=='Enviar reiterativo' or ESTADO_DOCE=='Eviar OCI'")
        self.tabla_ppr = self.tabla_inicial1.rename(columns={'COD_DE':'HT SALIDA','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
        self.tabla_ppr['FECHA ULTIMO MOV.'] = pd.to_datetime(self.tabla_ppr['FECHA ULTIMO MOV.'], dayfirst=True)
        self.tabla_renombrada2 = self.tabla_ppr.sort_values(by='FECHA ULTIMO MOV.', ascending=True)
        self.tabla_renombrada2['FECHA ULTIMO MOV.'] = self.tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
        self.tabla_ppr0 = self.tabla_renombrada2.loc[:, ['HT SALIDA','DESTINATARIO','NRO DOCUMENTO','ESPECIALISTA','FECHA ULTIMO MOV.','CATEGORIA','DETALLE']]
        self.tabla_pprF = self.tabla_ppr0.head(100)

        # Información para las listas desplegables
        self.categoriappr = list(set(self.tabla_ppr['CATEGORIA']))
        self.destinatarioppr = list(set(self.tabla_ppr['DESTINATARIO']))
        self.tipodocemitpfirmappr = list(set(self.tabla_ppr['TIPO DOC']))
        self.especialistappr = list(set(self.tabla_ppr['ESPECIALISTA']))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Documentos pendientes de reiterar/comunicación al OCI', 
                                            self.inicio_app, self.cerrar_sesion)


        self.rejilla_ppr = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 44, self.categoriappr, '', 'readonly'),

            ('L', 1, 0, 'Nro registro Siged'),
            ('EE', 1, 1),

            ('L', 0, 2, 'Destinatario'),
            ('CXE', 0, 3, 44, self.destinatarioppr, '', 'normal'),

            ('L', 1, 2, 'Especialista'),
            ('CXP', 1, 3, 44, self.especialistappr, '', 'readonly'),

            ('L', 2, 0, 'Tipo de documento'),
            ('CXP', 2, 1, 44, self.tipodocemitpfirmappr, '', 'readonly'),

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
            ('B', 5, 6, 'Actualizar', self.actualizar_preiter),
            ('B', 5, 7, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.ppr15 = Cuadro(self)
        self.ppr15.agregar_rejilla(self.rejilla_2_ppr)
        self.frame_vitrina_ppr = Cuadro(self)

        
        if len(self.tabla_pprF.index) > 0:
            self.vppr = Vitrina(self, self.tabla_pprF, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_prei_vitrina)

            return self.vppr
        else:
            self.frame_vitrina_ppr = Cuadro(self)
            self.frame_vitrina_ppr.agregar_label(1, 2, '                  0 documentos pendientes de reiterar/OCI')
       
        # Franja inferior
            self.ppr16 = Cuadro(self)
            self.ppr16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

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
        self.filtro0 = self.tabla_renombrada2
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

        self.filtro0 = self.tabla_renombrada2
        
        if len(self.htppr)>0: # Filtro por palabra clave
            self.vppr.eliminar_vitrina2()
            self.filtro0['HT_SALIDA']=self.filtro0['HT_SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT_SALIDA'].str.contains(self.htppr)]
            self.Complementoppr(self.filtro0)

        if len(self.destinppr)>0: # Filtro por palabra clave
            self.vppr.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.destinppr)]
            self.Complementoppr(self.filtro0)

        if len(self.espeppr)>0: # Filtro por palabra clave
            self.vppr.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['ESPECIALISTA'].str.contains(self.espeppr)]
            self.Complementoppr(self.filtro0)
  
        if len(filtro)>0:

            self.vppr.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementoppr(self.filtro1)

        else:
            self.vppr.eliminar_vitrina2()
            self.Complementoppr(self.filtro0)

    #----------------------------------------------------------------------
    def Complementoppr(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['HT SALIDA','DESTINATARIO','NRO DOCUMENTO','ESPECIALISTA','FECHA ULTIMO MOV.','CATEGORIA','DETALLE']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_ppr.eliminar_cuadro()
           
            self.frame_vitrina_ppr = Cuadro(self)
            self.vppr = Vitrina(self, tabla_filtro3, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_prei_vitrina)
            
        else:
            self.frame_vitrina_ppr.eliminar_cuadro()
            
            self.frame_vitrina_ppr = Cuadro(self)
            self.frame_vitrina_ppr.agregar_label(1, 2, '                  0 documentos encontrados')
            
    #----------------------------------------------------------------------

    def limpiar_ppr(self):

        # Eliminando campos
        self.ppr1.eliminar_cuadro()
        self.vppr.eliminar_vitrina2()
        self.ppr15.eliminar_cuadro()
        self.frame_vitrina_ppr.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.ppr1 = Cuadro(self)
        self.ppr1.agregar_rejilla(self.rejilla_ppr)
        self.ppr15 = Cuadro(self)
        self.ppr15.agregar_rejilla(self.rejilla_2_ppr)
        self.frame_vitrina_ppr = Cuadro(self)
        # Creando vitrina
        self.vppr = Vitrina(self, self.tabla_pprF, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_prei_vitrina)
       
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
        b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
        b_dr_tabla = b_dr.generar_dataframe()
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("F_EJECUCION_1==''")
        self.tabla_inicial2 = self.tabla_inicial1.query("ESPECIALISTA_1!='' or ESPECIALISTA_1!=' '")
        self.tabla_peq1t = self.tabla_inicial2.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO','ESPECIALISTA_1':'ESPECIALISTA','APORTE_DOC':'APORTE DOC.'})
        self.tabla_peq1t['FECHA ULTIMO MOV.'] = pd.to_datetime(self.tabla_peq1t['FECHA ULTIMO MOV.'], dayfirst=True)
        self.tabla_renombrada2 = self.tabla_peq1t.sort_values(by='FECHA ULTIMO MOV.', ascending=True)
        self.tabla_renombrada2['FECHA ULTIMO MOV.'] = self.tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
        self.tabla_peq1tF0 = self.tabla_renombrada2.loc[:, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','ESPECIALISTA','ASUNTO']]
        self.tabla_peq1tF = self.tabla_peq1tF0.head(100)



        # Información para las listas desplegables
        self.peq1ttipodoc = list(set(self.tabla_peq1t['TIPO DOC']))
        self.peq1tremitente = list(set(self.tabla_peq1t['REMITENTE']))
        self.peq1espec = list(set(self.tabla_peq1t['ESPECIALISTA']))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Pendientes del equipo 1', 
                                            self.inicio_app, self.cerrar_sesion)

        # Armando rejilla con los filtros
        self.rejilla_peq1t = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 44, self.peq1ttipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 44, self.peq1tremitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3),

            ('L', 0, 4, 'Especialista'),
            ('CXP', 0, 5, 44, self.peq1espec, '', 'readonly'),

            ('L', 1, 4, 'Palabra clave asunto doc.'),
            ('EE', 1, 5),

        )

        # Agregando rejilla a la ventana
        self.peq1t1 = Cuadro(self)
        self.peq1t1.agregar_rejilla(self.rejilla_peq1t)

        # Generando rejilla para botones
        self.rejilla_peq1t2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_peq1t),
            ('B', 5, 5, 'Limpiar', self.limpiar_peq1t),
            ('B', 5, 6, 'Actualizar', self.actualizar_peq1),
            ('B', 5, 7, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.peq1t15 = Cuadro(self)
        self.peq1t15.agregar_rejilla(self.rejilla_peq1t2)

        self.frame_vitrina_peq1t = Cuadro(self)

        if len(self.tabla_peq1tF.index) > 0:
            self.vpeq1t = Vitrina(self, self.tabla_peq1tF, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_peq1_vitrina)

            return self.vjpa
        else:
            self.frame_vitrina_peq1t = Cuadro(self)
            self.frame_vitrina_peq1t.agregar_label(1, 2, '                  0 documentos pendientes de trabajar')


        # Creando vitrina 

        # Franja inferior
            self.peq1t16 = Cuadro(self)
            self.peq1t16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

    #----------------------------------------------------------------------

    def Buscar_peq1t(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtro_peq1t = self.peq1t1.obtener_lista_de_datos()
        self.htpeq1t = self.listas_filtro_peq1t[0]
        self.tipodocpeq1t = self.listas_filtro_peq1t[1]
        self.remitentepeq1t = self.listas_filtro_peq1t[2]
        self.nrodocpeq1t = self.listas_filtro_peq1t[3]
        self.especpeq1t = self.listas_filtro_peq1t[4]
        self.aporte = self.listas_filtro_peq1t[5]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodocpeq1t)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodocpeq1t+"' "

        if len(self.especpeq1t)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESPECIALISTA=="+"'"+self.especpeq1t+"' "
        
        self.mostrarDatospeq1t(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatospeq1t(self, filtro):

        self.filtro0 = self.tabla_renombrada2
        
        if len(self.remitentepeq1t)>0: # Filtro por palabra clave
            self.vpeq1t.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['REMITENTE'].str.contains(self.remitentepeq1t)]
            self.Complementopeq1t(self.filtro0)

        if len(self.nrodocpeq1t)>0: # Filtro por palabra clave
            self.vpeq1t.eliminar_vitrina2()
            self.filtro0['NRO DOC']=self.filtro0['NRO DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOC'].str.contains(self.nrodocpeq1t)]
            self.Complementopeq1t(self.filtro0)

        if len(self.htpeq1t)>0: # Filtro por palabra clave
            self.vpeq1t.eliminar_vitrina2()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.htpeq1t)]
            self.Complementopeq1t(self.filtro0)

        if len(self.aporte)>0: # Filtro por palabra clave
            self.vpeq1t.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['ASUNTO'].str.contains(self.aporte)]
            self.Complementopeq1t(self.filtro0)

        if len(filtro)>0:

            self.vpeq1t.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopeq1t(self.filtro1)

        else:
            self.vpeq1t.eliminar_vitrina2()
            self.Complementopeq1t(self.filtro0)

    #----------------------------------------------------------------------

    def Complementopeq1t(self,filtro0):


        tabla_filtro2 = filtro0.loc[:, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','ESPECIALISTA','ASUNTO']]
        
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_peq1t.eliminar_cuadro()
            self.frame_vitrina_peq1t = Cuadro(self)
            self.vpeq1t = Vitrina(self, tabla_filtro3, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_peq1_vitrina)
            
        else:
            self.frame_vitrina_peq1t.eliminar_cuadro()
            self.frame_vitrina_peq1t = Cuadro(self)
            self.frame_vitrina_peq1t.agregar_label(1, 2, '                  0 documentos encontrados')
            
    #----------------------------------------------------------------------
    def limpiar_peq1t(self):
        
        # Eliminando campos
        self.peq1t1.eliminar_cuadro()
        self.vpeq1t.eliminar_vitrina2()
        self.peq1t15.eliminar_cuadro()
        self.frame_vitrina_peq1t.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.peq1t1 = Cuadro(self)
        self.peq1t1.agregar_rejilla(self.rejilla_peq1t)
        self.peq1t15 = Cuadro(self)
        self.peq1t15.agregar_rejilla(self.rejilla_peq1t2)
        self.frame_vitrina_peq1t = Cuadro(self)
        
        # Creando vitrina
        self.vpeq1t = Vitrina(self, self.tabla_peq1tF, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_peq1_vitrina)
        
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
        b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
        b_dr_tabla = b_dr.generar_dataframe()
        self.tabla_inicial0 = b_dr_tabla
        self.tabla_inicial1 = self.tabla_inicial0.query("F_EJECUCION_2==''")
        self.tabla_inicial2 = self.tabla_inicial1.query("ESPECIALISTA_2!='' or ESPECIALISTA_2!=' '")
        self.tabla_peq2t = self.tabla_inicial2.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO','ESPECIALISTA_2':'ESPECIALISTA','APORTE_DOC':'APORTE DOC.'})
        self.tabla_peq2t['FECHA INGRESO SEFA'] = pd.to_datetime(self.tabla_peq2t['FECHA INGRESO SEFA'], dayfirst=True)
        self.tabla_peq2t['FECHA ULTIMO MOV.'] = pd.to_datetime(self.tabla_peq2t['FECHA ULTIMO MOV.'], dayfirst=True)
        self.tabla_renombrada2 = self.tabla_peq2t.sort_values(by='FECHA INGRESO SEFA', ascending=True)
        self.tabla_renombrada2['FECHA INGRESO SEFA'] = self.tabla_renombrada2['FECHA INGRESO SEFA'].dt.strftime('%d/%m/%Y')
        self.tabla_renombrada2['FECHA ULTIMO MOV.'] = self.tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
        self.tabla_peq2tF0 = self.tabla_peq2t.loc[:, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','ESPECIALISTA_1','ESPECIALISTA','ASUNTO']]
        self.tabla_peq2tF = self.tabla_peq2tF0.head(100)

        # Información para las listas desplegables
        self.peq2ttipodoc = list(set(self.tabla_peq2t['TIPO DOC']))
        self.peq2tremitente = list(set(self.tabla_peq2t['REMITENTE']))
        self.peq2tespecialista = list(set(self.tabla_peq2t['ESPECIALISTA']))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Pendientes de calificar respuesta', 
                                            self.inicio_app, self.cerrar_sesion)

        # Armando rejilla con los filtros
        self.rejilla_peq2t = (

            ('L', 0, 0, 'Nro registro Siged'),
            ('EE', 0, 1),

            ('L', 1, 0, 'Tipo de documento'),
            ('CXP', 1, 1, 44, self.peq2ttipodoc, '', 'readonly'),

            ('L', 0, 2, 'Remitente'),
            ('CXE', 0, 3, 44, self.peq2tremitente, '', 'normal'),

            ('L', 1, 2, 'Número de doc'),
            ('EE', 1, 3),

            ('L', 0, 4, 'Especialista'),    
            ('CXP', 0, 5, 44, self.peq2tespecialista, '', 'readonly'),

            ('L', 1, 4, 'Palabra clave asunto doc.'),
            ('EE', 1, 5),

        )

        # Agregando rejilla a la ventana
        self.peq2t1 = Cuadro(self)
        self.peq2t1.agregar_rejilla(self.rejilla_peq2t)

        # Generando rejilla para botones
        self.rejilla_peq2t2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_peq2t),
            ('B', 5, 5, 'Limpiar', self.limpiar_peq2t),
            ('B', 5, 6, 'Volver', self.volver),
            ('B', 5, 7, 'Actualizar', self.actualizar_peq2)
        )
        
        # Agregando rejilla de botones a la ventana
        self.peq2t15 = Cuadro(self)
        self.peq2t15.agregar_rejilla(self.rejilla_peq2t2)

        self.frame_vitrina_peq2t = Cuadro(self)

        if len(self.tabla_peq2tF.index) > 0:
            self.vpeq2t = Vitrina(self, self.tabla_peq2tF, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_peq2_vitrina)

            return self.vpeq2t
        else:
            self.frame_vitrina_peq2t = Cuadro(self)
            self.frame_vitrina_peq2t.agregar_label(1, 2, '                  0 documentos pendientes de trabajar')


        # Creando vitrina 

        # Franja inferior
            self.peq2t16 = Cuadro(self)
            self.peq2t16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

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
        self.aporte = self.listas_filtro_peq2t[5]

        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.tipodocpeq2t)>0 :
            filtro="`TIPO DOC`=="+"'"+self.tipodocpeq2t+"' "

        if len(self.especialistapeq2t)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESPECIALISTA=="+"'"+self.especialistapeq2t+"' "
        
        self.mostrarDatospeq2t(filtro)

    #----------------------------------------------------------------------  

    def mostrarDatospeq2t(self, filtro):

        self.filtro0 = self.tabla_renombrada2
        
        if len(self.remitentepeq2t)>0: # Filtro por palabra clave
            self.vpeq2t.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['REMITENTE'].str.contains(self.remitentepeq2t)]
            self.Complementopeq2t(self.filtro0)

        if len(self.aporte)>0: # Filtro por palabra clave
            self.vpeq2t.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['ASUNTO'].str.contains(self.aporte)]
            self.Complementopeq2t(self.filtro0)

        if len(self.nrodocpeq2t)>0: # Filtro por palabra clave
            self.vpeq2t.eliminar_vitrina2()
            self.filtro0['NRO DOC']=self.filtro0['NRO DOC'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['NRO DOC'].str.contains(self.nrodocpeq2t)]
            self.Complementopeq2t(self.filtro0)

        if len(self.htpeq2t)>0: # Filtro por palabra clave
            self.vpeq2t.eliminar_vitrina2()
            self.filtro0['HT INGRESO']=self.filtro0['HT INGRESO'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT INGRESO'].str.contains(self.htpeq2t)]
            self.Complementopeq2t(self.filtro0)

        if len(filtro)>0:

            self.vpeq2t.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopeq2t(self.filtro1)

        else:
            self.vpeq2t.eliminar_vitrina2()
            self.Complementopeq2t(self.filtro0)

    #----------------------------------------------------------------------

    def Complementopeq2t(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['NRO DOC','FECHA INGRESO SEFA','REMITENTE','HT INGRESO','FECHA ULTIMO MOV.','ESPECIALISTA_1','ESPECIALISTA','ASUNTO']]

        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_peq2t.eliminar_cuadro()
            self.frame_vitrina_peq2t = Cuadro(self)
            self.vpeq2t = Vitrina(self, tabla_filtro3, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_peq2_vitrina)
            
        else:
            self.frame_vitrina_peq2t.eliminar_cuadro()
            self.frame_vitrina_peq2t = Cuadro(self)
            self.frame_vitrina_peq2t.agregar_label(1, 2, '                  0 documentos encontrados')
            
    #----------------------------------------------------------------------
    def limpiar_peq2t(self):
        
        # Eliminando campos
        self.peq2t1.eliminar_cuadro()
        self.vpeq2t.eliminar_vitrina2()
        self.peq2t15.eliminar_cuadro()
        self.frame_vitrina_peq2t.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.peq2t1 = Cuadro(self)
        self.peq2t1.agregar_rejilla(self.rejilla_peq2t)
        self.peq2t15 = Cuadro(self)
        self.peq2t15.agregar_rejilla(self.rejilla_peq2t2)
        self.frame_vitrina_peq2t = Cuadro(self)
        # Creando vitrina
        self.vpeq2t = Vitrina(self, self.tabla_peq2tF, self.ver_dr, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_peq2_vitrina)
       

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
        b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
        b_de_tabla = b_de.generar_dataframe()
        self.tabla_inicial0 = b_de_tabla
        self.tabla_inicial1 = self.tabla_inicial0[self.tabla_inicial0['CATEGORIA']=='Programación'] 
        self.tabla_peq2pr = self.tabla_inicial1.rename(columns={'COD_DE':'DOC EMITIDO','FECHA_PROYECTO_FINAL':'FECHA ACCION','FECHA_FIRMA':'FECHA PROGRAMACION','TIPO_DOC':'TIPO DOC','ESTADO_DOCE':'ESTADO'})
        self.tabla_peq2pr['FECHA ACCION'] = pd.to_datetime(self.tabla_peq2pr['FECHA ACCION'], dayfirst=True)
        self.tabla_renombrada2 = self.tabla_peq2pr.sort_values(by='FECHA ACCION', ascending=True)
        self.tabla_renombrada2['FECHA ACCION'] = self.tabla_renombrada2['FECHA ACCION'].dt.strftime('%d/%m/%Y')
        self.tabla_peq2prF0 = self.tabla_renombrada2.loc[:, ['DESTINATARIO','FECHA ACCION','ESPECIALISTA','ESTADO']]
        self.tabla_peq2prF = self.tabla_peq2prF0.head(100)

        # Información para las listas desplegables
        self.peq2prremitente = list(set(self.tabla_peq2pr['DESTINATARIO']))
        self.peq2prespecialista = list(set(self.tabla_peq2pr['ESPECIALISTA']))
        self.peq2prestado = list(set(self.tabla_peq2pr['ESTADO']))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Programaciones', 
                                            self.inicio_app, self.cerrar_sesion)


        # Armando rejilla con los filtros
        self.rejilla_peq2pr = (

            ('L', 0, 0, 'Destinatario'),
            ('CXE', 0, 1, 44, self.peq2prremitente, '', 'normal'),

            ('L', 1, 0, 'Especialista'),
            ('CXP', 1, 1, 44, self.peq2prespecialista, '', 'readonly'),

            ('L', 0, 2, 'Estado'),
            ('CXP', 0, 3, 44, self.peq2prestado, '', 'readonly')

        )

        # Agregando rejilla a la ventana
        self.peq2pr1 = Cuadro(self)
        self.peq2pr1.agregar_rejilla(self.rejilla_peq2pr)

        # Generando rejilla para botones
        self.rejilla_peq2pr2 = (
            ('B', 5, 4, 'Buscar', self.Buscar_peq2pr),
            ('B', 5, 5, 'Limpiar', self.limpiar_peq2pr),
            ('B', 5, 6, 'Actualizar', self.actualizar_programaciones),
            ('B', 5, 7, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.peq2pr15 = Cuadro(self)
        self.peq2pr15.agregar_rejilla(self.rejilla_peq2pr2)

        self.frame_vitrina_peq2pr = Cuadro(self)

        # Creando vitrina 
        self.vpeq2pr = Vitrina(self, self.tabla_peq2prF, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_progr_vitrina)
        
        # Franja inferior
        self.peq2pr16 = Cuadro(self)
        self.peq2pr16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

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

        self.filtro0 = self.tabla_renombrada2
        
        if len(self.remitentepeq2pr)>0: # Filtro por palabra clave
            self.vpeq2pr.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.remitentepeq2pr)]
            self.Complementopeq2pr(self.filtro0)

        if len(filtro)>0:

            self.vpeq2pr.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopeq2pr(self.filtro1)

        else:
            self.vpeq2pr.eliminar_vitrina2()
            self.Complementopeq2pr(self.filtro0)

    #----------------------------------------------------------------------

    def Complementopeq2pr(self,filtro0):

        tabla_filtro2 = filtro0.loc[:, ['DESTINATARIO','FECHA ACCION','ESPECIALISTA','ESTADO']]
        if len(tabla_filtro2.index) > 100:
            tabla_filtro3 = tabla_filtro2.head(100)
        else:
            tabla_filtro3 = tabla_filtro2
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_peq2pr.eliminar_cuadro()
            self.frame_vitrina_peq2pr = Cuadro(self)
            self.vpeq2pr = Vitrina(self, tabla_filtro3, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)
           
        else:
            self.frame_vitrina_peq2pr.eliminar_cuadro()
            self.frame_vitrina_peq2pr = Cuadro(self)
            self.frame_vitrina_peq2pr.agregar_label(1, 2, '                  0 programaciones encontradas')
            
    #----------------------------------------------------------------------
    def limpiar_peq2pr(self):
        
        # Eliminando campos
        self.peq2pr1.eliminar_cuadro()
        self.vpeq2pr.eliminar_vitrina2()
        self.peq2pr15.eliminar_cuadro()
        self.frame_vitrina_peq2pr.eliminar_cuadro()

        # Agregando rejilla a la ventana
        self.peq2pr1 = Cuadro(self)
        self.peq2pr1.agregar_rejilla(self.rejilla_peq2pr)
        self.peq2pr15 = Cuadro(self)
        self.peq2pr15.agregar_rejilla(self.rejilla_peq2pr2)
        self.frame_vitrina_peq2pr = Cuadro(self)
        # Creando vitrina
        self.vpeq2pr = Vitrina(self, self.tabla_peq2prF, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_mp_vitrina)
     
class Pendientes_notificar(funcionalidades_ospa):
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
        b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
        self.b_de_tabla = b_de.generar_dataframe()
        conditionlist = [(self.b_de_tabla['FECHA_NOTIFICACION'] == '') & (self.b_de_tabla['FECHA_FIRMA'] != ''),
        (self.b_de_tabla['FECHA_NOTIFICACION_REIT'] == '') & (self.b_de_tabla['FECHA_FIRMA_REIT'] != ''),
        (self.b_de_tabla['FECHA_NOTIFICACION_OCI'] == '') & (self.b_de_tabla['FECHA_FIRMA_OCI'] != '')]
        choicelist = ['CUENTA', 'CUENTA', 'CUENTA']
        self.b_de_tabla['AUXILIAR'] = np.select(conditionlist, choicelist, default='NO CUENTA')
        self.tabla_inicial1 =  self.b_de_tabla.query("AUXILIAR=='CUENTA'")
        self.tabla_inicial2 =  self.tabla_inicial1.query("FECHA_FIRMA!=''")
        self.tabla_renombrada = self.renombrar_encabezados(self.tabla_inicial2, tipo_base = 'de')
        self.tabla_seleccionada = self.seleccionar_encabezados(self.tabla_renombrada, tipo_base = 'pf')
        self.tabla_pfirmaF = self.tabla_seleccionada.head(100)

        # Información para las listas desplegables
        self.categoria = sorted(list(set(self.tabla_renombrada['CATEGORIA'])))
        self.destinatario = sorted(list(set(self.tabla_renombrada['DESTINATARIO'])))
        self.tipodocemitpfirma = sorted(list(set(self.tabla_renombrada['TIPO DOC'])))
        self.especialista = sorted(list(set(self.tabla_renombrada['ESPECIALISTA'])))

        # Agregando logo del ospa a la ventana y título
        titulos = Cuadro(self)
        titulos.agregar_franja_superior_ospa('Documentos pendientes de notificación', 
                                            self.inicio_app, self.cerrar_sesion)

        # Armando rejilla con los filtros

        self.rejilla_pfirma = (

            ('L', 0, 0, 'Categoría'),
            ('CXP', 0, 1, 44, self.categoria, '', 'readonly'),

            ('L', 0, 2, 'Nro registro Siged'),
            ('EE', 0, 3),

            ('L', 0, 4, 'Destinatario'),
            ('CXE', 0, 5, 44, self.destinatario, '', 'normal'),

            ('L', 1, 0, 'Especialista'),
            ('CXP', 1, 1, 44, self.especialista, '', 'readonly'),

            ('L', 1, 2, 'Palabra clave del detalle'),
            ('EE', 1, 3)

        )
        
        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)

        # Generando rejilla para botones
        self.rejilla_2_pfirma = (
            ('B', 5, 4, 'Buscar', self.Buscar_pfirma),
            ('B', 5, 5, 'Limpiar', self.limpiar_pfirma),
            ('B', 5, 6, 'Actualizar', self.actualizar_pf),
            ('B', 5, 7, 'Volver', self.volver)
        )
        
        # Agregando rejilla de botones a la ventana
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)

        # Creando vitrina
        self.vpfirma = Vitrina(self, self.tabla_pfirmaF, 
                                                    self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_pf_vitrina)
        
        # Franja inferior
        self.pfirma16 = Cuadro(self)
        self.pfirma16.agregar_franja_inferior('Franja_Inferior_Ancha_OSPA.png', df.alto_v_busqueda_franja, df.ancho_v_busqueda_franja)

    #----------------------------------------------------------------------

    def Buscar_pfirma(self):
        """"""
        # Obteniendo valores de la rejilla
        self.listas_filtropfirma = self.pfirma1.obtener_lista_de_datos()
        self.decatepfirma = self.listas_filtropfirma[0] #
        self.htpfirma = self.listas_filtropfirma[1]
        self.destinpfirma = self.listas_filtropfirma[2]
        self.espepfirma = self.listas_filtropfirma[3]
        self.detallepfirma = self.listas_filtropfirma[4] #
        self.filtro0 = self.tabla_renombrada
        self.filtro0['NRO DOCUMENTO']=self.filtro0['NRO DOCUMENTO'].apply(str)
        # Filtrando datos por palabras exactas

        filtro=""
        if len(self.decatepfirma)>0 :
            filtro="CATEGORIA=="+"'"+self.decatepfirma+"' "

        if len(self.espepfirma)>0 :
            if len(filtro)>0 :
                filtro = filtro+" & "
            else:
                filtro
            filtro=filtro+"ESPECIALISTA=="+"'"+self.espepfirma+"' "
        
        self.mostrarDatospfirma(filtro)

    #----------------------------------------------------------------------

    def mostrarDatospfirma(self, filtro):

        self.filtro0 = self.tabla_renombrada
        
        if len(self.htpfirma)>0: # Filtro por palabra clave
            self.vpfirma.eliminar_vitrina2()
            self.filtro0['HT SALIDA']=self.filtro0['HT SALIDA'].apply(str)
            self.filtro0 = self.filtro0[self.filtro0['HT SALIDA'].str.contains(self.htpfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.detallepfirma)>0: # Filtro por palabra clave
            self.vpfirma.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DETALLE'].str.contains(self.detallepfirma)]
            self.Complementopfirma(self.filtro0)

        if len(self.destinpfirma)>0: # Filtro por palabra clave
            self.vpfirma.eliminar_vitrina2()
            self.filtro0 = self.filtro0[self.filtro0['DESTINATARIO'].str.contains(self.destinpfirma)]
            self.Complementopfirma(self.filtro0)
  
        if len(filtro)>0:

            self.vpfirma.eliminar_vitrina2()
            self.filtro1 = self.filtro0.query(filtro)
            self.Complementopfirma(self.filtro1)

        else:
            self.vpfirma.eliminar_vitrina2()
            self.Complementopfirma(self.filtro0)

    #----------------------------------------------------------------------
    def Complementopfirma(self,filtro0):

        self.tabla_seleccionada = self.seleccionar_encabezados(filtro0, tipo_base = 'pf')
        self.tabla = self.tabla_seleccionada.loc[:]
        if len(self.tabla.index) > 100:
            tabla_filtro3 = self.tabla.head(100)
        else:
            tabla_filtro3 = self.tabla
        if len(tabla_filtro3.index) > 0:
            self.frame_vitrina_pfirma.eliminar_cuadro()
            self.frame_vitrina_pfirma = Cuadro(self)
            self.vpfirma = Vitrina(self, tabla_filtro3, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_pf_vitrina)
            
        else:
            self.frame_vitrina_pfirma.eliminar_cuadro()
            self.frame_vitrina_pfirma = Cuadro(self)
            self.frame_vitrina_pfirma.agregar_label(1, 2, '                  0 documentos encontrados')
            
    #----------------------------------------------------------------------

    def limpiar_pfirma(self):

        # Eliminando campos
        self.pfirma1.eliminar_cuadro()
        self.vpfirma.eliminar_vitrina2()
        self.pfirma15.eliminar_cuadro()
        self.frame_vitrina_pfirma.eliminar_cuadro()
        # Agregando rejilla a la ventana
        self.pfirma1 = Cuadro(self)
        self.pfirma1.agregar_rejilla(self.rejilla_pfirma)
        self.pfirma15 = Cuadro(self)
        self.pfirma15.agregar_rejilla(self.rejilla_2_pfirma)
        self.frame_vitrina_pfirma = Cuadro(self)
       
        # Creando vitrina
        self.vpfirma = Vitrina(self, self.tabla_pfirmaF, self.ver_de, funcion2=None, funcion3=None, tipo_vitrina = "Modelo5", height=df.alto_v_busqueda_vitrina, width=df.ancho_v_busqueda_pf_vitrina)
        