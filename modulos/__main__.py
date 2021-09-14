from tkinter import Tk
from modulos import logueo

########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()
        subFrame = logueo.logueo1_Ingreso_de_usuario(self, 450, 400, "Acceso de usuarios")

#----------------------------------------------------------------------
def main():
    root = Tk()
    app = Aplicacion(root)
    root.mainloop()

