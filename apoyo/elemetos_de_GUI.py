from tkinter import *
from tkinter import scrolledtext as sc
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import datetime
import apoyo.formato as formato 
import pandas as pd
from PIL import Image, ImageTk

class Ventana(Toplevel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, ventana_anterior, alto = 300, ancho = 520, titulo = "Aplicativo de Sefa"):
        """Constructor especial de la clase Ventana.\n
        Sirve para generar nuevas ventanas en una desktop app"""

        self.ventana_anterior = ventana_anterior
        Toplevel.__init__(self)
        self.alto = alto
        self.ancho = ancho
        self.titulo = titulo 
        self.box_sw = self.winfo_screenwidth()
        self.box_sh = self.winfo_screenheight()
        self.box_x = (self.box_sw - self.ancho)/2
        self.box_y = (self.box_sh - self.alto)/2
        self.geometry('%dx%d+%d+%d' % (self.ancho, self.alto, self.box_x, self.box_y))
        self.menu = MenuSefa(self)
        self.iconbitmap('images/S_de_Sefa.ico')
        self.title(self.titulo)
        self.config(background= formato.fondo)

    #----------------------------------------------------------------------
    def desaparecer(self):
        """"""
        self.withdraw()
        
    #----------------------------------------------------------------------
    def aparecer(self):
        """"""
        self.update()
        self.deiconify()

    #----------------------------------------------------------------------
    def volver(self):
        """"""
        self.desaparecer()
        self.ventana_anterior.aparecer()

