import pandas as pd
from tkinter import Tk
from apoyo.elementos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos
from modulos import administracion as adm

class logueo1_Ingreso_de_usuario(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        c1.agregar_imagen(1,0,'herramientas_de_sefa.png',300,100)
        c1.agregar_titulo(2,0,'ACCESO DE USUARIOS')

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
            ('BL',1,0,'Cambiar contraseña', self.ir_a_cambiar_contrasena),
            ('BL',2,0,'Acceso de administrador', self.ir_a_administracion)
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
        subframe = logueo2_Recuperar_contrasena(self, 350, 500,'Recuperar contraseña')

    #----------------------------------------------------------------------
    def ir_a_cambiar_contrasena(self, event):
        """"""

        self.desaparecer()
        subframe = logueo3_Cambiar_contrasena(self, 500, 500,'Cambiar contraseña')
    
    #----------------------------------------------------------------------
    def ir_a_administracion(self, event):
        """"""

        self.desaparecer()
        subframe = adm.Ingresar_contrasena_de_adminitrador(self, 450,400,'Acceso de administrador')

class logueo2_Recuperar_contrasena(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        c1.agregar_imagen(1,0,'email.png',100,100)
        c1.agregar_titulo(2,0,'RECUPERAR CONTRASEÑA')

        c2 = Cuadro(self)
        rejilla = (
            ('L',0,0,'Correo electrónico:'),
            ('E',1,0)
        )
        c2.agregar_rejilla(rejilla)

        c3 = Cuadro(self)
        c3.agregar_label(0,0,' ')
        c3.agregar_button(1,0,'Enviar', self.enviar_contrasena_al_email)
        c3.agregar_button(1,1,'Volver', self.volver)

    #----------------------------------------------------------------------
    def enviar_contrasena_al_email(self):
        """"""

        print('Contraseña enviada al email')

class logueo3_Cambiar_contrasena(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)
    
        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        c1.agregar_imagen(1,0,'password.png',100,100)
        c1.agregar_titulo(2,0,'CAMBIAR CONTRASEÑA')

        c2 = Cuadro(self)
        rejilla = (
            ('L',0,0,'Correo electrónico:'),
            ('E',1,0),
            ('L',2,0,'Contraseña actual:'),
            ('E',3,0),
            ('L',4,0,'Nueva contraseña:'),
            ('E',5,0),
            ('L',6,0,'Confirmar nueva contraseña:'),
            ('E',7,0),
        )
        c2.agregar_rejilla(rejilla)

        c3 = Cuadro(self)
        c3.agregar_label(0,0,' ')
        c3.agregar_button(1,0,'Cambiar', self.cambiar_contrasena)
        c3.agregar_button(1,1,'Volver', self.volver)

    #----------------------------------------------------------------------
    def cambiar_contrasena(self):
        """"""

        print('Contraseña cambiada')
    

