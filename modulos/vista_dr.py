from PIL.Image import ImagePointHandler
import pandas as pd
from tkinter import Tk
from modulos import busqueda_dr
import gspread
from apoyo.elemetos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos
from apoyo.vsf import Vitrina_vista
from tkinter import messagebox
import apoyo.datos_frecuentes as dfrec

# Valores de lista desplegable
tipo_ingreso = ('DIRECTO', 'DERIVACION-SUBDIRECCION', 
                'DERIVACION-SUPERVISION', 'DERIVACION-SINADA')
tipo_documento = ('', 'OFICIO', 'MEMORANDO', 'CARTA', 'OFICIO CIRCULAR','MEMORANDO CIRCULAR', 'CARTA CIRCULAR',
                  'INFORME', 'RESOLUCIÓN', 'CÉDULA DE NOTIFICACIÓN', 'INFORME MÚLTIPLE', 'OTROS')
especialista = ('','Zurita, Carolina', 'López, José')
tipo_indicacion = ('','No corresponde', 'Archivar')
si_no = ('','Si', 'No')
tipo_respuesta = ('','Ejecutó supervisión','Solicitó información a administrado',
                  'Ejecutó acción de evaluación', 'Inició PAS', 'Administrado en adecuación / formalización',
                  'Programó supervisión', 'Programó acción de evaluación', 'No es competente',
                  'No corresponde lo solicitado', 'En evaluación de la EFA', 'Otros')
categorias = ('','Pedido de información', 'Pedido de información adicional', 'Pedido de información urgente',
              'Reiterativo', 'Oficio a OCI')
marco_pedido = ('','EFA', 'OEFA',
                'Colaboración', 'Delegación', 'Conocimiento')

