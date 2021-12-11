import datetime as dt

from tkinter import messagebox

from modulos.funcionalidades_ospa import funcionalidades_ospa
from modulos import ventanas_busqueda, ventanas_vista
from modulos import variables_globales as vg

from apoyo.elementos_de_GUI import Cuadro, Ventana

# Parámetros ventana
ancho_v_vista = vg.ancho_v_vista
alto_v_vista = vg.alto_v_vista
ancho_v_busqueda = vg.ancho_v_busqueda
alto_v_busqueda = vg.alto_v_busqueda

# 0. Métodos de generación de ventanas
class ventanas_ospa(funcionalidades_ospa):
    """"""
    def __init__(self, *args):
        """Constructor"""

# I. Inicio de aplicativo
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

        c2 = Cuadro(self)
        c2.agregar_franja_inferior('Franja_Inferior_OSPA.png', 70, 400)

    #----------------------------------------------------------------------
    def inicio_jefe(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_jefe(self, 400, 400, "Bienvenido/a Jefe/a del OSPA", False)
    
    #----------------------------------------------------------------------
    def inicio_adm(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_admin(self, 250, 400, "Bienvenido/a")

    #----------------------------------------------------------------------
    def inicio_e1(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Inicio_eq1(self, 250, 400, "Documentos emitidos")
    
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

# II. Menú de jefe
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
        c1.agregar_label(6, 1,'Creación de macroproblema')
        c1.agregar_button(7, 1, "Ir", self.nuevo_mp)
        c1.agregar_label(8, 1,'Búsqueda')
        c1.agregar_button(9, 1, "Ir", self.ver_menu_busquedas)
        c1.agregar_label(10, 1,' ')
        c1.agregar_button(13, 2, "Volver", self.volver_anterior)

    #----------------------------------------------------------------------
    def jefe_asig(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_jefe_asignar(self, 500, 1000, "Documentos pendientes de asignar")
    
    #----------------------------------------------------------------------
    def jefe_firma(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_jefe_firma(self, 550, 1300, "Documentos pendientes de firma")
    
    #----------------------------------------------------------------------
    def ver_menu_busquedas(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_busquedas(self, 450, 400, 
                    "Búsquedas", False)

# III. Menú de búsquedas
class Menu_busquedas(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0, 1, ' ')
        c1.agregar_imagen(1, 1,'Logo_OSPA.png',202,49)
        c1.agregar_label(2, 1,'Búsqueda DR')
        c1.agregar_button(3, 1, "Ir", self.n_busqueda_dr)
        c1.agregar_label(4, 1,'Búsqueda DE')
        c1.agregar_button(5, 1, "Ir", self.n_busqueda_de)
        c1.agregar_label(6, 1,'Búsqueda de extremos')
        c1.agregar_button(7, 1, "Ir", self.n_busqueda_ep)
        c1.agregar_label(8, 1,'Búsqueda de macroproblemas')
        c1.agregar_button(9, 1, "Ir", self.n_busqueda_mp)
        c1.agregar_label(10, 1,'Búsqueda de administrados')
        c1.agregar_button(11, 1, "Ir", self.n_busqueda_administrados)
        c1.agregar_label(12, 1,' ')
        c1.agregar_button(14, 2, "Volver", self.volver_anterior)
    
    #----------------------------------------------------------------------
    def n_busqueda_dr(self):

        self.desaparecer()

        texto_b_dr = "Búsqueda de documentos recibidos"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Doc_recibidos_busqueda(self, alto_v_busqueda, ancho_v_busqueda, texto_b_dr, False)
     

    #----------------------------------------------------------------------
    def n_busqueda_de(self):

        self.desaparecer()

        texto_b_de = "Búsqueda de documentos emitidos"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Doc_emitidos_busqueda(self, alto_v_busqueda, ancho_v_busqueda, False)
    
    #----------------------------------------------------------------------
    def n_busqueda_ep(self):
        
        self.desaparecer()

        texto_b_ep = "Búsqueda de extremos de problemas"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Extremos(self, alto_v_busqueda, ancho_v_busqueda, texto_b_ep, False)
    

    #----------------------------------------------------------------------
    def n_busqueda_mp(self):
        
        self.desaparecer()

        texto_b_mp = "Búsqueda de macroproblemas"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Macroproblemas(self, alto_v_busqueda, ancho_v_busqueda, texto_b_mp, False)
    
    #----------------------------------------------------------------------
    def n_busqueda_administrados(self):
        
        self.desaparecer()

        texto_b_adm = "Búsqueda de administrados"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Administrados(self, alto_v_busqueda, ancho_v_busqueda, texto_b_adm, False)

# IV. Menú administrativo    
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
        SubFrame = ventanas_vista.Doc_recibidos_vista(self, 650, 1150, 
                    "Registra de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def Pendientes_reiterar(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_por_reiterar(self, 560, 1090, "Documentos pendientes de reiterar/comunicar al OCI")

# V. Menú Equipo 1
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
        SubFrame = ventanas_busqueda.Pendientes_eq1_trabajar(self, 560, 1150, "Documentos pendientes de trabajar")

# VI. Menú Equipo 2
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
        c1.agregar_label(8, 1,'Creación de macroproblema')
        c1.agregar_button(9, 1, "Ir", self.nuevo_mp)
        c1.agregar_label(10, 1,' ')
        c1.agregar_button(13, 2, "Volver", self.volver_anterior)


    #----------------------------------------------------------------------
    def pendientes_eq2(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq2_calificarrpta(self, 580, 1300, 
                    "Documentos pendientes de calificar respuesta")

    #----------------------------------------------------------------------
    def pendientes_prog(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq2_programaciones(self, 580, 1300, 
                    "Programaciones")