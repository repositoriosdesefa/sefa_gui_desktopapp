import datetime as dt

from tkinter import messagebox

from modulos.funcionalidades_ospa import funcionalidades_ospa
from modulos import ventanas_busqueda, ventanas_vista
from modulos import variables_globales as vg

from apoyo.elementos_de_GUI import Cuadro, Ventana

# Parámetros ventana
alto_ventana_secundaria = vg.alto_ventana_secundaria
ancho_ventana_secundaria = vg.ancho_ventana_secundaria

ancho_v_vista = vg.ancho_v_vista
alto_v_vista = vg.alto_v_vista
ancho_v_busqueda = vg.ancho_v_busqueda
alto_v_busqueda = vg.alto_v_busqueda

alto_logo = vg.alto_logo
ancho_logo = vg.ancho_logo

alto_franja_inferior_1 = vg.alto_franja_inferior_1
ancho_franja_inferior_1 = vg.ancho_franja_inferior_1

# I. Inicio de aplicativo
class inicio_app_OSPA(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c0 = Cuadro(self)
        c0.agregar_label(0, 1, ' ')
        c0.agregar_imagen(1, 1,'Logo_OSPA.png', ancho_logo, alto_logo)
        c1 = Cuadro(self)
        c1.agregar_label(1, 1,'Jefe')
        c1.agregar_button(2, 1, "Ir", self.inicio_jefe)
        c1.agregar_label(3, 1,'Equipo Administrativo')
        c1.agregar_button(4, 1, "Ir", self.inicio_adm)
        c1.agregar_label(5, 1,'Equipo 1')
        c1.agregar_button(6, 1, "Ir", self.inicio_e1)
        c1.agregar_label(7, 1,'Equipo 2')
        c1.agregar_button(8, 1, "Ir", self.inicio_e2)
        c1.agregar_label(9, 1, ' ')

        c2 = Cuadro(self)
        c2.agregar_franja_inferior('Franja_Inferior_OSPA.png', alto_franja_inferior_1, ancho_franja_inferior_1)

    #----------------------------------------------------------------------
    def inicio_jefe(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_jefe(self, alto_ventana_secundaria, ancho_ventana_secundaria, "Bienvenido/a Jefe/a del OSPA", False)
    
    #----------------------------------------------------------------------
    def inicio_adm(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_admin(self, alto_ventana_secundaria, ancho_ventana_secundaria,  "Bienvenido/a")

    #----------------------------------------------------------------------
    def inicio_e1(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Inicio_eq1(self, alto_ventana_secundaria, ancho_ventana_secundaria,  "Documentos emitidos")
    
    #----------------------------------------------------------------------
    def inicio_e2(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Inicio_eq2(self, alto_ventana_secundaria, ancho_ventana_secundaria,  "Búsqueda de documentos emitidos")

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

        c0 = Cuadro(self)
        c0.agregar_label(0, 1, ' ')
        c0.agregar_imagen(1, 0,'Logo_OSPA.png', ancho_logo, alto_logo)

        c1 = Cuadro(self)
        c1.agregar_label(2, 1,' ')
        c1.agregar_label(3, 1,' ')
        c1.agregar_label(4, 0,'Asignaciones pendientes')
        c1.agregar_button(4, 1, "Ir", self.jefe_asig)
        c1.agregar_label(5, 0,'Documentos por firmar')
        c1.agregar_button(5, 1, "Ir", self.jefe_firma)
        c1.agregar_label(6, 0,'Creación de macroproblema')
        c1.agregar_button(6, 1, "Ir", self.nuevo_mp)
        c1.agregar_label(7, 0,'Búsqueda')
        c1.agregar_button(7, 1, "Ir", self.ver_menu_busquedas)
        c1.agregar_label(8, 0,' ')
        c1.agregar_label(9, 1,' ')

        c2 = Cuadro(self)
        c2.agregar_button(0, 0, "Volver", self.volver_anterior)

        c3 = Cuadro(self)
        c3.agregar_franja_inferior('Franja_Inferior_OSPA.png', alto_franja_inferior_1, ancho_franja_inferior_1)


    #----------------------------------------------------------------------
    def jefe_asig(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_jefe_asignar(self, alto_v_busqueda, ancho_v_busqueda, "Documentos pendientes de asignar")
    
    #----------------------------------------------------------------------
    def jefe_firma(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_jefe_firma(self, alto_v_busqueda, ancho_v_busqueda, "Documentos pendientes de firma")
    
    #----------------------------------------------------------------------
    def ver_menu_busquedas(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = Menu_busquedas(self, alto_ventana_secundaria, ancho_ventana_secundaria, 
                    "Búsquedas", False)

# III. Menú de búsquedas
class Menu_busquedas(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c0 = Cuadro(self)
        c0.agregar_label(0, 0, ' ')
        c0.agregar_imagen(1, 0,'Logo_OSPA.png', ancho_logo, alto_logo)

        c1 = Cuadro(self)
        c1.agregar_label(3, 1,' ')
        c1.agregar_label(4, 0,'Búsqueda DR')
        c1.agregar_button(4, 1, "Ir", self.n_busqueda_dr)
        c1.agregar_label(5, 0,'Búsqueda DE')
        c1.agregar_button(5, 1, "Ir", self.n_busqueda_de)
        c1.agregar_label(6, 0,'Búsqueda de extremos')
        c1.agregar_button(6, 1, "Ir", self.n_busqueda_ep)
        c1.agregar_label(7, 0, 'Búsqueda de macroproblemas')
        c1.agregar_button(7, 1, "Ir", self.n_busqueda_mp)
        c1.agregar_label(8, 0,'Búsqueda de administrados')
        c1.agregar_button(8, 1, "Ir", self.n_busqueda_administrados)
        c1.agregar_label(9, 1,' ')

        c2 = Cuadro(self)
        c2.agregar_button(0, 0,  "Volver", self.volver_anterior)
        c2.agregar_label(1, 0,' ')

        c3 = Cuadro(self)
        c3.agregar_franja_inferior('Franja_Inferior_OSPA.png', alto_franja_inferior_1, ancho_franja_inferior_1)

    
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
        SubFrame = ventanas_busqueda.Macroproblemas(self, alto_v_busqueda, ancho_v_busqueda, texto_b_mp, False, 
                                                    nuevo = False)
    
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

        c0 = Cuadro(self)
        c0.agregar_label(0, 0, ' ')
        c0.agregar_imagen(1, 0,'Logo_OSPA.png', ancho_logo, alto_logo)
        c1 = Cuadro(self)
        c1.agregar_label(3, 0, ' ')
        c1.agregar_label(4, 0,'Registro documento recibido')
        c1.agregar_button(5, 0, "Ir", self.nuevo_dr)
        c1.agregar_label(6, 0,'Envío de reiterativo / OCI')
        c1.agregar_button(7, 0, "Ir", self.Pendientes_reiterar)
        c1.agregar_label(8, 0,'Notificación de documentos')
        c1.agregar_button(9, 0, "Ir", self.busqueda_de)

        c2 = Cuadro(self)
        c2.agregar_label(0, 1, ' ')
        c2.agregar_button(1, 0, "Volver", self.volver_anterior)

        c3 = Cuadro(self)
        c3.agregar_franja_inferior('Franja_Inferior_OSPA.png', alto_franja_inferior_1, ancho_franja_inferior_1)

    
    #----------------------------------------------------------------------
    def vista_dr(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_vista.Doc_recibidos_vista(self, alto_v_vista, ancho_v_vista, 
                    "Registro de un nuevo documento recibido")

    #----------------------------------------------------------------------
    def Pendientes_reiterar(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_por_reiterar(self, alto_v_busqueda, ancho_v_busqueda, 
                    "Documentos pendientes de reiterar/comunicar al OCI")

# V. Menú Equipo 1
class Inicio_eq1(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c0 = Cuadro(self)
        c0.agregar_label(0, 1, ' ')
        c0.agregar_imagen(1, 1,'Logo_OSPA.png', ancho_logo, alto_logo)

        c1 = Cuadro(self)
        c1.agregar_label(2, 0,' ')
        c1.agregar_label(3, 0,' ')
        c1.agregar_label(4, 0,'Asignaciones pendientes')
        c1.agregar_button(5, 0, "Ir", self.pendientes_eq1)
        c1.agregar_label(6, 0,'Creación de macroproblema'),
        c1.agregar_button(7, 0, "Ir", self.nuevo_mp)
        c1.agregar_label(8, 0,' ')
        c1.agregar_label(9, 0,' ')

        c2 = Cuadro(self)
        c2.agregar_label(0, 0,' ')
        c2.agregar_button(1, 0, "Volver", self.volver_anterior)

        c3 = Cuadro(self)
        c3.agregar_franja_inferior('Franja_Inferior_OSPA.png', alto_franja_inferior_1, ancho_franja_inferior_1)

    
    #----------------------------------------------------------------------
    def pendientes_eq1(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq1_trabajar(self, alto_v_busqueda, ancho_v_busqueda, "Documentos pendientes de trabajar")

# VI. Menú Equipo 2
class Inicio_eq2(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c0 = Cuadro(self)
        c0.agregar_label(0, 0, ' ')
        c0.agregar_imagen(1, 0,'Logo_OSPA.png', ancho_logo, alto_logo)
        
        c1 = Cuadro(self)
        c1.agregar_label(2, 0,' ')
        c1.agregar_label(3, 0,' ')
        c1.agregar_label(4, 0,'Seguimiento al problema')
        c1.agregar_button(4, 1, "Ir", self.busqueda_ep)
        c1.agregar_label(5, 0,'Calificación de respuesta')
        c1.agregar_button(5, 1, "Ir", self.pendientes_eq2)
        c1.agregar_label(6, 0,'Programaciones')
        c1.agregar_button(6, 1, "Ir", self.pendientes_prog)
        c1.agregar_label(7, 0,'Creación de macroproblema')
        c1.agregar_button(7, 1, "Ir", self.nuevo_mp)
        c1.agregar_label(8, 0,' ')
        c1.agregar_label(9, 0,' ')

        c2 = Cuadro(self)
        c2.agregar_button(7, 0, "Volver", self.volver_anterior)

        c3 = Cuadro(self)
        c3.agregar_franja_inferior('Franja_Inferior_OSPA.png', alto_franja_inferior_1, ancho_franja_inferior_1)



    #----------------------------------------------------------------------
    def pendientes_eq2(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq2_calificarrpta(self, alto_v_busqueda, ancho_v_busqueda, 
                    "Documentos pendientes de calificar respuesta")

    #----------------------------------------------------------------------
    def pendientes_prog(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq2_programaciones(self, alto_v_busqueda, ancho_v_busqueda, 
                    "Programaciones")