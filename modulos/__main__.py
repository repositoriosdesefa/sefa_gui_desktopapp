from tkinter import Tk

from modulos import logueo, menus

from apoyo.elementos_de_GUI import Ventana

########################################################################
class Aplicacion(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        self.root = parent
        self.root.withdraw()
        #subFrame = logueo.logueo1_Ingreso_de_usuario(self, 590, 453, "ASPA - Versión 0.0", False)
        subFrame = menus.inicio_app_OSPA(self, 600, 403, 'Bienvenido')

        # LargoxAncho
        # subFrame = vista_dr.Doc_recibidos_vista(self, 650, 1100,'Documentos recibidos')


#----------------------------------------------------------------------
def main():
    root = Tk()
    root.iconbitmap('images/A_de_ASPA.ico')
    app = Aplicacion(root)
    root.mainloop()

