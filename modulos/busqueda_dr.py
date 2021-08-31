from tkinter.constants import X
import pandas as pd
import numpy as np
from tkinter import Tk

from pyasn1.type.univ import Null
from apoyo.elemetos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos
from apoyo.vsf import Vitrina_busqueda
import apoyo.datos_frecuentes as dfrec
from modulos import vista_dr
import datetime

class Doc_recibidos_busqueda(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS')
        self.tabla_inicial = b1.generar_dataframe()
        self.tabla_inicial2 = self.tabla_inicial.rename(columns={'Tipo de documento':'Tipodedocumento','HT Entrante':'HTEntrante'})
        self.tabla_de_dr = self.tabla_inicial2.iloc[:, [0,2,3,6,4,5,8]]
        self.tabla_de_dr = self.tabla_de_dr.rename(columns={'HTEntrante':'N° registro Siged','Fecha de ingreso SEFA':'Fecha ingreso SEFA','Remitente':'Remitente','Tipodedocumento':'Tipo de documento'})

        self.listatipodoc = list(set(self.tabla_inicial2['Tipodedocumento']))
        self.listadestina = list(set(self.tabla_inicial2['Remitente']))
        self.listaht = list(set(self.tabla_inicial2['HTEntrante']))


        self.rejilla_dr = (
            ('L', 0, 0, 'Tipo de documento'),
            ('CX', 0, 1, self.listatipodoc),

            ('L', 1, 0, 'Remitente'),
            ('CX', 1, 1, self.listadestina),

            ('L', 0, 2, 'HT entrante'),
            ('E', 0, 3),

            ('L', 1, 2, 'Fecha de recepción OEFA'),
            ('D', 1, 3)

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


        self.v1 = Vitrina_busqueda(self, self.tabla_de_dr, self.ver_dr, 
                                   self.funcion_de_prueba, height=200, width=1030)

    def Buscar(self):

        self.listas_filtro = self.c1.obtener_lista_de_datos()
        self.tipodoc = self.listas_filtro[0]
        self.remitente = self.listas_filtro[1]
        self.ht = self.listas_filtro[2]
        self.fecha = self.listas_filtro[3]

        if self.tipodoc != "":
            self.v1.Eliminar_vitrina()
            self.tabla_filtrada = self.tabla_de_dr[self.tabla_de_dr['Tipo de documento']==self.tipodoc]
            self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
            if self.remitente != "":
                self.v1.Eliminar_vitrina()
                self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['Remitente']==self.remitente]
                self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['N° registro Siged']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada4 = self.tabla_filtrada3[self.tabla_filtrada3['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada4, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                    
                else:
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                  
            else:
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['N° registro Siged']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada3, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                else:
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                   
        
        else:
            if self.remitente != "":
                self.v1.Eliminar_vitrina()
                self.tabla_filtrada = self.tabla_de_dr[self.tabla_de_dr['Remitente']==self.remitente]
                self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['N° registro Siged']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada3 = self.tabla_filtrada2[self.tabla_filtrada2['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada4, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                else:
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
              
            else:
                if self.ht != "":
                    self.v1.Eliminar_vitrina()
                    self.tabla_filtrada = self.tabla_de_dr[self.tabla_de_dr['N° registro Siged']==self.ht]
                    self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada2 = self.tabla_filtrada[self.tabla_filtrada['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada2, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
  
                else:
                    if self.fecha != "":
                        self.v1.Eliminar_vitrina()
                        self.tabla_filtrada = self.tabla_de_dr[self.tabla_de_dr['Fecha de ingreso OEFA']==self.fecha]
                        self.v1 = Vitrina_busqueda(self, self.tabla_filtrada, self.Buscar, self.funcion_de_prueba, height=200, width=1030)
    

    def limpiar(self):
        
        
        self.v1.Eliminar_vitrina()




    def ver_dr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS')
        lb1 = b1.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[0], lb1[1], lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        
        self.desaparecer()
        subframe = vista_dr.Doc_recibidos_vista(self, 600, 1100, texto_documento, nuevo=False, lista=lista_para_insertar)


    def funcion_de_prueba(self, x):
        """"""

        print(x)

    #def Buscar(self):

     #   if len(self.c1.obtener_dato(1))>0 :

      #      self.mostrar_datos()

       # self.mostrar_datos()