class Cuadro(Frame):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, window, scrollable=FALSE):
        """Constructor especial de la clase Cuadro.\n
        Permite generar objetos Frame con opción de agregar scrollbar. 
        Posee métodos que permiten incorporar otros wingets de Tkinter."""

        Frame.__init__(self)
        self.scrollable = scrollable
        
        if self.scrollable:
            self.main_frame = Frame(window)
            self.main_frame.pack(side="top", fill="both", expand=True)
            self.scrollframe = ScrollFrame(self.main_frame, height=50, width=50)
            self.scrollframe.pack(side="top", fill=None, expand=False)
            # Frame que contiene objetos:
            self.z = Frame(self.scrollframe.viewPort)
            self.z.pack(side="top", fill="both", expand=True)

        else:
            # Frame que contiene objetos:
            self.z = Frame(window)
            self.z.pack()

        self.lista_de_objetos = []
        self.lista_de_datos = []

    #----------------------------------------------------------------------
    
    def agregar_titulo(self, y, x, texto):
        """Método de la clase Cuadro. \n
        Permite agregar un título centrado al Frame creado con la Clase Cuadro."""
    
        self.y= y
        self.x= x
        self.texto= texto
        self.etiqueta = Label(
            self.z, 
            text= self.texto,
            font= formato.tipo_de_letra_titulo,
            )
        self.etiqueta.grid(row= self.y, column=self.x, sticky='news', pady=8, padx=8)
        self.lista_de_objetos.append((self.etiqueta))

    #----------------------------------------------------------------------
    def agregar_label(self, y, x, texto):
        """Método de la clase Cuadro. \n
        Permite agregar texto al Frame creado con la Clase Cuadro."""

        self.y= y
        self.x= x
        self.texto= texto
        self.etiqueta = Label(
            self.z, 
            text= self.texto,
            font= formato.tipo_de_letra,
            anchor="w"
            )
        self.etiqueta.grid(row= self.y, column=self.x, sticky='news', pady=4, padx=8)
        self.lista_de_objetos.append((self.etiqueta))
    
    #----------------------------------------------------------------------
    def agregar_button(self, y, x, texto, funcion):
        """Método de la clase Cuadro. \n
        Permite agregar un botón al Frame creado con la Clase Cuadro."""

        #----------------------------------------------------------------------
        def Efecto_de_boton(boton):
            """"""

            #----------------------------------------------------------------------
            def Pasar_sobre_boton(e):
                """"""
                boton['bg'] = formato.boton_cuando_pasa_cursor
        
            #----------------------------------------------------------------------
            def Dejar_boton(e):
                """"""
                boton['bg'] = formato.boton_sin_que_pase_cursor
        
            boton.bind('<Enter>', Pasar_sobre_boton)
            boton.bind('<Leave>', Dejar_boton)

        self.y= y
        self.x= x
        self.texto = texto
        self.funcion = funcion
        self.boton = Button(
                        self.z, 
                        text= self.texto, 
                        command=self.funcion,
                        font= formato.tipo_de_letra,
                        fg = formato.letras_del_boton,
                        bg = formato.boton_sin_que_pase_cursor,
                        relief="flat",
                        cursor="hand2",
                        width = 10
                        )
        self.boton.grid(row= self.y, column=self.x, pady=4, padx=8)
        Efecto_de_boton(self.boton)
        self.lista_de_objetos.append((self.boton))

    #----------------------------------------------------------------------
    def agregar_imagen(self, y, x, archivo, largo, alto):
        """Método de la clase Cuadro. \n
        Permite agregar una imagen al Frame creado con la Clase Cuadro."""
        
        self.y = y
        self.x = x
        self.archivo = archivo
        self.largo = largo
        self.alto = alto
        self.ubicacion = str('images/' + self.archivo)
        self.imagen_cargada = Image.open(self.ubicacion)
        self.imagen_cargada = self.imagen_cargada.resize((self.largo, self.alto), Image.ANTIALIAS)
        self.imagen = ImageTk.PhotoImage(self.imagen_cargada)
        self.imagen_label = Label(self.z, image=self.imagen)
        self.imagen_label.grid(row = self.y, column = self.x, pady=4, padx=8)
        self.lista_de_objetos.append((self.imagen_label))

    #----------------------------------------------------------------------
    def agregar_entry(self, y, x):
        """Método de la clase Cuadro. \n
        Permite agregar una entrada de texto al Frame creado con la Clase Cuadro."""

        self.y= y
        self.x= x
        self.data = StringVar()
        self.entrada = Entry(self.z, textvariable=self.data, width= 42)
        self.entrada.grid(row= self.y, column=self.x, pady=4, padx=8)
        self.lista_de_objetos.append((self.entrada))
        self.lista_de_datos.append((self.data))

    #----------------------------------------------------------------------
    def agregar_entry_password(self, y, x):
        """Método de la clase Cuadro. \n
        Permite agregar una entrada de texto al Frame creado con la Clase Cuadro."""

        self.y= y
        self.x= x
        self.data = StringVar()
        self.entrada = Entry(self.z, textvariable=self.data, width= 43, show='*')
        self.entrada.grid(row= self.y, column=self.x, pady=4, padx=8)
        self.lista_de_objetos.append((self.entrada))
        self.lista_de_datos.append((self.data))

    #----------------------------------------------------------------------
    def agregar_scrolltext(self, y, x):
        """Método de la clase Cuadro. \n
        Permite agregar una entrada de texto largo que posee su propio scrollbar al Frame creado con la Clase Cuadro."""

        self.y= y
        self.x= x
        self.text_area = sc.ScrolledText(self.z, 
                            wrap = WORD, 
                            width = 40, 
                            height = 5, 
                            font = ("Times New Roman",
                            11))
        self.text_area.grid(row = self.y, column = self.x, pady=4, padx=8)
        self.lista_de_objetos.append((self.text_area))
        self.lista_de_datos.append((self.text_area))

    #----------------------------------------------------------------------
    def agregar_radiobutton(self, y, x, lista):
        """Método de la clase Cuadro. \n
        Permite agregar una lista del tipo "opción múltiple" al Frame creado con la Clase Cuadro."""
        
        self.y = y
        self.x = x
        self.data = IntVar()
        self.lista = lista
        self.range_y = range(self.y, self.y + len(self.lista))
        self.tabla_lista_y_range_y = pd.DataFrame(self.lista, self.range_y)

        for i, j in zip(self.lista, self.range_y):
            self.radiobutton = Radiobutton(self.z, text= i, variable= self.data, 
            value=j+1)
            self.radiobutton.grid(row = j, column = self.x)
            self.lista_de_objetos.append((self.radiobutton))
        self.lista_de_datos.append((self.data))

    #----------------------------------------------------------------------
    def agregar_checkbutton(self, y, x, texto):
        """Método de la clase Cuadro. \n
        Permite agregar una casilla de confirmación al Frame creado con la Clase Cuadro."""

        self.y = y
        self.x = x
        self.texto = texto
        self.data = IntVar()
        self.checkbuttom = Checkbutton(self.z, text=self.texto, variable=self.data, 
            onvalue=1, offvalue=0)
        self.checkbuttom.grid(row = self.y, column = self.x)
        self.lista_de_objetos.append((self.checkbuttom))
        self.lista_de_datos.append((self.data))

    #----------------------------------------------------------------------
    def agregar_combobox(self, y, x, listadesplegable):
        """Método de la clase Cuadro. \n
        Permite agregar una lista desplegable al Frame creado con la Clase Cuadro."""
        
        self.y = y
        self.x = x
        self.listadesplegable = listadesplegable
        self.combo = ttk.Combobox(self.z, state="normal", width=39)
        self.combo.grid(row = self.y, column = self.x, pady=4, padx=8)
        self.combo["values"] = self.listadesplegable
        self.combo.set('')
        self.lista_de_objetos.append((self.combo))
        self.lista_de_datos.append((self.combo))

    #----------------------------------------------------------------------
    def agregar_spinbox(self, y, x, inicio, fin, incremento, defecto):
        """Método de la clase Cuadro. \n
        Permite agregar un winget con botones para incrementar o dismunir una cantidad al Frame creado con la Clase Cuadro."""

        self.y = y
        self.x = x
        self.inicio = inicio
        self.fin = fin
        self.incremento = incremento
        self.defecto = defecto
        self.spin_box = ttk.Spinbox(self.z, from_= self.inicio, to=self.fin, increment=self.incremento, format="%.0f")
        self.spin_box.insert(0, self.defecto)
        self.spin_box["state"] = "readonly"
        self.spin_box.grid(row=self.y, column=self.x, pady=4, padx=8)
        self.lista_de_objetos.append((self.spin_box))
        self.lista_de_datos.append((self.spin_box))

    #----------------------------------------------------------------------
    def agregar_dateentry(self, y, x):
        """Método de la clase Cuadro. \n
        Permite agregar una entrada de calendario al Frame creado con la Clase Cuadro."""

        # Recordar que es importante utilizar: pyinstaller --hidden-import babel.numbers myscript.py
        # Ver: https://tkcalendar.readthedocs.io/en/stable/howtos.html 
        
        self.y = y
        self.x = x

        # No es necesario crear un StringVar()
        self.cal = DateEntry(self.z, width=39, background='darkblue',
                            foreground='white', borderwidth=1)
        
        self.cal.grid(row = self.y, column = self.x, pady=4, padx=8)
        #self.cal.set_date()
        self.cal["state"] = "normal"
        self.lista_de_objetos.append((self.cal))
        self.lista_de_datos.append((self.cal))

    #----------------------------------------------------------------------
    def agregar_rejilla(self, rejilla):
        """Método de la clase Cuadro. \n
        Permite utilizar una tupla de tuplas para incorporar diversos wingets al Frame creado con la Clase Cuadro."""

        self.rejilla = rejilla

        self.tabla = pd.DataFrame(list(self.rejilla))

        for i,row in self.tabla.iterrows():
            
            if row[0] == 'L':

                self.agregar_label(row[1], row[2], row[3])

            elif row[0] == 'I':
                
                # En este caso row[3] debe ser un archivo de imagen (p.e. png)
                self.agregar_imagen(row[1], row[2], row[3], row[4], row[5])

            elif row[0] == 'B':

                self.agregar_button(row[1], row[2], row[3], row[4])

            elif row[0] == 'E':

                self.agregar_entry(row[1], row[2])

            elif row[0] == 'EP':

                self.agregar_entry_password(row[1], row[2])

            elif row[0] == 'ST':

                self.agregar_scrolltext(row[1], row[2])
            
            elif row[0] == 'R':
                
                # En este caso row[3] debe ser una lista:
                self.agregar_radiobutton(row[1], row[2], row[3])
            
            elif row[0] == 'CB':

                self.agregar_checkbutton(row[1], row[2], row[3])
            
            elif row[0] == 'CX':
                
                # En este caso row[3] debe ser una lista:
                self.agregar_combobox(row[1], row[2], row[3])
            
            elif row[0] == "SB":

                self.agregar_spinbox(row[1], row[2], row[3], row[4], row[5], row[6])

            elif row[0] == 'D':

                self.agregar_dateentry(row[1], row[2])

            else:

                print('Error, el valor de i[0] es {row[0]}')

    #----------------------------------------------------------------------
    def agregar_escenario(self, row, column, data_frame, funcion1, funcion2):
        """Método de la clase Cuadro. \n
        Permite..."""

        #----------------------------------------------------------------------
        def Efecto_de_boton(boton):
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

        self.row = row
        self.column = column
        self.tabla = data_frame
        self.funcion1 = funcion1
        self.funcion2 = funcion2
        #self.funcion3 = funcion3

        escenario_frame = Frame(self.z)
        escenario_frame.grid(row=self.row, column=self.column)

        # Construir encabezados:

        columnas_de_tabla = self.tabla.columns.values.tolist()
        indice_de_columnas = range(len(columnas_de_tabla))
        elementos_columnas = {
            'index': indice_de_columnas,
            'columnas': columnas_de_tabla
            }
        tabla_columna = pd.DataFrame(elementos_columnas)
        
        encabezados_frame = Frame(escenario_frame)
        encabezados_frame.pack()
        for i,row in tabla_columna.iterrows():
            encabezado = Label(
                encabezados_frame, 
                text=row[1],
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width= 25, 
                height=1, 
                relief=GROOVE,
                bg=formato.fondo_encabezados_de_tabla
                )
            encabezado.grid(row=0, column=row[0])
        opciones_label = Label(
            encabezados_frame,
            text='Opciones',
            font=formato.tipo_de_letra_tabla,
            fg = formato.letras_del_boton,
            width= 14, 
            height=1, 
            relief=GROOVE,
            bg=formato.fondo_encabezados_de_tabla
            )
        opciones_label.grid(row=0, column=len(columnas_de_tabla)+1)
        
        # Construir tabla

        valores_frame = Frame(escenario_frame)
        valores_frame.pack()
        for i, row in self.tabla.iterrows():
            valores_subframe = Frame(valores_frame)
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
                    width=25, 
                    height=1, 
                    relief=GROOVE,
                    bg= formato.fondo_valores_de_tabla)
                valor.grid(row=0, column=row[0])
            
            # Agregar botones
            
            argumento = lista_de_valores[0]

            boton_ver = Label(
                valores_subframe,
                text='Detalle',
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width=8,
                height=1,
                relief=GROOVE,
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
            #    width=4,
            #    height=1,
            #    relief=GROOVE,
            #    cursor="hand2",
            #    bg=formato.boton_sin_que_pase_cursor
            #)
            #boton_editar.grid(row=0, column=len(lista_de_valores)+2)
            #boton_editar.bind("<Button-1>",lambda e,argumento=argumento:self.funcion3(argumento))
            #self.Efecto_de_boton(boton_editar)

            boton_eliminar = Label(
                valores_subframe,
                text='Eliminar',
                font=formato.tipo_de_letra_tabla,
                fg = formato.letras_del_boton,
                width=8,
                height=1,
                relief=GROOVE,
                cursor="hand2",
                bg=formato.boton_sin_que_pase_cursor
            )
            boton_eliminar.grid(row=0, column=len(lista_de_valores)+2)
            boton_eliminar.bind("<Button-1>",lambda e,argumento=argumento:self.funcion2(argumento))
            self.Efecto_de_boton(boton_eliminar)

    #----------------------------------------------------------------------
    def obtener_dato(self, n):
        """Método de la clase Cuadro. \n
        Permite recuperar la información registrada a través de los wingets agregados al Frame creado con la Clase Cuadro."""
        
        # Esta función obtiene un dato "n" de la lista que se guarda en el objeto cuadro.
        self.lista = self.lista_de_datos
        if type(self.lista[n]).__name__ == 'DateEntry':
            return self.lista[n].get_date()
        elif type(self.lista[n]).__name__ == 'ScrolledText':
            return self.lista[n].get("1.0", "end-1c")
        else:
            return self.lista[n].get()
    
    #----------------------------------------------------------------------
    def obtener_lista_de_datos(self):
        """"""

        self.lista = self.lista_de_datos
        self.lista_output = []
        for i in self.lista:
            if type(i).__name__ == 'DateEntry':
                fecha = i.get_date()
                self.lista_output.append(str(fecha.strftime("%d/%m/%Y")))
            elif type(i).__name__ == 'ScrolledText':
                self.lista_output.append(i.get("1.0", "end-1c"))
            else:
                self.lista_output.append(i.get())
        return self.lista_output

    #----------------------------------------------------------------------
    def insertar_lista_de_datos(self, informacion_a_introducir):
        """"""
        self.informacion_a_introducir = informacion_a_introducir

        self.lista = self.lista_de_datos
        df_listas = list(zip(self.informacion_a_introducir, self.lista))
        tabla_listas = pd.DataFrame(df_listas)
        for i, row in tabla_listas.iterrows():
            try:
                row[1].set(row[0])
            except:
                row[1].set_date(str(row[0]))
            else:
                row[1].set(row[0])

class MenuSefa():

    #----------------------------------------------------------------------
    def __init__(self, window):
        """Constructor"""

        menubar = Menu(window)
        window.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Cerrar sesión")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=window.quit)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Ayuda")
        helpmenu.add_separator()
        helpmenu.add_command(label="Acerca de...")

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)

class ScrollFrame(Frame):

    #----------------------------------------------------------------------
    def __init__(self, parent, **kwargs):
        """Constructor"""

        super().__init__(parent, **kwargs)
        
        self.canvas = Canvas(self, borderwidth=1, background=formato.fondo)
        self.viewPort = Frame(self.canvas, background=formato.fondo)

        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.hsb.pack(side="bottom", fill="x")
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas_window = self.canvas.create_window((0,0), window=self.viewPort, anchor="nw", tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.onFrameConfigure(None)

    #----------------------------------------------------------------------
    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    #----------------------------------------------------------------------
    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        
        if (event.widget.winfo_width() != event.width) and (event.widget.winfo_height()  != event.height):
            canvas_width, canvas_height = event.width, event.height
            self.canvas.itemconfig(self.canvas_window, width = canvas_width, height = canvas_height)



