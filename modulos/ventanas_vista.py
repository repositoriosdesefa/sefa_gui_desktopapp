import datetime as dt

from tkinter import *
from tkinter import messagebox
from tkinter.constants import TRUE

from modulos import ventanas_busqueda
import apoyo.datos_frecuentes as vg
from apoyo.funcionalidades_ospa import funcionalidades_ospa
from apoyo.elementos_de_GUI import Cuadro, Ventana

# Parámetros ventana
ancho_v_vista = vg.ancho_v_vista
alto_v_vista = vg.alto_v_vista
ancho_v_vista_vitrina = vg.ancho_v_vista_vitrina
alto_v_vista_vitrina = vg.alto_v_vista_vitrina

# 1. Bases
b_dr = vg.b_dr
b_dr_cod = vg.b_dr_cod
b_dr_hist = vg.b_dr_hist
b_de = vg.b_de
b_de_cod = vg.b_de_cod
b_de_hist = vg.b_de_hist
b_pr = vg.b_pr
b_ep = vg.b_ep
b_pr_cod = vg.b_pr_cod
b_ep_cod = vg.b_ep_cod
b_pr_hist = vg.b_pr_hist
b_ep_hist = vg.b_ep_hist
b_mp = vg.b_mp
b_mp_cod = vg.b_mp_cod
b_mp_hist = vg.b_mp_hist

base_datos_usuario = vg.base_datos_usuario
base_relacion_docs = vg.base_relacion_docs
base_relacion_dr_pr = vg.base_relacion_dr_pr
base_relacion_de_pr = vg.base_relacion_de_pr
base_relacion_mp_pr = vg.base_relacion_mp_pr
base_relacion_ep_pr = vg.base_relacion_ep_pr

base_relacion_docs_hist = vg.base_relacion_docs_hist
base_relacion_dr_pr_hist = vg.base_relacion_dr_pr_hist
base_relacion_de_pr_hist = vg.base_relacion_de_pr_hist
base_relacion_mp_pr_hist = vg.base_relacion_mp_pr_hist
base_relacion_ep_pr_hist = vg.base_relacion_ep_pr_hist

# 2. Tablas
tabla_directorio = vg.tabla_directorio
tabla_directorio_efa = vg.tabla_directorio_efa_final
tabla_lista_efa = vg.tabla_lista_efa

# 3. Listas dependientes
# 21. Lista de EFA
lista_efa_dependiente = vg.lista_efa_dependiente
lista_efa_ospa = sorted(list(lista_efa_dependiente['EFA_OSPA'].unique()))
# 3.2 Ubigeo
tabla_departamento_efa = vg.tabla_departamento_efa
departamento_ospa = vg.departamento_ospa

# 4. Parámetros
# 4.1 Bases de datos
tabla_parametros = vg.tabla_parametros
# 4.2 Desplegables en Drive
combo_vacio = ()
agente_conta = vg.agente_conta
componente_amb = vg.componente_amb
actividad_eco = vg.actividad_eco
extension = vg.extension
ubicacion = vg.ubicacion
ocurrencia = vg.ocurrencia
tipo_afectacion = vg.tipo_afectacion
tipo_administrado =vg.tipo_administrado
estado_problemas = vg.estado_problemas
tipo_causa = vg.tipo_causa
tipo_ingreso = vg.tipo_ingreso
tipo_documento = vg.tipo_documento
especialista_1 = vg.especialista_1
tipo_accion_1 = vg.tipo_accion_1
especialista_2 = vg.especialista_2
tipo_accion_2 = vg.tipo_accion_2
si_no = vg.si_no
tipo_respuesta = vg.tipo_respuesta
categorias = vg.categorias
marco_pedido = vg.marco_pedido


# 5. Tablas resumen
# 5.0 Relaciones
tabla_relacion_dr_de = vg.tabla_relacion_dr_de
tabla_relacion_dr_pr = vg.tabla_relacion_dr_pr
tabla_relacion_de_pr = vg.tabla_relacion_de_pr
tabla_relacion_mp_pr = vg.tabla_relacion_mp_pr
tabla_relacion_ep_pr = vg.tabla_relacion_ep_pr
# 5.1 Documentos recibidos
tabla_de_dr_cod = vg.tabla_de_dr_cod
tabla_de_dr_completa = vg.tabla_de_dr_completa
tabla_de_dr_resumen = vg.tabla_de_dr_resumen
# 5.2 Documentos emitidos
tabla_de_de_cod = vg.tabla_de_de_cod
tabla_de_de_completa = vg.tabla_de_de_completa
tabla_de_de_resumen = vg.tabla_de_de_resumen
# 5.3 Problema
tabla_de_pr_cod = vg.tabla_de_pr_completa
tabla_de_pr_completa = vg.tabla_de_pr_completa
tabla_de_ep_resumen = vg.tabla_de_ep_resumen
# 5.4 Macroproblemas
tabla_de_mp_cod = vg.tabla_de_mp_completa
tabla_de_mp_completa = vg.tabla_de_mp_completa
tabla_de_mp_resumen = vg.tabla_de_mp_resumen
# 5.4 Extremos
tabla_de_ep_cod = vg.tabla_de_ep_completa
tabla_de_ep_completa = vg.tabla_de_ep_completa
tabla_de_ep2_resumen = vg.tabla_de_ep2_resumen
    
