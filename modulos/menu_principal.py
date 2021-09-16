import pandas as pd
from tkinter import Tk
from apoyo.elementos_de_GUI import Cuadro, Ventana

class Menu_principal(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1= Cuadro(self)
        c1.agregar_button(0,0,'OSPA', self.ir_a_OSPA)
        c1.agregar_button(0,1,'Volver', self.volver)
    
    #----------------------------------------------------------------------
    def ir_a_OSPA(self):
        """"""

        print('Ir al aplicativo del OSPA')
