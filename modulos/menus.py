import datetime as dt
import webbrowser
from tkinter import messagebox
from apoyo.funcionalidades_ospa import funcionalidades_ospa
from modulos import ventanas_busqueda, ventanas_vista
import apoyo.datos_frecuentes as df
from apoyo.elementos_de_GUI import Cuadro, Ventana

# I. Inicio de aplicativo
class inicio_app_OSPA(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c0 = Cuadro(self)
        c0.agregar_label(0, 1, ' ')
        c0.agregar_label(1, 1, ' ')
        c0.agregar_label(2, 1, ' ')
        c0.agregar_imagen(3, 1,'Logo_OSPA.png', df.ancho_logo, df.alto_logo)
        c0.agregar_label(4, 1, ' ')
        c1 = Cuadro(self)
        c1.agregar_label(5, 1,' ')
        c1.agregar_label(6, 1,' ')
        c1.agregar_label(7, 1,' ')
        c1.agregar_boton_grande(8, 1, "Equipos", self.pantallaequipos, 20, color = "Modelo1")
        c1.agregar_label(9, 1,' ')
        c1.agregar_label(10, 1,' ')
        c1.agregar_label(11, 1,' ')
        c1.agregar_boton_grande(12, 1, "Buscadores", self.pantallabuscadores, 20, color = "Modelo1")
        c1.agregar_label(13, 1, ' ')
        c1.agregar_label(14, 1, ' ')
        c1.agregar_label(15, 1, ' ')
        c1.agregar_label(16, 1, ' ')
        
     
        c2 = Cuadro(self)
        c2.agregar_franja_inferior('Franja_Inferior_OSPA.png', df.alto_franja_inferior_1, df.ancho_franja_inferior_1)


    #----------------------------------------------------------------------
    def n_busqueda_mp(self):
        
        self.desaparecer()

        texto_b_mp = "Búsqueda de macroproblemas"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Macroproblemas(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_mp, False, 
                                                    nuevo = False)
    
    #----------------------------------------------------------------------
    def n_busqueda_ep(self):
        
        self.desaparecer()

        texto_b_pr = "Búsqueda de problemas"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Extremos(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_pr, False)

    #----------------------------------------------------------------------
    def n_busqueda_dr(self):

        self.desaparecer()

        texto_b_dr = "Búsqueda de documentos recibidos"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Doc_recibidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_dr, False)
    
    #----------------------------------------------------------------------
    def n_busqueda_de(self):

        self.desaparecer()

        texto_b_de = "Búsqueda de documentos emitidos"
        # LargoxAncho
        SubFrame = ventanas_busqueda.Doc_emitidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_de, False)

    
    #----------------------------------------------------------------------
    def pantallaequipos(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Equipos(self, df.alto_ventana_secundaria, df.ancho_ventana_secundaria,  "Pantalla de equipos")

        #----------------------------------------------------------------------
    def pantallabuscadores(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = Buscadores(self, df.alto_ventana_secundaria, df.ancho_ventana_secundaria,  "Pantalla de buscadores")

    #----------------------------------------------------------------------
    def volver_anterior(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

# II. Menú Equipos
class Equipos(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo = None):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        # Información sobre la ventana
        self.nuevo = nuevo

        c0 = Cuadro(self)
        c0.agregar_label(0, 0, ' ')
        c0.agregar_imagen(1, 0,'Logo_OSPA.png', df.ancho_logo, df.alto_logo)
        
        c1 = Cuadro(self)
        c1.agregar_label(2, 0,' ')
        #c1.agregar_label(4, 0,'Seguimiento al problema')
        c1.agregar_boton_grande(3, 1, "Asignaciones pendientes", self.jefe_asig, 20, color = "Modelo2")
        c1.agregar_label(3, 0,'JEFE')
        c1.agregar_boton_grande(4, 1, "Documentos por firmar", self.jefe_firma, 20, color = "Modelo2")
        c1.agregar_label(5, 1,' ')
        c1.agregar_boton_grande(6, 1, "Documento recibido", self.nuevo_dr, 20, color = "Modelo1")
        c1.agregar_label(6, 0,'ADMINISTRATIVO')
        c1.agregar_boton_grande(7, 1, "Envío de reiterativo/OCI", self.Pendientes_reiterar, 20, color = "Modelo1")
        c1.agregar_boton_grande(8, 1, "Notificación documentos", self.Pendientes_notificar, 20, color = "Modelo1")
        c1.agregar_label(9, 1,' ')
        c1.agregar_label(10, 0,'EQUIPO 1')
        c1.agregar_boton_grande(10, 1, "Asignaciones pendientes", self.pendientes_eq1, 20, color = "Modelo2")
        c1.agregar_label(11, 1,' ')
        c1.agregar_boton_grande(12, 1, "Calificación de respuestas", self.pendientes_eq2, 20, color = "Modelo1")
        c1.agregar_label(12, 0,'EQUIPO 2')
        c1.agregar_boton_grande(13, 1, "Programaciones", self.pendientes_prog, 20, color = "Modelo1")
        c1.agregar_label(14, 1,' ')

        c2 = Cuadro(self)
        c2.agregar_boton_grande(15, 0, "Volver", self.volver_anterior, 12, color = "Modelo1")
        c2.agregar_boton_grande(15, 1, "Acceso BD", self.LinkBD, 12, color = "Modelo1")
        c2.agregar_boton_grande(15, 2, "Tablero control", self.LinkTC, 12, color = "Modelo1")


        c3 = Cuadro(self)
        c3.agregar_franja_inferior('Franja_Inferior_OSPA.png', df.alto_franja_inferior_1, df.ancho_franja_inferior_1)

 #----------------------------------------------------------------------
    def jefe_asig(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_jefe_asignar(self, df.alto_v_busqueda, df.ancho_v_busqueda, "Documentos pendientes de asignar")
    
#----------------------------------------------------------------------
    def jefe_firma(self):
        
        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_jefe_firma(self, df.alto_v_busqueda, df.ancho_v_busqueda, "Documentos pendientes de firma")
#----------------------------------------------------------------------

    def Pendientes_reiterar(self):

        self.desaparecer()
        # LargoxAncho

        SubFrame = ventanas_busqueda.Pendientes_por_reiterar(self, df.alto_v_busqueda, df.ancho_v_busqueda, 
                    "Documentos pendientes de reiterar/comunicar al OCI")

#----------------------------------------------------------------------
    def Pendientes_notificar(self):

        self.desaparecer()
        # LargoxAncho

        SubFrame = ventanas_busqueda.Pendientes_notificar(self, df.alto_v_busqueda, df.ancho_v_busqueda, 
                    "Documentos pendientes de notificación")

#----------------------------------------------------------------------
    def pendientes_eq1(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq1_trabajar(self, df.alto_v_busqueda, df.ancho_v_busqueda, "Documentos pendientes de trabajar")

    #----------------------------------------------------------------------
    def pendientes_eq2(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq2_calificarrpta(self, df.alto_v_busqueda, df.ancho_v_busqueda, 
                    "Documentos pendientes de calificar respuesta")

    #----------------------------------------------------------------------
    def pendientes_prog(self):

        self.desaparecer()
        # LargoxAncho
        SubFrame = ventanas_busqueda.Pendientes_eq2_programaciones(self, df.alto_v_busqueda, df.ancho_v_busqueda, 
                    "Programaciones")
    #----------------------------------------------------------------------
    def LinkBD(self):

        webbrowser.open("https://docs.google.com/spreadsheets/d/1gEjSnBH53SDyyyetMKZ0ci9XYvAvaDcLtl7w2Ax717U/edit#gid=1146630177")
    
    #----------------------------------------------------------------------
    def LinkTC(self):

        webbrowser.open("https://datastudio.google.com/u/0/reporting/6df9744f-15c8-4d44-86ab-5421643636fc/page/zMF5B?s=qNfv_U6QI-c")


class Buscadores(inicio_app_OSPA):
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo = None):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        # Información sobre la ventana
        self.nuevo = nuevo
        
        c0 = Cuadro(self)
        c0.agregar_label(0, 1, ' ')
        c0.agregar_label(1, 1, ' ')
        c0.agregar_imagen(2, 1,'Logo_OSPA.png', df.ancho_logo, df.alto_logo)
        c0.agregar_label(3, 1, ' ')
        c1 = Cuadro(self)
        c1.agregar_label(4, 1,' ')
        c1.agregar_label(5, 1,' ')
        c1.agregar_boton_grande(6, 1, "Macroproblemas", self.n_busqueda_mp, 20, color = "Modelo1")
        c1.agregar_label(7, 1,' ')
        c1.agregar_boton_grande(8, 1, "Problemas", self.n_busqueda_ep, 20, color = "Modelo1")
        c1.agregar_label(9, 1,' ')
        c1.agregar_boton_grande(10, 1, "Documentos recibidos", self.n_busqueda_dr, 20, color = "Modelo1")
        c1.agregar_label(11, 1,' ')
        c1.agregar_boton_grande(12, 1, "Documentos emitidos", self.n_busqueda_de, 20, color = "Modelo1")
        c1.agregar_label(13, 1, ' ')
        c1.agregar_label(14, 1, ' ')
        c1.agregar_label(15, 1, ' ')
       

        c2 = Cuadro(self)
        c2.agregar_boton_grande(16, 0, "Volver", self.volver_anterior, 12, color = "Modelo1")


        c3 = Cuadro(self)
        c3.agregar_franja_inferior('Franja_Inferior_OSPA.png', df.alto_franja_inferior_1, df.ancho_franja_inferior_1)
