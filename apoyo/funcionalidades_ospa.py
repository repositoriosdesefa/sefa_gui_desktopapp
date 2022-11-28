from tkinter import  messagebox
import pandas as pd
from apoyo.elementos_de_GUI import  Ventana, Vitrina
from modulos import menus, ventanas_busqueda, ventanas_vista, logueo
import apoyo.datos_frecuentes as df
import webbrowser
import datetime as dt
from apoyo.manejo_de_bases import Base_de_datos


class funcionalidades_ospa(Ventana):
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto = None):
        """Constructor"""
        
        # Objetos de clase
        self.nuevo = nuevo
        self.lista = lista
        self.id_objeto_ingresado = id_objeto
        self.tipo_objeto = tipo_objeto

        # Frame de Scrollbar
        if self.scrollable_ventana == True:
            self.frame_principal = self.scrollframe
        else:
            self.frame_principal = self

    #----------------------------------------------------------------------
    def inicio_app(self, evento = None):
        """"""
        # Confirmación
        pregunta = "¿Está seguro de que desea volver a la pantalla de inicio? \n ¡Todo cambio no guardado se perderá!"
        confirmacion = messagebox.askyesno("Inicio ASPA", pregunta)

        if confirmacion == True:
            self.destruir()
            texto_bienvenida = df.texto_bienvenida
            # LargoxAncho
            subFrame = menus.inicio_app_OSPA(self, df.alto_ventana_secundaria, df.ancho_ventana_secundaria, texto_bienvenida)
        else:
            messagebox.showinfo("¡Importante!", "No olvides guardar tus cambios")
        
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
        usuario = df.cod_usuario
        
        
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
            base_objeto.cambiar_un_dato_de_una_fila(cod_objeto_clase, 4, nuevo_cod_objeto_clase) #revisar

            # Pestaña 2:       
            # Cambio los datos de una fila
            # Código interno del aplicativo + Código del usuario del DR + Hora de modificación
            lista_a_sobreescribir = [id_interno_objeto_clase] + [nuevo_cod_objeto_clase] + datos_ingresados + [hora_de_modificacion] + [usuario]
            base_objeto.cambiar_los_datos_de_una_fila(nuevo_cod_objeto_clase, lista_a_sobreescribir) # Se sobreescribe la información
            
            # Pestaña 3
            lista_historial = lista_a_sobreescribir
            base_objeto_hist.agregar_datos(lista_historial) # Se sube la info

            # Mensaje
            messagebox.showinfo("¡Excelente!", "Se ha actualizado el registro")
            funcion_ver(nuevo_cod_objeto_clase)

	    # B. Es un código nuevo
        else:
            id_objeto_ingresado3 = self.id_objeto_ingresado
            print(id_objeto_ingresado3)
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
                    base_cod_objeto.agregar_codigo(cod_objeto_ingresado, ahora, usuario)
                elif cod_entrada == "COD_PR":
                    departamento = datos_ingresados[1]
	                # Obtención de sigla de departamento
                    tabla_parametros = df.tabla_parametros
                    tabla_siglas_filtrada = tabla_parametros[tabla_parametros['DEPARTAMENTO']==departamento]
                    sigla_cod_interno = tabla_siglas_filtrada.iloc[0,1]
		            # Obtención de número de problema
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
                    base_cod_objeto.agregar_codigo(cod_objeto_ingresado, ahora, departamento, usuario)
                elif cod_entrada == "COD_MP":
                    tabla_objeto_clase = base_cod_objeto.generar_dataframe()
                    numero_mp = len(tabla_objeto_clase.index) + 1
                    if numero_mp < 10:
                        numero_codigo = "-00" + str(numero_mp)
                    elif numero_mp < 100:
                        numero_mp = "-0" + str(numero_mp)
                    else:
        	            numero_mp = "-" + str(numero_mp)
                    cod_objeto_ingresado = "MP" + numero_mp
                    base_cod_objeto.agregar_codigo(cod_objeto_ingresado, ahora, usuario)
                else:
                    print(ahora)
                    base_cod_objeto.agregar_codigo(cod_objeto_ingresado, ahora, usuario)

                # Descargo el código único
                lista_descargada_codigo = base_cod_objeto.listar_datos_de_fila(ahora) # Se trae la info
        
                # Pestaña 2:       
                # Obtengo el ID interno
                id_objeto = lista_descargada_codigo[0]
                cod_objeto = lista_descargada_codigo[3]
                # Creo el vector a subir 
                lista_a_cargar = [id_objeto] + [cod_objeto] + datos_ingresados + [ahora] + [usuario]
                base_objeto.agregar_datos(lista_a_cargar) # Se sube la info

                # Pestaña 3
                hora_de_creacion = str(ahora) # De lo creado en la pestaña 1
                lista_historial = lista_a_cargar #+ [hora_de_creacion] # Lo subido a la pestaña 2 + hora
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
        
        # Confirmación
        pregunta = "¿Está seguro de eliminar la asociación con el código: " + str(codigo_a_eliminar) + "?"
        confirmacion = messagebox.askyesno("Eliminar asociación", pregunta)

        if confirmacion == True:

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
            elif cod_objeto == "COD_DE" and cod_salida == "COD_PR":
                id_relacion_objetos = id_interno_objeto_clase + "/" + id_interno_objeto_a_eliminar
            elif cod_objeto == "COD_PR":
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
            messagebox.showinfo("¡Asociación eliminada!", "El registro se ha desasociado correctamente")
        
        else:
            messagebox.showinfo("Elimianr asociación", "El registro NO se ha desasociado")

    #----------------------------------------------------------------------
    def generar_vitrina(self, nuevo, 
                        frame_vitrina,
                        texto_boton, funcion_boton,
                        texto_titulo,
                        codigo_frame, tabla_codigo_ficha, 
                        tabla_vista_vitrina, tabla_relacion, 
                        id_entrada, id_salida, cod_salida, 
                        funcion_ver, funcion_eliminar, funcion3):
        """"""

        # Se agrega el botón y título del Frame
        frame_vitrina.agregar_boton_grande(0, 0, texto_boton, funcion_boton, 16, color = "Modelo1")
        frame_vitrina.agregar_titulo_2(0, 1,'                                         ')
        frame_vitrina.agregar_titulo_2(0, 2, texto_titulo)
        frame_vitrina.agregar_titulo_2(0, 3,'                              ')
        frame_vitrina.agregar_titulo_2(0, 4,'                              ')

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
                if texto_titulo == 'Problemas asociados':

                    self.vitrina = Vitrina(self.frame_principal, tabla_vitrina, funcion_ver, funcion_eliminar, funcion3, tipo_vitrina = 'Modelo5',
                                             height=df.alto_v_vista_vitrina, width=df.ancho_v_vista_vitrinapr)

                elif texto_titulo == 'Lista de extremos asociados':

                    self.vitrina = Vitrina(self.frame_principal, tabla_vitrina, funcion_ver, funcion_eliminar, funcion3, tipo_vitrina = 'Modelo5',
                                             height=df.alto_v_vista_vitrina, width=df.ancho_v_vista_vitrinaep)

                elif texto_titulo == 'Macroproblemas asociados':

                    self.vitrina = Vitrina(self.frame_principal, tabla_vitrina, funcion_ver, funcion_eliminar, funcion3, tipo_vitrina = 'Modelo5',
                                             height=df.alto_v_vista_vitrina, width=df.ancho_v_vista_vitrinaep)

                elif texto_titulo == 'Documentos emitidos asociados':

                    self.vitrina = Vitrina(self.frame_principal, tabla_vitrina, funcion_ver, funcion_eliminar, funcion3, tipo_vitrina = 'Modelo5',
                                             height=df.alto_v_vista_vitrina, width=df.ancho_v_vista_vitrinaep)

                else:
                    self.vitrina = Vitrina(self.frame_principal, tabla_vitrina, funcion_ver, funcion_eliminar, funcion3, tipo_vitrina = 'Modelo5',
                                             height=df.alto_v_vista_vitrina, width=df.ancho_v_vista_vitrinaep)
                    
                return self.vitrina
            else:
                frame_vitrina.agregar_label(1, 2, '     ')
                frame_vitrina.agregar_label(2, 2, '                  0 resultados')
                frame_vitrina.agregar_titulo(3, 2, '     ')
        else:
            frame_vitrina.agregar_label(1, 2, '     ')
            frame_vitrina.agregar_label(2, 2, '                  0 resultados')
            frame_vitrina.agregar_titulo(3, 2, '     ')
    
    #----------------------------------------------------------------------
    def nuevo_dr(self):
        
        self.destruir()

        texto_dr = "Nuevo documento Recibido"
        # LargoxAncho
        SubFrame = ventanas_vista.Doc_recibidos_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_dr, True)

    #----------------------------------------------------------------------
    def busqueda_dr(self):
        """"""
        if self.nuevo == False:

            id_objeto_ingresado = self.id_objeto_ingresado
            tipo_objeto_pantalla = self.tipo_objeto
            texto_pantalla = "Documento recibido que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.destruir()
            SubFrame = ventanas_busqueda.Doc_recibidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla, 
                                                                nuevo=False, id_objeto = id_objeto_ingresado, tipo_objeto_anterior = tipo_objeto_pantalla)

        elif self.nuevo == None:

            texto_pantalla = "Búsqueda de Documento Recibido"

            # Genero la nueva ventana
            self.destruir()
            SubFrame = ventanas_busqueda.Doc_recibidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla)
           
        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar, asegurate de guardar lo registrado")
 
    #----------------------------------------------------------------------
    def ver_dr(self, id_objeto_ingresado):
        """"""
        texto_documento = 'Documento recibido: ' + id_objeto_ingresado
        b_dr = Base_de_datos(df.id_b_docs, 'DOC_RECIBIDOS')
        lb1 = b_dr.listar_datos_de_fila(id_objeto_ingresado)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8], lb1[9], lb1[10], lb1[11], 
                                 lb1[12], lb1[13], lb1[14], lb1[15], lb1[16],  lb1[17], lb1[18], lb1[19], lb1[20], lb1[21]]
        
        self.destruir()
        subframe = ventanas_vista.Doc_recibidos_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_documento, True,
                                                      nuevo=False, lista=lista_para_insertar, id_objeto = id_objeto_ingresado)

    #----------------------------------------------------------------------
    def nuevo_de(self):
        
        self.destruir()

        texto_de = "Nuevo documento emitido"
        # LargoxAncho
        SubFrame = ventanas_vista.Doc_emitidos_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_de, True)
    
   #----------------------------------------------------------------------
    def busqueda_de(self):
        """"""
        if self.nuevo == False: 

            id_objeto_ingresado = self.id_objeto_ingresado
            tipo_objeto_pantalla = self.tipo_objeto
            texto_pantalla = "Documento recibido que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.destruir()
            SubFrame = ventanas_busqueda.Doc_emitidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla, 
                                                                nuevo=False, id_objeto = id_objeto_ingresado, tipo_objeto_anterior = tipo_objeto_pantalla)
        elif self.nuevo == None:

            # Genero la nueva ventana
            texto_pantalla = "Búsqueda de documentos emitidos"

            self.destruir()
            SubFrame = ventanas_busqueda.Doc_emitidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla)
   
        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar, asegurate de guardar lo registrado")

    #----------------------------------------------------------------------
    def ver_de(self, id_usuario):
        """"""
        texto_documento = 'Documento emitido: ' + id_usuario
        b_de = Base_de_datos(df.id_b_docs, 'DOC_EMITIDOS')
        lb1 = b_de.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2], lb1[3], lb1[4], lb1[5], lb1[6], lb1[7],
                                lb1[8], lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], lb1[14],
                                lb1[15], lb1[16], lb1[17], lb1[18], lb1[19], lb1[20],
                                lb1[21], lb1[22], lb1[23], lb1[24], lb1[25], lb1[26]]
        self.destruir()
        subframe = ventanas_vista.Doc_emitidos_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_documento, True,
                                                     nuevo=False, lista=lista_para_insertar, id_objeto = id_usuario)
    
    #----------------------------------------------------------------------
    def nuevo_ep(self):
        
        self.destruir()

        texto_ep = "Nuevo problema"
        # LargoxAncho
        SubFrame = ventanas_vista.Problemas_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_ep, True)
    #----------------------------------------------------------------------
    def nuevo_extremo2(self):

        if self.nuevo == False: 

            id_objeto_ingresado = self.id_objeto_ingresado
            tipo_objeto_pantalla = self.tipo_objeto
            texto_ep = "Problema que se asociará: " + id_objeto_ingresado
        
            self.destruir()

            # LargoxAncho
            SubFrame = ventanas_vista.Extremo_vinculados(self, df.alto_v_vista, df.ancho_v_vista, texto_ep, True,
             id_objeto = id_objeto_ingresado)
    
        elif self.nuevo == None:

            # Genero la nueva ventana
            texto_pantalla = "Búsqueda de extremos de problemas"

            self.destruir()
            SubFrame = ventanas_vista.Extremo_vinculados(self, df.alto_v_vista, df.ancho_v_vista, texto_ep, True)
   
        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar, asegurate de guardar lo registrado")
            
    #----------------------------------------------------------------------
    def busqueda_ep(self):
        """"""
        if self.nuevo == False:

            id_objeto_ingresado = self.id_objeto_ingresado
            tipo_objeto_pantalla = self.tipo_objeto
            texto_pantalla = "Macroproblema que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.destruir()
            SubFrame = ventanas_busqueda.Extremos(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla, 
                                                  nuevo=False, id_objeto = id_objeto_ingresado, tipo_objeto_anterior = tipo_objeto_pantalla)

        elif self.nuevo == None:
            
            # Genero la nueva ventana
            texto_pantalla = "Búsqueda de extremos de problema"

            self.destruir()
            SubFrame = ventanas_busqueda.Extremos(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla)

        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar, asegurate de guardar lo registrado")
        
    #----------------------------------------------------------------------
    def ver_ep(self, id_usuario):
        """"""
        texto_documento = 'Problema: ' + id_usuario
        b_pr = Base_de_datos(df.id_b_problemas, 'PROBLEMA')
        lb1 = b_pr.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2], lb1[3], lb1[4], lb1[5], lb1[6]]

        self.destruir()
        subframe = ventanas_vista.Problemas_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_documento, True,
                                        nuevo=False, lista=lista_para_insertar, id_objeto = id_usuario)

    #----------------------------------------------------------------------
    def ver_ep2(self, id_usuario):
        """"""
        texto_documento = 'Extremo de problema: ' + id_usuario
        b_ep = Base_de_datos(df.id_b_problemas, 'EXT_PROBLEMA')
        lb1 = b_ep.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2],lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8],
                               lb1[9], lb1[10], lb1[11], lb1[12], lb1[13], lb1[14],
                               lb1[15], lb1[16], lb1[17], lb1[18], lb1[19], lb1[20], lb1[21], lb1[22], lb1[23]]

        self.destruir()
        subframe = ventanas_vista.Extremo_vinculados(self, df.alto_v_vista, df.ancho_v_vista, texto_documento, True,
                                        nuevo=False, lista=lista_para_insertar, id_objeto = id_usuario)
    
    #----------------------------------------------------------------------
    def nuevo_mp(self):
        
        self.destruir()

        texto_mp = "Creación de macroproblemas"
        # LargoxAncho
        SubFrame = ventanas_vista.Macroproblemas_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_mp, True)
    
    #----------------------------------------------------------------------
    def busqueda_mp(self):
        """"""
        if self.nuevo == False:
            # En caso exista un código insertado en la rejilla
            id_objeto_ingresado = self.id_objeto_ingresado
            tipo_objeto_pantalla = self.tipo_objeto
            texto_pantalla = "Macroproblema que se asociará: " + id_objeto_ingresado

            # Genero la nueva ventana
            self.destruir()
            SubFrame = ventanas_busqueda.Macroproblemas(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla, 
                                                        nuevo=False, id_objeto = id_objeto_ingresado, tipo_objeto_anterior = tipo_objeto_pantalla)
        
        elif self.nuevo == None:

            self.destruir()

            # Genero la nueva ventana
            texto_pantalla = "Búsqueda de macroproblemas"

            SubFrame = ventanas_busqueda.Macroproblemas(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_pantalla)
  
        else:
            # En caso no estuviera guardado la ficha
            messagebox.showerror("¡Guardar!", "Antes de asociar, asegurate de guardar lo registrado")
    
    #----------------------------------------------------------------------
    def ver_mp(self, id_usuario):
        """"""
        texto_documento = 'Macroproblema: ' + id_usuario
        b_mp = Base_de_datos(df.id_b_problemas, 'MACROPROBLEMA')
        lb1 = b_mp.listar_datos_de_fila(id_usuario)
        lista_para_insertar = [lb1[2], lb1[3], lb1[4], lb1[5], lb1[6], lb1[7], lb1[8]]

        self.destruir()
        subframe = ventanas_vista.Macroproblemas_vista(self, df.alto_v_vista, df.ancho_v_vista, texto_documento, True,
                                                        nuevo=False, lista=lista_para_insertar, id_objeto = id_usuario)
    
    #----------------------------------------------------------------------
    def comprobar_id(self, base_codigo, id_usuario):
        """"""
        # Comprobar coincidencias
        cantidad_de_coincidencias = base_codigo.contar_coincidencias(id_usuario)

        if cantidad_de_coincidencias != 0:
            return True
        else:
            return False
    
    #----------------------------------------------------------------------
    def cerrar_sesion(self, evento = None):
        
        # Confirmación
        pregunta = "¿Está seguro de que desea cerrar sesión? \n ¡Todo cambio no guardado se perderá!"
        confirmacion = messagebox.askyesno("ASPA", pregunta)

        if confirmacion == True:
            self.destruir()
            df.cod_usuario = None
            df.usuario = None
            df.oficina = None
            df.texto_bienvenida = None
            subFrame = logueo.logueo1_Ingreso_de_usuario(self, 590, 453, "ASPA - Versión 0.0", False)
        else:
            messagebox.showinfo("¡Importante!", "No olvides guardar tus cambios")
    
     #----------------------------------------------------------------------
    def LinkBD(self):

        webbrowser.open("https://datastudio.google.com/u/0/reporting/6df9744f-15c8-4d44-86ab-5421643636fc/page/zMF5B?s=qNfv_U6QI-c")
    

        #----------------------------------------------------------------------
    def renombrar_encabezados(self, tabla, tipo_base = None):

        self.tabla = tabla
        self.tipo_base = tipo_base

        if self.tipo_base == 'dr':
            tabla_renombrada = self.tabla.rename(columns={'COD_DR':'NRO DOC','F_ING_SEFA':'FECHA INGRESO SEFA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_ENTRANTE':'HT INGRESO','ACCION_1':'INDICACION','APORTE_DOC':'APORTE DOC.'})
            tabla_renombrada['FECHA INGRESO SEFA'] = pd.to_datetime(tabla_renombrada['FECHA INGRESO SEFA'], dayfirst=True)
            tabla_renombrada['FECHA ULTIMO MOV.'] = pd.to_datetime(tabla_renombrada['FECHA ULTIMO MOV.'], dayfirst=True)
            tabla_renombrada2 = tabla_renombrada.sort_values(by='FECHA INGRESO SEFA', ascending=True)
            tabla_renombrada2['FECHA INGRESO SEFA'] = tabla_renombrada2['FECHA INGRESO SEFA'].dt.strftime('%d/%m/%Y')
            tabla_renombrada2['FECHA ULTIMO MOV.'] = tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
            return tabla_renombrada2
        elif self.tipo_base == 'de':
            tabla_renombrada = self.tabla.rename(columns={'COD_DE':'HT','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO','NUM_DOC':'NRO DOCUMENTO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','TIPO_DOC':'TIPO DOC','HT_SALIDA':'HT SALIDA','FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION','FECHA_PROYECTO_FINAL':'FECHA PROYECTO'})
            tabla_renombrada['FECHA ULTIMO MOV.'] = pd.to_datetime(tabla_renombrada['FECHA ULTIMO MOV.'], dayfirst=True)
            tabla_renombrada2 = tabla_renombrada.sort_values(by='FECHA ULTIMO MOV.', ascending=True)
            tabla_renombrada2['FECHA ULTIMO MOV.'] = tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
        
            return tabla_renombrada2

        elif self.tipo_base == 'ep':
            tabla_renombrada = self.tabla.rename(columns={'COD_PR':'CODIGO EXTREMO','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.'})
            tabla_renombrada['FECHA ULTIMO MOV.'] = pd.to_datetime(tabla_renombrada['FECHA ULTIMO MOV.'], dayfirst=True)
            tabla_renombrada2 = tabla_renombrada.sort_values(by='FECHA ULTIMO MOV.', ascending=True)
            tabla_renombrada2['FECHA ULTIMO MOV.'] = tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
        
            return tabla_renombrada2    

        elif self.tipo_base == 'mp':
            tabla_renombrada = self.tabla.rename(columns={'COD_MP':'COD. MACROPROBLEMA','NOMBRE_DEL_PROBLEMA':'NOMBRE PROBLEMA','FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.'})
            tabla_renombrada['FECHA ULTIMO MOV.'] = pd.to_datetime(tabla_renombrada['FECHA ULTIMO MOV.'], dayfirst=True)
            tabla_renombrada2 = tabla_renombrada.sort_values(by='FECHA ULTIMO MOV.', ascending=True)
            tabla_renombrada2['FECHA ULTIMO MOV.'] = tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
        
            return tabla_renombrada2
        elif self.tipo_base == 'pf':
            tabla_renombrada = self.tabla.rename(columns={'COD_DE':'HT','DETALLE_REQUERIMIENTO':'DETALLE','ESTADO_DOCE':'ESTADO',
            'FECHA_ULTIMO_MOV':'FECHA ULTIMO MOV.','HT_SALIDA':'HT SALIDA',
            'FECHA_FIRMA':'FECHA FIRMA','FECHA_NOTIFICACION':'FECHA NOTIFICACION',
            'FECHA_PROYECTO_FINAL':'FECHA PROYECTO','FECHA_PROYECTO_REIT':'PROYE REIT',
            'FECHA_PROYECTO_OCI':'FECHA PROYECTO OCI'})
            tabla_renombrada['FECHA ULTIMO MOV.'] = pd.to_datetime(tabla_renombrada['FECHA ULTIMO MOV.'], dayfirst=True)
            tabla_renombrada2 = tabla_renombrada.sort_values(by='FECHA ULTIMO MOV.', ascending=True)
            tabla_renombrada2['FECHA ULTIMO MOV.'] = tabla_renombrada2['FECHA ULTIMO MOV.'].dt.strftime('%d/%m/%Y')
        
            return tabla_renombrada2
        else:
            print("Hola")
