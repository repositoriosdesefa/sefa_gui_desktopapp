from apoyo.elementos_de_GUI import CustomHovertip
import tkinter as tk
from tkinter import Frame, Canvas, Label
import apoyo.formato as formato 
import pandas as pd

class VerticalScrolledFrame:
    """
    From: https://gist.github.com/novel-yet-trivial/3eddfce704db3082e38c84664fc1fdf8
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    :width:, :height:, :bg: are passed to the underlying Canvas
    :bg: and all other keyword arguments are passed to the inner Frame
    note that a widget layed out in this frame will have a self.master 3 layers deep,
    (outer Frame, Canvas, inner Frame) so 
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.
    """
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)

class Vitrina_vista(Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, window, tabla, funcion1, funcion2, height=100, width=1600):
        """Constructor"""

        self.window = window
        self.tabla = tabla
        self.funcion1 = funcion1
        self.funcion2 = funcion2
        #self.funcion3 = funcion3
        self.height = height
        self.width = width
        
        self.main_frame = Frame(self.window)
        self.main_frame.pack()

        # Encabezados (entorno)

        self.frame_base_encabezado = Frame(self.main_frame)
        self.frame_base_encabezado.pack()

        self.canvas_encabezado = Canvas(self.frame_base_encabezado, height=23, width=self.width)
        self.canvas_encabezado.pack(side='left', fill='both', expand=True)

        self.empty_frame = Frame(self.frame_base_encabezado, width=12)
        self.empty_frame.pack(side='right', fill='both', expand=True)

        self.frame_dentro_del_canvas = Frame(self.canvas_encabezado) # Éste es el frame donde colocaremos los encabezados

        self.canvas_encabezado.create_window(4, 4, window=self.frame_dentro_del_canvas, anchor='nw')

        # Cuerpo de la tabla (entorno)

        self.frame_con_scrollbar = VerticalScrolledFrame(self.main_frame, height=self.height, width=self.width)
        self.frame_con_scrollbar.pack()

        # Incluir encabezados de la tabla

        columnas_de_tabla = self.tabla.columns.values.tolist()
        indice_de_columnas = range(len(columnas_de_tabla))
        elementos_columnas = {
            'index': indice_de_columnas,
            'columnas': columnas_de_tabla
            }
        tabla_columna = pd.DataFrame(elementos_columnas)

        for i,row in tabla_columna.iterrows():
            encabezado = Label(
                self.frame_dentro_del_canvas, 
                text=row[1],
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width= 25, 
                height=1, 
                relief='groove',
                bg=formato.fondo_encabezados_de_tabla
                )
            encabezado.grid(row=0, column=row[0])
    
        opciones_label = Label(
            self.frame_dentro_del_canvas,
            text='Opciones',
            font=formato.tipo_de_letra_tabla,
            fg = formato.letras_del_boton,
            width= 16,
            height=1, 
            relief='groove',
            bg=formato.fondo_encabezados_de_tabla
            )
        opciones_label.grid(row=0, column=len(columnas_de_tabla)+1)

        # Incluir elementos en el cuerpo de la tabla

        for i, row in self.tabla.iterrows():
            valores_subframe = Frame(self.frame_con_scrollbar)
            valores_subframe.pack()
            lista_de_valores = row.values
            indice_de_valores = range(len(lista_de_valores))
            elementos_valores = {
                'index': indice_de_valores,
                'valores': lista_de_valores 
            }

            # Valores de tabla
            tabla_valor = pd.DataFrame(elementos_valores)
            for i,row in tabla_valor.iterrows():
                valor = Label(
                    valores_subframe, 
                    text=row[1],
                    font=formato.tipo_de_letra_tabla,
                    width=25, 
                    height = 2,
                    relief='groove',
                    bg= formato.fondo_valores_de_tabla,
                    wraplength=125, 
                    justify="center")
                valor.grid(row=0, column=row[0])

            # Agregar botones
            
            argumento = lista_de_valores[0]

            boton_ver = Label(
                valores_subframe,
                text='Detalle',
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width=7,
                height=2,
                relief='groove',
                cursor="hand2",
                bg=formato.boton_sin_que_pase_cursor
            )
            boton_ver.grid(row=0, column=len(lista_de_valores)+1)
            boton_ver.bind("<Button-1>", lambda e, argumento=argumento:self.funcion1(argumento))
            self.Efecto_de_boton(boton_ver)

            #boton_editar = Label(
            #    valores_subframe,
            #    text='EDIT',
            #    font=formato.tipo_de_letra_tabla,
            #    fg = formato.letras_del_boton,
            #    width=5,
            #    height=1,
            #    relief='groove',
            #    cursor="hand2",
            #    bg=formato.boton_sin_que_pase_cursor
            #)
            #boton_editar.grid(row=0, column=len(lista_de_valores)+2)
            #boton_editar.bind("<Button-1>",lambda e,argumento=argumento:self.funcion2(argumento))
            #self.Efecto_de_boton(boton_editar)

            boton_eliminar = Label(
                valores_subframe,
                text='Eliminar',
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width=7,
                height=2,
                relief='groove',
                cursor="hand2",
                bg=formato.boton_sin_que_pase_cursor
            )
            boton_eliminar.grid(row=0, column=len(lista_de_valores)+2)
            CustomHovertip(boton_eliminar, text = "Pruebaaaaaaaaaaaa aaaaaaaaaaaaaaa aaaaaaaaaaaaaa")
            boton_eliminar.bind("<Button-1>",lambda e,argumento=argumento:self.funcion2(argumento))
            #self.Efecto_de_boton(boton_eliminar)

    #----------------------------------------------------------------------
    def Efecto_de_boton(self, boton):
        """"""

        #----------------------------------------------------------------------
        def Pasar_sobre_boton(e):
            """"""
            boton['bg'] = formato.boton_cuando_pasa_cursor
            boton['fg'] = formato.letras_del_boton_cuando_pasa_cursor

        #----------------------------------------------------------------------
        def Dejar_boton(e):
            """"""
            boton['bg'] = formato.boton_sin_que_pase_cursor
            boton['fg'] = formato.letras_del_boton

        boton.bind('<Enter>', Pasar_sobre_boton)
        boton.bind('<Leave>', Dejar_boton)


