import datetime as dt

from tkinter import *
from tkinter import messagebox
from tkinter.constants import TRUE

from modulos import ventanas_busqueda
from modulos import variables_globales as vg
from modulos.funcionalidades_ospa import funcionalidades_ospa
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
b_ep = vg.b_ep
b_ep_cod = vg.b_ep_cod
b_ep_hist = vg.b_ep_hist
b_mp = vg.b_mp
b_mp_cod = vg.b_mp_cod
b_mp_hist = vg.b_mp_hist

base_datos_usuario = vg.base_datos_usuario
base_relacion_docs = vg.base_relacion_docs
base_relacion_dr_ep = vg.base_relacion_dr_ep
base_relacion_de_ep = vg.base_relacion_de_ep
base_relacion_mp_ep = vg.base_relacion_mp_ep

base_relacion_docs_hist = vg.base_relacion_docs_hist
base_relacion_dr_ep_hist = vg.base_relacion_dr_ep_hist
base_relacion_de_ep_hist = vg.base_relacion_de_ep_hist
base_relacion_mp_ep_hist = vg.base_relacion_mp_ep_hist

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
tabla_parametros_act = vg.tabla_parametros_act
# 4.2 Desplegables en Drive
agente_conta = list(set(tabla_parametros['AGENTE CALCULADORA']))
componente_amb = list(set(tabla_parametros['COMPONENTE CALCULADORA']))
actividad_eco = list(set(tabla_parametros['ACTIVIDAD CALCULADORA']))
extension = list(set(tabla_parametros['EXTENSION CALCULADORA']))
ubicacion = list(set(tabla_parametros['UBICACION CALCULADORA']))
ocurrencia = list(set(tabla_parametros['OCURRENCIA CALCULADORA']))
# 4.4 Desplegables en Local
combo_vacio = ()
tipo_afectacion = ('AGENTE CONTAMINANTE', 'EXTRACCIÓN DE RECURSOS')
tipo_administrado = ('PERSONA NATURAL', 'PERSONA JURÍDICA')
estado_problemas = ('ABIERTO', 'CERRADO')
tipo_causa = ('CAUSA DESCONOCIDA', 'CAUSA NATURAL', 'CAUSA HUMANA')
tipo_ingreso = ('DIRECTO', 'DERIVACION-SUBDIRECCION', 
                'DERIVACION-SUPERVISION', 'DERIVACION-SINADA')
tipo_documento = ('OFICIO', 'MEMORANDO', 'CARTA', 'OFICIO CIRCULAR','MEMORANDO CIRCULAR', 'CARTA CIRCULAR',
                  'INFORME', 'RESOLUCIÓN', 'CÉDULA DE NOTIFICACIÓN', 'INFORME MÚLTIPLE', 'OTROS')
especialista_1 = ('Zurita, Carolina', 'López, José')
tipo_accion_1 = ('Actualizar', 'Crear', 'No corresponde', 'Archivar')

especialista_2 = ('Melendez, Assur', 'Cueto, María Mónica', 'Gamarra, Ibon', 'Guevara, Sandra', 'Terrones, Leslie')
tipo_accion_2 = ('Archivo por insumo de cierre', 'Archivo por conocimiento', 'Archivo - Insumo de seguimiento')

si_no = ('Si', 'No')
tipo_respuesta = ('Ejecutó supervisión','Solicitó información a administrado',
                  'Ejecutó acción de evaluación', 'Inició PAS', 'Administrado en adecuación / formalización',
                  'Programó supervisión', 'Programó acción de evaluación', 'No es competente',
                  'No corresponde lo solicitado', 'En evaluación de la EFA', 'Otros')
categorias = ('Pedido de información', 'Pedido de información adicional', 'Pedido de información urgente',
              'Traslado de Información', 'Programación')
marco_pedido = ('EFA', 'OEFA',
                'Colaboración', 'Delegación', 'Conocimiento')