#----------------------------------------------------------------------
    def seleccionar_encabezados(self, tabla, tipo_base = None):

        self.tabla = tabla
        self.tipo_base = tipo_base

        if self.tipo_base == 'dr':
            tabla_seleccionada = self.tabla.loc[:,['NRO DOC','REMITENTE','HT INGRESO','FECHA INGRESO SEFA','INDICACION','FECHA ULTIMO MOV.','ASUNTO']]
            return tabla_seleccionada
        elif self.tipo_base == 'de':
            tabla_seleccionada = self.tabla.loc[:,['HT','DESTINATARIO','TIPO DOC','NRO DOCUMENTO','FECHA ULTIMO MOV.','ESTADO','CATEGORIA','DETALLE']]
            return tabla_seleccionada
        elif self.tipo_base == 'ep':
            tabla_seleccionada = self.tabla.loc[:,['CODIGO EXTREMO','DEPARTAMENTO','ESTADO','FECHA ULTIMO MOV.','DESCRIPCION']]
            return tabla_seleccionada
        elif self.tipo_base == 'mp':
            tabla_seleccionada = self.tabla.loc[:,['COD. MACROPROBLEMA','FECHA ULTIMO MOV.','NOMBRE PROBLEMA','ESTADO','DESCRIPCION']]
            return tabla_seleccionada
        elif self.tipo_base == 'pf':
            tabla_seleccionada = self.tabla.loc[:,['HT','DESTINATARIO','FECHA ULTIMO MOV.','CATEGORIA','ESPECIALISTA','DETALLE']]
            return tabla_seleccionada
        elif self.tipo_base == 'paj':
            tabla_seleccionada = self.tabla.loc[:,['NRO DOC','REMITENTE','HT INGRESO','FECHA INGRESO SEFA','FECHA ULTIMO MOV.','ASUNTO']]
            return tabla_seleccionada
        else:
            print("Hola")