class Doc_recibidos_vista(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None, tipo_objeto = "DR"):
        """Constructor"""

        Ventana.__init__(self, *args)
        # Determinar la ventana principal a partir si es (o no) scrollable
        if self.scrollable_ventana == True:
            self.frame_principal = self.scrollframe
        else:
            self.frame_principal = self

        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.id_objeto_ingresado = id_objeto
        self.cod_usuario_dr = id_objeto
        self.tipo_objeto = tipo_objeto
        self.cod_tipo_objeto = 'COD_' + str(tipo_objeto)
        # Parámetros de vitrina
        self.vitrina_1 = None
        self.vitina_2 = None

        # I. Labels, entries y rejilla
        # Incluida en el IF

        # Tablas para vitrina
        # 0. Tablas de código de objeto
        self.tabla_de_dr_cod = tabla_de_dr_cod
        # II.1 Lista de DE
        self.tabla_de_de =  tabla_de_de_resumen
        self.tabla_relacion_dr_de = tabla_relacion_dr_de
        # II.2 Lista de EP
        self.tabla_de_ep = tabla_de_ep_resumen
        self.tabla_relacion_dr_pr = tabla_relacion_dr_pr

        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Documento recibido', 
                                            self.inicio_app, self.cerrar_sesion)
        #titulos.agregar_encabezado('Detalle de documento recibido')
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada
            self.cod_usuario_dr = id_objeto
            self.lista_para_insertar = lista

            self.tabla_de_dr_cod = b_dr_cod.generar_dataframe()
            self.tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
            self.tabla_relacion_dr_pr = base_relacion_dr_pr.generar_dataframe()

            creador = b_dr_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_dr_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_dr.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_dr.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            rejilla_dr = [

                # Sección 1: Detalle
                ('T2', 0, 0, 'Ingreso'),   
                
                ('L', 1, 0, 'Tipo de documento'),
                ('CX', 1, 1, tipo_documento),

                ('L', 1, 2, 'N° de documento'),
                ('E', 1, 3),

                ('L', 2, 0, 'Asunto'),
                ('EL', 2, 1, 122, 3),

                ('L', 3, 0, 'Fecha de recepción OEFA'),
                ('D', 3, 1),

                ('L', 3, 2, 'Fecha de recepción SEFA'),
                ('D', 3, 3),

                ('L', 4, 0, 'Vía de recepción'),
                ('CX', 4, 1, tipo_ingreso),

                ('L', 4, 2, 'HT de documento'),
                ('E', 4, 3),

                ('L', 5, 0, 'Tipo Remitente'),
                ('CXDEP3', 5, 1, 44, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Remitente', 'EFA_OSPA', 'Remitente', 'Entidad u oficina'),

                ('L', 6, 2, '¿Es respuesta?'),
                ('CX', 6, 3, si_no),

                ('L', 7, 0, 'Fecha asignación'),
                ('DE', 7, 1),

                ('L', 7, 2, 'Especialista Eq. 1'),
                ('CX', 7, 3, especialista_1),

                # Sección 2: Análisis Equipo 1
                ('T2', 8, 0, 'Aporte'),   

                ('L', 9, 0, 'Fecha de ejecución'),
                ('DE', 9, 1),

                ('L', 9, 2, 'Acción'),
                ('CX', 9, 3, tipo_accion_1),

                ('L', 10, 0, 'Aporte del documento'),
                ('ST', 10, 1),

                ('L', 11, 0, 'Fecha asignación'),
                ('DE', 11, 1),

                ('L', 11, 2, 'Especialista Eq. 2'),
                ('CX', 11, 3, especialista_2),

                # Sección 3: Contenido (Equipo 2)
                ('T2', 12, 0, 'Respuesta'),  

                ('L', 13, 0, 'Fecha de ejecución'),
                ('DE', 13, 1),

                ('L', 13, 2, 'Respuesta'),
                ('CX', 13, 3, tipo_respuesta),

                # Sección 4: Datos
                ('T2', 14, 0, 'Datos'),  

                ('L', 15, 0, 'Creado por:'),
                ('L', 15, 1, str(creador)),

                ('L', 15, 2, 'Actualizado por:'),
                ('L', 15, 3, str(ultimo_nombre)),

                ('L', 16, 0, 'Fecha creación:'),
                ('L', 16, 1, str(fecha_creacion)),

                ('L', 16, 2, 'Fecha actualización:'),
                ('L', 16, 3, str(fecha_ultimo))
            ]

            self.frame_rejilla.agregar_rejilla(rejilla_dr)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)
        else:
            rejilla_dr_nuevo = [
            
                # Sección 1: Detalle
                ('T2', 0, 0, 'Ingreso'),   
                
                ('L', 1, 0, 'Tipo de documento'),
                ('CX', 1, 1, tipo_documento),

                ('L', 1, 2, 'N° de documento'),
                ('E', 1, 3),

                ('L', 2, 0, 'Asunto'),
                ('EL', 2, 1, 122, 3),

                ('L', 3, 0, 'Fecha de recepción OEFA'),
                ('D', 3, 1),

                ('L', 3, 2, 'Fecha de recepción SEFA'),
                ('D', 3, 3),

                ('L', 4, 0, 'Vía de recepción'),
                ('CX', 4, 1, tipo_ingreso),

                ('L', 4, 2, 'HT de documento'),
                ('E', 4, 3),

                ('L', 5, 0, 'Tipo Remitente'),
                ('CXDEP3', 5, 1, 44, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Remitente', 'EFA_OSPA', 'Remitente', 'Entidad u oficina'),

                ('L', 6, 2, '¿Es respuesta?'),
                ('CX', 6, 3, si_no),

                ('L', 7, 0, 'Fecha asignación'),
                ('DE', 7, 1),

                ('L', 7, 2, 'Especialista Eq. 1'),
                ('CX', 7, 3, especialista_1),

                # Sección 2: Análisis Equipo 1
                ('T2', 8, 0, 'Análisis'),   

                ('L', 9, 0, 'Fecha de ejecución'),
                ('DE', 9, 1),

                ('L', 9, 2, 'Acción'),
                ('CX', 9, 3, tipo_accion_1),

                ('L', 10, 0, 'Aporte del documento'),
                ('ST', 10, 1),

                ('L', 11, 0, 'Fecha asignación'),
                ('DE', 11, 1),

                ('L', 11, 2, 'Especialista Eq. 2'),
                ('CX', 11, 3, especialista_2),

                # Sección 3: Contenido (Equipo 2)
                ('T2', 12, 0, 'Acciones'),  

                ('L', 13, 0, 'Fecha de ejecución'),
                ('DE', 13, 1),

                ('L', 13, 2, 'Respuesta'),
                ('CX', 13, 3, tipo_respuesta)

            ]
            self.frame_rejilla.agregar_rejilla(rejilla_dr_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self.frame_principal)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_dr)
        f_boton.agregar_button(0, 2, 'Nuevo', self.ingresar_nuevo_dr)

        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self.frame_principal)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_1,
                                            '(+) Agregar', self.busqueda_de,
                                            'Documentos emitidos asociados', 
                                            self.cod_usuario_dr, self.tabla_de_dr_cod, 
                                            self.tabla_de_de, self.tabla_relacion_dr_de, 
                                            "ID_DR", "ID_DE", "COD_DR", 
                                            self.ver_de, self.eliminar_de_y_actualizar)

        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self.frame_principal)
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_2,
                                            '(+) Agregar', self.busqueda_ep,
                                            'Problemas ambientales asociados',
                                            self.cod_usuario_dr, self.tabla_de_dr_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_dr_pr, 
                                            "ID_DR", "ID_PR", "COD_DR", 
                                            self.ver_ep, self.eliminar_ep_y_actualizar)

    #----------------------------------------------------------------------
    def guardar_y_actualizar_dr(self):
        
        # Agregamos el objeto
        self.guardar_objeto(self.frame_rejilla,
                            self.cod_usuario_dr, "COD_DR", self.tabla_de_dr_cod, 
                            b_dr_cod, b_dr, b_dr_hist, self.ver_dr)
        # Actualización de tabla de código y visualización
        self.tabla_de_dr_cod = b_dr_cod.generar_dataframe()

    #----------------------------------------------------------------------
    def ingresar_nuevo_dr(self):
        
        # Confirmación
        pregunta = "¿Está seguro de que desea abrir un nuevo formulario? \n ¡Solo hágalo si desea registrar un nuevo documento!"
        confirmacion = messagebox.askyesno("Nuevo registro de documento", pregunta)

        if confirmacion == True:
            self.nuevo_dr()
        else:
            messagebox.showinfo("¡Importante!", "Siempre guarda tus cambios")

    #----------------------------------------------------------------------
    def eliminar_de_y_actualizar(self, id_objeto):
        """"""
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_dr, "COD_DR", id_objeto, "COD_DE",
                            self.tabla_de_dr_cod, tabla_de_de_cod, 
                            base_relacion_docs, base_relacion_docs_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_dr()

    #----------------------------------------------------------------------
    def eliminar_ep_y_actualizar(self, id_objeto):
        """"""
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_dr, "COD_DR", id_objeto, "COD_PR",
                            self.tabla_de_dr_cod, tabla_de_pr_cod, 
                            base_relacion_dr_pr, base_relacion_dr_pr_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_dr_pr = base_relacion_dr_pr.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_dr()
    
    #----------------------------------------------------------------------
    def actualizar_vitrinas_dr(self):
        # 0. Elimino el último frame
        self.frame_vitrina_2.eliminar_cuadro()
        if self.vitrina_2 != None:
            self.vitrina_2.eliminar_posible_vitrina()

        # I. Situo las ventanas actualizadas
        # I.1 Ventana de documentos emitidos
        self.frame_vitrina_1.eliminar_cuadro()
        if self.vitrina_1 != None: 
            self.vitrina_1.eliminar_posible_vitrina()

        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_1,
                                            '(+) Agregar', self.busqueda_de,
                                            'Documentos emitidos asociados',   
                                            self.cod_usuario_dr, self.tabla_de_dr_cod, 
                                            self.tabla_de_de, self.tabla_relacion_dr_de, 
                                            "ID_DR", "ID_DE", "COD_DR", 
                                            self.ver_de, self.eliminar_de_y_actualizar)
        
        # I.2 Ventana de documentos recibidos   
        self.frame_vitrina_2.eliminar_cuadro()                     
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_2,
                                            '(+) Agregar', self.busqueda_ep,
                                            'Problemas asociados',
                                            self.cod_usuario_dr, self.tabla_de_dr_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_dr_pr, 
                                            "ID_DR", "ID_PR", "COD_DR", 
                                            self.ver_ep, self.eliminar_ep_y_actualizar)
    
