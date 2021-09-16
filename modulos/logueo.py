import datetime as dt
import pandas as pd
from tkinter import Tk, messagebox
from apoyo.elementos_de_GUI import Cuadro, Ventana
from apoyo.manejo_de_bases import Base_de_datos, Correo_electronico
from modulos import administracion as adm
from modulos import menu_principal as mp
from modulos import variables_globales as vg

class logueo1_Ingreso_de_usuario(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        c1.agregar_imagen(1,0,'herramientas_de_sefa.png',300,100)
        c1.agregar_titulo(2,0,'ACCESO DE USUARIOS')

        self.c2 = Cuadro(self)
        rejilla = (
            ('L',0,0,'Correo electrónico:'),
            ('E',1,0),
            ('L',2,0, 'Contraseña:'),
            ('EP',3,0)
        )
        self.c2.agregar_rejilla(rejilla)

        c3 = Cuadro(self)
        c3.agregar_label(0,0,' ')
        c3.agregar_button(1,0,'Ingresar', self.comprobar_datos)

        c4 = Cuadro(self)
        rejilla2 = (
            ('BL',0,0,'Recuperar contraseña', self.ir_a_recuperar_contrasena),
            ('BL',1,0,'Cambiar contraseña', self.ir_a_cambiar_contrasena),
            ('BL',2,0,'Acceso de administrador', self.ir_a_administracion)
        )
        c4.agregar_rejilla(rejilla2)

    #----------------------------------------------------------------------
    def comprobar_datos(self):
        """"""

        datos_ingresados = self.c2.obtener_lista_de_datos()
        correo = datos_ingresados[0]
        contrasenna = datos_ingresados[1]

        b1 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Usuario')
        b2 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Datos_de_usuario')

        if b1.contar_coincidencias(correo) == 0:
            messagebox.showerror('Error al ingresar datos', 'Usted ha ingresado un correo electrónico no registrado.')
        else:
            lista_para_identificar_usuario = b1.listar_datos_de_fila(correo)
            vg.cod_usuario = lista_para_identificar_usuario[0]
            lista_con_datos_de_usuario = b2.listar_datos_de_fila(vg.cod_usuario)
            if lista_con_datos_de_usuario[7] == 'ELIMINADO':
                messagebox.showinfo('Usuario deshabilitado', 'El correo ingresado pertenece a un usuario que se encuentra deshabilitado. En caso de requerir su habilitación, por favor contáctese con el administrador a través del correo proyectossefa@oefa.gob.pe')
            else:
                if lista_con_datos_de_usuario[6] != contrasenna:
                    messagebox.showerror('Error al ingresar datos', 'Usted ha ingresado una contraseña incorrecta')
                else:
                    vg.usuario = lista_con_datos_de_usuario[4]
                    vg.oficina = lista_con_datos_de_usuario[5]
                    self.ir()

    #----------------------------------------------------------------------
    def ir(self):
        """"""
        
        self.desaparecer()
        subframe = mp.Menu_principal(self, 500, 500, 'Menu principal')
    
    #----------------------------------------------------------------------
    def ir_a_recuperar_contrasena(self, event):
        """"""

        self.desaparecer()
        subframe = logueo2_Recuperar_contrasena(self, 350, 500,'Recuperar contraseña')

    #----------------------------------------------------------------------
    def ir_a_cambiar_contrasena(self, event):
        """"""

        self.desaparecer()
        subframe = logueo3_Cambiar_contrasena(self, 500, 500,'Cambiar contraseña')
    
    #----------------------------------------------------------------------
    def ir_a_administracion(self, event):
        """"""

        self.desaparecer()
        subframe = adm.Ingresar_contrasena_de_adminitrador(self, 450,400,'Acceso de administrador')

class logueo2_Recuperar_contrasena(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)

        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        c1.agregar_imagen(1,0,'email.png',100,100)
        c1.agregar_titulo(2,0,'RECUPERAR CONTRASEÑA')

        self.c2 = Cuadro(self)
        rejilla = (
            ('L',0,0,'Correo electrónico:'),
            ('E',1,0)
        )
        self.c2.agregar_rejilla(rejilla)

        c3 = Cuadro(self)
        c3.agregar_label(0,0,' ')
        c3.agregar_button(1,0,'Enviar', self.enviar_contrasena_al_email)
        c3.agregar_button(1,1,'Volver', self.volver)

    #----------------------------------------------------------------------
    def enviar_contrasena_al_email(self):
        """"""

        datos_ingresados = self.c2.obtener_lista_de_datos()
        correo = datos_ingresados[0]

        b1 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Usuario')
        b2 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Datos_de_usuario')

        if b1.contar_coincidencias(correo) == 0:
            messagebox.showerror('Error al ingresar datos', 'Usted ha ingresado un correo electrónico no registrado.')
        else:
            lista_para_identificar_usuario = b1.listar_datos_de_fila(correo)
            vg.cod_usuario = lista_para_identificar_usuario[0]
            lista_con_datos_de_usuario = b2.listar_datos_de_fila(vg.cod_usuario)
            if lista_con_datos_de_usuario[7] == 'ELIMINADO':
                messagebox.showinfo('Usuario deshabilitado', 'El correo ingresado pertenece a un usuario que se encuentra deshabilitado. En caso de requerir su habilitación, por favor contáctese con el administrador a través del correo proyectossefa@oefa.gob.pe.')
            else:
                contrasena = lista_con_datos_de_usuario[6]
                asunto = 'Herramientas de Sefa | Recuperación de contraseña'
                mensaje = 'Su contraseña actual es: ' + contrasena

                email = Correo_electronico(correo, asunto, mensaje)
                email.enviar()
                self.volver()
                messagebox.showwarning('Operación exitosa', 'Su contraseña ha sido enviada a su correo electrónico. Si tuviese algún problema para recuperar su contraseña, por favor contáctese con el administrador a través del correo proyectossefa@oefa.gob.pe.')

class logueo3_Cambiar_contrasena(Ventana):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""

        Ventana.__init__(self, *args)
    
        c1 = Cuadro(self)
        c1.agregar_label(0,0,' ')
        c1.agregar_imagen(1,0,'password.png',100,100)
        c1.agregar_titulo(2,0,'CAMBIAR CONTRASEÑA')

        self.c2 = Cuadro(self)
        rejilla = (
            ('L',0,0,'Correo electrónico:'),
            ('E',1,0),
            ('L',2,0,'Contraseña actual:'),
            ('E',3,0),
            ('L',4,0,'Nueva contraseña:'),
            ('E',5,0),
            ('L',6,0,'Confirmar nueva contraseña:'),
            ('E',7,0),
        )
        self.c2.agregar_rejilla(rejilla)

        c3 = Cuadro(self)
        c3.agregar_label(0,0,' ')
        c3.agregar_button(1,0,'Cambiar', self.cambiar_contrasena)
        c3.agregar_button(1,1,'Volver', self.volver)

    #----------------------------------------------------------------------
    def cambiar_contrasena(self):
        """"""

        datos_ingresados = self.c2.obtener_lista_de_datos()
        correo = datos_ingresados[0]
        contrasenna_actual = datos_ingresados[1]
        nueva_contrasenna = datos_ingresados[2]
        nueva_contrasenna_confirmacion = datos_ingresados[3]

        b1 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Usuario')
        b2 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Datos_de_usuario')
        b3 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY', 'Historial')

        if b1.contar_coincidencias(correo) == 0:
            messagebox.showerror('Error al ingresar datos', 'Usted ha ingresado un correo electrónico no registrado.')
        else:
            lista_para_identificar_usuario = b1.listar_datos_de_fila(correo)
            vg.cod_usuario = lista_para_identificar_usuario[0]
            lista_con_datos_de_usuario = b2.listar_datos_de_fila(vg.cod_usuario)
            if lista_con_datos_de_usuario[7] == 'ELIMINADO':
                messagebox.showinfo('Usuario deshabilitado', 'El correo ingresado pertenece a un usuario que se encuentra deshabilitado. En caso de requerir su habilitación, por favor contáctese con el administrador a través del correo proyectossefa@oefa.gob.pe')
            else:
                if lista_con_datos_de_usuario[6] != contrasenna_actual:
                    messagebox.showerror('Error al ingresar datos', 'Usted ha ingresado una contraseña incorrecta.')
                else:
                    if nueva_contrasenna != nueva_contrasenna_confirmacion:
                        messagebox.showerror('Error al ingresar datos', 'La nueva contraseña no coincide con el texto ingresado para su confirmación.')
                    else:
                        b2.cambiar_un_dato_de_una_fila(vg.cod_usuario, 7, nueva_contrasenna)
                        nuevos_datos_de_usuario = b2.listar_datos_de_fila(vg.cod_usuario)
                        hora = str(dt.datetime.now())
                        nuevos_datos_de_usuario_para_historial = nuevos_datos_de_usuario + [hora]
                        b3.agregar_datos(nuevos_datos_de_usuario_para_historial)
                        self.volver()
                        messagebox.showwarning('Operación exitosa', 'Su contraseña ha sido modificada.')