class Doc_recibidos_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None):
        """Constructor"""

        Ventana.__init__(self, *args)

        self.nuevo = nuevo

        # Labels and Entries
        rejilla_dr = (
            ('L', 0, 0, 'HT entrante'),
            ('E', 0, 1),

            ('L', 0, 2, 'Vía de recepción'),
            ('CX', 0, 3, tipo_ingreso),

            ('L', 1, 0, 'Fecha de recepción OEFA'),
            ('E', 1, 1),

            ('L', 1, 2, 'Fecha de recepción SEFA'),
            ('E', 1, 3),

            ('L', 2, 0, 'Tipo de documento'),
            ('CX', 2, 1, tipo_documento),

            ('L', 2, 2, 'N° de documento'),
            ('E', 2, 3),

            ('L', 3, 0, 'Remitente'),
            ('E', 3, 1),

            ('L', 3, 2, 'Asunto'),
            ('E', 3, 3),

            ('L', 4, 0, 'Especialista asignado'),
            ('CX', 4, 1, especialista),

            ('L', 4, 2, 'Indicación'),
            ('CX', 4, 3, tipo_indicacion),

            ('L', 5, 0, 'Aporte del documento'),
            ('E', 5, 1),

            ('L', 5, 2, '¿Es respuesta?'),
            ('CX', 5, 3, si_no),

            ('L', 6, 0, 'Respuesta'),
            ('CX', 6, 1, tipo_respuesta)
        )

        # Lista de DE
        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS')
        tabla_de_de = b1.generar_dataframe()
        tabla_de_de = tabla_de_de.drop(['ID_DE', 'ID_DR', 'ID_EP', 'Fecha proyecto final', 'Fecha de firma',
                                        'Tipo de documento', 'Marco de pedido', '¿Se emitió documento?'], axis=1)
        # Lista de EP
        b2 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'EXTREMOS')
        tabla_de_ep = b2.generar_dataframe()
        tabla_de_ep = tabla_de_ep.drop(['ID_DE', 'ID_DR', 'ID_EP'], axis=1)

        # Ubicaiones
        # Frame de Título
        self.c0 = Cuadro(self)
        self.c0.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        self.c0.agregar_titulo(0,1,'                             ')
        self.c0.agregar_titulo(0,2,'Detalle de documento recibido')
        self.c0.agregar_titulo(0,3,'                             ')
        self.c0.agregar_titulo(0,4,'                             ')
        # 1er Frame
        self.c1 = Cuadro(self)
        self.c1.agregar_rejilla(rejilla_dr)

        if self.nuevo != True:
            self.lista_para_insertar = lista
            self.c1.insertar_lista_de_datos(self.lista_para_insertar)

        # 2do Frame
        c2 = Cuadro(self)
        c2.agregar_button(1,1,'Enviar', self.enviar_dr)
        c2.agregar_button(1,2,'Búsqueda', self.busqueda_dr)
        # 3er Frame
        c3 = Cuadro(self)
        c3.agregar_titulo(2, 0, 'Documentos emitidos asociados')
        v1 = Vitrina_vista(self, tabla_de_de, self.ver_de, 
                    self.funcion_de_prueba,
                    height=80, width=1050)       
        # 4to Frame
        c4 = Cuadro(self)
        c4.agregar_titulo(2,0,'Extremo de problemas asociados')
        v2 = Vitrina_vista(self, tabla_de_ep, self.ver_de, 
                    self.funcion_de_prueba,
                    height=80, width=1050)
        
        
    #----------------------------------------------------------------------
    def funcion_de_prueba(self, x):
        """"""
        print(x)

     #----------------------------------------------------------------------
    def enviar_dr(self):
        """"""
        datos_ingresados = self.c1.obtener_lista_de_datos()
        b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS')
        b0.agregar_datos(datos_ingresados)
        
        # Confirmación de registro
        messagebox.showinfo("¡Excelente!", "El registro se ha ingresado correctamente")

    #----------------------------------------------------------------------
    def ver_de(self, x):
        """"""
        
        self.x = x
        texto_documento = 'Documento emitido: ' + x

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS')
        lb1 = b1.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[0], lb1[1],lb1[2],lb1[3], lb1[4], lb1[5], 
                               lb1[6], lb1[7], lb1[8], lb1[9], lb1[10]]
        
        self.desaparecer()
        subframe = Doc_emitidos_vista(self, 600, 1100, texto_documento, nuevo=False, lista=lista_para_insertar)

    #----------------------------------------------------------------------
    def ir_a_busqueda_ep(self):
        """"""
        #self.desaparecer()
        #subframe = Pantalla_de_busqueda_ep(self, 500, 400, 'Búsqueda de extremos de problemas')

        #----------------------------------------------------------------------

    def busqueda_dr(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = busqueda_dr.Doc_recibidos_busqueda(self, 600, 1200, "Pantalla de búsqueda")



class Doc_emitidos_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None):
        """Constructor"""

        Ventana.__init__(self, *args)

        self.nuevo = nuevo

        # Labels and Entries
        rejilla_dr = (
            ('L', 0, 0, 'HT de salida'),
            ('E', 0, 1),

            ('L', 0, 2, 'Categorías'),
            ('CX', 0, 3, categorias),

            ('L', 1, 0, 'Fecha de proyecto final'),
            ('E', 1, 1),

            ('L', 1, 2, 'Fecha de firma'),
            ('E', 1, 3),

            ('L', 2, 0, 'Tipo de documento'),
            ('CX', 2, 1, tipo_documento),

            ('L', 2, 2, 'N° de documento'),
            ('E', 2, 3),

            ('L', 3, 0, 'Destinatario'),
            ('E', 3, 1),

            ('L', 3, 2, 'Detalle de requerimiento'),
            ('E', 3, 3),

            ('L', 4, 0, 'Marco de pedido'),
            ('CX', 4, 1, marco_pedido),

            ('L', 4, 2, 'Fecha de notificación'),
            ('E', 4, 3),

            ('L', 5, 0, '¿Se emitió documento?'),
            ('CX', 5, 1, si_no)

        )

        # Lista de DE
        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS')
        tabla_de_dr = b1.generar_dataframe()
        tabla_de_dr = tabla_de_dr.drop(['ID_DE', 'ID_DR', 'ID_EP', 'Via de recepción',
                                        'Fecha de ingreso OEFA', 'Tipo de documento', 'Especialista',
                                        'Indicación', '¿Es respuesta?', 'Respuesta'], axis=1)
        # Lista de EP
        b2 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'EXTREMOS')
        tabla_de_ep = b2.generar_dataframe()
        tabla_de_ep = tabla_de_ep.drop(['ID_DE', 'ID_DR', 'ID_EP'], axis=1)

        # Ubicaiones
        # Frame de Título
        self.c0 = Cuadro(self)
        self.c0.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        self.c0.agregar_titulo(0,1,'                             ')
        self.c0.agregar_titulo(0,2,'Detalle de documento emitido ')
        self.c0.agregar_titulo(0,3,'                             ')
        self.c0.agregar_titulo(0,4,'                             ')
        # 1er Frame
        self.c1 = Cuadro(self)
        self.c1.agregar_rejilla(rejilla_dr)

        if self.nuevo != True:
            self.lista_para_insertar = lista
            self.c1.insertar_lista_de_datos(self.lista_para_insertar)

        # 2do Frame
        c2 = Cuadro(self)
        c2.agregar_button(1,1,'Enviar', self.enviar_de)
        c2.agregar_button(1,2,'Búsqueda', self.busqueda_dr)
        # 3er Frame
        c3 = Cuadro(self)
        c3.agregar_titulo(2,0,'Extremo de problemas asociados')
        v1 = Vitrina_vista(self, tabla_de_ep, self.ver_dr, 
                    self.funcion_de_prueba,
                    height=80, width=1050)
        # 4to Frame
        c4 = Cuadro(self)
        c4.agregar_titulo(2, 0, 'Documentos recibidos asociados')
        v2 = Vitrina_vista(self, tabla_de_dr, self.ver_dr, 
                    self.funcion_de_prueba,
                    height=80, width=1050)  
        
        
    #----------------------------------------------------------------------
    def funcion_de_prueba(self, x):
        """"""
        print(x)

     #----------------------------------------------------------------------
    def enviar_de(self):
        """"""
        datos_ingresados = self.c1.obtener_lista_de_datos()
        b0 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS')
        b0.agregar_datos(datos_ingresados)
        
        # Confirmación de registro
        messagebox.showinfo("¡Excelente!", "El registro se ha ingresado correctamente")

    #----------------------------------------------------------------------
    def ver_dr(self, x):
        """"""
        self.x = x
        texto_documento = 'Documento recibido: ' + x

        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_RECIBIDOS')
        lb1 = b1.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[0], lb1[1],lb1[2],lb1[3], lb1[4], lb1[5], 
                               lb1[6], lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        
        self.desaparecer()
        subframe = Doc_recibidos_vista(self, 600, 1100, texto_documento, nuevo=False, lista=lista_para_insertar)

    #----------------------------------------------------------------------
    def ir_a_vista_ep(self):
        """"""
        #self.desaparecer()
        #subframe = Pantalla_de_vista_ep(self, 500, 400, 'Búsqueda de extremos de problemas')

        #----------------------------------------------------------------------

    def busqueda_dr(self):
        """"""
        #self.desaparecer()
        # LargoxAncho
        #subFrame = busqueda_dr.Doc_recibidos_busqueda(self, 600, 1200, "Pantalla de búsqueda")
