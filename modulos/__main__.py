from tkinter import Tk
#from modulos.menus import  inicio_app_OSPA
from modulos.vista_dr import inicio_app_OSPA

########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()
        subFrame = inicio_app_OSPA(self, 350, 400, "Inicio")
        
        # LargoxAncho
        # subFrame = vista_dr.Doc_recibidos_vista(self,650, 1100,'Documentos recibidos')

#----------------------------------------------------------------------
def main():
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()