class Doc_emitidos_vista(funcionalidades_ospa):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None,  tipo_objeto = "DE"):
        """Constructor"""

        Ventana.__init__(self, *args)
         # Determinar la ventana principal a partir si es (o no) scrollable
        if self.scrollable_ventana == True:
            self.frame_principal = self.scrollframe
        else:
            self.frame_principal = self

        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.cod_usuario_de = id_objeto
        self.id_objeto_ingresado = id_objeto
        self.tipo_objeto = tipo_objeto
        self.cod_tipo_objeto = 'COD_' + str(tipo_objeto)
        # Parámetros de vitrina
        self.vitrina_1 = None
        self.vitina_2 = None

        # I. Labels and Entries
        # Dentro del if

        # II. Tablas en ventana
        self.tabla_de_de_cod = tabla_de_de_cod
        # II.1 Lista de DR
        self.tabla_de_dr =  tabla_de_dr_resumen
        self.tabla_relacion_dr_de = tabla_relacion_dr_de
        # II.2 Lista de EP
        self.tabla_de_ep = tabla_de_ep_resumen
        self.tabla_relacion_de_pr = tabla_relacion_de_pr

        # III. Ubicaciones
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Documento Emitido', 
                                            self.inicio_app, self.cerrar_sesion)
        
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)

        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada
            self.cod_usuario_de = id_objeto
            self.lista_para_insertar = lista

            self.tabla_de_de_cod = b_de_cod.generar_dataframe()
            self.tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
            self.tabla_relacion_de_pr = base_relacion_de_pr.generar_dataframe()
            
            creador = b_de_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_de_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_de.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_de.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            rejilla_de = [
                # Sección 1: Emisión
                ('T2', 0, 0, 'Emisión'),

                ('L', 1, 0, 'HT de salida'),
                ('E', 1, 1),

                ('L', 1, 2, 'Fecha de proyecto'),
                ('DE', 1, 3), 

                ('L', 2, 0, 'Categoría'),
                ('CX', 2, 1, categorias),

                ('L', 2, 2, 'Especialista'),
                ('CX', 2, 3, especialista_2), 

                ('L', 3, 0, 'Tipo Destinatario'),
                ('CXDEP3', 3, 1, 44, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Destinatario', 'EFA_OSPA', 'Destinatario', 'Entidad u oficina'),

                ('L', 4, 2, 'Marco de pedido'),
                ('CX', 4, 3, marco_pedido),

                # Sección 2: Contenido de Documento
                ('T2', 5, 0, 'Documento'),

                ('L', 6, 0, 'Tipo de documento'),
                ('CX', 6, 1, tipo_documento),

                ('L', 6, 2, 'N° de documento'),
                ('E', 6, 3),

                ('L', 7, 0, 'Fecha de firma'),
                ('DE', 7, 1), 

                ('L', 7, 2, 'Fecha de notificación'),
                ('DE', 7, 3),

                ('L', 8, 0, 'Detalle de requerimiento'),
                ('ST', 8, 1),

                # Sección 3: Reiterativo
                ('T2', 9, 0, 'Reiterativo'),

                ('L', 10, 0, 'Fecha de proyecto'),
                ('DE', 10, 1), 

                ('L', 10, 2, '¿Se emitió?'),
                ('CX', 10, 3, si_no), 

                ('L', 11, 0, 'Tipo de documento'),
                ('CX', 11, 1, tipo_documento),

                ('L', 11, 2, 'N° de documento'),
                ('E', 11, 3),

                ('L', 12, 0, 'Fecha de firma'),
                ('DE', 12, 1), 

                ('L', 12, 2, 'Fecha de notificación'),
                ('DE', 12, 3),

                # Sección 4: OCI
                ('T2', 13, 0, 'OCI'),

                ('L', 14, 0, 'Fecha de proyecto'),
                ('DE', 14, 1), 

                ('L', 14, 2, '¿Se emitió?'),
                ('CX', 14, 3, si_no), 

                ('L', 15, 0, 'Tipo de documento'),
                ('CX', 15, 1, tipo_documento),

                ('L', 15, 2, 'N° de documento'),
                ('E', 15, 3),

                ('L', 16, 0, 'Fecha de firma'),
                ('DE', 16, 1), 

                ('L', 16, 2, 'Fecha de notificación'),
                ('DE', 16, 3),
                
                # Sección 5: Datos
                ('T2', 17, 0, 'Datos'),

                ('L', 18, 0, 'Creado por:'),
                ('L', 18, 1, str(creador)),

                ('L', 18, 2, 'Actualizado por:'),
                ('L', 18, 3, str(ultimo_nombre)),

                ('L', 19, 0, 'Fecha creación:'),
                ('L', 19, 1, str(fecha_creacion)),

                ('L', 19, 2, 'Fecha actualización:'),
                ('L', 19, 3, str(fecha_ultimo))
            ]
            
            self.frame_rejilla.agregar_rejilla(rejilla_de)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        else:
            rejilla_de_nuevo = [
                # Sección 1: Emisión
                ('T2', 0, 0, 'Emisión'),

                ('L', 1, 0, 'HT de salida'),
                ('E', 1, 1),

                ('L', 1, 2, 'Fecha de proyecto'),
                ('DE', 1, 3), 

                ('L', 2, 0, 'Categoría'),
                ('CX', 2, 1, categorias),

                ('L', 2, 2, 'Especialista'),
                ('CX', 2, 3, especialista_2), 

                ('L', 3, 0, 'Tipo Destinatario'),
                ('CXDEP3', 3, 1, 44, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Destinatario', 'EFA_OSPA', 'Destinatario', 'Entidad u oficina'),

                ('L', 4, 2, 'Marco de pedido'),
                ('CX', 4, 3, marco_pedido),

                # Sección 2: Contenido de Documento
                ('T2', 5, 0, 'Documento'),

                ('L', 6, 0, 'Tipo de documento'),
                ('CX', 6, 1, tipo_documento),

                ('L', 6, 2, 'N° de documento'),
                ('E', 6, 3),

                ('L', 7, 0, 'Fecha de firma'),
                ('DE', 7, 1), 

                ('L', 7, 2, 'Fecha de notificación'),
                ('DE', 7, 3),

                ('L', 8, 0, 'Detalle de requerimiento'),
                ('ST', 8, 1),

                # Sección 3: Reiterativo
                ('T2', 9, 0, 'Reiterativo'),

                ('L', 10, 0, 'Fecha de proyecto'),
                ('DE', 10, 1), 

                ('L', 10, 2, '¿Se emitió?'),
                ('CX', 10, 3, si_no), 

                ('L', 11, 0, 'Tipo de documento'),
                ('CX', 11, 1, tipo_documento),

                ('L', 11, 2, 'N° de documento'),
                ('E', 11, 3),

                ('L', 12, 0, 'Fecha de firma'),
                ('DE', 12, 1), 

                ('L', 12, 2, 'Fecha de notificación'),
                ('DE', 12, 3),

                # Sección 4: OCI
                ('T2', 13, 0, 'OCI'),

                ('L', 14, 0, 'Fecha de proyecto'),
                ('DE', 14, 1), 

                ('L', 14, 2, '¿Se emitió?'),
                ('CX', 14, 3, si_no), 

                ('L', 15, 0, 'Tipo de documento'),
                ('CX', 15, 1, tipo_documento),

                ('L', 15, 2, 'N° de documento'),
                ('E', 15, 3),

                ('L', 16, 0, 'Fecha de firma'),
                ('DE', 16, 1), 

                ('L', 16, 2, 'Fecha de notificación'),
                ('DE', 16, 3)
                
            ]
            
            self.frame_rejilla.agregar_rejilla(rejilla_de_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self.frame_principal)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_de)

        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self.frame_principal)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_1,
                                            '(+) Agregar', self.busqueda_dr,
                                            'Documentos recibidos asociados',
                                            self.cod_usuario_de, self.tabla_de_de_cod, 
                                            self.tabla_de_dr, self.tabla_relacion_dr_de, 
                                            "ID_DE", "ID_DR", "COD_DE", 
                                            self.ver_de, self.eliminar_dr_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self.frame_principal)
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_2,
                                            '(+) Agregar', self.busqueda_ep,
                                            'Problemas asociados',
                                            self.cod_usuario_de, self.tabla_de_de_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_de_pr, 
                                            "ID_DE", "ID_PR", "COD_DE", 
                                            self.ver_ep, self.eliminar_ep_y_actualizar)

   #----------------------------------------------------------------------
    def guardar_y_actualizar_de(self):
        
        # Agregamos el objeto
        self.guardar_objeto(self.frame_rejilla,
                            self.cod_usuario_de, "COD_DE", self.tabla_de_de_cod, 
                            b_de_cod, b_de, b_de_hist, self.ver_de)
        # Actualización de tabla de código y visualización
        self.tabla_de_de_cod = b_de_cod.generar_dataframe()

    #----------------------------------------------------------------------
    def eliminar_dr_y_actualizar(self, id_objeto):
        """"""
        # Se elimina el DR
        self.eliminar_objeto(self.cod_usuario_de, "COD_DE", id_objeto, "COD_DR",
                            self.tabla_de_de_cod, tabla_de_dr_cod, 
                            base_relacion_docs, base_relacion_docs_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_de()

    #----------------------------------------------------------------------
    def eliminar_ep_y_actualizar(self, id_objeto):
        """"""
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_de, "COD_DE", id_objeto, "COD_PR",
                            self.tabla_de_de_cod, tabla_de_pr_cod, 
                            base_relacion_de_pr, base_relacion_de_pr_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_de_pr = base_relacion_de_pr.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_de()
    
    #----------------------------------------------------------------------
    def actualizar_vitrinas_de(self):
        # 0. Elimino el último frame
        self.frame_vitrina_2.eliminar_cuadro()
        if self.vitrina_2 != None:
            self.vitrina_2.eliminar_posible_vitrina()

        # I. Situo las ventanas actualizadas
        # I.1 Ventana de documentos emitidos
        self.frame_vitrina_1.eliminar_cuadro()
        if self.vitrina_1 != None: 
            self.vitrina_1.eliminar_posible_vitrina()

        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_1,
                                            '(+) Agregar', self.busqueda_dr,
                                            'Documentos recibidos asociados',
                                            self.cod_usuario_de, self.tabla_de_de_cod, 
                                            self.tabla_de_dr, self.tabla_relacion_dr_de, 
                                            "ID_DE", "ID_DR", "COD_DE", 
                                            self.ver_dr, self.eliminar_dr_y_actualizar)
        
        # I.2 Ventana de documentos recibidos   
        self.frame_vitrina_2.eliminar_cuadro()                     
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_2,
                                            '(+) Agregar', self.busqueda_ep,
                                            'Problemas asociados',
                                            self.cod_usuario_de, self.tabla_de_de_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_de_pr, 
                                            "ID_DE", "ID_PR", "COD_DE", 
                                            self.ver_ep, self.eliminar_ep_y_actualizar)
         
