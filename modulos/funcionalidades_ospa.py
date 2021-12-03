from tkinter import  messagebox

from apoyo.elementos_de_GUI import  Ventana, Vitrina_vista
from modulos import menus, ventanas_busqueda, ventanas_vista, variables_globales

import datetime as dt

# 1. Bases
b_dr = variables_globales.b_dr
b_dr_cod = variables_globales.b_dr_cod
b_dr_hist = variables_globales.b_dr_hist
b_de = variables_globales.b_de
b_de_cod = variables_globales.b_de_cod
b_de_hist = variables_globales.b_de_hist
b_ep = variables_globales.b_ep
b_ep_cod = variables_globales.b_ep_cod
b_ep_hist = variables_globales.b_ep_hist
b_mp = variables_globales.b_mp
b_mp_cod = variables_globales.b_mp_cod
b_mp_hist = variables_globales.b_mp_hist
# 2. Tablas
tabla_parametros = variables_globales.tabla_parametros
tabla_parametros_dep = variables_globales.tabla_parametros_dep

class funcionalidades_ospa(Ventana):
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None):
        """Constructor"""
        
        # Objetos de clase
        self.nuevo = nuevo
        self.lista = lista
        self.id_objeto_ingresado = id_objeto

    #----------------------------------------------------------------------
    def inicio_app(self):
        """"""
        self.desaparecer()
        # LargoxAncho
        subFrame = menus.inicio_app_OSPA(self, 400, 400, "Inicio")
        
         #----------------------------------------------------------------------
    def guardar_objeto(self, rejilla_datos, 
                        cod_objeto_clase, cod_entrada, tabla_objeto_clase,
                        base_codigo_objeto, base_objeto_clase, base_objeto_clase_hist,
                        funcion_ver):
        """"""
        
        # 0. Obtengo los datos ingresados
	    # 0.1 Datos de rejilla
        rejilla_frame = rejilla_datos
        datos_ingresados = rejilla_frame.obtener_lista_de_datos()
        # 0.2 Parámetros de objeto
        codigo_objeto = cod_objeto_clase
        cod_objeto = cod_entrada
        tabla_objeto = tabla_objeto_clase
        base_objeto = base_objeto_clase
        base_objeto_hist = base_objeto_clase_hist
        base_cod_objeto = base_codigo_objeto
        tabla_objeto_clase = base_objeto.generar_dataframe()
        ahora = str(dt.datetime.now())
	
	    # A. Existe un código en la rejilla
        if self.nuevo == False:
            # Pestaña 1: Obtengo el ID interno a partir del código de usuario
            tabla_codigo_objeto_filtrada = tabla_objeto[tabla_objeto[cod_objeto]==codigo_objeto]
            id_interno_objeto_clase = tabla_codigo_objeto_filtrada.iloc[0,0]
            # Obtengo los datos ingresados
            lista_descargada_codigo = base_cod_objeto.listar_datos_de_fila(id_interno_objeto_clase)
            cod_objeto_clase = lista_descargada_codigo[3]
            correlativo = lista_descargada_codigo[2]

            if cod_entrada == "COD_DR":
                nuevo_cod_objeto_clase = datos_ingresados[0] + " " + datos_ingresados[1]
            elif cod_entrada == "COD_DE":
                nuevo_cod_objeto_clase = correlativo + "/" + datos_ingresados[0]
            else:
                nuevo_cod_objeto_clase = lista_descargada_codigo[3]
            
            # Actualizo las tablas en la web
            hora_de_modificacion = ahora
            # Se actualiza código interno
            base_objeto.cambiar_un_dato_de_una_fila(cod_objeto_clase, 4, nuevo_cod_objeto_clase)

            # Pestaña 2:       
            # Cambio los datos de una fila
            # Código interno del aplicativo + Código del usuario del DR + Hora de modificación
            lista_a_sobreescribir = [id_interno_objeto_clase] + [nuevo_cod_objeto_clase] + datos_ingresados + [hora_de_modificacion]
            base_objeto.cambiar_los_datos_de_una_fila(nuevo_cod_objeto_clase, lista_a_sobreescribir) # Se sobreescribe la información
            
            # Pestaña 3
            lista_historial = lista_a_sobreescribir
            base_objeto_hist.agregar_datos(lista_historial) # Se sube la info

            # Mensaje
            messagebox.showinfo("¡Excelente!", "Se ha actualizado el registro")
            funcion_ver(nuevo_cod_objeto_clase)

	    # B. Es un código nuevo
        else:
            # Caso especial para DR
            if cod_entrada =="COD_DR":
                cod_objeto_ingresado = datos_ingresados[0] + " " + datos_ingresados[1]
            else:
                cod_objeto_ingresado = datos_ingresados[0]

            # Comprobación de que no se ingresa un código de usuario repetido
            valor_de_comprobacion = self.comprobar_id(base_codigo_objeto, cod_objeto_ingresado) # Comprobar si el id de usuario ya existe

            if valor_de_comprobacion == True: # Verifico que lo ingresado no exista
                messagebox.showerror("Error", "Este documento ya existe")

            else:
                # Pestaña 1: Código Único
                # Creo el código único
                if cod_entrada == "COD_DR":
                    base_cod_objeto.agregar_codigo(cod_objeto_ingresado, ahora)
                elif cod_entrada == "COD_EP":
                    departamento = datos_ingresados[2]
	                # Obtención de sigla de departamento
                    tabla_siglas_filtrada = tabla_parametros_dep[tabla_parametros_dep['DEPARTAMENTO']==departamento]
                    sigla_cod_interno = tabla_siglas_filtrada.iloc[0,1]
		            # Obtención de número de extremo
                    tabla_objeto_clase = base_cod_objeto.generar_dataframe()
                    tabla_codigo_ep_filtrada = tabla_objeto_clase[tabla_objeto_clase['DEPARTAMENTO']==departamento]
                    numero_problemas = len(tabla_codigo_ep_filtrada.index) + 1
                    if numero_problemas < 10:
                        numero_codigo = "-00" + str(numero_problemas)
                    elif numero_problemas < 100:
                        numero_codigo = "-0" + str(numero_problemas)
                    else:
        	            numero_codigo = "-" + str(numero_problemas)
                    cod_objeto_ingresado = sigla_cod_interno + numero_codigo
                    base_cod_objeto.agregar_codigo(cod_objeto_ingresado, ahora, departamento)
                else:
                    base_cod_objeto.agregar_nuevo_codigo(cod_objeto_ingresado, ahora)

                # Descargo el código único
                lista_descargada_codigo = base_cod_objeto.listar_datos_de_fila(ahora) # Se trae la info
        
                # Pestaña 2:       
                # Obtengo el ID interno
                id_objeto = lista_descargada_codigo[0]
                cod_objeto = lista_descargada_codigo[3]
                # Creo el vector a subir 
                lista_a_cargar = [id_objeto] + [cod_objeto] + datos_ingresados + [ahora]
                base_objeto.agregar_datos(lista_a_cargar) # Se sube la info

                # Pestaña 3
                hora_de_creacion = str(ahora) # De lo creado en la pestaña 1
                lista_historial = lista_a_cargar + [hora_de_creacion] # Lo subido a la pestaña 2 + hora
                base_objeto_hist.agregar_datos(lista_historial) # Se sube la info

                # Actualización de base y confirmación de registro
                tabla_objeto_clase = base_cod_objeto.generar_dataframe()
                messagebox.showinfo("¡Excelente!", "Se ha ingresado un nuevo registro")
                funcion_ver(cod_objeto)
    
    #----------------------------------------------------------------------
    def eliminar_objeto(self, cod_objeto_clase, cod_entrada, 
                        cod_objeto_a_eliminar, cod_salida, 
                        tabla_objeto_clase, tabla_a_objeto_a_eliminar, 
                        base_relacion_objetos, base_relacion_hist):
        """"""
        # Objeto de Frame
        codigo_objeto = cod_objeto_clase
        cod_objeto = cod_entrada
        tabla_objeto = tabla_objeto_clase
        # Objeto de vitrina
        codigo_a_eliminar = cod_objeto_a_eliminar
        cod_a_eliminar = cod_salida
        # Base de relación
        b_relacion_objetos = base_relacion_objetos

        # Filtro las tablas para obtener el ID interno
        tabla_codigo_objeto_filtrada = tabla_objeto[tabla_objeto[cod_objeto]==codigo_objeto]
        id_interno_objeto_clase = tabla_codigo_objeto_filtrada.iloc[0,0] # ID de frame
        tabla_codigo_a_eliminar = tabla_a_objeto_a_eliminar[tabla_a_objeto_a_eliminar[cod_a_eliminar]==codigo_a_eliminar]
        id_interno_objeto_a_eliminar = tabla_codigo_a_eliminar.iloc[0,0] # ID de vitrina
        
        # ID de relación
        if cod_objeto == "COD_DR":
            id_relacion_objetos = id_interno_objeto_clase + "/" + id_interno_objeto_a_eliminar
        elif cod_objeto == "COD_DE" and cod_salida == "COD_DR":
            id_relacion_objetos = id_interno_objeto_a_eliminar + "/" + id_interno_objeto_clase
        elif cod_objeto == "COD_DE" and cod_salida == "COD_EP":
            id_relacion_objetos = id_interno_objeto_clase + "/" + id_interno_objeto_a_eliminar
        elif cod_objeto == "COD_EP":
            id_relacion_objetos = id_interno_objeto_a_eliminar + "/" + id_interno_objeto_clase
        else:
            id_relacion_objetos = id_interno_objeto_clase + "/" + id_interno_objeto_a_eliminar
        # Se cambia dato en tabla de relación
        b_relacion_objetos.cambiar_un_dato_de_una_fila(id_relacion_objetos, 4,'ELIMINADO')

        # Actualización de historial
        datos_modificados = base_relacion_objetos.listar_datos_de_fila(id_relacion_objetos)
        hora = str(dt.datetime.now())
        datos_a_cargar_hist = datos_modificados + [hora]
        base_relacion_hist.agregar_datos(datos_a_cargar_hist)
        # Confirmación de eliminación de documento emitido
        messagebox.showinfo("¡Documento emitido eliminado!", "El registro se ha desasociado correctamente")


    #----------------------------------------------------------------------
    def generar_vitrina(self, nuevo, 
                        frame_vitrina,
                        texto_boton, funcion_boton,
                        texto_titulo,
                        codigo_frame, tabla_codigo_ficha, 
                        tabla_vista_vitrina, tabla_relacion, 
                        id_entrada, id_salida, cod_salida, 
                        funcion_ver, funcion_eliminar):
        """"""

        # Se agrega el botón y título del Frame
        frame_vitrina.agregar_button(0, 0, texto_boton, funcion_boton)
        frame_vitrina.agregar_titulo(0, 1,'                                                       ')
        frame_vitrina.agregar_titulo(0, 2, texto_titulo)
        frame_vitrina.agregar_titulo(0, 3,'                              ')
        frame_vitrina.agregar_titulo(0, 4,'                              ')

        if nuevo == False:
            # Obtengo el código del usuario que heredo
            cod_usuario = codigo_frame
            # Genero las tablas para el filtrado 
            tabla_de_codigo = tabla_codigo_ficha 
            tabla_de_relacion = tabla_relacion
            # Filtro la tabla para obtener el código interno 
            tabla_de_codigo_filtrada = tabla_de_codigo[tabla_de_codigo[cod_salida]==cod_usuario]
            cod_interno = tabla_de_codigo_filtrada.iloc[0,0]
            # Filtro para obtener las relaciones activas
            tabla_relacion_activos = tabla_de_relacion[tabla_de_relacion['ESTADO']=="ACTIVO"]
            # Con ese ID, filtro la tabla de relacion
            tabla_relacion_filtrada = tabla_relacion_activos[tabla_relacion_activos[id_entrada]==cod_interno]
            # Me quedo con el vector a filtrar en forma de lista
            lista_objetos = list(tabla_relacion_filtrada[id_salida].unique())
            # Filtro la tabla de documentos recibidos
            tabla_filtrada = tabla_vista_vitrina[tabla_vista_vitrina[id_salida].isin(lista_objetos)]
            # Tabla de documentos emitidos filtrada
            tabla_vitrina = tabla_filtrada.drop([id_salida], axis=1)
            if len(tabla_vitrina.index) > 0:
                self.vitrina = Vitrina_vista(self, tabla_vitrina, funcion_ver, funcion_eliminar, 
                                             height=80, width=1050) 
                return self.vitrina
            else:
                frame_vitrina.agregar_label(1, 2, '                  0 documentos recibidos asociados')
        else:
            frame_vitrina.agregar_label(1, 2, '                  0 documentos recibidos asociados')
    
    
    #----------------------------------------------------------------------
    def busqueda_dr(self):
        """"""
        if self.nuevo != True:

            id_objeto_ingresado = self.id_objeto_ingresado
            texto_pantalla = "Documento recibido que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = ventanas_busqueda.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla,
                                                                nuevo=False, id_objeto = id_objeto_ingresado)

        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar un documento emitido, por favor guarde la información registrada")
 
    #----------------------------------------------------------------------
    def ver_dr(self, id_objeto_ingresado):
        """"""
        texto_documento = 'Documento recibido: ' + id_objeto_ingresado

        lb1 = b_dr.listar_datos_de_fila(id_objeto_ingresado)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], lb1[9], lb1[10], 
                                 lb1[11], lb1[12], lb1[13], lb1[14], lb1[15], lb1[16],  lb1[17], lb1[18]]
        
        self.desaparecer()
        subframe = ventanas_vista.Doc_recibidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                                    lista=lista_para_insertar, id_objeto = id_objeto_ingresado)

   #----------------------------------------------------------------------
    def busqueda_de(self):
        """"""
        if self.nuevo != True: 

            id_objeto_ingresado = self.id_objeto_ingresado
            texto_pantalla = "Documento recibido que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = ventanas_busqueda.Doc_emitidos_busqueda(self, 500, 1200, texto_pantalla,
                                                           nuevo=False, id_objeto = id_objeto_ingresado)

        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar un documento emitido, por favor guarde la información registrada")

    #----------------------------------------------------------------------
    def ver_de(self, id_usuario):
        """"""
        texto_documento = 'Documento emitido: ' + id_usuario

        lb1 = b_de.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2], lb1[3], lb1[4], lb1[5], lb1[6], 
                                lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], lb1[12]]
        self.desaparecer()
        subframe = ventanas_vista.Doc_emitidos_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_objeto = id_usuario)
    
    #----------------------------------------------------------------------
    def busqueda_ep(self):
        """"""
        if self.nuevo != True:

            id_objeto_ingresado = self.id_objeto_ingresado
            texto_pantalla = "Extremo de problema que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = ventanas_busqueda.Doc_recibidos_busqueda(self, 500, 1200, texto_pantalla,
                                                                nuevo=False, id_objeto = id_objeto_ingresado)

        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar un documento emitido, por favor guarde la información registrada")
 

    #----------------------------------------------------------------------
    def ver_ep(self, id_usuario):
        """"""
        texto_documento = 'Extremo de problema: ' + id_usuario

        lb1 = b_ep.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], 
                                lb1[8], lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], 
                                lb1[14], lb1[15], lb1[16], lb1[17], lb1[18], lb1[19], lb1[20]]

        self.desaparecer()
        subframe = ventanas_vista.Extremo_problemas_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_objeto = id_usuario)
    
    #----------------------------------------------------------------------
    def busqueda_mp(self):
        """"""
        if self.nuevo != True:
            # En caso exista un código insertado en la rejilla
            id_objeto_ingresado = self.id_objeto_ingresado
            texto_pantalla = "Macroproblema que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.desaparecer()
            SubFrame = ventanas_busqueda.Extremos(self, 500, 1200, texto_pantalla,
                                                           nuevo=False, id_objeto = id_objeto_ingresado)

        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar un documento emitido, por favor guarde la información registrada")

    #----------------------------------------------------------------------
    def ver_mp(self, id_usuario):
        """"""
        texto_documento = 'Macroproblema: ' + id_usuario

        lb1 = b_mp.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4]]

        self.desaparecer()
        subframe = ventanas_vista.Extremo_problemas_vista(self, 650, 1150, texto_documento, nuevo=False, 
                                        lista=lista_para_insertar, id_objeto = id_usuario)
    
    #----------------------------------------------------------------------
    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False

