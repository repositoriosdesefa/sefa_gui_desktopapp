from tkinter import Tk
from modulos import logueo
from modulos import administracion

########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()
        #subFrame = logueo.logueo1_Ingreso_de_usuario(self, 500, 500, "Ventana 1")

        subFrame = administracion.Administrar_usuarios(self, 500,1200,'Permisos de administrador')

#----------------------------------------------------------------------
def main():
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()

