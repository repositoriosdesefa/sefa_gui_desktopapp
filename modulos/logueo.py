import pandas as pd
from tkinter import Tk
from apoyo.elemetos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos
from modulos.administracion import Ingresar_contrasena_de_adminitrador as adm

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
            ('E',1,0),
            ('L',2,0, 'Contraseña:'),
            ('EP',3,0)
        )
        c2.agregar_rejilla(rejilla)

        c3 = Cuadro(self)
        c3.agregar_label(0,0,' ')
        c3.agregar_button(1,0,'Ingresar', self.ingresar_a_la_aplicacion)

        c4 = Cuadro(self)
        rejilla2 = (
            ('BL',0,0,'Recuperar contraseña', self.ir_a_recuperar_contrasena),
            ('BL',1,0,'Cambiar contraseña', self.ir_a_cambiar_contrasena)
        )
        c4.agregar_rejilla(rejilla2)

    #----------------------------------------------------------------------
    def ingresar_a_la_aplicacion(self):
        """"""

        print('Ingresar a aplicación')
    
    #----------------------------------------------------------------------
    def ir_a_recuperar_contrasena(self, event):
        """"""

        self.desaparecer()
        subframe = logueo2_Recuperar_contrasena(self, 500, 500,'Recuperar contraseña')

    #----------------------------------------------------------------------
    def ir_a_cambiar_contrasena(self, event):
        """"""

        self.desaparecer()
        subframe = logueo3_Cambiar_contrasena(self, 500, 500,'Cambiar contraseña')
    
    #----------------------------------------------------------------------
    def ir_a_administracion(self):
        """"""

        self.desaparecer()
        subframe = adm.Administrar_usuarios(self, 500,500,'Permisos de administrador')

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