class Problemas_vista(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None,  tipo_objeto = "PR"):
        """Constructor"""

        Ventana.__init__(self, *args)
         # Determinar la ventana principal a partir si es (o no) scrollable
        if self.scrollable_ventana == True:
            self.frame_principal = self.scrollframe
        else:
            self.frame_principal = self
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.cod_usuario_pr = id_objeto
        self.id_objeto_ingresado = id_objeto
        self.tipo_objeto = tipo_objeto
        self.cod_tipo_objeto = 'COD_' + str(tipo_objeto)
        # Parámetros de vitrina
        self.vitrina_1 = None
        self.vitina_2 = None

        # Tablas para vitrina
        # 0. Tablas de código de objeto (tabla de problemas)
        self.tabla_de_pr_cod = tabla_de_pr_cod
        # II.1 Lista de DR
        self.tabla_de_dr =  tabla_de_dr_resumen
        self.tabla_relacion_dr_pr = tabla_relacion_dr_pr
        # II.2 Lista de DE
        self.tabla_de_de =  tabla_de_de_resumen
        self.tabla_relacion_de_pr = tabla_relacion_de_pr
        # II.3 Lista de MP
        self.tabla_de_mp = tabla_de_mp_resumen
        self.tabla_relacion_mp_pr = tabla_relacion_mp_pr
        # II.3 Lista de EP
        self.tabla_de_ep2_resumen = tabla_de_ep2_resumen
        self.tabla_relacion_ep_pr = tabla_relacion_ep_pr

        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Registro de información del problema', 
                                            self.inicio_app, self.cerrar_sesion)
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada
            self.id_objeto_ingresado = id_objeto
            self.lista_para_insertar = lista

            self.tabla_de_pr_cod = b_pr_cod.generar_dataframe()
            self.tabla_relacion_de_pr = base_relacion_de_pr.generar_dataframe()
            self.tabla_relacion_dr_pr = base_relacion_dr_pr.generar_dataframe()
            self.tabla_relacion_mp_pr = base_relacion_mp_pr.generar_dataframe()

            creador = b_pr_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_pr_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_pr.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_pr.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            titulo_cod_problema = 'Código: ' + str(self.cod_usuario_pr)
            rejilla_ep = [
                # Sección 1: Estado
                ('T2', 0, 0, titulo_cod_problema),

                ('L', 1, 0, 'Estado'),
                ('CX', 1, 1, estado_problemas),

                # Sección 2: Ubigeo
                ('T2', 2, 0, 'Ubicación'),

                ('L', 3, 0, 'Departamento'),
                ('CXDEP3', 3, 1, 44, tabla_lista_efa, "Doble", 
                'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

                # Sección 3: Descripción de problema
                ('T2', 5, 0, 'Descripción del problema'),

                ('L', 6, 0, 'Descripción'),
                ('ST', 6, 1),
            
                # Sección 4: Datos
                ('T2', 7, 0, 'Datos'),

                ('L', 8, 0, 'Creado por:'),
                ('L', 8, 1, str(creador)),

                ('L', 8, 2, 'Actualizado por:'),
                ('L', 8, 3, str(ultimo_nombre)),

                ('L', 9, 0, 'Fecha creación:'),
                ('L', 9, 1, str(fecha_creacion)),

                ('L', 9, 2, 'Fecha actualización:'),
                ('L', 9, 3, str(fecha_ultimo))

            ]
            # Se inserta rejilla con datos
            self.frame_rejilla.agregar_rejilla(rejilla_ep)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        else:
            rejilla_ep_nuevo = [
                # Sección 1: Estado
                ('T2', 0, 0, 'Código'),

                ('L', 1, 0, 'Estado'),
                ('CXP', 1, 1, 44, estado_problemas, 'ABIERTO', "readonly"),

                # Sección 2: Ubigeo
                ('T2', 2, 0, 'Ubicación'),

                ('L', 3, 0, 'Departamento'),
                ('CXDEP3', 3, 1, 44, tabla_lista_efa, "Doble", 
                'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

                # Sección 3: Descripción de problema
                ('T2', 5, 0, 'Descripción del problema'),

                ('L', 6, 0, 'Descripción'),
                ('STP', 6, 1, 45, 2),

            ]
            # Se inserta rejilla nueva
            self.frame_rejilla.agregar_rejilla(rejilla_ep_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self.frame_principal)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_ep)

        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self.frame_principal)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_1,
                                                '(+) Añadir extremo', self.nuevo_extremo2,
                                                'Lista de extremos asociados',
                                                self.cod_usuario_pr, self.tabla_de_pr_cod, 
                                                self.tabla_de_ep2_resumen, self.tabla_relacion_ep_pr, 
                                                "ID_PR", "ID_EP", "COD_PR", 
                                                self.ver_ep2, self.eliminar_ep_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self.frame_principal)
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_2,
                                                '(+) Agregar', self.no_asociar,
                                                'Macroproblemas asociados',
                                                self.cod_usuario_pr, self.tabla_de_pr_cod, 
                                                self.tabla_de_mp, self.tabla_relacion_mp_pr, 
                                                "ID_PR", "ID_MP", "COD_PR", 
                                                self.ver_mp, self.eliminar_mp_y_actualizar)
        
        # III.6 Frame de vitrina 3
        self.frame_vitrina_3 = Cuadro(self.frame_principal)
        self.vitrina_3 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_3,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos emitidos asociados',
                                                self.cod_usuario_pr, self.tabla_de_pr_cod, 
                                                self.tabla_de_de, self.tabla_relacion_de_pr, 
                                                "ID_PR", "ID_DE", "COD_PR", 
                                                self.ver_de, self.eliminar_de_y_actualizar)
        
        # III.5 Frame de vitrina 3
        self.frame_vitrina_4 = Cuadro(self.frame_principal)
        self.vitrina_4 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_4,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos recibidos asociados',
                                                self.cod_usuario_pr, self.tabla_de_pr_cod, 
                                                self.tabla_de_dr, self.tabla_relacion_dr_pr, 
                                                "ID_PR", "ID_DR", "COD_PR", 
                                                self.ver_dr, self.eliminar_dr_y_actualizar)


    #----------------------------------------------------------------------
    def guardar_y_actualizar_ep(self):
        
        # Agregamos el objeto
        self.guardar_objeto(self.frame_rejilla,
                            self.cod_usuario_pr, "COD_PR", self.tabla_de_pr_cod,
                            b_pr_cod, b_pr, b_pr_hist, self.ver_ep)
        # Actualización de tabla de código y visualización
        self.tabla_de_pr_cod = b_pr_cod.generar_dataframe()

    #----------------------------------------------------------------------
    def actualizar_vitrinas_ep(self):
        
        # 0. Elimino los últimos frame
        # Frame 2
        self.frame_vitrina_2.eliminar_cuadro()
        if self.vitrina_2 != None:
            self.vitrina_2.eliminar_posible_vitrina()
        # Frame 3
        self.frame_vitrina_3.eliminar_cuadro()
        if self.vitrina_3 != None:
            self.vitrina_3.eliminar_posible_vitrina()

        # I. Situo las ventanas actualizadas
        # I.1 Ventana de documentos emitidos
        self.frame_vitrina_1.eliminar_cuadro()
        if self.vitrina_1 != None: 
            self.vitrina_1.eliminar_posible_vitrina()
        
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_1,
                                                '(+) Agregar', self.no_asociar,
                                                'Macroproblemas asociados',
                                                self.cod_usuario_pr, self.tabla_de_pr_cod, 
                                                self.tabla_de_mp, self.tabla_relacion_mp_pr, 
                                                "ID_PR", "ID_MP", "COD_PR", 
                                                self.ver_mp, self.eliminar_mp_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2.eliminar_cuadro()
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_2,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos emitidos asociados',
                                                self.cod_usuario_pr, self.tabla_de_pr_cod, 
                                                self.tabla_de_de, self.tabla_relacion_de_pr, 
                                                "ID_PR", "ID_DE", "COD_PR", 
                                                self.ver_de, self.eliminar_de_y_actualizar)
        
        # III.5 Frame de vitrina 3
        self.frame_vitrina_3.eliminar_cuadro()
        self.vitrina_3 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_3,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos recibidos asociados',
                                                self.cod_usuario_pr, self.tabla_de_pr_cod, 
                                                self.tabla_de_dr, self.tabla_relacion_dr_pr, 
                                                "ID_PR", "ID_DR", "COD_PR", 
                                                self.ver_dr, self.eliminar_dr_y_actualizar)

        
    #----------------------------------------------------------------------
    def eliminar_dr_y_actualizar(self, id_objeto):
        # Se elimina el DR
        self.eliminar_objeto(self.cod_usuario_pr, "COD_PR", id_objeto, "COD_DR",
                            self.tabla_de_pr_cod, tabla_de_dr_cod, 
                            base_relacion_dr_pr, base_relacion_dr_pr_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_dr_pr = base_relacion_dr_pr.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    
    #----------------------------------------------------------------------
    def eliminar_de_y_actualizar(self, id_objeto):
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_pr, "COD_PR", id_objeto, "COD_DE",
                            self.tabla_de_pr_cod, tabla_de_de_cod, 
                            base_relacion_de_pr, base_relacion_de_pr_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_de_pr = base_relacion_de_pr.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    #----------------------------------------------------------------------
    def eliminar_mp_y_actualizar(self, id_objeto):
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_pr, "COD_PR", id_objeto, "COD_MP",
                            self.tabla_de_pr_cod, tabla_de_mp_cod, 
                            base_relacion_mp_pr, base_relacion_mp_pr_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_mp_pr = base_relacion_mp_pr.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    #----------------------------------------------------------------------
    def eliminar_ep_y_actualizar(self, id_objeto):
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_pr, "COD_PR", id_objeto, "COD_EP",
                            self.tabla_de_pr_cod, tabla_de_pr_cod, 
                            base_relacion_ep_pr, base_relacion_ep_pr_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_ep_pr = base_relacion_ep_pr.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    #----------------------------------------------------------------------
    def no_asociar(self):
        messagebox.showerror("Error",
                            'Para asociar un documento, hágalo desde la vista de documentos')

class Extremo_vinculados(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None,  tipo_objeto = "EP"):
        """Constructor"""

        Ventana.__init__(self, *args)
         # Determinar la ventana principal a partir si es (o no) scrollable
        if self.scrollable_ventana == True:
            self.frame_principal = self.scrollframe
        else:
            self.frame_principal = self
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.cod_usuario_ep = id_objeto
        self.id_objeto_ingresado = id_objeto
        self.tipo_objeto = tipo_objeto
        self.cod_tipo_objeto = 'COD_' + str(tipo_objeto)
        # Parámetros de vitrina
        #self.vitrina_1 = None
        #self.vitina_2 = None
        # Tablas para vitrina
        # 0. Tablas de código de objeto (tabla de problemas)
        self.tabla_de_ep_cod = tabla_de_ep_cod


        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Registro extremo del problema', 
                                            self.inicio_app, self.cerrar_sesion)
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en un extremo creado
            self.id_objeto_ingresado = id_objeto
            self.lista_para_insertar = lista

            self.tabla_de_ep_cod = b_ep_cod.generar_dataframe()
            self.tabla_relacion_ep_pr = base_relacion_ep_pr.generar_dataframe()

            creador = b_ep_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_ep_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_ep.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_ep.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            titulo_cod_problema2 = 'Código: ' + str(self.cod_usuario_ep)
            rejilla_ep = [
                ('T2', 0, 0, titulo_cod_problema2),

                ('L', 1, 0, 'Estado'),
                ('CX', 1, 1, estado_problemas),

                # Sección 2: Origen
                ('T2', 2, 0, 'Origen'),

                ('L', 3, 0, 'Código SINADA'),
                ('EL', 3, 1, 47, 1),

                # Sección 3: Ubigeo
                ('T2', 4, 0, 'Ubicación'),

                ('L', 5, 0, 'Tipo de ubicación'),
                ('CX', 5, 1, ubicacion),

                ('L', 6, 0, 'Georreferencia Este'),
                ('EL', 6, 1, 47, 1),

                ('L', 6, 2, 'Georreferencia Norte'),
                ('EL', 6, 3, 47, 1),

                ('L', 7, 0, 'Extensión'),
                ('CX', 7, 1, extension),

                ('L', 7, 2, 'Ocurrencia'),
                ('CX', 7, 3, ocurrencia),

                # Sección 4: Descripción de problema
                ('T2', 8, 0, 'Caracterización'),

                ('L', 9, 0, 'Tipo de afectación'),
                ('CX', 9, 1, tipo_afectacion),
                
                ('L', 9, 2, 'Agente contaminante'),
                ('CX', 9, 3, agente_conta),

                ('L', 10, 0, 'Tipo de causa'),
                ('CX', 10, 1, tipo_causa),

                ('L', 10, 2, 'Componente ambiental'),
                ('CX', 10, 3, componente_amb),

                # Sección 4: Administrado
                ('T2', 11, 0, 'Administrado'),
                
                ('L', 12, 0, 'Tipo'),
                ('CX', 12, 1, tipo_administrado),

                ('L', 12, 2, 'Administrado'),
                ('EL', 12, 3, 47, 1),

                ('L', 13, 0, 'Actividad'),
                ('CXDEP3', 13, 1, 44, tabla_parametros, "Doble",
                 'ACTIVIDAD', 'Característica 1', 'CARACTERÍSTICA 1', 'Característica 2', 'CARACTERÍSTICA 2'),

                ('L', 14, 0, 'RUC/DNI'),
                ('EL', 14, 1, 47, 1),

                # Sección 5: 
                ('T2', 15, 0, 'EFA'),
                ('L', 16, 0, 'Tipo de EFA'),
                ('CXDEP3', 16, 1, 44, tabla_directorio, "Doble",
                'TIPO_OFICINA', 'Categoría EFA', 'EFA_OSPA', 'EFA', 'Entidad u oficina'),
            
                # Sección 6: Datos
                ('T2', 18, 0, 'Datos'),

                ('L', 19, 0, 'Creado por:'),
                ('L', 19, 1, str(creador)),

                ('L', 19, 2, 'Actualizado por:'),
                ('L', 19, 3, str(ultimo_nombre)),

                ('L', 20, 0, 'Fecha creación:'),
                ('L', 20, 1, str(fecha_creacion)),

                ('L', 20, 2, 'Fecha actualización:'),
                ('L', 20, 3, str(fecha_ultimo)),

                ('T2', 21, 0, '')

            ]
            # Se inserta rejilla con datos
            self.frame_rejilla.agregar_rejilla(rejilla_ep)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        else:
            rejilla_ep_nuevo = [
                # Sección 1: Estado
                ('T2', 0, 0, 'Código'),

                ('L', 1, 0, 'Estado'),
                ('CXP', 1, 1, 44, estado_problemas, 'ABIERTO', "readonly"),

                # Sección 2: Origen
                ('T2', 2, 0, 'Origen'),

                ('L', 3, 0, 'Código SINADA'),
                ('EL', 3, 1, 47, 1),

                # Sección 3: Ubigeo
                ('T2', 4, 0, 'Ubicación'),

                ('L', 5, 0, 'Tipo de ubicación'),
                ('CX', 5, 1, ubicacion),

                ('L', 6, 0, 'Georreferencia Este'),
                ('EL', 6, 1, 47, 1),

                ('L', 6, 2, 'Georreferencia Norte'),
                ('EL', 6, 3, 47, 1),

                ('L', 7, 0, 'Extensión'),
                ('CX', 7, 1, extension),

                ('L', 7, 2, 'Ocurrencia'),
                ('CX', 7, 3, ocurrencia),

                # Sección 4: Descripción de problema
                ('T2', 8, 0, 'Caracterización'),

                ('L', 9, 0, 'Tipo de afectación'),
                ('CX', 9, 1, tipo_afectacion),
                
                ('L', 9, 2, 'Agente contaminante'),
                ('CX', 9, 3, agente_conta),

                ('L', 10, 0, 'Tipo de causa'),
                ('CX', 10, 1, tipo_causa),

                ('L', 10, 2, 'Componente ambiental'),
                ('CX', 10, 3, componente_amb),

                # Sección 4: Administrado
                ('T2', 11, 0, 'Administrado'),
                
                ('L', 12, 0, 'Tipo'),
                ('CX', 12, 1, tipo_administrado),

                ('L', 12, 2, 'Administrado'),
                ('EL', 12, 3, 47, 1),

                ('L', 13, 0, 'Actividad'),
                ('CXDEP3', 13, 1, 44, tabla_parametros, "Doble",
                 'ACTIVIDAD', 'Característica 1', 'CARACTERÍSTICA 1', 'Característica 2', 'CARACTERÍSTICA 2'),

                ('L', 14, 0, 'RUC/DNI'),
                ('EL', 14, 1, 47, 1),

                # Sección 5: EFA
                ('T2', 15, 0, 'EFA'),
                ('L', 16, 0, 'Tipo de EFA'),
                ('CXDEP3', 16, 1, 44, tabla_directorio, "Doble",
                'TIPO_OFICINA', 'Categoría EFA', 'EFA_OSPA', 'EFA', 'Entidad u oficina'),

                ('T2', 17, 0, '')
            
                
            ]
            # Se inserta rejilla nueva
            self.frame_rejilla.agregar_rejilla(rejilla_ep_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self.frame_principal)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_ep)
        f_auxiliar = Cuadro(self.frame_principal)
        f_auxiliar.agregar_titulo_2(1, 0, '')



    #----------------------------------------------------------------------
    def guardar_y_actualizar_ep(self):

        
        # Agregamos el objeto
        self.asociar_ep_pr(self.ver_ep2, self.frame_rejilla,
                            b_ep_hist, self.tabla_de_ep_cod, "COD_EP", self.cod_usuario_ep,
                            b_ep_cod, b_ep)
        # Actualización de tabla de código y visualización
        self.tabla_de_ep_cod = b_ep_cod.generar_dataframe()
        self.tabla_de_pr_cod = b_pr_cod.generar_dataframe()

    def asociar_ep_pr(self, funcion_ver, rejilla_datos, base_objeto_clase_hist, tabla_objeto_clase, cod_entrada, cod_objeto_clase, base_codigo_objeto, base_objeto_clase):
        """"""
        tabla_objeto = tabla_objeto_clase
        cod_objeto = cod_entrada
        codigo_objeto = cod_objeto_clase
        base_cod_objeto = base_codigo_objeto
        base_objeto = base_objeto_clase
        rejilla_frame = rejilla_datos
        datos_ingresados = rejilla_frame.obtener_lista_de_datos()
        base_objeto_hist = base_objeto_clase_hist
        usuario = vg.cod_usuario
        ahora = str(dt.datetime.now())
        id_objeto_ingresado = self.id_objeto_ingresado
        # A. Existe un código en la rejilla
        if self.nuevo == False:
            # Pestaña 1: Obtengo el ID interno a partir del código de usuario
            tabla_codigo_objeto_filtrada = tabla_objeto[tabla_objeto[cod_objeto]==codigo_objeto]
            id_interno_objeto_clase = tabla_codigo_objeto_filtrada.iloc[0,0]
            
            # Actualizo las tablas en la web
            hora_de_modificacion = ahora

            # Pestaña 2:       
            # Cambio los datos de una fila
            # Código interno del aplicativo + Código del usuario del DR + Hora de modificación
            lista_a_sobreescribir = [id_interno_objeto_clase] + [codigo_objeto] + datos_ingresados + [hora_de_modificacion] + [usuario]
            base_objeto.cambiar_los_datos_de_una_fila(codigo_objeto, lista_a_sobreescribir) # Se sobreescribe la información
            # Pestaña 3
            lista_historial = lista_a_sobreescribir
            base_objeto_hist.agregar_datos(lista_historial) # Se sube la info

            # Mensaje
            messagebox.showinfo("¡Excelente!", "Se ha actualizado el registro")
            funcion_ver(codigo_objeto)

        # B. Es un código nuevo
        else:
            hora_de_modificacion = ahora
            #OBTENER EL ID USUARIO DEL PROBLEMA
            codigopr = id_objeto_ingresado
            # OBTENER EL ID INTERNO DEL PROBLEMA
            tabla_de_codigo_pr = b_pr.generar_dataframe()
            tabla_codigo_de_filtrada = tabla_de_codigo_pr[tabla_de_codigo_pr.COD_PR == codigopr]
            id_interno_pr = tabla_codigo_de_filtrada.iloc[0,0]
            # BUSCAR RELACIONES
            tabla_relaciones = base_relacion_ep_pr.generar_dataframe()
            tabla_codigo_relaciones_filtrada = tabla_relaciones[tabla_relaciones['ID_PR']==id_interno_pr]
            numero_extremo_problemas = len(tabla_codigo_relaciones_filtrada.index) + 1
            nuevo_codigo = codigopr + "-" + str(numero_extremo_problemas)
            base_cod_objeto.agregar_codigo(nuevo_codigo, ahora, usuario)
        
            # Definición de ID de relación
            self.IDEP = b_ep_cod.listar_datos_de_fila(nuevo_codigo)
            self.IDEP_FINAL = self.IDEP[0]
            id_relacion_ep_pr = self.IDEP_FINAL + "/" + id_interno_pr

            # GUARDAR RELACION
            # Pestaña 1: Código Único
            datos_insertar = [id_relacion_ep_pr,self.IDEP_FINAL,id_interno_pr,'ACTIVO',hora_de_modificacion]
            base_relacion_ep_pr.agregar_datos(datos_insertar)
            datos_a_cargar_hist = [id_relacion_ep_pr,self.IDEP_FINAL,id_interno_pr,'ACTIVO',hora_de_modificacion,hora_de_modificacion]
            base_relacion_ep_pr_hist.agregar_datos(datos_a_cargar_hist)
            # Descargo el código único
            lista_descargada_codigo = base_cod_objeto.listar_datos_de_fila(nuevo_codigo) # Se trae la info
        
            # Pestaña 2:       
            # Obtengo el ID interno
            id_objeto = lista_descargada_codigo[0]
            cod_objeto = lista_descargada_codigo[3]
            # Creo el vector a subir 
            lista_a_cargar = [id_objeto] + [cod_objeto] + datos_ingresados + [ahora] + [usuario]
            base_objeto.agregar_datos(lista_a_cargar) # Se sube la info

            # Pestaña 3
            hora_de_creacion = str(ahora) # De lo creado en la pestaña 1
            lista_historial = lista_a_cargar + [hora_de_creacion] # Lo subido a la pestaña 2 + hora
            base_objeto_hist.agregar_datos(lista_historial) # Se sube la info

            # Actualización de base y confirmación de registro
            tabla_objeto_clase = base_cod_objeto.generar_dataframe()
            messagebox.showinfo("¡Excelente!", "Se ha ingresado un nuevo registro")
            funcion_ver(cod_objeto)

