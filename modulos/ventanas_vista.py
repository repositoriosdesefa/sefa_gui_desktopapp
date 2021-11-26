import datetime as dt

from tkinter import *
from tkinter import messagebox
from tkinter.constants import TRUE

from modulos import ventanas_busqueda, variables_globales
from modulos.funcionalidades_ospa import funcionalidades_ospa
from apoyo.elementos_de_GUI import Cuadro, Ventana

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

base_relacion_docs = variables_globales.base_relacion_docs
base_relacion_dr_ep = variables_globales.base_relacion_dr_ep
base_relacion_de_ep = variables_globales.base_relacion_de_ep

base_relacion_docs_hist = variables_globales.base_relacion_docs_hist
base_relacion_dr_ep_hist = variables_globales.base_relacion_dr_ep_hist
base_relacion_de_ep_hist = variables_globales.base_relacion_de_ep_hist

# 2. Tablas
tabla_directorio = variables_globales.tabla_directorio
tabla_lista_efa = variables_globales.tabla_lista_efa

# 3. Listas dependientes
# 21. Lista de EFA
lista_efa_dependiente = variables_globales.lista_efa_dependiente
lista_efa_ospa = sorted(list(lista_efa_dependiente['EFA_OSPA'].unique()))
# 3.2 Ubigeo
tabla_departamento_efa = variables_globales.tabla_departamento_efa
departamento_ospa = variables_globales.departamento_ospa

# 4. Parámetros
# 4.1 Bases de datos
tabla_parametros = variables_globales.tabla_parametros
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
estado_problemas = ('ABIERTA', 'CERRADO')
tipo_causa = ('CAUSA DESCONOCIDA', 'CAUSA NATURAL', 'CAUSA HUMANA')
tipo_ingreso = ('DIRECTO', 'DERIVACION-SUBDIRECCION', 
                'DERIVACION-SUPERVISION', 'DERIVACION-SINADA')
tipo_documento = ('OFICIO', 'MEMORANDO', 'CARTA', 'OFICIO CIRCULAR','MEMORANDO CIRCULAR', 'CARTA CIRCULAR',
                  'INFORME', 'RESOLUCIÓN', 'CÉDULA DE NOTIFICACIÓN', 'INFORME MÚLTIPLE', 'OTROS')
especialista = ('Zurita, Carolina', 'López, José')
tipo_indicacion = ('No corresponde', 'Archivar', 'Actualizar', 'Crear')
si_no = ('Si', 'No')
tipo_respuesta = ('Ejecutó supervisión','Solicitó información a administrado',
                  'Ejecutó acción de evaluación', 'Inició PAS', 'Administrado en adecuación / formalización',
                  'Programó supervisión', 'Programó acción de evaluación', 'No es competente',
                  'No corresponde lo solicitado', 'En evaluación de la EFA', 'Otros')
categorias = ('Pedido de información', 'Pedido de información adicional', 'Pedido de información urgente',
              'Reiterativo', 'Oficio a OCI')
marco_pedido = ('EFA', 'OEFA',
                'Colaboración', 'Delegación', 'Conocimiento')

# 5. Tablas resumen
# 5.0 Relaciones
tabla_relacion_dr_de = variables_globales.tabla_relacion_dr_de
tabla_relacion_dr_ep = variables_globales.tabla_relacion_dr_ep
tabla_relacion_de_ep = variables_globales.tabla_relacion_de_ep
# 5.1 Documentos recibidos
tabla_de_dr_cod = variables_globales.tabla_de_dr_cod
tabla_de_dr_completa = variables_globales.tabla_de_dr_completa
tabla_de_dr_resumen = variables_globales.tabla_de_dr_resumen
# 5.2 Documentos emitidos
tabla_de_de_cod = variables_globales.tabla_de_de_cod
tabla_de_de_completa = variables_globales.tabla_de_de_completa
tabla_de_de_resumen = variables_globales.tabla_de_de_resumen
# 5.3 Extremos de problema
tabla_de_ep_cod = variables_globales.tabla_de_ep_completa
tabla_de_ep_completa = variables_globales.tabla_de_ep_completa
tabla_de_ep_resumen = variables_globales.tabla_de_ep_resumen
    
