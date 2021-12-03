from tkinter import Tk

from modulos import logueo
from modulos.administracion import Pantalla_de_usuario


########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()

        subFrame = logueo.logueo1_Ingreso_de_usuario(self, 400, 400, "ASPA - Versión 0.0")

        #subFrame = inicio_app_OSPA(self, 400, 400, "Inicio")
        
        # LargoxAncho
        # subFrame = vista_dr.Doc_recibidos_vista(self,650, 1100,'Documentos recibidos')


#----------------------------------------------------------------------
def main():
    root = Tk()
    root.iconbitmap('images/S_de_Sefa.ico')
    app = Aplicacion(root)
    root.mainloop()

