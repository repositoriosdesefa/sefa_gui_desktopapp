from tkinter.constants import X
from tkinter import messagebox
import datetime as dt

from apoyo.elementos_de_GUI import Cuadro, Ventana, Vitrina_busqueda
from apoyo.manejo_de_bases import Base_de_datos
import apoyo.datos_frecuentes as dfrec
from modulos import vista_dr


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

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS_FINAL')
        self.tabla_inicial = b1.generar_dataframe()
        self.tabla_2 = self.tabla_inicial.rename(columns={'HT_ID':'ID DOC RECIBIDO','HT_ENTRANTE':'NRO REGISTRO SIGED','COD_PROBLEMA':'CODIGO','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','APORTE_DOC':'ASUNTO'})
        self.tabla_3 = self.tabla_2.iloc[:, [1, 5, 17, 8, 12, 15, 9]]
        self.tabla_dr = self.tabla_2.iloc[0:99, [1, 5, 17, 8, 12, 15, 9]]


        self.listatipodoc = list(set(self.tabla_2['TIPO_DOC']))
        self.listadestina = list(set(self.tabla_2['REMITENTE']))


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
        
        self.c0 = Cuadro(self)
        self.c0.agregar_label(0,0,' ')
        self.c0.agregar_imagen(1,0,'Logo_OSPA.png',202,49)

        self.c1 = Cuadro(self)
        self.c1.agregar_rejilla(self.rejilla_dr)

        rejilla_b = (
            ('B', 5, 4, 'Buscar', self.Buscar),
            ('B', 5, 5, 'Limpiar', self.limpiar)
        )
        

        c15 = Cuadro(self)
        c15.agregar_rejilla(rejilla_b)

        c2 = Cuadro(self)
        c2.agregar_titulo(2, 0, 'Búsqueda de documentos recibidos')


        self.v1 = Vitrina_busqueda(self, self.tabla_dr, self.ver_dr, 
                                   self.funcion_de_asociar, height=200, width=1030)

    #----------------------------------------------------------------------
    def Buscar(self):

        self.listas_filtro = self.c1.obtener_lista_de_datos()
        self.ht = self.listas_filtro[0]
        self.tipodoc = self.listas_filtro[1]
        self.codigo = self.listas_filtro[2]
        self.remitente = self.listas_filtro[3]

        if self.tipodoc != "":
            self.v1.Eliminar_vitrina()
            self.tabla_filtrada = self.tabla_2[self.tabla_2['TIPO_DOC']==self.tipodoc]
            self.tabla_drr = self.tabla_filtrada.iloc[0:99, [1, 5, 17, 8, 12, 15, 9]]
            self.v1 = Vitrina_busqueda(self, self.tabla_drr, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
            if self.ht != "":

                self.v1.Eliminar_vitrina()
                self.tabla_filtrada3 = self.tabla_filtrada[self.tabla_filtrada['NRO REGISTRO SIGED']==self.ht]
                self.tabla_dr2 = self.tabla_filtrada3.iloc[:, [1, 5, 17, 8, 12, 15, 9]]
                self.v1 = Vitrina_busqueda(self, self.tabla_dr2, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                if self.remitente != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada2 = self.tabla_dr2[self.tabla_dr2['REMITENTE']==self.remitente]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada4 = self.tabla_filtrada2[self.tabla_filtrada2['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada4, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                    
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_dr2[self.tabla_dr2['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                  
            else:
                if self.remitente != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada3 = self.tabla_filtrada[self.tabla_filtrada['REMITENTE']==self.remitente]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada4 = self.tabla_filtrada3[self.tabla_filtrada3['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada4, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada[self.tabla_filtrada['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                   
        
        else:
            if self.ht != "":
                self.v1.Eliminar_vitrina()
                self.tabla_i = self.tabla_2[self.tabla_2['NRO REGISTRO SIGED']==self.ht]
                self.tabla_drr = self.tabla_i.iloc[:, [1, 5, 17, 8, 12, 15, 9]]
                self.v1 = Vitrina_busqueda(self, self.tabla_drr, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                if self.remitente != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada2 = self.tabla_dr[self.tabla_dr['REMITENTE']==self.remitente]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_drr[self.tabla_drr['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
              
            else:
                if self.remitente != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada = self.tabla_2[self.tabla_2['REMITENTE']==self.remitente]
                    self.tabla_drr = self.tabla_filtrada.iloc[0:99, [1, 5, 17, 8, 12, 15, 9]]
                    self.v1 = Vitrina_busqueda(self, self.tabla_drr, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_dr[self.tabla_dr['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
  
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada = self.tabla_2[self.tabla_2['CODIGO']==self.codigo]
                        self.tabla_drr = self.tabla_filtrada.iloc[0:99, [1, 5, 17, 8, 12, 15, 9]]
                        self.v1 = Vitrina_busqueda(self, self.tabla_drr, self.ver_dr, self.funcion_de_asociar, height=200, width=1030)
                    else:
                        self.v1.Eliminar_vitrina()
                        self.v1 = Vitrina_busqueda(self, self.tabla_dr, self.ver_dr, 
                                   self.funcion_de_asociar, height=200, width=1030)

    
    #----------------------------------------------------------------------
    def limpiar(self):
        
        self.v1.Eliminar_vitrina()


    #----------------------------------------------------------------------
    def ver_dr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS_FINAL')
        lb1 = b1.listar_datos_de_fila(self.x)
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
        self.b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS_FINAL')
        self.IDDR = self.b1.listar_datos_de_fila(self.x)
        self.IDDR_FINAL = self.IDDR[0]

        #OBTENER EL ID USUARIO DEL DOCUMENTO EMITIDO
        codigode = self.cod_doc_de
        # OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
        tabla_de_codigo_de = b_de.generar_dataframe()
        tabla_codigo_de_filtrada = tabla_de_codigo_de[tabla_de_codigo_de.HT_ID == codigode]
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

        bde = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS_FINAL')
        self.de = bde.generar_dataframe()
        self.tabla_de2 = self.de.rename(columns={'HT_ID':'ID DOC EMITIDO','COD_PROBLEMA':'CODIGO','HT_SALIDA':'NRO REGISTRO SIGED',
        'NUM_DOC':'NRO DOCUMENTO','ESTADO_DOCE':'ESTADO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','DETALLE_REQUERIMIENTO':'DETALLE'})
        self.tabla_de3 = self.tabla_de2.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
        self.tabla_de4 = self.tabla_de2.iloc[0:99, [1, 18, 8, 7, 13, 16, 14]]
        #self.tabla_dr = self.tabla_dr.rename(columns={'COD_PROBLEMA':'CODIGO','HT_ENTRANTE':'NRO REGISTRO SIGED','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.'})

        self.listacategoria = list(set(self.tabla_de2['CATEGORIA']))
        self.listadestinatario = list(set(self.tabla_de2['DESTINATARIO']))
        self.listatipodocemit = list(set(self.tabla_de2['TIPO_DOC']))
        #self.listacodigo = list(set(self.tabla_dr['COD_PROBLEMA']))



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
        
        self.cde0 = Cuadro(self)
        self.cde0.agregar_label(0, 0,' ')
        self.cde0.agregar_imagen(1, 0,'Logo_OSPA.png',202,49)

        self.cde1 = Cuadro(self)
        self.cde1.agregar_rejilla(self.rejilla_de)

        rejilla_bde = (
            ('B', 5, 4, 'Buscar', self.Buscar_de),
            ('B', 5, 5, 'Limpiar', self.limpiar_de)
        )
        

        cde15 = Cuadro(self)
        cde15.agregar_rejilla(rejilla_bde)

        cde2 = Cuadro(self)
        cde2.agregar_titulo(2, 0, 'Búsqueda de documentos emitidos')


        self.vde1 = Vitrina_busqueda(self, self.tabla_de4, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
    
    #----------------------------------------------------------------------
    def Buscar_de(self):

        self.listas_filtrode = self.cde1.obtener_lista_de_datos()
        self.decate = self.listas_filtrode[0] #
        self.deht = self.listas_filtrode[1]
        self.dedestin = self.listas_filtrode[2]
        self.decodigo = self.listas_filtrode[3]
        self.detipodoc = self.listas_filtrode[4] #
        self.dedoc = self.listas_filtrode[5]

        if self.deht != "":
            self.vde1.Eliminar_vitrina()
            self.tabla_filtradade = self.tabla_de2[self.tabla_de2['NRO REGISTRO SIGED']==self.deht]
            self.tabla_de4 = self.tabla_filtradade.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
            self.vde1 = Vitrina_busqueda(self, self.tabla_de4, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
            if self.detipodoc != "":
                self.vde1.Eliminar_vitrina()
                self.tabla_filtradade2 = self.tabla_filtradade[self.tabla_filtradade['TIPO_DOC']==self.detipodoc]
                self.tabla_de5 = self.tabla_filtradade2.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                if self.decate != "":
                    self.vde1.Eliminar_vitrina()
                    self.tabla_de6 = self.tabla_de5[self.tabla_de5['CATEGORIA']==self.decate]
                    self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_de7 = self.tabla_de6[self.tabla_de6['DESTINATARIO']==self.dedestin]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de8 = self.tabla_de7[self.tabla_de7['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de9 = self.tabla_de8[self.tabla_de8['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de9, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de7 = self.tabla_de6[self.tabla_de6['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                else:
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_de6 = self.tabla_de5[self.tabla_de5['DESTINATARIO']==self.dedestin]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de7 = self.tabla_de6[self.tabla_de6['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de6 = self.tabla_de5[self.tabla_de5['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de6 = self.tabla_de5[self.tabla_de5['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
            else:
                if self.decate != "":
                    self.vde1.Eliminar_vitrina()
                    self.tabla_filtradade2 = self.tabla_filtradade[self.tabla_filtradade['CATEGORIA']==self.decate]
                    self.tabla_de5 = self.tabla_filtradade2.iloc[:, [1, 18, 2, 7, 6, 13, 16]]
                    self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_de7 = self.tabla_de5[self.tabla_de5['DESTINATARIO']==self.dedestin]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de8 = self.tabla_de7[self.tabla_de7['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de9 = self.tabla_de8[self.tabla_de8['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de9, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de7 = self.tabla_de5[self.tabla_de5['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de5[self.tabla_de5['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                else:
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_filtradade2 = self.tabla_filtradade[self.tabla_filtradade['DESTINATARIO']==self.dedestin]
                        self.tabla_de5 = self.tabla_filtradade2.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de6 = self.tabla_de5[self.tabla_de5['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de6 = self.tabla_de5[self.tabla_de5['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_filtradade2 = self.tabla_filtradade[self.tabla_filtradade['CODIGO']==self.decodigo]
                            self.tabla_de5 = self.tabla_filtradade2.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de6 = self.tabla_de5[self.tabla_de5['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_filtradade2 = self.tabla_filtradade[self.tabla_filtradade['NRO DOCUMENTO']==self.dedoc]
                                self.tabla_de5 = self.tabla_filtradade2.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
        else:
            if self.detipodoc != "":
                self.vde1.Eliminar_vitrina()
                self.tabla_filtradade = self.tabla_de2[self.tabla_de2['TIPO_DOC']==self.detipodoc]
                self.tabla_de4 = self.tabla_filtradade.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                self.vde1 = Vitrina_busqueda(self, self.tabla_de4, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                if self.decate != "":
                    self.vde1.Eliminar_vitrina()
                    self.tabla_deI = self.tabla_filtradade[self.tabla_filtradade['CATEGORIA']==self.decate]
                    self.tabla_de5 = self.tabla_deI.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                    self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_de6 = self.tabla_de5[self.tabla_de5['DESTINATARIO']==self.dedestin]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de7 = self.tabla_de6[self.tabla_de6['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de6 = self.tabla_de5[self.tabla_de5['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de6 = self.tabla_de5[self.tabla_de5['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                else:
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_de5 = self.tabla_de4[self.tabla_de4['DESTINATARIO']==self.dedestin]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de7 = self.tabla_de5[self.tabla_de5['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de5[self.tabla_de5['NRO DOCUMENTO']==self.decodigo]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de5 = self.tabla_de4[self.tabla_de4['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de6 = self.tabla_de5[self.tabla_de5['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de5 = self.tabla_de4[self.tabla_de4['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de5, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                
            else:
                if self.decate != "":
                    self.vde1.Eliminar_vitrina()
                    self.tabla_filtradade = self.tabla_de2[self.tabla_de2['CATEGORIA']==self.decate]
                    self.tabla_de4 = self.tabla_filtradade.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                    self.vde1 = Vitrina_busqueda(self, self.tabla_de4, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_de6 = self.tabla_de4[self.tabla_de4['DESTINATARIO']==self.dedestin]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de7 = self.tabla_de6[self.tabla_de6['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de6 = self.tabla_de4[self.tabla_de4['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de6[self.tabla_de6['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de6 = self.tabla_de4[self.tabla_de4['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de6, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                else:
                    if self.dedestin != "":
                        self.vde1.Eliminar_vitrina()
                        self.tabla_filtradade = self.tabla_de2[self.tabla_de2['DESTINATARIO']==self.dedestin]
                        self.tabla_de4 = self.tabla_filtradade.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                        self.vde1 = Vitrina_busqueda(self, self.tabla_de4, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_de7 = self.tabla_de4[self.tabla_de4['CODIGO']==self.decodigo]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de8 = self.tabla_de7[self.tabla_de7['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de8, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de4[self.tabla_de4['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                    else:
                        if self.decodigo != "":
                            self.vde1.Eliminar_vitrina()
                            self.tabla_filtradade = self.tabla_de2[self.tabla_de2['CODIGO']==self.decodigo]
                            self.tabla_de4 = self.tabla_filtradade.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                            self.vde1 = Vitrina_busqueda(self, self.tabla_de4, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_de7 = self.tabla_de4[self.tabla_de4['NRO DOCUMENTO']==self.dedoc]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de7, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                        else:
                            if self.dedoc != "":
                                self.vde1.Eliminar_vitrina()
                                self.tabla_filtradade = self.tabla_de2[self.tabla_de2['NRO DOCUMENTO']==self.dedoc]
                                self.tabla_de4 = self.tabla_filtradade.iloc[:, [1, 18, 8, 7, 13, 16, 14]]
                                self.vde1 = Vitrina_busqueda(self, self.tabla_de4, self.ver_de, self.funcion_de_asociar_de, height=200, width=1030)
                           

    #----------------------------------------------------------------------
    def limpiar_de(self):
        self.vde1.Eliminar_vitrina()

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
        subframe = vista_dr.Doc_emitidos_vista(self, 650, 1150, texto_documento, 
                                                nuevo=False, lista=lista_para_insertar, id_doc=x)

    #----------------------------------------------------------------------
    def funcion_de_asociar_de(self, x):
        """"""
        self.x = x

        #OBTENER EL ID INTERNO DEL DOCUMENTO EMITIDO
        self.bdee = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS_FINAL')
        self.IDDE = self.bdee.listar_datos_de_fila(self.x)
        self.IDDE_FINAL = self.IDDE[0]

        #OBTENER EL ID USUARIO DEL DOCUMENTO RECIBIDO
        codigodr = self.cod_doc_dr
        # OBTENER EL ID INTERNO DEL DOCUMENTO RECIBIDO
        tabla_de_codigo_dr = b_dr.generar_dataframe()
        tabla_codigo_de_filtrada = tabla_de_codigo_dr[tabla_de_codigo_dr.HT_ID == codigodr]
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