class Vitrina_busqueda(Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, window, tabla, funcion1, funcion2, height=100, width=1600):
        """Constructor"""

        self.window = window
        self.tabla = tabla
        self.funcion1 = funcion1
        self.funcion2 = funcion2
        #self.funcion3 = funcion3
        self.height = height
        self.width = width
        
        self.main_frame = Frame(self.window)
        self.main_frame.pack()

        # Encabezados (entorno)

        self.frame_base_encabezado = Frame(self.main_frame)
        self.frame_base_encabezado.pack()

        self.canvas_encabezado = Canvas(self.frame_base_encabezado, height=23, width=self.width)
        self.canvas_encabezado.pack(side='left', fill='both', expand=True)

        self.empty_frame = Frame(self.frame_base_encabezado, width=12)
        self.empty_frame.pack(side='right', fill='both', expand=True)

        self.frame_dentro_del_canvas = Frame(self.canvas_encabezado) # Éste es el frame donde colocaremos los encabezados

        self.canvas_encabezado.create_window(4, 4, window=self.frame_dentro_del_canvas, anchor='nw')

        # Cuerpo de la tabla (entorno)

        self.frame_con_scrollbar = VerticalScrolledFrame(self.main_frame, height=self.height, width=self.width)
        self.frame_con_scrollbar.pack()

        # Incluir encabezados de la tabla

        columnas_de_tabla = self.tabla.columns.values.tolist()
        indice_de_columnas = range(len(columnas_de_tabla))
        elementos_columnas = {
            'index': indice_de_columnas,
            'columnas': columnas_de_tabla
            }
        tabla_columna = pd.DataFrame(elementos_columnas)

        for i,row in tabla_columna.iterrows():
            encabezado = Label(
                self.frame_dentro_del_canvas, 
                text=row[1],
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width= 21,#se modifico 
                height=1, 
                relief='groove',
                bg=formato.fondo_encabezados_de_tabla
                )
            encabezado.grid(row=0, column=row[0])
    
        opciones_label = Label(
            self.frame_dentro_del_canvas,
            text='Opciones',
            font=formato.tipo_de_letra_tabla,
            fg = formato.letras_del_boton,
            width= 16, #se modifico 
            height=1, 
            relief='groove',
            bg=formato.fondo_encabezados_de_tabla
            )
        opciones_label.grid(row=0, column=len(columnas_de_tabla)+1)

        # Incluir elementos en el cuerpo de la tabla

        for i, row in self.tabla.iterrows():
            valores_subframe = Frame(self.frame_con_scrollbar)
            valores_subframe.pack()
            lista_de_valores = row.values
            indice_de_valores = range(len(lista_de_valores))
            elementos_valores = {
                'index': indice_de_valores,
                'valores': lista_de_valores 
            }

            tabla_valor = pd.DataFrame(elementos_valores)
            for i,row in tabla_valor.iterrows():
                valor = Label(
                    valores_subframe, 
                    text=row[1],
                    font=formato.tipo_de_letra_tabla,
                    width=21,
                    height=3,#se modifico  
                    relief='groove',
                    bg= formato.fondo_valores_de_tabla,
                    wraplength=125, 
                    justify="center")
                valor.grid(row=0, column=row[0])

            # Agregar botones
            
            argumento = lista_de_valores[0]

            boton_ver = Label(
                valores_subframe,
                text='VER',
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width=7,
                height=3,
                relief='groove',
                cursor="hand2",
                bg=formato.boton_sin_que_pase_cursor
            )
            boton_ver.grid(row=0, column=len(lista_de_valores)+1)
            boton_ver.bind("<Button-1>",lambda e,argumento=argumento:self.funcion1(argumento))
            self.Efecto_de_boton(boton_ver)

            #boton_editar = Label(
            #    valores_subframe,
            #    text='EDIT',
            #    font=formato.tipo_de_letra_tabla,
            #    fg = formato.letras_del_boton,
            #    width=5,
            #    height=1,
            #    relief='groove',
            #    cursor="hand2",
            #    bg=formato.boton_sin_que_pase_cursor
            #)
            #boton_editar.grid(row=0, column=len(lista_de_valores)+2)
            #boton_editar.bind("<Button-1>",lambda e,argumento=argumento:self.funcion2(argumento))
            #self.Efecto_de_boton(boton_editar)

            boton_eliminar = Label(
                valores_subframe,
                text='ASOCIAR',
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width=8,
                height=3,
                relief='groove',
                cursor="hand2",
                bg=formato.boton_sin_que_pase_cursor
            )
            boton_eliminar.grid(row=0, column=len(lista_de_valores)+2)
            boton_eliminar.bind("<Button-1>",lambda e,argumento=argumento:self.funcion2(argumento))
            self.Efecto_de_boton(boton_eliminar)

    #----------------------------------------------------------------------
    def Efecto_de_boton(self, boton):
        """"""

        #----------------------------------------------------------------------
        def Pasar_sobre_boton(e):
            """"""
            boton['bg'] = formato.boton_cuando_pasa_cursor
            boton['fg'] = formato.letras_del_boton_cuando_pasa_cursor

        #----------------------------------------------------------------------
        def Dejar_boton(e):
            """"""
            boton['bg'] = formato.boton_sin_que_pase_cursor
            boton['fg'] = formato.letras_del_boton

        boton.bind('<Enter>', Pasar_sobre_boton)
        boton.bind('<Leave>', Dejar_boton)

    #----------------------------------------------------------------------
    def Eliminar_vitrina(self):
        """"""
        self.main_frame.destroy()