class Macroproblemas_vista(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None,  tipo_objeto = "MP"):
        """Constructor"""

        Ventana.__init__(self, *args)
         # Determinar la ventana principal a partir si es (o no) scrollable
        if self.scrollable_ventana == True:
            self.frame_principal = self.scrollframe
        else:
            self.frame_principal = self
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.cod_usuario_mp = id_objeto
        self.id_objeto_ingresado = id_objeto
        self.tipo_objeto = tipo_objeto
        self.cod_tipo_objeto = 'COD_' + str(tipo_objeto)
        # Parámetros de vitrina
        self.vitrina_1 = None
        self.vitina_2 = None

        # Tablas para vitrina
        # 0. Tablas de código de objeto
        self.tabla_de_mp_cod = tabla_de_mp_cod
        # II.1 Lista de EP
        self.tabla_de_ep =  tabla_de_ep_resumen
        self.tabla_relacion_mp_pr = tabla_relacion_mp_pr

        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Macroproblema', 
                                            self.inicio_app, self.cerrar_sesion)

        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)
        if self.nuevo == False: # Estamos en una ficha creada
            self.cod_usuario_mp = id_objeto
            self.lista_para_insertar = lista

            self.tabla_de_mp_cod = b_mp_cod.generar_dataframe()
            self.tabla_relacion_mp_pr = base_relacion_mp_pr.generar_dataframe()

            creador = b_mp_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_mp_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_mp.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_mp.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')


            rejilla_mp = [
                #Sección 1: Detalle
                ('T2', 0, 0, 'Detalle'),

                ('L', 1, 0, 'Código'),
                ('L', 1, 1, str(self.cod_usuario_mp)),

                ('L', 2, 0, 'Estado'),
                ('CX', 2, 1, estado_problemas),

                ('L', 2, 2, 'Avance'),
                ('E', 2, 3),

                ('L', 3, 0, 'Agente contaminante'),
                ('CX', 3, 1, agente_conta),

                ('L', 3, 2, 'Componente ambiental'),
                ('CX', 3, 3, componente_amb),

                #Sección 2: Contenido
                ('T2', 4, 0, 'Contenido'),

                ('L', 5, 0, 'Nombre'),
                ('EL', 5, 1, 122, 3),

                ('L', 6, 0, 'Descripción'),
                ('ST', 6, 1),

                ('L', 7, 0, 'Observaciones'),
                ('EL', 7, 1, 122, 3),

                #Sección 2: Datos
                ('T2', 8, 0, 'Datos'),

                ('L', 9, 0, 'Creado por:'),
                ('L', 9, 1, str(creador)),

                ('L', 9, 2, 'Actualizado por:'),
                ('L', 9, 3, str(ultimo_nombre)),

                ('L', 10, 0, 'Fecha creación:'),
                ('L', 10, 1, str(fecha_creacion)),

                ('L', 10, 2, 'Fecha actualización:'),
                ('L', 10, 3, str(fecha_ultimo))

            ]
            self.frame_rejilla.agregar_rejilla(rejilla_mp)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)
        else:
            rejilla_mp_nuevo = [
                #Sección 1: Detalle
                ('T2', 0, 0, 'Detalle'),

                ('L', 1, 0, 'Estado'),
                ('CXP', 1, 1, 44, estado_problemas, 'ABIERTO', "readonly"),

                ('L', 1, 2, 'Avance'),
                ('E', 1, 3),

                ('L', 2, 0, 'Agente contaminante'),
                ('CX', 2, 1, agente_conta),

                ('L', 2, 2, 'Componente ambiental'),
                ('CX', 2, 3, componente_amb),

                #Sección 2: Contenido
                ('T2', 3, 0, 'Contenido'),

                ('L', 4, 0, 'Nombre'),
                ('EL', 4, 1, 122, 3),

                ('L', 5, 0, 'Descripción'),
                ('ST', 5, 1),

                ('L', 6, 0, 'Observaciones'),
                ('EL', 6, 1, 122, 3)

            ]
            # Se inserta rejilla nueva
            self.frame_rejilla.agregar_rejilla(rejilla_mp_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self.frame_principal)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_mp)
        
        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self.frame_principal)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_1,
                                                '(+) Agregar', self.busqueda_ep,
                                                'Extremos de problemas asociados',
                                                self.cod_usuario_mp, self.tabla_de_mp_cod, 
                                                self.tabla_de_ep, self.tabla_relacion_mp_pr, 
                                                "ID_MP", "ID_PR", "COD_MP", 
                                                self.ver_ep, self.eliminar_ep_y_actualizar)
        
        
    #----------------------------------------------------------------------
    def guardar_y_actualizar_mp(self):
        """"""
        # Agregamos el objeto
        self.guardar_objeto(self.frame_rejilla,
                            self.cod_usuario_mp, "COD_MP", self.tabla_de_mp_cod, 
                            b_mp_cod, b_mp, b_mp_hist, self.ver_mp)
        # Actualización de tabla de código y visualización
        self.tabla_de_mp_cod = b_mp_cod.generar_dataframe()
    

    #----------------------------------------------------------------------
    def eliminar_ep_y_actualizar(self, id_objeto):
        """"""
         # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_mp, "COD_MP", id_objeto, "COD_PR",
                            self.tabla_de_mp_cod, tabla_de_pr_cod, 
                            base_relacion_mp_pr, base_relacion_mp_pr_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_mp_pr = base_relacion_mp_pr.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_mp()
    
    #----------------------------------------------------------------------
    def actualizar_vitrinas_mp(self):
        # I. Elimino y sitúo las vitrinas
        # I.1 Ventana de documentos emitidos
        self.frame_vitrina_1.eliminar_cuadro()
        if self.vitrina_1 != None: 
            self.vitrina_1.eliminar_posible_vitrina()

        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_1,
                                                '(+) Agregar', self.busqueda_ep,
                                                'Extremos de problemas asociados',
                                                self.cod_usuario_mp, self.tabla_de_mp_cod, 
                                                self.tabla_de_ep, self.tabla_relacion_mp_pr, 
                                                "ID_MP", "ID_PR", "COD_MP", 
                                                self.ver_ep, self.eliminar_ep_y_actualizar)
