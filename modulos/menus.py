import datetime as dt

from tkinter import messagebox

from modulos import busqueda_dr, vista_dr
from apoyo.elementos_de_GUI import Cuadro, Ventana, Hovertip_Sefa, Vitrina_vista 
from apoyo.manejo_de_bases import Base_de_datos
import apoyo.datos_frecuentes as dfrec

class inicio_app_OSPA(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_button(3, 1, "Jefe", self.inicio_jefe)
        c1.agregar_label(4, 1,' ')
        c1.agregar_button(5, 1, "Equipo Administrativo", self.inicio_adm)
        c1.agregar_label(6, 1,' ')
        c1.agregar_button(7, 1, "Equipo 1", self.inicio_e1)
        c1.agregar_label(8, 1,' ')
        c1.agregar_button(9, 1, "Equipo 2", self.inicio_e2)
        c1.agregar_label(10, 1,' ')

    #----------------------------------------------------------------------
    def inicio_jefe(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_jefe(self, 400, 400, "Bienvenido/a Jefe/a del OSPA")
    
    #----------------------------------------------------------------------
    def inicio_adm(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_admin(self, 400, 400, "Bienvenido/a")

    #----------------------------------------------------------------------
    def inicio_e1(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Inicio_eq1(self, 400, 400, "Documentos emitidos")
    
    #----------------------------------------------------------------------
    def inicio_e2(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Inicio_eq2(self, 400, 400, "Búsqueda de documentos emitidos")

class Menu_jefe(Ventana):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_button(3, 1, "Asignaciones pendientes", self.jefe_asig)
        c1.agregar_label(4, 1,' ')
        c1.agregar_button(5, 1, "Documentos por firmar", self.jefe_firma)
        c1.agregar_label(6, 1,' ')
        c1.agregar_button(7, 1, "Creación de macroproblema", self.vista_macro)
        c1.agregar_label(8, 1,' ')
        c1.agregar_button(9, 1, "Búsqueda", self.ver_menu_busquedas)
        c1.agregar_label(10, 1,' ')

    #----------------------------------------------------------------------
    def jefe_asig(self):
        
        print("Asignaciones pendientes")
        # self.desaparecer()
        # LargoxAncho
        #SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, 
        #            "Búsqueda de documentos emitidos")
    
    #----------------------------------------------------------------------
    def jefe_firma(self):
        
        print("Documentos por firmar")
        # self.desaparecer()
        # LargoxAncho
        #SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, 
        #            "Búsqueda de documentos emitidos")
    
    #----------------------------------------------------------------------
    def vista_macro(self):
        
        print("Creación de macroproblema")
        # self.desaparecer()
        # LargoxAncho
        #SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, 
        #            "Búsqueda de documentos emitidos")

    #----------------------------------------------------------------------
    def ver_menu_busquedas(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_busquedas(self, 400, 400, 
                    "Búsquedas")

class Menu_busquedas(Ventana):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_boton_grande(3, 1, "Búsqueda DR", self.busqueda_dr, 15, 2)
        c1.agregar_label(4, 1,' ')
        c1.agregar_boton_grande(5, 1, "Búsqueda DE", self.busqueda_de, 15, 2)
        c1.agregar_label(6, 1,' ')
        c1.agregar_boton_grande(7, 1, "Búsqueda de extremos", self.busqueda_ep, 20, 2)
        c1.agregar_label(8, 1,' ')
        c1.agregar_boton_grande(9, 1, "Búsqueda de macroproblemas", self.busqueda_mp, 25, 2)
        c1.agregar_label(10, 1,' ')
    
    #----------------------------------------------------------------------
    def busqueda_dr(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 400, 400,
                     "Búsqueda de documentos recibidos")
    
    #----------------------------------------------------------------------
    def busqueda_de(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 400, 400, 
                    "Búsqueda de documentos emitidos")
    
    #----------------------------------------------------------------------
    def busqueda_ep(self):
        
        print("Búsqueda de extremos de problema")
        # self.desaparecer()
        # LargoxAncho
        #SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, 
        #            "Búsqueda de documentos emitidos")
    
    #----------------------------------------------------------------------
    def busqueda_mp(self):
        
        print("Búsqueda de macroproblemas")
        # self.desaparecer()
        # LargoxAncho
        #SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, 
        #            "Búsqueda de documentos emitidos")

class Menu_admin(Ventana):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_button(3, 1, "Registro de nuevo documento", self.vista_dr)
        c1.agregar_label(4, 1,' ')
        c1.agregar_button(5, 1, "Envío de reiterativo / OCI", self.vista_de)
        c1.agregar_label(6, 1,' ')
    
    #----------------------------------------------------------------------
    def vista_dr(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
                    "Registra de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def vista_de(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = vista_dr.Doc_emitidos_vista(self, 650, 1150,
                    "Registra de un nuevo documento recibido")

class Inicio_eq1(Ventana):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_button(3, 1, "Asignaciones pendientes", self.pendientes_eq1)
        c1.agregar_label(4, 1,' ')
        c1.agregar_button(5, 1, "Creación de macroproblema", self.vista_mp)
        c1.agregar_label(6, 1,' ')
    
    #----------------------------------------------------------------------
    def pendientes_eq1(self):

        print("Vista del Equipo 1")
        # self.desaparecer()
        # LargoxAncho
        # SubFrame = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
        #            "Registra de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def vista_mp(self):

        print("Creación de macroproblema")
        # self.desaparecer()
        # LargoxAncho
        #SubFrame = vista_dr.Doc_emitidos_vista(self, 650, 1150,
        #            "Registra de un nuevo documento recibido")

class Inicio_eq2(Ventana):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,' ')
        c1.agregar_button(3, 1, "Seguimiento al problema", self.busqueda_ep)
        c1.agregar_label(4, 1,' ')
        c1.agregar_button(5, 1, "Calificación de respuesta", self.pendientes_eq2)
        c1.agregar_label(6, 1,' ')
        c1.agregar_button(7, 1, "Programaciones", self.pendientes_prog)
        c1.agregar_label(8, 1,' ')
        c1.agregar_button(9, 1, "Creación de macroproblema", self.vista_mp)
        c1.agregar_label(10, 1,' ')

    #----------------------------------------------------------------------
    def pendientes_eq2(self):

        print("Vista de pendientes del Equipo 2")
        # self.desaparecer()
        # LargoxAncho
        # SubFrame = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
        #            "Registra de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def pendientes_prog(self):

        print("Vista de pendientes de programación")
        # self.desaparecer()
        # LargoxAncho
        # SubFrame = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
        #            "Registra de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def busqueda_ep(self):

        print("Búsqueda de extremo de problemas")
        # self.desaparecer()
        # LargoxAncho
        # SubFrame = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
        #            "Registra de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def vista_mp(self):

        print("Creación de macroproblema")
        # self.desaparecer()
        # LargoxAncho
        #SubFrame = vista_dr.Doc_emitidos_vista(self, 650, 1150,
        #            "Registra de un nuevo documento recibido")