# 5. Tablas resumen
# 5.0 Relaciones
tabla_relacion_dr_de = vg.tabla_relacion_dr_de
tabla_relacion_dr_ep = vg.tabla_relacion_dr_ep
tabla_relacion_de_ep = vg.tabla_relacion_de_ep
tabla_relacion_mp_ep = vg.tabla_relacion_mp_ep
# 5.1 Documentos recibidos
tabla_de_dr_cod = vg.tabla_de_dr_cod
tabla_de_dr_completa = vg.tabla_de_dr_completa
tabla_de_dr_resumen = vg.tabla_de_dr_resumen
# 5.2 Documentos emitidos
tabla_de_de_cod = vg.tabla_de_de_cod
tabla_de_de_completa = vg.tabla_de_de_completa
tabla_de_de_resumen = vg.tabla_de_de_resumen
# 5.3 Extremos de problema
tabla_de_ep_cod = vg.tabla_de_ep_completa
tabla_de_ep_completa = vg.tabla_de_ep_completa
tabla_de_ep_resumen = vg.tabla_de_ep_resumen
# 5.4 Macroproblemas
tabla_de_mp_cod = vg.tabla_de_mp_completa
tabla_de_mp_completa = vg.tabla_de_mp_completa
tabla_de_mp_resumen = vg.tabla_de_mp_resumen
    
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
        self.tabla_relacion_dr_ep = tabla_relacion_dr_ep

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
            self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()

            creador = b_dr_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_dr_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_dr.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_dr.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            rejilla_dr = [

                # Sección 1: Detalle
                ('T2', 0, 0, 'Detalle'),   
                
                ('L', 1, 0, 'Tipo de documento'),
                ('CX', 1, 1, tipo_documento),

                ('L', 1, 2, 'N° de documento'),
                ('E', 1, 3),

                ('L', 2, 0, 'Asunto'),
                ('EL', 2, 1, 112, 3),

                ('L', 3, 0, 'Fecha de recepción OEFA'),
                ('D', 3, 1),

                ('L', 3, 2, 'Fecha de recepción SEFA'),
                ('D', 3, 3),

                ('L', 4, 0, 'Vía de recepción'),
                ('CX', 4, 1, tipo_ingreso),

                ('L', 4, 2, 'HT de documento'),
                ('E', 4, 3),

                ('L', 5, 0, 'Tipo Remitente'),
                ('CXDEP3', 5, 1, 39, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Remitente', 'EFA_OSPA', 'Remitente', 'Entidad u oficina'),

                ('L', 6, 2, '¿Es respuesta?'),
                ('CX', 6, 3, si_no),

                # Sección 2: Contenido (Equipo 1)
                ('T2', 7, 0, 'Contenido'),   

                ('L', 8, 0, 'Fecha asignación'),
                ('DE', 8, 1),

                ('L', 8, 2, 'Especialista Eq. 1'),
                ('CX', 8, 3, especialista_1),

                ('L', 9, 0, 'Fecha de ejecución'),
                ('DE', 9, 1),

                ('L', 9, 2, 'Acción'),
                ('CX', 9, 3, tipo_accion_1),

                ('L', 10, 0, 'Aporte del documento'),
                ('ST', 10, 1),

                # Sección 3: Contenido (Equipo 1)
                ('T2', 11, 0, 'Acciones'),  

                ('L', 12, 0, 'Fecha asignación'),
                ('DE', 12, 1),

                ('L', 12, 2, 'Especialista Eq. 2'),
                ('CX', 12, 3, especialista_2),

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
                ('T2', 0, 0, 'Detalle'),   
                
                ('L', 1, 0, 'Tipo de documento'),
                ('CX', 1, 1, tipo_documento),

                ('L', 1, 2, 'N° de documento'),
                ('E', 1, 3),

                ('L', 2, 0, 'Asunto'),
                ('EL', 2, 1, 112, 3),

                ('L', 3, 0, 'Fecha de recepción OEFA'),
                ('D', 3, 1),

                ('L', 3, 2, 'Fecha de recepción SEFA'),
                ('D', 3, 3),

                ('L', 4, 0, 'Vía de recepción'),
                ('CX', 4, 1, tipo_ingreso),

                ('L', 4, 2, 'HT de documento'),
                ('E', 4, 3),

                ('L', 5, 0, 'Tipo Remitente'),
                ('CXDEP3', 5, 1, 39, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Remitente', 'EFA_OSPA', 'Remitente', 'Entidad u oficina'),

                ('L', 6, 2, '¿Es respuesta?'),
                ('CX', 6, 3, si_no),

                # Sección 2: Contenido (Equipo 1)
                ('T2', 7, 0, 'Contenido'),   

                ('L', 8, 0, 'Fecha asignación'),
                ('DE', 8, 1),

                ('L', 8, 2, 'Especialista Eq. 1'),
                ('CX', 8, 3, especialista_1),

                ('L', 9, 0, 'Fecha de ejecución'),
                ('DE', 9, 1),

                ('L', 9, 2, 'Acción'),
                ('CX', 9, 3, tipo_accion_1),

                ('L', 10, 0, 'Aporte del documento'),
                ('ST', 10, 1),

                # Sección 3: Contenido (Equipo 1)
                ('T2', 11, 0, 'Acciones'),  

                ('L', 12, 0, 'Fecha asignación'),
                ('DE', 12, 1),

                ('L', 12, 2, 'Especialista Eq. 2'),
                ('CX', 12, 3, especialista_2),

                ('L', 13, 0, 'Fecha de ejecución'),
                ('DE', 13, 1),

                ('L', 13, 2, 'Respuesta'),
                ('CX', 13, 3, tipo_respuesta)

            ]
            self.frame_rejilla.agregar_rejilla(rejilla_dr_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self.frame_principal)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_dr)

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
                                            'Extremos de problemas asociados',
                                            self.cod_usuario_dr, self.tabla_de_dr_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_dr_ep, 
                                            "ID_DR", "ID_EP", "COD_DR", 
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
        self.eliminar_objeto(self.cod_usuario_dr, "COD_DR", id_objeto, "COD_EP",
                            self.tabla_de_dr_cod, tabla_de_ep_cod, 
                            base_relacion_dr_ep, base_relacion_dr_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
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
                                            'Extremo de problemas asociados',
                                            self.cod_usuario_dr, self.tabla_de_dr_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_dr_ep, 
                                            "ID_DR", "ID_EP", "COD_DR", 
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
        self.tabla_relacion_de_ep = tabla_relacion_de_ep

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
            self.tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
            
            creador = b_de_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_de_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_de.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_de.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            rejilla_de = [
                ('T2', 0, 0, 'Detalle'),

                ('L', 0, 0, 'HT de documento'),
                ('E', 0, 1),

                ('L', 0, 2, 'Categoría'),
                ('CX', 0, 3, categorias),

                ('L', 1, 0, 'Tipo Destinatario'),
                ('CXDEP3', 1, 1, 39, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Destinatario', 'EFA_OSPA', 'Destinatario', 'Entidad u oficina'),

                ('L', 2, 2, 'Marco de pedido'),
                ('CX', 2, 3, marco_pedido),

                # Sección 2: Documento
                ('T2', 3, 0, 'Elaboración'),

                ('L', 3, 0, 'Fecha de proyecto'),
                ('DE', 3, 1), 

                ('L', 3, 2, 'HT Salida'),
                ('E', 3, 3), 

                ('L', 4, 0, 'Tipo de documento'),
                ('CX', 4, 1, tipo_documento),

                ('L', 4, 2, 'N° de documento'),
                ('E', 4, 3),

                ('L', 5, 0, 'Fecha de firma'),
                ('DE', 5, 1), 

                ('L', 5, 2, 'Fecha de notificación'),
                ('DE', 5, 3),

                # Sección 3: Contenido
                ('T2', 6, 0, 'Contenido'),

                ('L', 7, 0, 'Detalle de requerimiento'),
                ('ST', 7, 1),

                # Sección 4: Reiterativo
                ('T2', 8, 0, 'Reiterativo'),

                ('L', 9, 0, 'Fecha de proyecto'),
                ('DE', 9, 1), 

                ('L', 9, 2, '¿Se emitió?'),
                ('CX', 9, 3, si_no), 

                ('L', 10, 0, 'Tipo de documento'),
                ('CX', 10, 1, tipo_documento),

                ('L', 10, 2, 'N° de documento'),
                ('E', 10, 3),

                ('L', 11, 0, 'Fecha de firma'),
                ('DE', 11, 1), 

                ('L', 11, 2, 'Fecha de notificación'),
                ('DE', 11, 3),

                # Sección 5: OCI
                ('T2', 12, 0, 'OCI'),

                ('L', 13, 0, 'Fecha de proyecto'),
                ('DE', 13, 1), 

                ('L', 13, 2, '¿Se emitió?'),
                ('CX', 13, 3, si_no), 

                ('L', 14, 0, 'Tipo de documento'),
                ('CX', 14, 1, tipo_documento),

                ('L', 14, 2, 'N° de documento'),
                ('E', 14, 3),

                ('L', 15, 0, 'Fecha de firma'),
                ('DE', 15, 1), 

                ('L', 15, 2, 'Fecha de notificación'),
                ('DE', 15, 3),
                
                # Sección 6: Datos
                ('T2', 16, 0, 'Datos'),

                ('L', 17, 0, 'Creado por:'),
                ('L', 17, 1, str(creador)),

                ('L', 17, 2, 'Actualizado por:'),
                ('L', 17, 3, str(ultimo_nombre)),

                ('L', 18, 0, 'Fecha creación:'),
                ('L', 18, 1, str(fecha_creacion)),

                ('L', 18, 2, 'Fecha actualización:'),
                ('L', 18, 3, str(fecha_ultimo))
            ]
            
            self.frame_rejilla.agregar_rejilla(rejilla_de)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        else:
            rejilla_de_nuevo = [
            
                ('T2', 0, 0, 'Detalle'),

                ('L', 0, 0, 'HT de documento'),
                ('E', 0, 1),

                ('L', 0, 2, 'Categoría'),
                ('CX', 0, 3, categorias),

                ('L', 1, 0, 'Tipo Destinatario'),
                ('CXDEP3', 1, 1, 39, tabla_directorio, "Doble",
                'Tipo de entidad u oficina', 'Categoría Destinatario', 'EFA_OSPA', 'Destinatario', 'Entidad u oficina'),

                ('L', 2, 2, 'Marco de pedido'),
                ('CX', 2, 3, marco_pedido),

                # Sección 2: Documento
                ('T2', 3, 0, 'Elaboración'),

                ('L', 4, 0, 'Especialista'),
                ('CX', 4, 1, especialista_2), 

                ('L', 4, 2, 'Fecha de elaboración'),
                ('DE', 4, 3), 

                ('L', 5, 0, 'Tipo de documento'),
                ('CX', 5, 1, tipo_documento),

                ('L', 5, 2, 'N° de documento'),
                ('E', 5, 3),

                ('L', 6, 0, 'Fecha de firma'),
                ('DE', 6, 1), 

                ('L', 6, 2, 'Fecha de notificación'),
                ('DE', 6, 3),

                # Sección 3: Contenido
                ('T2', 7, 0, 'Elaboración'),

                ('L', 8, 0, 'Detalle de requerimiento'),
                ('ST', 8, 1),

                # Sección 4: Reiterativo
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

                # Sección 5: OCI
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
                                            'Extremo de problemas asociados',
                                            self.cod_usuario_de, self.tabla_de_de_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_de_ep, 
                                            "ID_DE", "ID_EP", "COD_DE", 
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
        self.eliminar_objeto(self.cod_usuario_de, "COD_DE", id_objeto, "COD_EP",
                            self.tabla_de_de_cod, tabla_de_ep_cod, 
                            base_relacion_de_ep, base_relacion_de_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
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
                                            'Extremo de problemas asociados',
                                            self.cod_usuario_de, self.tabla_de_de_cod, 
                                            self.tabla_de_ep, self.tabla_relacion_de_ep, 
                                            "ID_DE", "ID_EP", "COD_DE", 
                                            self.ver_ep, self.eliminar_ep_y_actualizar)
         
class Extremo_problemas_vista(funcionalidades_ospa):
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
        self.vitrina_1 = None
        self.vitina_2 = None

        # Tablas para vitrina
        # 0. Tablas de código de objeto
        self.tabla_de_ep_cod = tabla_de_ep_cod
        # II.1 Lista de DR
        self.tabla_de_dr =  tabla_de_dr_resumen
        self.tabla_relacion_dr_ep = tabla_relacion_dr_ep
        # II.2 Lista de DE
        self.tabla_de_de =  tabla_de_de_resumen
        self.tabla_relacion_de_ep = tabla_relacion_de_ep
        # II.3 Lista de MP
        self.tabla_de_mp = tabla_de_mp_resumen
        self.tabla_relacion_mp_ep = tabla_relacion_mp_ep

        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Detalle de extremo de problema', 
                                            self.inicio_app, self.cerrar_sesion)
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada

            self.tabla_de_ep_cod = b_ep_cod.generar_dataframe()
            self.tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
            self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
            self.tabla_relacion_mp_ep = base_relacion_mp_ep.generar_dataframe()
            self.cod_usuario_dr = id_objeto
            self.lista_para_insertar = lista

            creador = b_ep_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_ep_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_ep.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_ep.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            rejilla_ep = [
                ('L', 0, 0, 'Código de problema'),
                ('L', 0, 1, str(self.cod_usuario_ep)),

                ('L', 0, 2, 'Código SINADA'),
                ('EL', 0, 3, 35, 1),

                ('L', 0, 4, 'Estado'),
                ('CXP', 0, 5, 32, estado_problemas, '', "readonly"),

                ('L', 1, 0, 'Departamento'),
                ('CXDEP3', 1, 1, 32, tabla_lista_efa, "Triple", 
                'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

                ('L', 2, 0, 'Tipo de ubicación'),
                ('CXP', 2, 1, 32, ubicacion, '', "readonly"),

                ('L', 2, 2, 'Extensión'),
                ('CXP', 2, 3, 32, extension, '', "readonly"),

                ('L', 2, 4, 'Ocurrencia'),
                ('CXP', 2, 5, 32, ocurrencia, '', "readonly"),

                ('L', 3, 0, 'Tipo de afectación'),
                ('CXP', 3, 1, 32, tipo_afectacion, '', "readonly"),
                
                ('L', 3, 2, 'Agente contaminante'),
                ('CXP', 3, 3, 32, agente_conta, '', "readonly"),

                ('L', 3, 4, 'Descripción'),
                ('STP', 3, 5, 33, 2),

                ('L', 4, 0, 'Tipo de causa'),
                ('CXP', 4, 1, 32, tipo_causa, '', "readonly"),

                ('L', 4, 2, 'Componente ambiental'),
                ('CXP', 4, 3, 32, componente_amb, '', "readonly"),
                
                ('L', 5, 0, 'Actividad'),
                ('CXDEP3', 5, 1, 32, tabla_parametros_act, "Triple",
                 'ACTIVIDAD', 'Característica 1', 'CARACTERÍSTICA 1', 'Característica 2', 'CARACTERÍSTICA 2'),

                ('L', 6, 0, 'Tipo de EFA'),
                ('CXDEP3', 6, 1, 32, tabla_directorio, "Triple",
                'TIPO_OFICINA', 'Categoría EFA', 'EFA_OSPA', 'EFA', 'Entidad u oficina'),

                ('L', 7, 0, 'Creado por:'),
                ('L', 7, 1, str(creador)),

                ('L', 7, 4, 'Actualizado por:'),
                ('L', 7, 5, str(ultimo_nombre)),

                ('L', 8, 0, 'Fecha creación:'),
                ('L', 8, 1, str(fecha_creacion)),

                ('L', 8, 4, 'Fecha actualización:'),
                ('L', 8, 5, str(fecha_ultimo))

            ]
            # Se inserta rejilla con datos
            self.frame_rejilla.agregar_rejilla(rejilla_ep)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)
        else:
            rejilla_ep_nuevo = [
                ('L', 0, 0, ' '),
                ('L', 0, 1, ' '),
                
                ('L', 0, 2, 'Código SINADA'),
                ('EL', 0, 3, 35, 1),

                ('L', 0, 4, 'Estado'),
                ('CXP', 0, 5, 32, estado_problemas, '', "readonly"),

                ('L', 1, 0, 'Departamento'),
                ('CXDEP3', 1, 1, 32, tabla_lista_efa, "Triple", 
                'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

                ('L', 2, 0, 'Tipo de ubicación'),
                ('CXP', 2, 1, 32, ubicacion, '', "readonly"),

                ('L', 2, 2, 'Extensión'),
                ('CXP', 2, 3, 32, extension, '', "readonly"),

                ('L', 2, 4, 'Ocurrencia'),
                ('CXP', 2, 5, 32, ocurrencia, '', "readonly"),

                ('L', 3, 0, 'Tipo de afectación'),
                ('CXP', 3, 1, 32, tipo_afectacion, '', "readonly"),
                
                ('L', 3, 2, 'Agente contaminante'),
                ('CXP', 3, 3, 32, agente_conta, '', "readonly"),

                ('L', 3, 4, 'Descripción'),
                ('STP', 3, 5, 33, 2),

                ('L', 4, 0, 'Tipo de causa'),
                ('CXP', 4, 1, 32, tipo_causa, '', "readonly"),

                ('L', 4, 2, 'Componente ambiental'),
                ('CXP', 4, 3, 32, componente_amb, '', "readonly"),
                
                ('L', 5, 0, 'Actividad'),
                ('CXDEP3', 5, 1, 32, tabla_parametros_act, "Triple",
                 'ACTIVIDAD', 'Característica 1', 'CARACTERÍSTICA 1', 'Característica 2', 'CARACTERÍSTICA 2'),

                ('L', 6, 0, 'Tipo de EFA'),
                ('CXDEP3', 6, 1, 32, tabla_directorio, "Triple",
                'TIPO_OFICINA', 'Categoría EFA', 'EFA_OSPA', 'EFA', 'Entidad u oficina')
            ]
            # Se inserta rejilla nueva
            self.frame_rejilla.agregar_rejilla(rejilla_ep_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self.frame_principal)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_ep)
        f_boton.agregar_button(0, 2, 'Alterno', self.nuevo_n_ep)
        
        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self.frame_principal)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_1,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos recibidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_dr, self.tabla_relacion_dr_ep, 
                                                "ID_EP", "ID_DR", "COD_EP", 
                                                self.ver_dr, self.eliminar_dr_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self.frame_principal)
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_2,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos emitidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_de, self.tabla_relacion_de_ep, 
                                                "ID_EP", "ID_DE", "COD_EP", 
                                                self.ver_de, self.eliminar_de_y_actualizar)
        
        # III.5 Frame de vitrina 3
        self.frame_vitrina_3 = Cuadro(self.frame_principal)
        self.vitrina_3 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_3,
                                                '(+) Agregar', self.no_asociar,
                                                'Macroproblemas asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_mp, self.tabla_relacion_mp_ep, 
                                                "ID_EP", "ID_MP", "COD_EP", 
                                                self.ver_mp, self.eliminar_mp_y_actualizar)

    #----------------------------------------------------------------------
    def guardar_y_actualizar_ep(self):
        
        # Agregamos el objeto
        self.guardar_objeto(self.frame_rejilla,
                            self.cod_usuario_ep, "COD_EP", self.tabla_de_ep_cod,
                            b_ep_cod, b_ep, b_ep_hist, self.ver_ep)
        # Actualización de tabla de código y visualización
        self.tabla_de_ep_cod = b_ep_cod.generar_dataframe()

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
                                                'Documentos recibidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_dr, self.tabla_relacion_dr_ep, 
                                                "ID_EP", "ID_DR", "COD_EP", 
                                                self.ver_dr, self.eliminar_dr_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2.eliminar_cuadro()
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_2,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos emitidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_de, self.tabla_relacion_de_ep, 
                                                "ID_EP", "ID_DE", "COD_EP", 
                                                self.ver_de, self.eliminar_de_y_actualizar)
        
        # III.5 Frame de vitrina 3
        self.frame_vitrina_3.eliminar_cuadro()
        self.vitrina_3 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_3,
                                                '(+) Agregar', self.no_asociar,
                                                'Macroproblemas asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_mp, self.tabla_relacion_mp_ep, 
                                                "ID_EP", "ID_MP", "COD_EP", 
                                                self.ver_mp, self.eliminar_mp_y_actualizar)


    #----------------------------------------------------------------------
    def eliminar_dr_y_actualizar(self, id_objeto):
        # Se elimina el DR
        self.eliminar_objeto(self.cod_usuario_ep, "COD_EP", id_objeto, "COD_DR",
                            self.tabla_de_ep_cod, tabla_de_dr_cod, 
                            base_relacion_dr_ep, base_relacion_dr_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    
    #----------------------------------------------------------------------
    def eliminar_de_y_actualizar(self, id_objeto):
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_ep, "COD_EP", id_objeto, "COD_DE",
                            self.tabla_de_ep_cod, tabla_de_de_cod, 
                            base_relacion_de_ep, base_relacion_de_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    #----------------------------------------------------------------------
    def eliminar_mp_y_actualizar(self, id_objeto):
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_ep, "COD_EP", id_objeto, "COD_MP",
                            self.tabla_de_ep_cod, tabla_de_mp_cod, 
                            base_relacion_mp_ep, base_relacion_mp_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_mp_ep = base_relacion_mp_ep.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    #----------------------------------------------------------------------
    def no_asociar(self):
        messagebox.showerror("Error",
                            'Para asociar un documento, hágalo desde la vista de documentos')

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
        # Parámetros de vitrina
        self.vitrina_1 = None
        self.vitina_2 = None

        # Tablas para vitrina
        # 0. Tablas de código de objeto
        self.tabla_de_mp_cod = tabla_de_mp_cod
        # II.1 Lista de EP
        self.tabla_de_ep =  tabla_de_ep_resumen
        self.tabla_relacion_mp_ep = tabla_relacion_mp_ep

        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Detalle de macroproblema', 
                                            self.inicio_app, self.cerrar_sesion)

        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)
        if self.nuevo == False: # Estamos en una ficha creada
            self.tabla_de_mp_cod = b_mp_cod.generar_dataframe()
            self.cod_usuario_mp = id_objeto
            self.lista_para_insertar = lista
            rejilla_mp = [

                ('L', 0, 0, 'Código de macroproblema'),
                ('L', 0, 1, str(self.cod_usuario_mp)),

                ('L', 1, 0, 'Nombre del problema'),
                ('EL', 1, 1, 110, 3),

                ('L', 2, 0, 'Descripción'),
                ('ST', 2, 1),

                ('L', 3, 0, 'Observaciones'),
                ('EL', 3, 1, 110, 3)

            ]
            self.frame_rejilla.agregar_rejilla(rejilla_mp)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)
        else:
            rejilla_mp_nuevo = [
                ('L', 0, 0, ''),
                ('L', 0, 1, ''),

                ('L', 1, 0, 'Nombre del problema'),
                ('EL', 1, 1, 110, 3),

                ('L', 2, 0, 'Descripción'),
                ('ST', 2, 1),

                ('L', 3, 0, 'Observaciones'),
                ('EL', 3, 1, 110, 3)
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
                                                self.tabla_de_ep, self.tabla_relacion_mp_ep, 
                                                "ID_MP", "ID_EP", "COD_MP", 
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
        self.eliminar_objeto(self.cod_usuario_mp, "COD_MP", id_objeto, "COD_EP",
                            self.tabla_de_mp_cod, tabla_de_ep_cod, 
                            base_relacion_mp_ep, base_relacion_mp_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_mp_ep = base_relacion_mp_ep.generar_dataframe()
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
                                                self.tabla_de_ep, self.tabla_relacion_mp_ep, 
                                                "ID_MP", "ID_EP", "COD_MP", 
                                                self.ver_ep, self.eliminar_ep_y_actualizar)

class N_Extremo_problemas_vista(funcionalidades_ospa):
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
        self.vitrina_1 = None
        self.vitina_2 = None

        # Tablas para vitrina
        # 0. Tablas de código de objeto
        self.tabla_de_ep_cod = tabla_de_ep_cod
        # II.1 Lista de DR
        self.tabla_de_dr =  tabla_de_dr_resumen
        self.tabla_relacion_dr_ep = tabla_relacion_dr_ep
        # II.2 Lista de DE
        self.tabla_de_de =  tabla_de_de_resumen
        self.tabla_relacion_de_ep = tabla_relacion_de_ep
        # II.3 Lista de MP
        self.tabla_de_mp = tabla_de_mp_resumen
        self.tabla_relacion_mp_ep = tabla_relacion_mp_ep

        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self.frame_principal)
        titulos.agregar_franja_superior_ospa('Detalle de extremo de problema', 
                                            self.inicio_app, self.cerrar_sesion)
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self.frame_principal)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada
            self.id_objeto_ingresado = id_objeto
            self.lista_para_insertar = lista

            self.tabla_de_ep_cod = b_ep_cod.generar_dataframe()
            self.tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
            self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
            self.tabla_relacion_mp_ep = base_relacion_mp_ep.generar_dataframe()

            creador = b_ep_cod.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_creacion = b_ep_cod.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'F_CREACION')

            ultimo_nombre = b_ep.obtener_usuario(base_datos_usuario, self.id_objeto_ingresado,  self.cod_tipo_objeto)
            fecha_ultimo =  b_ep.obtener_valor_columna_con_codigo_unico(self.cod_tipo_objeto, self.id_objeto_ingresado, 'FECHA_ULTIMO_MOV')

            titulo_cod_problema = 'Código: ' + str(self.cod_usuario_ep)
            rejilla_ep = [
                # Sección 1: Estado
                ('T2', 0, 0, titulo_cod_problema),

                ('L', 1, 0, 'Estado'),
                ('CXP', 1, 1, 39, estado_problemas, 'ABIERTO', "readonly"),

                # Sección 2: Origen
                ('T2', 2, 0, 'Origen'),

                ('L', 3, 0, 'Código SINADA'),
                ('EL', 3, 1, 42, 1),

                # Sección 3: Ubigeo
                ('T2', 4, 0, 'Ubicación'),

                ('L', 5, 0, 'Departamento'),
                ('CXDEP3', 5, 1, 39, tabla_lista_efa, "Doble", 
                'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

                ('L', 6, 2, 'Tipo de ubicación'),
                ('CX', 6, 3, ubicacion),

                ('L', 7, 0, 'Georreferencia Este'),
                ('EL', 7, 1, 42, 1),

                ('L', 7, 2, 'Georreferencia Norte'),
                ('EL', 7, 3, 42, 1),

                ('L', 8, 0, 'Extensión'),
                ('CX', 8, 1, extension),

                ('L', 8, 2, 'Ocurrencia'),
                ('CX', 8, 3, ocurrencia),

                # Sección 4: Descripción de problema
                ('T2', 9, 0, 'Caracterización'),

                ('L', 10, 0, 'Tipo de afectación'),
                ('CX', 10, 1, tipo_afectacion),
                
                ('L', 10, 2, 'Agente contaminante'),
                ('CX', 10, 3, agente_conta),

                ('L', 11, 0, 'Tipo de causa'),
                ('CX', 11, 1, tipo_causa),

                ('L', 11, 2, 'Descripción'),
                ('STP', 11, 3, 40, 2),

                ('L', 12, 0, 'Componente ambiental'),
                ('CX', 12, 1, componente_amb),

                # Sección 4: Administrado
                ('T2', 13, 0, 'Administrado'),
                
                ('L', 14, 0, 'Tipo'),
                ('CX', 14, 1, tipo_administrado),

                ('L', 14, 2, 'Administrado'),
                ('EL', 14, 3, 42, 1),

                ('L', 15, 0, 'Actividad'),
                ('CXDEP3', 15, 1, 39, tabla_parametros_act, "Doble",
                 'ACTIVIDAD', 'Característica 1', 'CARACTERÍSTICA 1', 'Característica 2', 'CARACTERÍSTICA 2'),

                # Sección 5: 
                ('T2', 17, 0, 'EFA'),
                ('L', 18, 0, 'Tipo de EFA'),
                ('CXDEP3', 18, 1, 39, tabla_directorio, "Doble",
                'TIPO_OFICINA', 'Categoría EFA', 'EFA_OSPA', 'EFA', 'Entidad u oficina'),
            
                # Sección 6: Datos
                ('L', 7, 0, 'Creado por:'),
                ('L', 7, 1, str(creador)),

                ('L', 7, 4, 'Actualizado por:'),
                ('L', 7, 5, str(ultimo_nombre)),

                ('L', 8, 0, 'Fecha creación:'),
                ('L', 8, 1, str(fecha_creacion)),

                ('L', 8, 4, 'Fecha actualización:'),
                ('L', 8, 5, str(fecha_ultimo))
            ]
            # Se inserta rejilla con datos
            self.frame_rejilla.agregar_rejilla(rejilla_ep)
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        else:
            rejilla_ep_nuevo = [
                # Sección 1: Estado
                ('T2', 0, 0, 'Código'),

                ('L', 1, 0, 'Estado'),
                ('CXP', 1, 1, 39, estado_problemas, 'ABIERTO', "readonly"),

                # Sección 2: Origen
                ('T2', 2, 0, 'Origen'),

                ('L', 3, 0, 'Código SINADA'),
                ('EL', 3, 1, 42, 1),

                # Sección 3: Ubigeo
                ('T2', 4, 0, 'Ubicación'),

                ('L', 5, 0, 'Departamento'),
                ('CXDEP3', 5, 1, 39, tabla_lista_efa, "Doble", 
                'DEPARTAMENTO ', 'Provincia', 'PROVINCIA ', 'Distrito', 'DISTRITO '),

                ('L', 6, 2, 'Tipo de ubicación'),
                ('CX', 6, 3, ubicacion),

                ('L', 7, 0, 'Georreferencia Este'),
                ('EL', 7, 1, 42, 1),

                ('L', 7, 2, 'Georreferencia Norte'),
                ('EL', 7, 3, 42, 1),

                ('L', 8, 0, 'Extensión'),
                ('CX', 8, 1, extension),

                ('L', 8, 2, 'Ocurrencia'),
                ('CX', 8, 3, ocurrencia),

                # Sección 4: Descripción de problema
                ('T2', 9, 0, 'Caracterización'),

                ('L', 10, 0, 'Tipo de afectación'),
                ('CX', 10, 1, tipo_afectacion),
                
                ('L', 10, 2, 'Agente contaminante'),
                ('CX', 10, 3, agente_conta),

                ('L', 11, 0, 'Tipo de causa'),
                ('CX', 11, 1, tipo_causa),

                ('L', 11, 2, 'Descripción'),
                ('STP', 11, 3, 40, 2),

                ('L', 12, 0, 'Componente ambiental'),
                ('CX', 12, 1, componente_amb),

                # Sección 4: Administrado
                ('T2', 13, 0, 'Administrado'),
                
                ('L', 14, 0, 'Tipo'),
                ('CX', 14, 1, tipo_administrado),

                ('L', 14, 2, 'Administrado'),
                ('EL', 14, 3, 42, 1),

                ('L', 15, 0, 'Actividad'),
                ('CXDEP3', 15, 1, 39, tabla_parametros_act, "Doble",
                 'ACTIVIDAD', 'Característica 1', 'CARACTERÍSTICA 1', 'Característica 2', 'CARACTERÍSTICA 2'),

                # Sección 5: EFA
                ('T2', 17, 0, 'EFA'),
                ('L', 18, 0, 'Tipo de EFA'),
                ('CXDEP3', 18, 1, 39, tabla_directorio, "Doble",
                'TIPO_OFICINA', 'Categoría EFA', 'EFA_OSPA', 'EFA', 'Entidad u oficina')
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
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos recibidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_dr, self.tabla_relacion_dr_ep, 
                                                "ID_EP", "ID_DR", "COD_EP", 
                                                self.ver_dr, self.eliminar_dr_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self.frame_principal)
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_2,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos emitidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_de, self.tabla_relacion_de_ep, 
                                                "ID_EP", "ID_DE", "COD_EP", 
                                                self.ver_de, self.eliminar_de_y_actualizar)
        
        # III.5 Frame de vitrina 3
        self.frame_vitrina_3 = Cuadro(self.frame_principal)
        self.vitrina_3 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_3,
                                                '(+) Agregar', self.no_asociar,
                                                'Macroproblemas asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_mp, self.tabla_relacion_mp_ep, 
                                                "ID_EP", "ID_MP", "COD_EP", 
                                                self.ver_mp, self.eliminar_mp_y_actualizar)

    #----------------------------------------------------------------------
    def guardar_y_actualizar_ep(self):
        
        # Agregamos el objeto
        self.guardar_objeto(self.frame_rejilla,
                            self.cod_usuario_ep, "COD_EP", self.tabla_de_ep_cod,
                            b_ep_cod, b_ep, b_ep_hist, self.ver_ep)
        # Actualización de tabla de código y visualización
        self.tabla_de_ep_cod = b_ep_cod.generar_dataframe()

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
                                                'Documentos recibidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_dr, self.tabla_relacion_dr_ep, 
                                                "ID_EP", "ID_DR", "COD_EP", 
                                                self.ver_dr, self.eliminar_dr_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2.eliminar_cuadro()
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_2,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos emitidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_de, self.tabla_relacion_de_ep, 
                                                "ID_EP", "ID_DE", "COD_EP", 
                                                self.ver_de, self.eliminar_de_y_actualizar)
        
        # III.5 Frame de vitrina 3
        self.frame_vitrina_3.eliminar_cuadro()
        self.vitrina_3 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_3,
                                                '(+) Agregar', self.no_asociar,
                                                'Macroproblemas asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_mp, self.tabla_relacion_mp_ep, 
                                                "ID_EP", "ID_MP", "COD_EP", 
                                                self.ver_mp, self.eliminar_mp_y_actualizar)


    #----------------------------------------------------------------------
    def eliminar_dr_y_actualizar(self, id_objeto):
        # Se elimina el DR
        self.eliminar_objeto(self.cod_usuario_ep, "COD_EP", id_objeto, "COD_DR",
                            self.tabla_de_ep_cod, tabla_de_dr_cod, 
                            base_relacion_dr_ep, base_relacion_dr_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    
    #----------------------------------------------------------------------
    def eliminar_de_y_actualizar(self, id_objeto):
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_ep, "COD_EP", id_objeto, "COD_DE",
                            self.tabla_de_ep_cod, tabla_de_de_cod, 
                            base_relacion_de_ep, base_relacion_de_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    #----------------------------------------------------------------------
    def eliminar_mp_y_actualizar(self, id_objeto):
        # Se elimina el DE
        self.eliminar_objeto(self.cod_usuario_ep, "COD_EP", id_objeto, "COD_MP",
                            self.tabla_de_ep_cod, tabla_de_mp_cod, 
                            base_relacion_mp_ep, base_relacion_mp_ep_hist)
        
        # Se actualiza tabla de relaciones
        self.tabla_relacion_mp_ep = base_relacion_mp_ep.generar_dataframe()
        # Se actualiza la vista de vitrinas
        self.actualizar_vitrinas_ep()

    #----------------------------------------------------------------------
    def no_asociar(self):
        messagebox.showerror("Error",
                            'Para asociar un documento, hágalo desde la vista de documentos')