#----------------------------------------------------------------------
    def actualizar_dr(self):

        self.destruir()
        texto_b_dr = "Búsqueda de documentos recibidos"
        SubFrame = ventanas_busqueda.Doc_recibidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_dr, False)
#----------------------------------------------------------------------
    def actualizar_de(self):

        self.destruir()
        texto_b_de = "Búsqueda de documentos emitidos"
        SubFrame = ventanas_busqueda.Doc_emitidos_busqueda(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_de, False)
#----------------------------------------------------------------------
    def actualizar_ep(self):

        self.destruir()
        texto_b_pr = "Búsqueda de extremos de problemas"
        SubFrame = ventanas_busqueda.Extremos(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_pr, False)
#----------------------------------------------------------------------
    def actualizar_peq1(self):

        self.destruir()
        texto_b_peq1 = "Documentos pendientes de trabajar - Equipo 1"
        SubFrame = ventanas_busqueda.Pendientes_eq1_trabajar(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_peq1, False)
#----------------------------------------------------------------------
    def actualizar_peq2(self):

        self.destruir()
        texto_b_peq2 = "Pendientes de calificar respuesta"
        SubFrame = ventanas_busqueda.Pendientes_eq2_calificarrpta(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_peq2, False)

#----------------------------------------------------------------------
    def actualizar_bmp(self):

        self.destruir()
        texto_b_mp = "Búsqueda de Macroproblemas"
        SubFrame = ventanas_busqueda.Macroproblemas(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_mp, False)

#----------------------------------------------------------------------
    def actualizar_pf(self):

        self.destruir()
        texto_b_pf = "Documentos pendientes de firma"
        SubFrame = ventanas_busqueda.Pendientes_jefe_firma(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_pf, False)

#----------------------------------------------------------------------
    def actualizar_pasignar(self):

        self.destruir()
        texto_b_pa = "Documentos pendientes de asignar"
        SubFrame = ventanas_busqueda.Pendientes_jefe_asignar(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_pa, False)
#----------------------------------------------------------------------
    def actualizar_preiter(self):

        self.destruir()
        texto_b_proci = "Documentos pendientes de reiterar/comunicación al OCI"
        SubFrame = ventanas_busqueda.Pendientes_por_reiterar(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_proci, False)
#----------------------------------------------------------------------
    def actualizar_programaciones(self):

        self.destruir()
        texto_b_progra = "Programaciones"
        SubFrame = ventanas_busqueda.Pendientes_eq2_programaciones(self, df.alto_v_busqueda, df.ancho_v_busqueda, texto_b_progra, False)
