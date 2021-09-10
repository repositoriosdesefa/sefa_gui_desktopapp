import pandas as pd
from tkinter import Tk
from apoyo.elementos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos

class logueo1_Ingreso_de_usuario(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        c1.agregar_imagen(1,0,'herramientas.png',200,50)
        c1.agregar_label(2,0,' ')

        c2 = Cuadro(self)
        rejilla = (
            ('L',0,0,'Correo electrónico:'),
            ('E',0,1),
            ('L',1,0, 'Contraseña:'),
            ('E',1,1)
        )
        c2.agregar_rejilla(rejilla)

        c3 = Cuadro(self)
        c3.agregar_button(0,0,'Ingresar', self.ingresar_a_la_aplicacion)

    #----------------------------------------------------------------------
    def ingresar_a_la_aplicacion(self):
        """"""

        print('Ingreso')
    
    #----------------------------------------------------------------------
    def ir_a_recuperar_contrasena(self):
        """"""

        print('recuperar contraseña')

    #----------------------------------------------------------------------
    def ir_a_cambiar_contrasena(self):
        """"""

        print('cambiar contraseña')
    


class logueo2_Recuperar_contrasena(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

class logueo3_Cambiar_contrasena(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

