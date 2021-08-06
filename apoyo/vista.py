# I. Librerias
import gspread
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import datetime
from elemetos_de_GUI import *

# Tabla
t_doc_rec = {
    'Categoria': ['Oficio', 'Reiterativo'],
    'HT': ['2021-E01-234102', '2021-E01-0335102'],
    'Destinatario': ['DGM', 'Metropolitana de Lima']
}

tabla = pd.DataFrame(t_doc_rec)



# II. Funciones

# o) Obtener dato


# i) Validación de números
def valnum(digito):
    if digito.isdigit():
	    return True
    elif digito == "":
	    return True
    else:
	    return False

def valfecha(fecha1, fecha2):
    if fecha1<fecha2:
        return TRUE
    else: 
        raise messagebox.showerror("Error", "Inconsistencia de fechas. La fecha de carga del informe de supervisión no puede ser anterior a la fecha fin de supervisión.")

# iii) Registro de Información
def enviar():
    # Validación de fechas
    valfecha(l2_valor1.get(),l2_valor2.get())

    # Conexión con Google Sheets
    gc = gspread.service_account(filename='accesos.json')
    sh = gc.open_by_key('13EgFGcKnHUomMtjBlgZOlPIg_cb4N3aGpkYH13zG6-4')
    worksheet = sh.worksheet("DOC_RECIBIDOS")

    # Obtención de valores
    od = l1_valor1.get()
    exp = l1_valor2.get()
    #nivel = l1_valor3.get()

    f_fin = l2_valor1.get()
    f_carga = l2_valor2.get()
    objetivos_plan = l2_valor3.get()
    objetivos_acta = l2_valor4.get()

    # Subida de información
    worksheet.append_row([od, exp, f_fin, f_carga, int(objetivos_plan), int(objetivos_acta)])
    # Confirmación de registro
    messagebox.showinfo("¡Excelente!", "El registro se ha ingresado correctamente")

# III. Aplicativo

# i) Apertura de ventana
app_ospa = Tk()

# Interpretación Tcl a Python
reg = app_ospa.register(valnum)

# Frames de la aplicación
lienzo1 = Frame(app_ospa)
lienzo1.pack()

lienzo2 = Frame(app_ospa)
lienzo2.pack()

lienzo3 = Cuadro(app_ospa)

# ii) Objetos
# Labels
l1_titulo = Label(lienzo1, text="Ospa: Observatorio")
l1_label1 = Label(lienzo1, text="HT entrante")
l1_label2 = Label(lienzo1, text="Vía de recepción")
# l1_label3 = Label(lienzo1, text="Aporte del documento")

# l2_titulo = Label(lienzo2, text="Otros")
l2_label1 = Label(lienzo2, text="Fecha de ingreso OEFA")
l2_label2 = Label(lienzo2, text="Fecha de ingreso SEFA")
l2_label3 = Label(lienzo2, text="Tipo de documento")
l2_label4 = Label(lienzo2, text="N° de documento")

# Valores
l1_valor1 = StringVar()
l1_valor2 = StringVar()
# l1_valor3 = StringVar()

l2_valor1 = StringVar()
l2_valor2 = StringVar()
l2_valor3 = StringVar()
l2_valor4 = StringVar()

# Entries
l1_entry1 = Entry(lienzo1, textvariable=l1_valor1, width= 20, borderwidth=2)
l1_entry2 = Entry(lienzo1, textvariable=l1_valor2, width= 20, borderwidth=2)
# l1_entry3 = Entry(lienzo1, textvariable=l1_valor3, width= 20, borderwidth=2)

l2_entry1 = DateEntry(lienzo2, textvariable=l2_valor1, background='darkblue', foreground='white', width= 9, borderwidth=2)
l2_entry2 = DateEntry(lienzo2, textvariable=l2_valor2, background='darkblue', foreground='white', width= 9, borderwidth=2)
l2_entry3 = Entry(lienzo2, textvariable=l2_valor3, width= 12, borderwidth=2)
l2_entry3.config(validate="key", validatecommand=(reg, '%P'))
l2_entry4 = Entry(lienzo2, textvariable=l2_valor4, width= 12, borderwidth=2)
l2_entry4.config(validate="key", validatecommand=(reg, '%P'))

# Botones
boton = Button(lienzo2, text="Guardar", command=enviar)

# Objetos definidos por elemetos de GUI
lienzo3.agregar_escenario(2, 2, tabla, enviar, enviar, enviar)

# Ubicaciones
# Lienzo 1
l1_titulo.grid(row= 0, column=0, columnspan=4)
l1_label1.grid(row= 1, column=0)
l1_label2.grid(row= 1, column=2)
# l1_label3.grid(row= 3, column=0)

l1_entry1.grid(row= 1, column=1)
l1_entry2.grid(row= 1, column=3)
# l1_entry3.grid(row= 3, column=1)

# Lienzo 2
# l2_titulo.grid(row= 0, column=0, columnspan=2)
l2_label1.grid(row= 0, column=0)
l2_label2.grid(row= 0, column=2)
l2_label3.grid(row= 1, column=0)
l2_label4.grid(row= 1, column=2)

l2_entry1.grid(row= 0, column=1)
l2_entry2.grid(row= 0, column=3)
l2_entry3.grid(row= 1, column=1)
l2_entry4.grid(row= 1, column=3)

boton.grid(row= 2, column=0, columnspan=4)


# iii) Loop para App
app_ospa.mainloop()