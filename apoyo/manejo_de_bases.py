import gspread as gs
import pandas as pd
import string
import datetime as dt
from email.utils import formataddr
import smtplib
import email.message
from email.message import EmailMessage
import email.mime.text
import apoyo.formato as formato 

class Base_de_datos():
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, key, pestanna):
        """Constructor"""
        
        self.key = key
        self.pestanna = pestanna
        self.gc = gs.service_account(filename='accesos.json')
        self.sh = self.gc.open_by_key(self.key)
        self.worksheet = self.sh.worksheet(self.pestanna)
        self.hoy = dt.datetime.now()

    #----------------------------------------------------------------------
    def generar_dataframe(self):
        """[...]"""

        self.dataframe = pd.DataFrame(self.worksheet.get_all_records())
        return self.dataframe

    #----------------------------------------------------------------------
    def imprimir_dataframe(self):
        """[...]"""

        self.tabla = self.generar_dataframe()
        print(self.tabla)

    #----------------------------------------------------------------------
    def contar_coincidencias(self, variable):
        """[...]"""

        self.variable = variable
        lista_de_coincidencias = self.worksheet.findall(self.variable)
        return len(lista_de_coincidencias)

    #----------------------------------------------------------------------
    def identificar_fila_por_variable(self, variable):
        """[...]"""

        self.variable = variable
        self.cell = self.worksheet.find(self.variable)
        return self.cell.row
    
    #----------------------------------------------------------------------
    def listar_datos_de_fila(self, variable):
        """[...]"""

        self.variable = variable
        self.fila = self.identificar_fila_por_variable(self.variable)
        self.values_list = self.worksheet.row_values(self.fila)
        return self.values_list

    #----------------------------------------------------------------------
    def cambiar_un_dato_de_una_fila(self, variable, posicion_de_dato, nuevo_valor_de_dato):
        """[...]"""
        
        self.variable = variable
        self.posicion_de_dato = posicion_de_dato
        self.nuevo_valor_de_dato = nuevo_valor_de_dato
        self.fila = self.identificar_fila_por_variable(self.variable)
        self.worksheet.update_cell(self.fila, self.posicion_de_dato, self.nuevo_valor_de_dato)

    #----------------------------------------------------------------------
    def cambiar_los_datos_de_una_fila(self, variable, lista_de_nuevos_valores):
        """[...]"""

        self.variable = variable
        self.lista_de_nuevos_valores = lista_de_nuevos_valores

        self.fila_identificada = self.identificar_fila_por_variable(self.variable)
        self.values_list = self.worksheet.row_values(self.fila_identificada)

        listAlphabet = list(string.ascii_uppercase)
        newlist = []
        for i in listAlphabet:
            first_letter = i
            for i in listAlphabet:
                combinacion = first_letter + i
                newlist.append(combinacion)
        newlistAlphabet = listAlphabet + newlist
        newlistNumbers = list(range(1,len(newlistAlphabet)+1))
        equivalencias = pd.DataFrame(list(zip(newlistNumbers, newlistAlphabet)), columns= ['Número', 'Letra'])

        self.celda_inicial = 'A' + str(self.fila_identificada)
        self.criterio_para_buscar = equivalencias['Número'] == len(self.values_list)+1
        self.equivalencia_encontrada = equivalencias[self.criterio_para_buscar]
        self.lista_de_valores_en_letra = self.equivalencia_encontrada['Letra'].tolist()
        self.valor_en_letra = self.lista_de_valores_en_letra[0]
        self.celda_final = self.valor_en_letra + str(self.fila_identificada)
        self.rango_a_cambiar = self.celda_inicial + ':' + self.celda_final
        self.worksheet.update(self.rango_a_cambiar, [self.lista_de_nuevos_valores])

    #----------------------------------------------------------------------
    def agregar_datos(self, lista_de_datos):
        """[...]"""

        self.lista_de_datos_sencilla = lista_de_datos
        self.worksheet.append_row(self.lista_de_datos_sencilla)
    
    #---------------------------------------------------------------------
    def agregar_datos_generando_codigo(self, lista_de_datos):
        """[...]"""

        self.lista_de_datos = [lista_de_datos]
        tabla = self.generar_dataframe()
        if len(tabla.index) == 0:
            numero = 1
        elif dt.datetime.strptime(tabla['F_CREACION'].tolist()[-1], "%Y-%m-%d %H:%M:%S.%f").year != self.hoy.year: 
            numero = 1
        else:
            last = tabla['CORRELATIVO'].tolist()[-1]
            numero = last + 1
        
        self.codigo = self.pestanna + "-" + str(self.hoy.year) + "-" + str(numero)
        self.datos_obligatorios = [self.codigo, str(self.hoy), numero]
        self.lista_de_datos_completos = self.datos_obligatorios + self.lista_de_datos
        self.worksheet.append_row(self.lista_de_datos_completos)
    
    #---------------------------------------------------------------------
    def agregar_nuevo_codigo(self, dato, tiempo):
        """[...]"""

        tabla = self.generar_dataframe()
        if len(tabla.index) == 0:
            numero = 1
        elif dt.datetime.strptime(tabla['F_CREACION'].tolist()[-1], "%Y-%m-%d %H:%M:%S.%f").year != self.hoy.year: 
            numero = 1
        else:
            last = tabla['CORRELATIVO'].tolist()[-1]
            numero = last + 1
        
        self.codigo = self.pestanna + "-" + str(self.hoy.year) + "-" + str(numero)
        self.datos_obligatorios = [self.codigo, str(tiempo), numero]
        dato_unico =  str(self.hoy.year) + "-" + str(numero) + "/" + dato
        self.lista_de_datos_completos = self.datos_obligatorios + [dato_unico]
        self.worksheet.append_row(self.lista_de_datos_completos)

    #---------------------------------------------------------------------
    def agregar_codigo(self, dato, tiempo, dato_adicional = ""):
        """[...]"""

        tabla = self.generar_dataframe()
        if len(tabla.index) == 0:
            numero = 1
        elif dt.datetime.strptime(tabla['F_CREACION'].tolist()[-1], "%Y-%m-%d %H:%M:%S.%f").year != self.hoy.year: 
            numero = 1
        else:
            last = tabla['CORRELATIVO'].tolist()[-1]
            numero = last + 1
        
        self.codigo = self.pestanna + "-" + str(self.hoy.year) + "-" + str(numero)
        self.datos_obligatorios = [self.codigo, str(tiempo), numero]
        dato_unico = dato
        if dato_adicional == "":
            self.lista_de_datos_completos = self.datos_obligatorios + [dato_unico]
        else:
            dato_2 = dato_adicional
            self.lista_de_datos_completos = self.datos_obligatorios + [dato_unico] + [dato_2]
            
        self.worksheet.append_row(self.lista_de_datos_completos)


class Correo_electronico():
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, destinatario, asunto, mensaje):
        """Constructor"""

        self.destinatario = destinatario
        self.asunto = asunto
        self.msg = mensaje

        self.sender = 'herramientasdesefa@gmail.com'
        self.from_ = formataddr(('Herramientas de Sefa', self.sender))
        self.to_ = self.destinatario
        self.subject = self.asunto
        self.firma = self.obtener()

        self.em = EmailMessage()
        self.em.set_content(self.msg)
        self.em['To'] = self.to_
        self.em['From'] = self.from_
        self.em['Subject'] = self.subject

    #----------------------------------------------------------------------
    def obtener(self):
        """[...]"""
        
        b0 = Base_de_datos('12gzaAx7GkEUDjEmiJG693in8ADyCPxej5cUv9YA2vyY','Administrador')
        datos_registrados = b0.listar_datos_de_fila('ADMIN_001')
        firma = datos_registrados[2]
        return firma

    #----------------------------------------------------------------------
    def enviar(self):
        """[...]"""

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(self.sender, self.firma)
        s.send_message(self.em, self.em['From'], [self.em['To']])