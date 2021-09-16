from tkinter import Tk
from modulos import logueo
from modulos import vista_dr
from modulos import administracion

########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()
        subFrame = vista_dr.Doc_recibidos_vista(self, 650, 1200, "Inicio")
        
        # LargoxAncho
        # subFrame = vista_dr.Doc_recibidos_vista(self,650, 1100,'Documentos recibidos')

#----------------------------------------------------------------------
def main():
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()

