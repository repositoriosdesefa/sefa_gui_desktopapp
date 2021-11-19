import datetime as dt

from tkinter import messagebox

from modulos import busqueda_dr, vista_dr
from apoyo.elementos_de_GUI import Cuadro, Ventana, Hovertip_Sefa, Vitrina_vista 
from apoyo.manejo_de_bases import Base_de_datos
import apoyo.datos_frecuentes as dfrec


class ventanas_ospa(Ventana):
    """"""
    def __init__(self, *args):
        """Constructor"""

    #----------------------------------------------------------------------
    def nuevo_dr(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = vista_dr.Doc_recibidos_vista(self, 550, 1090, "Registro Documento Recibido")

    #----------------------------------------------------------------------
    def busqueda_dr(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 560, 1150,
                     "Búsqueda de documentos recibidos")
     
    #----------------------------------------------------------------------
    def nuevo_de(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = vista_dr.Doc_emitidos_vista(self, 550, 1090, "Registro Documento Emitido")
    
    #----------------------------------------------------------------------
    def busqueda_de(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_emitidos_busqueda(self, 500, 1200, 
                    "Búsqueda de documentos emitidos")
    
    #----------------------------------------------------------------------
    def nuevo_ep(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = vista_dr.Extremo_problemas_vista(self, 550, 1090, "Registro Extremo de Problema")
    
    
    #----------------------------------------------------------------------
    def busqueda_ep(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Extremos(self, 600, 1400, 
                    "Búsqueda de extremos de problemas")
    
    #----------------------------------------------------------------------
    def nuevo_mp(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = vista_dr.Macroproblemas_vista(self, 550, 1090, "Creación de macroproblemas")
    
    #----------------------------------------------------------------------
    def busqueda_mp(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Macroproblemas(self, 500, 1200, 
                    "Búsqueda de macroproblemas")



class inicio_app_OSPA(ventanas_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,'Jefe')
        c1.agregar_button(3, 1, "Ir", self.inicio_jefe)
        c1.agregar_label(4, 1,'Equipo Administrativo')
        c1.agregar_button(5, 1, "Ir", self.inicio_adm)
        c1.agregar_label(6, 1,'Equipo 1')
        c1.agregar_button(7, 1, "Ir", self.inicio_e1)
        c1.agregar_label(8, 1,'Equipo 2')
        c1.agregar_button(9, 1, "Ir", self.inicio_e2)
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

    #----------------------------------------------------------------------
    def volver_anterior(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()


class Menu_jefe(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,'Asignaciones pendientes')
        c1.agregar_button(3, 1, "Ir", self.jefe_asig)
        c1.agregar_label(4, 1,'Documentos por firmar')
        c1.agregar_button(5, 1, "Ir", self.jefe_firma)
        c1.agregar_label(6, 1,'Creación de extremo de problema')
        c1.agregar_button(7, 1, "Ir", self.nuevo_mp)
        c1.agregar_label(8, 1,'Búsqueda')
        c1.agregar_button(9, 1, "Ir", self.ver_menu_busquedas)
        c1.agregar_label(10, 1,' ')
        c1.agregar_button(13, 2, "Volver", self.volver_anterior)

    #----------------------------------------------------------------------
    def jefe_asig(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Pendientes_jefe_asignar(self, 500, 1000, "Documentos pendientes de asignar")
    
    #----------------------------------------------------------------------
    def jefe_firma(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Pendientes_jefe_firma(self, 550, 1090, "Documentos pendientes de firma")
    
    #----------------------------------------------------------------------
    def ver_menu_busquedas(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_busquedas(self, 400, 400, 
                    "Búsquedas")


class Menu_busquedas(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,'Búsqueda DR')
        c1.agregar_button(3, 1, "Ir", self.busqueda_dr)
        c1.agregar_label(4, 1,'Búsqueda DE')
        c1.agregar_button(5, 1, "Ir", self.busqueda_de)
        c1.agregar_label(6, 1,'Búsqueda de extremos')
        c1.agregar_button(7, 1, "Ir", self.busqueda_ep)
        c1.agregar_label(8, 1,'Búsqueda de macroproblemas')
        c1.agregar_button(9, 1, "Ir", self.busqueda_mp)
        c1.agregar_label(10, 1,' ')
        c1.agregar_button(13, 2, "Volver", self.volver_anterior)
    

class Menu_admin(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,'Registro de nuevo documento recibido')
        c1.agregar_button(3, 1, "Ir", self.nuevo_dr)
        c1.agregar_label(4, 1,'Envío de reiterativo / OCI')
        c1.agregar_button(5, 1, "Ir", self.Pendientes_reiterar)
        c1.agregar_label(6, 1,' ')
        c1.agregar_button(9, 2, "Volver", self.volver_anterior)
    
    #----------------------------------------------------------------------
    def vista_dr(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
                    "Registra de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def Pendientes_reiterar(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Pendientes_por_reiterar(self, 560, 1090, "Documentos pendientes de reiterar/comunicar al OCI")


class Inicio_eq1(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,'Asignaciones pendientes')
        c1.agregar_button(3, 1, "Ir", self.pendientes_eq1)
        c1.agregar_label(4, 1,'Creación de macroproblema'),
        c1.agregar_button(5, 1, "Ir", self.nuevo_mp)
        c1.agregar_label(6, 1,' ')
        c1.agregar_button(9, 2, "Volver", self.volver_anterior)
    
    #----------------------------------------------------------------------
    def pendientes_eq1(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Doc_recibidos_busqueda(self, 500, 1000, "Documentos pendientes de trabajar - Equipo 1")


class Inicio_eq2(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,'Seguimiento al problema')
        c1.agregar_button(3, 1, "Ir", self.busqueda_ep)
        c1.agregar_label(4, 1,'Calificación de respuesta')
        c1.agregar_button(5, 1, "Ir", self.pendientes_eq2)
        c1.agregar_label(6, 1,'Programaciones')
        c1.agregar_button(7, 1, "Ir", self.pendientes_prog)
        c1.agregar_label(8, 1,'Creación de extremo de problema')
        c1.agregar_button(9, 1, "Ir", self.nuevo_mp)
        c1.agregar_label(10, 1,' ')
        c1.agregar_button(13, 2, "Volver", self.volver_anterior)


    #----------------------------------------------------------------------
    def pendientes_eq2(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = busqueda_dr.Pendientes_eq2_calificarrpta(self, 580, 1300, 
                    "Documentos pendientes de calificar respuesta - Equipo 2")

    #----------------------------------------------------------------------
    def pendientes_prog(self):

        self.desaparecer()
        # LargoxAncho
        # SubFrame = vista_dr.Doc_recibidos_vista(self, 650, 1150, 
        #            "Registra de un nuevo documento recibido")
