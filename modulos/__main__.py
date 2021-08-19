from tkinter import Tk
from modulos import logueo
from modulos import administracion
from modulos import vista_dr

########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()
        #subFrame = administracion.Ingresar_contrasena_de_adminitrador(self, 450, 400, "Inicio")
        
        # LargoxAncho
        subFrame = vista_dr.Doc_recibidos_vista(self,625, 1100,'Documentos recibidos')

#----------------------------------------------------------------------
def main():
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()