class Doc_recibidos_vista(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None):
        """Constructor"""

        Ventana.__init__(self, *args)
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.id_objeto_ingresado = id_objeto
        self.cod_usuario_dr = id_objeto
        # Parámetros de vitrina
        self.vitrina_1 = None
        self.vitina_2 = None

        # I. Labels, entries y rejilla
        # I.1 Rejilla de documento recibido
        rejilla_dr = [
            ('L', 0, 0, 'Tipo de documento'),
            ('CX', 0, 1, tipo_documento),

            ('L', 0, 2, 'N° de documento'),
            ('E', 0, 3),

            ('L', 1, 0, 'Fecha de recepción OEFA'),
            ('D', 1, 1),

            ('L', 1, 2, 'Fecha de recepción SEFA'),
            ('D', 1, 3),

            ('L', 2, 0, 'Vía de recepción'),
            ('CX', 2, 1, tipo_ingreso),

            ('L', 2, 2, 'HT de documento'),
            ('E', 2, 3),

            ('L', 3, 0, 'Asunto'),
            ('EL', 3, 1, 112, 3),

            ('L', 4, 0, 'Categoria Remitente'),
            ('CXD1', 4, 1, lista_efa_ospa, 39, lista_efa_dependiente, 'EFA_OSPA', 'Entidad u oficina', 17, 8),

            ('L', 4, 2, 'Remitente'),
            ('CXR', 4, 3, combo_vacio, 17, 8),

            ('L', 5, 0, '¿Es respuesta?'),
            ('CX', 5, 1, si_no),

            ('L', 5, 2, 'Respuesta'),
            ('CX', 5, 3, tipo_respuesta),

            ('L', 6, 0, 'Indicación'),
            ('CX', 6, 1, tipo_indicacion),

            ('L', 6, 2, 'Especialista asignado'),
            ('CX', 6, 3, especialista),

            ('L', 7, 0, 'Aporte del documento'),
            ('ST', 7, 1)
            
        ]

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
        titulos = Cuadro(self)
        titulos.agregar_encabezado('Detalle de documento recibido')
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_dr)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada
            self.tabla_de_dr_cod = b_dr_cod.generar_dataframe()
            self.tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
            self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
            self.cod_usuario_dr = id_objeto
            self.lista_para_insertar = lista
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_dr)
        f_boton.agregar_button(0, 2, 'Volver', self.volver)
        f_boton.agregar_button(0, 3, 'Inicio', self.inicio_app)

        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_1,
                                            '(+) Agregar', self.busqueda_de,
                                            'Documentos emitidos asociados', 
                                            self.cod_usuario_dr, self.tabla_de_dr_cod, 
                                            self.tabla_de_de, self.tabla_relacion_dr_de, 
                                            "ID_DR", "ID_DE", "COD_DR", 
                                            self.ver_de, self.eliminar_de_y_actualizar)

        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_2,
                                            '(+) Agregar', self.busqueda_ep,
                                            'Extremo de problemas asociados',
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
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None):
        """Constructor"""

        Ventana.__init__(self, *args)

        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.cod_usuario_de = id_objeto
        self.id_objeto_ingresado = id_objeto
        # Parámetros de vitrina
        self.vitrina_1 = None
        self.vitina_2 = None

        # I. Labels and Entries
        rejilla_de = [
            ('L', 0, 0, 'HT de documento'),
            ('E', 0, 1),

            ('L', 0, 2, 'Categoría'),
            ('CX', 0, 3, categorias),

            ('L', 1, 0, 'Categoria Destinatario'),
            ('CXD1', 1, 1, lista_efa_ospa, 39, lista_efa_dependiente, 'EFA_OSPA', 'Entidad u oficina', 7, 3),
            
            ('L', 1, 2, 'Remitente'),
            ('CXR', 1 , 3, combo_vacio, 7, 3),

            ('L', 2, 0, 'Tipo de documento'),
            ('CX', 2, 1, tipo_documento),

            ('L', 2, 2, 'N° de documento'),
            ('E', 2, 3),

            ('L', 3, 0, 'Detalle de requerimiento'),
            ('ST', 3, 1),

            ('L', 4, 0, 'Marco de pedido'),
            ('CX', 4, 1, marco_pedido),

            ('L', 4, 2, 'Fecha de proyecto'),
            ('E', 4, 3), 

            ('L', 5, 0, 'Fecha de firma'),
            ('E', 5, 1), 

            ('L', 5, 2, 'Fecha de notificación'),
            ('E', 5, 3) 

        ]

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
        titulos = Cuadro(self)
        titulos.agregar_encabezado('Detalle del Documento Emitido')
        
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_de)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada
            self.tabla_de_de_cod = b_de_cod.generar_dataframe()
            self.tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
            self.tabla_relacion_de_ep = base_relacion_de_ep.generar_dataframe()
            self.cod_usuario_de = id_objeto
            self.lista_para_insertar = lista
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_de)
        f_boton.agregar_button(0, 2, 'Volver', self.volver)
        f_boton.agregar_button(0, 3, 'Inicio', self.inicio_app)

        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                            self.frame_vitrina_1,
                                            '(+) Agregar', self.busqueda_dr,
                                            'Documentos recibidos asociados',
                                            self.cod_usuario_de, self.tabla_de_de_cod, 
                                            self.tabla_de_dr, self.tabla_relacion_dr_de, 
                                            "ID_DE", "ID_DR", "COD_DE", 
                                            self.ver_de, self.eliminar_dr_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
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
    def __init__(self, *args, nuevo=True, lista=None, id_objeto = None):
        """Constructor"""

        Ventana.__init__(self, *args)
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        self.cod_usuario_ep = id_objeto
        self.id_objeto_ingresado = id_objeto
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

        # III. Títulos e imagen
        # III.1 Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_encabezado('Detalle de extremo de problema')
        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo == False: # Estamos en una ficha creada
            self.tabla_de_dr_cod = b_dr_cod.generar_dataframe()
            self.tabla_relacion_dr_de = base_relacion_docs.generar_dataframe()
            self.tabla_relacion_dr_ep = base_relacion_dr_ep.generar_dataframe()
            self.cod_usuario_dr = id_objeto
            self.lista_para_insertar = lista
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)
            rejilla_ep = [
                ('L', 0, 0, 'Código de problema'),
                ('L', 0, 1, str(self.cod_usuario_ep)),

                ('L', 0, 1, 'Componente ambiental'),
                ('CXP', 0, 2, 27, componente_amb, '', "readonly"),
                
                ('L', 0, 3, 'Tipo de afectación'),
                ('CXP', 0, 4, 27, tipo_afectacion, '', "readonly"),

                ('L', 1, 0, 'Departamento'),
                ('CXD1', 1, 1, departamento_ospa, 27, tabla_departamento_efa, 'DEP_OSPA', 'PROV_DIST_OSPA', 7, 'CXD1'),

                ('L', 0, 4, 'Ocurrencia'),
                ('CXP', 0, 5, 27, ocurrencia, '', "readonly"),

                ('L', 1, 2, 'Provincia/Distrito'),
                ('CXR', 1, 3, combo_vacio),

                ('L', 1, 4, 'Descripción'),
                ('STP', 1, 5, 28, 2),

                ('L', 2, 2, 'Tipo de ubicación'),
                ('CXP', 2, 3, 27, ubicacion, '', "readonly"),

                ('L', 3, 0, 'Agente contaminante'),
                ('CXP', 3, 1, 27, agente_conta, '', "readonly"),

                ('L', 3, 2, 'Extensión'),
                ('CXP', 3, 3, 27, extension, '', "readonly"),

                ('L', 3, 4, 'EFA'),
                ('CXP', 3, 5, 27, lista_efa_ospa, '', "readonly"),

                ('L', 4, 0, 'Actividad'),
                ('CXP', 4, 1, 27, actividad_eco, '', "readonly"),

                ('L', 4, 2, 'Tipo de causa'),
                ('CXP', 4, 3, 27, tipo_causa, '', "readonly"),
            
                ('L', 4, 4, 'Estado'),
                ('CXP', 4, 5, 27, estado_problemas, '', "readonly"),

                ('L', 5, 0, 'Característica 1'),
                ('EL', 5, 1, 30, 1),

                ('L', 5, 2, 'Característica 2'),
                ('EL', 5, 3, 30, 1),

                ('L', 5, 4, 'Código SINADA'),
                ('EL', 5, 5, 30, 1)

            ]
            # Se inserta rejilla con datos
            self.frame_rejilla.agregar_rejilla(rejilla_ep)
        else:
            rejilla_ep_nuevo = [
                ('L', 0, 0, ' '),
                ('L', 0, 1, ' '),
                
                ('L', 0, 2, 'Componente ambiental'),
                ('CXP', 0, 3, 27, componente_amb, '', "readonly"),

                ('L', 0, 4, 'Tipo de afectación'),
                ('CXP', 0, 5, 27, tipo_afectacion, '', "readonly"),

                ('L', 1, 0, 'Categoria EFA'),
                ('CXD1', 1, 1, lista_efa_ospa, 24, lista_efa_dependiente, 'EFA_OSPA', 'Entidad u oficina', 9, 4),
            
                ('L', 1, 2, 'EFA'),
                ('CXR', 1 , 3, combo_vacio, 9, 4),

                ('L', 1, 4, 'Descripción'),
                ('STP', 1, 5, 28, 2),

                ('L', 2, 0, 'Departamento'),
                ('CXD1', 2, 1, departamento_ospa, 24, tabla_departamento_efa, 'DEP_OSPA', 'PROV_DIST_OSPA', 15, 7),

                ('L', 2, 2, 'Provincia/Distrito'),
                ('CXR', 2, 3, combo_vacio, 15, 7),

                #('L', 2, 2, 'Tipo de ubicación'),
                #('CXP', 2, 3, 27, ubicacion, '', "readonly"),

                ('L', 3, 0, 'Agente contaminante'),
                ('CXP', 3, 1, 27, agente_conta, '', "readonly"),

                ('L', 3, 2, 'Extensión'),
                ('CXP', 3, 3, 27, extension, '', "readonly"),

                ('L', 3, 4, 'Ocurrencia'),
                ('CXP', 3, 5, 27, ocurrencia, '', "readonly"),

                ('L', 4, 0, 'Actividad'),
                ('CXP', 4, 1, 27, actividad_eco, '', "readonly"),

                ('L', 4, 2, 'Tipo de causa'),
                ('CXP', 4, 3, 27, tipo_causa, '', "readonly"),
            
                ('L', 4, 4, 'Estado'),
                ('CXP', 4, 5, 27, estado_problemas, 30, 1),

                ('L', 5, 0, 'Característica 1'),
                ('EL', 5, 1, 30, 1),

                ('L', 5, 2, 'Característica 2'),
                ('EL', 5, 3, 30, 1),

                ('L', 5, 4, 'Código SINADA'),
                ('EL', 5, 5, 30, 1)

                #('L', 6, 2, '¿Es prioridad?'),
                #('CXP', 6, 3, 27, si_no, ' ', "readonly")

                #('L', 6, 4, 'Puntaje'),
                #('EL', 6, 5, 30, 1)

            ]
            # Se inserta rejilla nueva
            self.frame_rejilla.agregar_rejilla(rejilla_ep_nuevo)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.guardar_y_actualizar_ep)
        f_boton.agregar_button(0, 2, 'Volver', self.volver)
        f_boton.agregar_button(0, 3, 'Inicio', self.inicio_app)
        
        # III.4 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        self.vitrina_1 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_1,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos recibidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_dr, self.tabla_relacion_dr_ep, 
                                                "ID_EP", "ID_DR", "COD_EP", 
                                                self.ver_dr, self.eliminar_dr_y_actualizar)
        
        # III.5 Frame de vitrina 2
        self.frame_vitrina_2 = Cuadro(self)
        self.vitrina_2 = self.generar_vitrina(self.nuevo, 
                                                self.frame_vitrina_2,
                                                '(+) Agregar', self.no_asociar,
                                                'Documentos emitidos asociados',
                                                self.cod_usuario_ep, self.tabla_de_ep_cod, 
                                                self.tabla_de_de, self.tabla_relacion_de_ep, 
                                                "ID_EP", "ID_DE", "COD_EP", 
                                                self.ver_de, self.eliminar_de_y_actualizar)

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
    def no_asociar(self):
        messagebox.showerror("Error",
                            'Para asociar un documento, hágalo desde la vista de documentos')


    
