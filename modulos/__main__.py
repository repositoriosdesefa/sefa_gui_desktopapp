from tkinter import Tk

#from modulos import logueo

from modulos.menus import  inicio_app_OSPA
#from modulos.vista_dr import inicio_app_OSPA


########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()

        #subFrame = logueo.logueo1_Ingreso_de_usuario(self, 450, 400, "Herramientas de Sefa - Versión 0.0")

        subFrame = inicio_app_OSPA(self, 400, 400, "Inicio")
        
        # LargoxAncho
        # subFrame = vista_dr.Doc_recibidos_vista(self,650, 1100,'Documentos recibidos')


#----------------------------------------------------------------------
def main():
    root = Tk()
    root.iconbitmap('images/S_de_Sefa.ico')
    app = Aplicacion(root)
    root.mainloop()

