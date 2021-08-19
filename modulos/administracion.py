import pandas as pd
from tkinter import Tk
from apoyo.elemetos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos
from apoyo.vsf import Vitrina_vista
import apoyo.datos_frecuentes as dfrec

class Ingresar_contrasena_de_adminitrador(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

        self.c1 = Cuadro(self)
        self.c1.agregar_label(0,0,' ')
        self.c1.agregar_imagen(1,0,'Logo_OSPA.png',350,120)
        self.c1.agregar_titulo(2,0,'Inicio')
        
        rejilla =(
            ('L',0,0,'Usuario:'),
            ('E',1,0),
            ('L',2,0,'Contraseña:'),
            ('EP',3,0)
        )
        self.c2 = Cuadro(self)
        self.c2.agregar_rejilla(rejilla)

        self.c3 = Cuadro(self)
        self.c3.agregar_label(0,0,' ')
        self.c3.agregar_button(1,0,'Acceder', self.comprobar_datos_de_administrador)
        self.c3.agregar_button(1,1,'Volver', self.volver)
    
    #----------------------------------------------------------------------
    def ir(self):
        """"""
        
        self.desaparecer()
        subframe = Administrar_usuarios(self, 500, 1300, 'Interfaz para el control de usuarios')

    #----------------------------------------------------------------------
    def comprobar_datos_de_administrador(self):
        """"""

        datos_ingresados = self.c2.obtener_lista_de_datos()
        b0 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY','Administrador')
        datos_registrados = b0.listar_datos_de_fila('ADMIN_001')
        if datos_ingresados[0] != datos_registrados[1]:
            print('Usuario incorrecto')
        else:
            if datos_ingresados[1] != datos_registrados[2]:
                print('Contraseña incorrecta')
            else:
                self.ir()

class Administrar_usuarios(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

        b1 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Datos_de_usuario')
        tabla_de_usuarios = b1.generar_dataframe()
        tabla_de_usuarios = tabla_de_usuarios.drop(['Nombres', 'Apellidos', 'Contraseña'], axis=1)

        self.c1 = Cuadro(self)
        self.c1.agregar_label(0,0,' ')
        self.c1.agregar_imagen(1,0,'Logo_OSPA.png',692,200)
        self.c1.agregar_titulo(2,0,'Inicio')
        
        v1 = Vitrina_vista(self, tabla_de_usuarios, self.ver_usuario, self.funcion_de_prueba, self.funcion_de_prueba, height=120, width=850)

        c2 = Cuadro(self)
        c2.agregar_button(0,0,'Crear usuario', self.ir_a_crear_usuario)
        c2.agregar_button(0,1,'Menu principal', self.ir_a_crear_usuario)
    
    #----------------------------------------------------------------------
    def ir_a_crear_usuario(self):
        """"""
        self.desaparecer()
        subframe = Pantalla_de_usuario(self, 500, 400, 'Nuevo usuario')
    
    #----------------------------------------------------------------------
    def ver_usuario(self, x):
        """"""
        
        self.x = x
        texto_usuario = 'Usuario: ' + x

        b1 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY','Usuario')
        lb1 = b1.listar_datos_de_fila(self.x)
        b2 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY','Datos_de_usuario')
        lb2 = b2.listar_datos_de_fila(self.x)
        lista_para_insertar = [lb1[3],lb2[1],lb2[2],lb2[4]]
        
        self.desaparecer()
        subframe = Pantalla_de_usuario(self, 500, 400, texto_usuario, nuevo=False, lista=lista_para_insertar)
    
    #----------------------------------------------------------------------
    def funcion_de_prueba(self, x):
        """"""

        print(x)

class Pantalla_de_usuario(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None):
        """Constructor"""

        Ventana.__init__(self, *args)

        self.nuevo = nuevo

        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        if self.nuevo == True:
            c1.agregar_imagen(1,0,'agregar_usuario.png',100,100)
        else:
            c1.agregar_imagen(1,0,'usuario.png',100,100)
        c1.agregar_label(2,0,' ')
        
        rejilla = (
            ('L', 0, 0, 'Correo electrónico:'),
            ('E', 1, 0),
            ('L', 2, 0, 'Nombres:'),
            ('E', 3, 0),
            ('L', 4, 0, 'Apellidos:'),
            ('E', 5, 0),
            ('L', 6, 0, 'Oficina:'),
            ('CX', 7, 0, dfrec.oficinas)
        )
        
        c2 = Cuadro(self)
        c2.agregar_rejilla(rejilla)

        if self.nuevo != True:
            self.lista_para_insertar = lista
            c2.insertar_lista_de_datos(self.lista_para_insertar)

        c3 = Cuadro(self)
        c3.agregar_label(0,0,' ')
        if self.nuevo == True:
            c3.agregar_button(1,0,'Crear', self.crear_nuevo_usuario)
        else:
            c3.agregar_button(1,0,'Guardar', self.guardar_cambios_usuario)
        c3.agregar_button(1,1, 'Volver', self.volver)
    
    #----------------------------------------------------------------------
    def crear_nuevo_usuario(self):
        """"""


    #----------------------------------------------------------------------
    def guardar_cambios_usuario(self):
        """"""



