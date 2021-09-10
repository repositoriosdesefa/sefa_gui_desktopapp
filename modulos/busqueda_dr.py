from tkinter.constants import X
import pandas as pd
import numpy as np
from tkinter import Tk
import gspread

from pyasn1.type.univ import Null
from apoyo.elemetos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos
from apoyo.vsf import Vitrina_busqueda
import apoyo.datos_frecuentes as dfrec
from modulos import vista_dr
import datetime
from tkinter import messagebox

class Doc_recibidos_busqueda(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS_FINAL')
        self.tabla_inicial = b1.generar_dataframe()
        self.tabla_2 = self.tabla_inicial.rename(columns={'COD_PROBLEMA':'CODIGO','HT_ENTRANTE':'NRO REGISTRO SIGED','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','APORTE_DOC':'ASUNTO'})
        self.tabla_3 = self.tabla_2.iloc[:, [1, 2, 5, 8, 11, 15, 12]]
        self.tabla_dr = self.tabla_2.iloc[1:100, [1, 2, 5, 8, 11, 15, 12]]
        #self.tabla_dr = self.tabla_dr.rename(columns={'COD_PROBLEMA':'CODIGO','HT_ENTRANTE':'NRO REGISTRO SIGED','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.'})

        self.listatipodoc = list(set(self.tabla_2['TIPO_DOC']))
        self.listadestina = list(set(self.tabla_2['REMITENTE']))
        #self.listaht = list(set(self.tabla_dr['HT_ENTRANTE']))
        #self.listacodigo = list(set(self.tabla_dr['COD_PROBLEMA']))



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

    def Buscar(self):

        self.listas_filtro = self.c1.obtener_lista_de_datos()
        self.ht = self.listas_filtro[0]
        self.tipodoc = self.listas_filtro[1]
        self.codigo = self.listas_filtro[2]
        self.remitente = self.listas_filtro[3]

        if self.tipodoc != "":
            self.v1.Eliminar_vitrina()
            self.tabla_filtrada = self.tabla_2[self.tabla_2['TIPO_DOC']==self.tipodoc]
            self.tabla_dr = self.tabla_filtrada.iloc[:, [1, 2, 5, 8, 11, 15, 12]]
            self.v1 = Vitrina_busqueda(self, self.tabla_dr, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
            if self.remitente != "":
                self.v1.Eliminar_vitrina()
                self.tabla_filtrada2 = self.tabla_dr[self.tabla_dr['REMITENTE']==self.remitente]
                self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['NRO REGISTRO SIGED']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada4 = self.tabla_filtrada3[self.tabla_filtrada3['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada4, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                    
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                  
            else:
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada2 = self.tabla_dr[self.tabla_dr['NRO REGISTRO SIGED']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_dr[self.tabla_dr['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                   
        
        else:
            if self.remitente != "":
                self.v1.Eliminar_vitrina()
                self.tabla_filtrada = self.tabla_3[self.tabla_3['REMITENTE']==self.remitente]
                self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['NRO REGISTRO SIGED']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
              
            else:
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada = self.tabla_3[self.tabla_3['NRO REGISTRO SIGED']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
  
                else:
                    if self.codigo != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada = self.tabla_3[self.tabla_3['CODIGO']==self.codigo]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_asociar, height=200, width=1030)
                    else:
                        self.v1.Eliminar_vitrina()
                        self.v1 = Vitrina_busqueda(self, self.tabla_dr, self.ver_dr, 
                                   self.funcion_de_asociar, height=200, width=1030)

    

    def limpiar(self):
        
        
        self.v1.Eliminar_vitrina()




    def ver_dr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS_FINAL')
        lb1 = b1.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[1], lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12], lb1[13]]
        
        self.desaparecer()
        subframe = vista_dr.Doc_recibidos_vista(self, 600, 1100, texto_documento, nuevo=False, lista=lista_para_insertar)


    def funcion_de_asociar(self, x):
        """"""
        self.x = x

        #OBTENER EL ID DEL DOCUMENTO RECIBIDO
        self.b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS_FINAL')
        self.IDDR = self.b1.listar_datos_de_fila(self.x)
        self.IDDR_FINAL = self.IDDR[0]

        #OBTENER EL ID DEL DOCUMENTO EMITIDO
        self.b2 = 'DOCS_E-2021-1'

        # GUARDAR RELACION
        b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'RELACION')

        # Pestaña 1: Código Único
        datos_insertar = [self.IDDR_FINAL,self.IDDR_FINAL,self.b2,self.b2,'ACTIVO']
        b0.agregar_datos(datos_insertar)

        messagebox.showinfo("¡Excelente!", "El registro ha sido asociado con éxito")
        messagebox.showerror("Error", "No se logró asociar")