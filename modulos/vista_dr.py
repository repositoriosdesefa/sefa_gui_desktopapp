from PIL.Image import ImagePointHandler
import pandas as pd
from tkinter import Tk
import gspread
from apoyo.elemetos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos
from apoyo.vsf import Vitrina
from tkinter import messagebox
import apoyo.datos_frecuentes as dfrec

class Doc_recibidos_vista(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)
        # Valores de lista desplegable
        tipo_respuesta = ('Si', 'No')
        tipo_ingreso = ('DIRECTO', 'DERIVACION-SUBDIRECCION', 
                        'DERIVACION-SUPERVISION', 'DERIVACION-SINADA')
        tipo_documento = ('OFICIO', 'MEMORANDO', 'CARTA', 'OFICIO CIRCULAR','MEMORANDO CIRCULAR', 'CARTA CIRCULAR',
                          'INFORME', 'RESOLUCIÓN', 'CÉDULA DE NOTIFICACIÓN', 'INFORME MÚLTIPLE', 'OTROS')
        especialista = ('Zurita, Carolina', 'López, José')
        tipo_indicacion = ('No corresponde', 'Archivar')

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
            ('E', 3, 1),

            ('L', 3, 2, '¿Es respuesta?'),
            ('CX', 3, 3, tipo_respuesta),

            ('L', 4, 0, 'Asunto'),
            ('E', 4, 1),

            ('L', 4, 2, 'Especialista asignado'),
            ('CX', 4, 3, especialista),

            ('L', 5, 0, 'Aporte del documento'),
            ('E', 5, 1),

            ('L', 5, 2, 'Indicación'),
            ('CX', 5, 3, tipo_indicacion)
        )

        # Lista de DE
        b1 = Base_de_datos('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4', 'DOC_EMITIDOS')
        tabla_de_dr = b1.generar_dataframe()
        tabla_de_dr = tabla_de_dr.drop(['ID_DE', 'ID_DR', 'ID_EP'], axis=1)
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
        # 2do Frame
        c2 = Cuadro(self)
        c2.agregar_button(1,1,'Enviar', self.enviar_dr)
        # 3er Frame
        c3 = Cuadro(self)
        c3.agregar_titulo(2, 0, 'Documentos emitidos asociados')
        v1 = Vitrina(self, tabla_de_dr, self.funcion_de_prueba, 
                    self.funcion_de_prueba,
                    height=80, width=1050)       

        c4 = Cuadro(self)
        c4.agregar_titulo(2,0,'Extremo de problemas asociados')
        v2 = Vitrina(self, tabla_de_ep, self.funcion_de_prueba, 
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
    def ir_a_busqueda_de(self):
        """"""
        self.desaparecer()
        subframe = Pantalla_de_busqueda_de(self, 500, 400, 'Búsqueda de documentos recibidos')

    #----------------------------------------------------------------------
    def ir_a_busqueda_ep(self):
        """"""
        self.desaparecer()
        subframe = Pantalla_de_busqueda_ep(self, 500, 400, 'Búsqueda de extremos de problemas')


class Pantalla_de_usuario(Ventana):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None):
        """Constructor"""

        Ventana.__init__(self, *args)

class Pantalla_de_busqueda_ep(Ventana):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None):
        """Constructor"""

        Ventana.__init__(self, *args)
       