class Macroproblemas_vista(funcionalidades_ospa):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, *args, nuevo=True, lista=None, id_mp = None):
        """Constructor"""

        Ventana.__init__(self, *args)
        
        # 0. Almacenamos información heredada
        self.nuevo = nuevo
        if self.nuevo != True: # En caso exista
            self.lista_para_insertar = lista
            self.cod_usuario_mp = id_mp

        # I. Labels and Entries
        rejilla_mp = [
            ('L', 0, 0, 'Nombre del problema'),
            ('ST', 0, 1),

            ('L', 1, 0, 'Descripción'),
            ('ST', 1, 1),

            ('L', 2, 0, 'Observaciones'),
            ('ST', 2, 1),

            ('L', 3, 0, 'Estado'),
            ('E', 3, 1)
        ]

        # II. Tablas en ventana
        # II.1 Lista de DE
        tabla_de_ep_completa = b_ep.generar_dataframe()
        tabla_de_ep_id = tabla_de_ep_completa
        self.tabla_de_ep = tabla_de_ep_id.drop(['OCURRENCIA', 'EXTENSION', 'TIPO DE AFECTACION',
                                                'PROVINCIA', 'DESCRIPCION', 'TIPO DE UBICACION',
                                                'CARACTERISTICA 1', 'CARACTERISTICA 2', 'TIPO CAUSA',
                                                'CODIGO SINADA', 'ACTIVIDAD', 'FECHA_ULTIMO_MOV'], axis=1)
        
        # III. Ubicaciones
        # III.1 Frame de Título
        titulos = Cuadro(self)
        titulos.agregar_imagen(0,0,'Logo_OSPA.png',202,49)
        titulos.agregar_titulo(0,1,'                             ')
        titulos.agregar_titulo(0,2,'Detalle del macroproblema')
        titulos.agregar_titulo(0,3,'                             ')
        titulos.agregar_titulo(0,4,'                             ')

        # III.2 Frame de rejillas
        self.frame_rejilla = Cuadro(self)
        self.frame_rejilla.agregar_rejilla(rejilla_mp)
        # En caso exista precedente, se inserta en la rejilla
        if self.nuevo != True:
            self.frame_rejilla.insertar_lista_de_datos(self.lista_para_insertar)

        # III.3 Frame de botón de rejilla
        f_boton = Cuadro(self)
        f_boton.agregar_button(0, 1, 'Guardar', self.enviar_mp)
        f_boton.agregar_button(0, 2, 'Inicio', self.inicio_app) # Botón provisional
        
        # III.4 Frame de botón y títulos de vitrina 1
        self.boton_vitrina_1 = Cuadro(self)
        self.boton_vitrina_1.agregar_button(0, 0,'(+) Agregar', self.busqueda_de)
        self.boton_vitrina_1.agregar_titulo(0, 1,'                                                       ')
        self.boton_vitrina_1.agregar_titulo(0, 2, 'Extremo de problemas asociados')
        self.boton_vitrina_1.agregar_titulo(0, 3,'                              ')
        self.boton_vitrina_1.agregar_titulo(0, 4,'                              ')

        # III.5 Frame de vitrina 1
        self.frame_vitrina_1 = Cuadro(self)
        if self.nuevo != True:
            self.generar_vitrina(self.frame_vitrina_1,
                                 b_dr_cod, self.tabla_de_ep, base_relacion_dr_ep, 
                                 "ID_DR", "ID_EP", self.ver_ep, self.eliminar_ep)
        else:
            self.frame_vitrina_1.agregar_label(1, 2,'                  0 extremos de problemas asociados') 

    #----------------------------------------------------------------------
    def enviar_mp(self, x):
        """"""
        print("Guardar macroproblemas")
    

    #----------------------------------------------------------------------
    def eliminar_ep(self, x):
        """"""
        print("Eliminar extremo de problema asociado")