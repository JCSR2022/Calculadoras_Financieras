# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 18:02:51 2023

@author: jhona
"""

#Librerias a utilizar 
#import time
import os
#import sys
#import os
#from datetime import datetime
import re
import xlwings as xw
import numpy as np
import matplotlib.pyplot as plt
import calendar
from datetime import date, timedelta
import sympy as sp
#from itertools import combinations
import scipy.optimize as optimize
from sklearn.linear_model import LinearRegression
import pandas as pd
from openpyxl.utils import get_column_letter

from BI_CETES import CETES
from S_UDIBONOS import UDIBONOS
from M_TASA_FIJA import M_TasaFija
from LD_BONDES_D import LD_BondesD


# ----------------Clase para conexion Excel_pyton--------------------------------------
# -------------------------------------------------------------------------------------

class xlwings_Excel:
    """Este código facilita la manipulación de archivos de Excel desde Python.
    kjbk
    La clase tiene un constructor __init__ que permite abrir 
    un archivo de Excel especificado (incialmente debe estar en la misma 
    carpeta que el ejecutable de Python) por su nombre o trabajar 
    con el archivo de Excel que llamó al script de Python. """

    def __init__(self, nombre_archivo=False):
        """De no introducir un nombre se asume se esta llamando desde Excel.
        Por ahora se limita a que el .xlsm y .py esten en la misma carpeta"""
        try:
            # Manejo de llamadas desde Excel
            if not nombre_archivo:
                self.wb = xw.Book.caller()
            
            # Manejo desde Python
            elif isinstance(nombre_archivo, str):
                # Verificación si el Excel y el .py están en la misma carpeta
                directorio_actual = os.path.dirname(__file__)
                ruta_archivo = os.path.join(directorio_actual, nombre_archivo)
                if os.path.isfile(ruta_archivo):
                    self.wb = xw.Book(nombre_archivo)
                else:
                    print(f"Error en nombre o ruta de archivo {nombre_archivo}")
            else:
                print(f"Error {nombre_archivo}, debe ser un nombre de archivo")

        except Exception as e:
            print("Error: ", e)


    def check_hoja(self,nombre_hoja=False):
        try:
            if not nombre_hoja:
                # Si no se introdujo una hoja específica, se trabaja con la activa
                hoja = self.wb.sheets.active
                nombre_hoja = hoja.name
                return(nombre_hoja)
            elif ((isinstance(nombre_hoja, str) 
                   and nombre_hoja in [hoja.name for hoja in self.wb.sheets])):
                return(nombre_hoja)
            else:
                print("Error: nombre de hoja")
                return 0
        except Exception as e:
            print("Error: ", e)
            return 0
        
    def check_celda(self, nombre_celda=False):
        try:
            # Si no se introdujo una celda específica, se trabaja con la activa
            patron_celdas_excel = r'^\$?[A-Za-z]+\$?\d+(\:\$?[A-Za-z]+\$?\d+)?$'
            if not nombre_celda:
                #celda = self.xw.apps.active.selection 
                #nombre_celda = celda.address 
                
                letra_columna = get_column_letter(self.wb.app.selection.column)
                numero_fila = self.wb.app.selection.row
                nombre_celda = f"${letra_columna}${numero_fila}"
                return nombre_celda
            elif isinstance(nombre_celda, str) and re.match(patron_celdas_excel,nombre_celda):
                return nombre_celda
            else:
                print("Error: nombre de celda")
                return 0   
        except Exception as e:
            print("Error: ", e)
            return 0
    
    
    def leer_celda(self,dir_celda=False,nombre_hoja =False):
        try:
            hoja = self.check_hoja(nombre_hoja)
            celda = self.check_celda(dir_celda)
            return self.wb.sheets[hoja][celda].value
        except Exception as e:
            print("Error: ", e) 
        
    def escribir_celda(self,valor,dir_celda=False,nombre_hoja = False):
        try:
            hoja = self.check_hoja(nombre_hoja)
            celda = self.check_celda(dir_celda)
            self.wb.sheets[hoja][celda].value = valor
        except Exception as e:
            print("Error: ", e)
            
    def leer_tabla(self,dir_celda=False,nombre_hoja =False):
        try:
            hoja = self.check_hoja(nombre_hoja)
            celda = self.check_celda(dir_celda)
            #tambien se puede sin usar pandas:
            # matriz = self.wb[hoja].range(celda).options(expand='table')
            df = self.wb.sheets[hoja][celda].options(pd.DataFrame, expand='table', index=False).value
            return df
        except Exception as e:
            print("Error: ", e)

    def escribir_tabla(self,df,dir_celda=False,nombre_hoja =False):
        try:
            hoja = self.check_hoja(nombre_hoja)
            celda = self.check_celda(dir_celda)
            
            self.wb.sheets[hoja][celda].options(index=False).value = df 
            
            return df
        except Exception as e:
            print("Error: ", e)
            
            
    def Graficar(self,fig,nombre="",dir_celda=False,nombre_hoja =False):
        try:
            hoja = self.check_hoja(nombre_hoja)
            celda = self.check_celda(dir_celda)
            
            self.wb.sheets[hoja][celda].add(fig, name=nombre, update=True)
            
        except Exception as e:
            print("Error: ", e)





# -------------------Cargar informacion de bono----------------------------------------
# -------------------------------------------------------------------------------------    
def cargarBonos():
    """
    Funcion previa para cargar la informacion de bonos, la informacion esta almacenada
    en un excel en la carpeta info_Bonos, son archivos .xlxs ya preparados con toda
    la informacion. 
    Entrada:
        A traves de xlwings: celda C9 de la hoja Calculadora, tipo de bono a trabajar
    Salida:
        Segun la entrada se escge el archivo en funcion del dicc_info_Bonos, 
        Se devuelve la direccion del archivo para despues ser utilizada por cargarInfoBono()
        Tambien la info en el excel de la carpeta info_Bonos se cargara en la pagina "Info_Bonos"
    """
    dicc_info_Bonos =  {'M_TASA_FIJA':"info_Bonos\\20230831_t-1_Vector_M.xlsx",
                        'LD_BONDES_D':"info_Bonos\\20230831_t-1_Vector_LD.xlsx",
                    'BI_CETES':"info_Bonos\\20230831_t-1_Vector_BI.xlsx " ,
                    'S_UDIBONOS':"info_Bonos\\20230831_t-1_Vector_S.xlsx   "   
                        }
    
    enlace = xlwings_Excel()
    nombre_hoja = "Calculadora"
    tipo_bono = enlace.leer_celda("$C$9",nombre_hoja)
    df = pd.DataFrame([])
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo_info_Bono = os.path.join(directorio_actual, dicc_info_Bonos[tipo_bono] )
    df = pd.read_excel(ruta_archivo_info_Bono)
    enlace.escribir_tabla(df,"$A$1","Info_Bonos" )  
    
    return ruta_archivo_info_Bono


def cargarInfoBono(num_serie = False ,archivo =  False):
    """
    Funcion para cargar la informacion de bonos, la informacion esta almacenada
    en un excel en la carpeta info_Bonos, son archivos .xlxs ya preparados con toda
    la informacion.
    Entrada:
        A traves de xlwings: celda C9 de la hoja Calculadora
                             celda D9 con el numero de serie 
    Salida:
        Devuelve al excel la informacion del bono,serial seleccionado
        Devuelve el objeto BonoEnEvaluacion con toda la informacion del bono
    """
    
    if not archivo: archivo = cargarBonos()
    
    # Se lee el numero de serial del bono
    enlace = xlwings_Excel()
    nombre_hoja = "Calculadora"
    num_serie = int(enlace.leer_celda("$D$9",nombre_hoja))
    
    # Se carga la informacion del bono 
    df_vectorInvex = pd.read_excel(archivo)
    serie = [ x for x in ['Serie','SERIE'] if x in df_vectorInvex.columns][0]
    bono_analizar = df_vectorInvex[df_vectorInvex[serie] == num_serie].reset_index(drop=True)
    info_bono_analizar = {}
    for key in bono_analizar.columns:
        val = bono_analizar.loc[0,key]
        info_bono_analizar[key] = val 
    
    # Se crea el objeto Bono respectivo:
    tipo_bono = enlace.leer_celda("$C$9",nombre_hoja)
    if tipo_bono == 'M_TASA_FIJA': BonoEnEvaluacion = M_TasaFija(info_bono_analizar)
    elif  tipo_bono == 'LD_BONDES_D': BonoEnEvaluacion = LD_BondesD(info_bono_analizar)
    elif  tipo_bono == 'BI_CETES': BonoEnEvaluacion = CETES(info_bono_analizar)  
    elif  tipo_bono =='S_UDIBONOS' : BonoEnEvaluacion = UDIBONOS(info_bono_analizar)   
    
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['Serie'],"$H$4",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['ValorNominal'],"$H$5",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['FrecCpn' ],"$H$6",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()[ 'TasaCupon'],"$H$7",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['FechaVcto' ],"$H$8",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['FechaEmision' ],"$H$9",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()[ 'TimId'],"$H$10",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()[ 'PrecioLimpio'],"$H$11",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()[ 'PrecioSucio'],"$H$12",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['TasaDeRendimiento'],"$H$13",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['Sobretasa'],"$H$14",nombre_hoja)    
    return BonoEnEvaluacion

# -------------------Calculos----------------------------------------------------------
# -------------------------------------------------------------------------------------   

def calculoPrecioRendimiento(BonoEnEvaluacion = False):
    
    if not BonoEnEvaluacion: BonoEnEvaluacion = cargarInfoBono()
    
    enlace = xlwings_Excel()
    nombre_hoja = "Calculadora"

    # Confirmacion de datos para calculo
    BonoEnEvaluacion.modInfoBono({'ValorNominal': enlace.leer_celda("$I$5", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'FrecCpn': enlace.leer_celda("$I$6", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'TasaCupon': enlace.leer_celda("$I$7", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'FechaVcto': enlace.leer_celda("$I$8", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'FechaEmision': enlace.leer_celda("$I$9", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'TimId': enlace.leer_celda("$I$10", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'PrecioLimpio': enlace.leer_celda("$I$11", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'PrecioSucio': enlace.leer_celda("$I$12", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'TasaDeRendimiento': enlace.leer_celda("$I$13", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'Sobretasa': enlace.leer_celda("$I$14", nombre_hoja)})
    
    # Calculo precio limpio
    Precio_limpio = BonoEnEvaluacion.calcPrecioLimpio()
    enlace.escribir_celda(Precio_limpio,"$D$16",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['TasaDeRendimiento'],"$D$17",nombre_hoja)
    
    # Calculo rendimiento
    rendimiento = BonoEnEvaluacion.calcRendimiento()
    enlace.escribir_celda(rendimiento,"$D$19",nombre_hoja)
    enlace.escribir_celda(BonoEnEvaluacion.verInfoBono()['PrecioLimpio'],"$D$20",nombre_hoja)


def calculoRegresos(BonoEnEvaluacion = False):
    
    if not BonoEnEvaluacion: BonoEnEvaluacion = cargarInfoBono()
    
    enlace = xlwings_Excel()
    nombre_hoja = "Calculadora"
    
    # Confirmacion de datos para calculo
    BonoEnEvaluacion.modInfoBono({'ValorNominal': enlace.leer_celda("$I$5", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'FrecCpn': enlace.leer_celda("$I$6", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'TasaCupon': enlace.leer_celda("$I$7", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'FechaVcto': enlace.leer_celda("$I$8", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'FechaEmision': enlace.leer_celda("$I$9", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'TimId': enlace.leer_celda("$I$10", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'PrecioLimpio': enlace.leer_celda("$I$11", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'PrecioSucio': enlace.leer_celda("$I$12", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'TasaDeRendimiento': enlace.leer_celda("$I$13", nombre_hoja)})
    BonoEnEvaluacion.modInfoBono({'Sobretasa': enlace.leer_celda("$I$14", nombre_hoja)})
    
    
    TasaReporto = enlace.leer_celda("$H$19", nombre_hoja)
    plazoReporto = enlace.leer_celda("$H$20", nombre_hoja)
    

    # Calculo precio sucio
    PrecioRegreso = BonoEnEvaluacion.CalcRegresos(TasaReporto, plazoReporto)
    enlace.escribir_celda(PrecioRegreso,"$D$26",nombre_hoja)

    
    # Calculo rendimiento
    RendimientoRegreso = BonoEnEvaluacion.calcRendimiento(PrecioRegreso)
    enlace.escribir_celda(RendimientoRegreso,"$D$27",nombre_hoja)



# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------











# -------------------------- Calculos para CETES --------------------------------------
# -------------------------------------------------------------------------------------
def calcular_CETES(entrada):
    # Los valores de entrada deben estar en el siguiente orden:
     # [valor_VN, Precio, Tasa_descuento, Num_dias,Tasa_rendimiento , Descuento ]
    valores = entrada.copy()
    # Define el número de decimales de precisión
    redGen = 12
    
    # Definir las variables simbólicas
    VN, P, b, t, r, D = sp.symbols('VN P b t r D')
    variables = [VN, P, b, t, r, D]
    
    # Definir las ecuaciones
    ecuacion1 = sp.Eq(P, VN / (1 + r * t / 360))
    ecuacion2 = sp.Eq(b, r / (1 + r * t / 360))
    ecuacion3 = sp.Eq(P, VN - D)
    ecuacion4 = sp.Eq(P, VN *(1 - b * t / 360))
    ecuaciones = [ ecuacion1, ecuacion2, ecuacion3, ecuacion4]
    
    #Identificar valores conocidos
    conocidos = {}
    desconocidos = []
    for i,valor in enumerate(valores):
        if valor and isinstance(valor, (float, int, bool)):
            conocidos[variables[i]]= valor
        else:
            desconocidos.append(variables[i])
    
    
    #Encontrando soluciones 
    parada = True
    while (len(conocidos)< len(valores)) and parada:
        parada = False
        #Evaluando en cada ecuacion para cada variable:
        for variable in desconocidos:
            for ecuacion in ecuaciones:
                sol = sp.solve([ecuacion.subs(conocidos)], (variable,))
                if sol:
                    valor = sol[list(sol.keys())[0]]
                    if isinstance(valor, (sp.core.numbers.Float,sp.core.numbers.Integer,sp.core.numbers.Rational)):
                        conocidos[variable] = float(valor)
                        parada = True

    # Actualizar los valores originales con los conocidos
    for i, variable in enumerate(variables):
        if variable in conocidos:
            valores[i] = round(conocidos[variable], redGen)
            
    return valores


def Calculo_CETES_desde_Excel():
    "para pruebas"
    enlace = xlwings_Excel()
    
    nombre_hoja = "CETES"
    VN = enlace.leer_celda("$D$5",nombre_hoja)
    
    def leer_temp(celda,nombre_hoja):
        temp = enlace.leer_celda(celda,nombre_hoja)
        if temp == "":
            return  False
        else:
            return  temp
    
    t = leer_temp("$D$6",nombre_hoja)
    b = leer_temp("$D$7",nombre_hoja)
    P = leer_temp("$D$8",nombre_hoja)    
    r = leer_temp("$D$9",nombre_hoja)  
    D = leer_temp("$D$10",nombre_hoja)


    entrada = [VN,P,b,t,r,D]
    
    salida = calcular_CETES(entrada)
       # Los valores de entrada deben estar en el siguiente orden:
        # [valor_VN, Precio, Tasa_descuento, Num_dias,Tasa_rendimiento , Descuento ]

    VN,P,b,t,r,D = salida

    enlace.escribir_celda(VN,"$J$5",nombre_hoja)
    enlace.escribir_celda(t,"$J$6",nombre_hoja)
    enlace.escribir_celda(b,"$J$7",nombre_hoja)
    enlace.escribir_celda(P,"$J$8",nombre_hoja)
    enlace.escribir_celda(r,"$J$9",nombre_hoja)
    enlace.escribir_celda(D,"$J$10",nombre_hoja)
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------    
    
    
    

    
    
# -------------------Calculos bono M --------------------------------------------------
# ------------------------------------------------------------------------------------- 
    
def calcular_fechas_cupon(vencimiento, emision, fecha_interes, dias=182):
    """
    Calcula las fechas de pago de cupones desde la fecha de vencimiento hasta la fecha de interés
    con plazos de 182 días (por defecto).

    Entrada:
        - vencimiento (datetime): Fecha de vencimiento del cupón.
        - emisión (datetime): Fecha de emisión del cupón o límite hasta el cual se desea calcular.
        - fecha_interes (datetime): Fecha para la cual se desea saber cuántos cupones faltan.
        - dias (int, opcional): Número de días en cada período de cupón. Valor por defecto: 182.

    Salida:
        Lista con fechas de pago de cupón.
    """
    if fecha_interes >=  emision and fecha_interes<=vencimiento:
        fechas = [vencimiento]
        while fechas[-1] > fecha_interes:
            if fecha_interes < vencimiento:
                fecha_anterior = fechas[-1] - timedelta(days=dias)
                if fecha_anterior > emision:
                    fechas.append(fecha_anterior)
                else:
                    break
            else:
                break
        fechas.reverse()
        return fechas


def calcular_dias_ultimo_cupon(fechas_cupon, fecha_analisis, dias=182):
    """
    Calcula el número de días transcurridos desde el vencimiento del último cupón hasta la fecha indicada.
    
    Entradas:
        - fechas_cupon (list): Lista con fechas de pago de cupones, preferiblemente obtenidas de la función "calcular_fechas_cupon".
        - fecha_analisis (datetime): Fecha para la cual se desea calcular el número de días.
        - dias (int, opcional): Número de días en cada período de cupón. Valor por defecto: 182.
    
    Devolución:
        Número de días transcurridos. Si se introduce una fecha incorrecta, no devuelve nada.
    """
    # Verificar que la fecha de análisis esté en el intervalo de los cupones, desde la emisión hasta el vencimiento.
    if (fechas_cupon[0] - timedelta(days=dias) < fecha_analisis < fechas_cupon[-1]):
        i = 0
        while True:
            if fecha_analisis < fechas_cupon[i]:
                dias_faltantes = (fechas_cupon[i] - fecha_analisis).days
                return dias - dias_faltantes
            else:
                i += 1

def calcular_precio_limpio(vencimiento, liquidacion, emision, tasa_cupon, rendimiento, valor_nominal=100, num_dias_por_cupon=182):
    """
    Calcula el precio limpio de un bono a tasa fija.

    Entradas:
        - vencimiento (datetime): Fecha de vencimiento del cupón.
        - liquidacion (datetime): Fecha para la cual se desea saber cuántos cupones faltan.
        - emisión (datetime): Fecha de emisión del cupón o límite hasta el cual se desea calcular.
        - tasa_cupon (float): Tasa de interés anual del bono.
        - rendimiento (float): Rendimiento anual esperado por el inversionista.
        - valor_nominal (float, opcional): Valor nominal del bono. Valor por defecto: 100.
        - num_dias_por_cupon (int, opcional): Número de días en cada período de cupón. Valor por defecto: 182.

    Salida:
        Precio limpio del bono.
    """
    
    def calcular_Cj(tasa_cupon, valor_nominal=100, num_dias_por_cupon=182):
        return valor_nominal * num_dias_por_cupon * tasa_cupon / 360

    def calcular_R(rendimiento):
        return rendimiento * num_dias_por_cupon / 360
    
    def calcular_interes_devengado(tasa_cupon, dias_ultimo_cupon, valor_nominal=100):
        return valor_nominal * dias_ultimo_cupon * tasa_cupon / 360
    
    
    def calc_CuponesRestantes(liquidacion,fechas_cupon):
        n = 0
        for fecha in fechas_cupon:
            if fecha > liquidacion:
                n += 1
        return n

    
    def calcular_precio_simple(C, R, K, d, valor_nominal=100, num_dias_por_cupon=182):
        """ 
        Cálculo del precio limpio de un bono a tasa fija según la fórmula (2) del APÉNDICE 2A
        Descripción técnica de los BONOS de desarrollo del gobierno federal con tasa de interés fija.
          
        Nota: El valor por defecto de num_dias_por_cupon es 182, sin embargo, este valor se debe ajustar a días hábiles. 
        """
        return (C + C * (1 / R - 1 / (R * (1 + R)**(K-1))) + valor_nominal / (1 + R)**(K-1)) / ((1 + R)**(1 - d / num_dias_por_cupon)) - C * d / num_dias_por_cupon
    
    # def calc_intDev(TC,d, VN=100):
    #     return VN*d*TC/360
    
    fechas_cupon = calcular_fechas_cupon(vencimiento, emision, liquidacion)
    
    dias_ultimo_cupon = calcular_dias_ultimo_cupon(fechas_cupon, liquidacion)
    
    C = calcular_Cj(tasa_cupon)
    
    R = calcular_R(rendimiento)  
    
    # Número de cupones por liquidar, incluyendo el vigente   
    K = calc_CuponesRestantes(liquidacion,fechas_cupon)      
    
    PrecioLimpio = calcular_precio_simple(C, R, K, dias_ultimo_cupon)
    
#     intDev = calc_intDev(tasa_cupon,dias_ultimo_cupon)
    
#     PrecioSucio = PrecioLimpio + intDev
    
    return PrecioLimpio  #,PrecioSucio


def calc_PrecioSucio(PrecioLimpio,TC,vencimiento, liquidacion,emision):
    
    def calc_intDev(TC,d, VN=100):
        return VN*d*TC/360
    
    fechas_cupon = calcular_fechas_cupon(vencimiento, emision, liquidacion)
    dias_ultimo_cupon = calcular_dias_ultimo_cupon(fechas_cupon, liquidacion)
    
    intDev = calc_intDev(TC,dias_ultimo_cupon)
    
    return PrecioLimpio + intDev


def calc_rendimientoVencimiento(PrecioLimpio,vencimiento, liquidacion, emision, TC):
    
    # Definicion de función objetivo que encuentra la tasa de rendimiento
    def objetivo(r):
        return calcular_precio_limpio(vencimiento, liquidacion, emision, TC, r) - PrecioLimpio
    
    # Encontrar la tasa de rendimiento utilizando scipy.optimize.newton
    tasa_rendimiento = optimize.newton(objetivo, 0.1)  # Suponemos siempre una tasa inicial del 10%
    
    return tasa_rendimiento



def Graf_Precio_vs_rendimiento(emision,vencimiento,liquidacion,TC,rendimiento,serie=""):

    num_valores = 100
    x_vector = np.linspace(0.9 * rendimiento, 1.1 * rendimiento, num_valores)
    y_vector = [calcular_precio_limpio(vencimiento, liquidacion, emision, TC,r) for r in x_vector]


    def calcPendienteRegLin(X,y):
        """
        Funcion para el calculo de la pendiente de la recta obtenida 
        utilizando regression lineal con los valores de X, y
        Entrada:
        X = Puede estar en formato de lista o np array de dimesion (1,0), valores int, o float
        y = Puede estar en formato de lista o np array de dimesion (1,0), valores int, o float
        Salida:
        Pendiente 
        """
        y = np.array(y_vector)
        X = np.array(x_vector).reshape(-1, 1)

        modelo = LinearRegression()
        modelo.fit(X, y)

        # Devuelve la pendiente (coeficiente)
        return modelo.coef_[0]

    Estimado_duracion  = calcPendienteRegLin(x_vector,y_vector)

    print("---- Bono seleccionado con las siguientes características: ---")
    print("Número de serie:", serie)
    print("Fecha de emisión:", emision)
    print("Fecha de vencimiento:", vencimiento)
    print("Fecha de liquidación:", liquidacion)
    print("Tasa de cupón:", TC)
    print("Duracion Estimada:", Estimado_duracion)


    r0 = x_vector[num_valores//2]
    P0 = y_vector[num_valores//2]
    pendiente = Estimado_duracion

    def RectPrecio(r,r0,P0,pendiente):
        return pendiente*(r-r0) + P0
    P_regLin = [RectPrecio(x_vector[x],r0,P0,pendiente)   for x in range(num_valores)]

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.scatter(x_vector * 100, y_vector, alpha=0.5, label='Datos')
    plt.title('Rendimiento vs. Precio Limpio')
    plt.xlabel('Rendimiento (%)')
    plt.ylabel('Precio Limpio')
    plt.plot(x_vector * 100, P_regLin, color='blue', lw=2, label='Línea de Regresión')

    # Agregar leyenda con los datos
    leyenda_texto = (
        f"Número de serie: {serie}\n"
        f"Fecha de emisión: {emision.date()}\n"
        f"Fecha de vencimiento: {vencimiento.date()}\n"
        f"Fecha de liquidación: {liquidacion.date()}\n"
        f"Tasa de cupón: %{TC*100}\n"
        f"Pendiente (duracion): {Estimado_duracion:.4f}"
    )

    plt.grid(True)

    # Mostrar el gráfico con la leyenda
    plt.legend(loc='best')
    plt.text(0.5, .6, leyenda_texto, transform=ax.transAxes, fontsize=10, verticalalignment='bottom', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
    plt.show()


def Graf_CurvaRendimiento(dir_vector = "info_Bonos\\20230831_t-1_Vector_M.xlsx"):

    df = pd.read_excel(dir_vector)
    # Seleccion de datos a analizar
    df_analisis = df[['SERIE','FECHA', 'FECHA EMISION', 'FECHA VCTO','TASA CUPON','TASA DE RENDIMIENTO','PRECIO LIMPIO', 'PRECIO SUCIO']].copy()
    
    # Convierte la columna 'FECHA' a formato datetime64[ns]'
    df_analisis['FECHA'] = df_analisis.loc[:,'FECHA'].astype(str)
    df_analisis['FECHA'] = pd.to_datetime(df_analisis.loc[:,'FECHA'], format='%Y%m%d')
    df_analisis['Calc_rendimiento'] = df_analisis.apply(lambda x: pd.Series(calc_rendimientoVencimiento(x['PRECIO LIMPIO'],
                                                                                                    x['FECHA VCTO'],
                                                                                                    x['FECHA'],
                                                                                                    x['FECHA EMISION'],
                                                                                                    x['TASA CUPON'] / 100)), axis=1)*100
    def tiempo(fecha, vencimiento):
        # Convierte las columnas en objetos datetime
        fecha = pd.to_datetime(fecha)
        vencimiento = pd.to_datetime(vencimiento)

        # Calcula la diferencia entre las fechas en días
        diferencia = (vencimiento - fecha).dt.days

        # Convierte los días en años (asumiendo un año de 365 días)
        tiempo_en_anios = diferencia / 365

        return list(tiempo_en_anios.astype(float))  # Convierte a años como entero

    x = tiempo(df_analisis['FECHA'], df_analisis['FECHA VCTO'])
    y = df_analisis['Calc_rendimiento']

    # Crear el gráfico
    plt.scatter(x, y, alpha=0.5, label='Rendimientos')
    plt.title('Vencimientos vs. Rendimientos')
    plt.xlabel('Años para Vencimientos')
    plt.ylabel('Rendimientos')

    plt.grid(True)
    plt.legend(loc='best')

    plt.show()


def Leer_Datos_BonosM_desde_Excel():
    
    enlace = xlwings_Excel()   
    nombre_hoja = "BONOS_TASA_FIJA"
    valores = {
    'serie': enlace.leer_celda("$D$5", nombre_hoja),
    'Valor_nominal': enlace.leer_celda("$D$6", nombre_hoja),
    'Plazo_cupon': enlace.leer_celda("$D$7", nombre_hoja),
    'Tasa_cupon': enlace.leer_celda("$D$8", nombre_hoja),
    'fecha_vencimiento': enlace.leer_celda("$D$9", nombre_hoja),
    'Fecha_emision': enlace.leer_celda("$D$10", nombre_hoja),
    'fecha_liquidacion': enlace.leer_celda("$D$11", nombre_hoja),
    'PrecioLimpio': enlace.leer_celda("$E$12", nombre_hoja),
    'Rendimiento': enlace.leer_celda("$E$14", nombre_hoja)
}
    return valores

def Calc_Precio_Limpio_BonosM_Excel():
    
    
    Entrada = Leer_Datos_BonosM_desde_Excel()
    valor_nominal = Entrada['Valor_nominal']
    vencimiento = Entrada['fecha_vencimiento']
    liquidacion = Entrada['fecha_liquidacion']
    emision = Entrada['Fecha_emision']
    tasa_cupon = Entrada['Tasa_cupon']
    rendimiento = Entrada['Rendimiento']
    num_dias_por_cupon = Entrada['Plazo_cupon']
    
    PrecioLimpio = calcular_precio_limpio(vencimiento, liquidacion, emision, tasa_cupon, rendimiento, valor_nominal, num_dias_por_cupon)
    PrecioSucio = calc_PrecioSucio(PrecioLimpio,tasa_cupon,vencimiento, liquidacion,emision)
    
    enlace = xlwings_Excel()
    enlace.escribir_celda(PrecioLimpio,"$L$6","BONOS_TASA_FIJA")
    enlace.escribir_celda(PrecioSucio,"$L$8","BONOS_TASA_FIJA")
    enlace.escribir_celda(rendimiento,"$L$10","BONOS_TASA_FIJA")
   
    
def Calc_rendimiento_BonosM_Excel():
    
    Entrada = Leer_Datos_BonosM_desde_Excel()
    vencimiento = Entrada['fecha_vencimiento']
    liquidacion = Entrada['fecha_liquidacion']
    emision = Entrada['Fecha_emision']
    tasa_cupon = float(Entrada['Tasa_cupon'])
    PrecioLimpio = float(Entrada['PrecioLimpio'])
    
    
    rendimiento = calc_rendimientoVencimiento(PrecioLimpio,vencimiento, liquidacion, emision, tasa_cupon)
    PrecioSucio = calc_PrecioSucio(PrecioLimpio,tasa_cupon,vencimiento, liquidacion,emision)
    
    enlace = xlwings_Excel()
    enlace.escribir_celda( PrecioLimpio,"$L$6","BONOS_TASA_FIJA")
    enlace.escribir_celda(PrecioSucio,"$L$8","BONOS_TASA_FIJA")
    enlace.escribir_celda( rendimiento,"$L$10","BONOS_TASA_FIJA")
    
    
    
def Graf_Precio_vs_rendimiento_Excel():
    
    Entrada = Leer_Datos_BonosM_desde_Excel()
    serie = Entrada['serie']
    vencimiento = Entrada['fecha_vencimiento']
    liquidacion = Entrada['fecha_liquidacion']
    emision = Entrada['Fecha_emision']
    tasa_cupon = float(Entrada['Tasa_cupon'])
    
    enlace = xlwings_Excel()
    nombre_hoja = "BONOS_TASA_FIJA"
    rendimiento = float(enlace.leer_celda("$L$10", nombre_hoja))
    
    
    fig = Graf_Precio_vs_rendimiento(emision,vencimiento,liquidacion,tasa_cupon,rendimiento,serie)
    
    enlace = xlwings_Excel()
    enlace.Graficar(fig,"Precio_vs_rendimiento")
    
    
def Graf_CurvaRendimiento_Excel():
    
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(directorio_actual, "info_Bonos\\20230831_t-1_Vector_M.xlsx")
    
    fig = Graf_CurvaRendimiento(ruta)
    enlace = xlwings_Excel()
    enlace.Graficar(fig,"Curva de Rendimiento")
    
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------   
    
    
    
    
    
    
    
    
# ------------------------------Otras funciones ---------------------------------------    
# -------------------------------------------------------------------------------------






def cambio_xlsm():
    enlace = xlwings_Excel()
    hoja = enlace.check_hoja()
    celda = enlace.check_celda()
    enlace.escribir_celda(str(hoja) + " " +str(celda),"A1")
    
    df2 = pd.DataFrame()
    n = 5
    m = 50
    for i in range(n):
        promedio = np.random.randint(10,100)
        desviacion = np.random.randint(1,10)
        df2[f"mean_{promedio}_std_{desviacion}"] = np.random.normal(promedio, desviacion , size=m)
    enlace.escribir_tabla(df2)
    
    celda_lect = "$A$1"
    nombre_hoja = "Hoja1"
    valor = enlace.leer_celda(celda_lect,nombre_hoja)
    enlace.escribir_celda(valor,"A2")


def Cambio_Py():    
    enlace = xlwings_Excel('Calc_BondesD_v01.xlsm')
    celda_lect = "$A$1"
    nombre_hoja = "Hoja1"
    valor = enlace.leer_celda(celda_lect,nombre_hoja)
    print(type(valor),valor.strftime('%d/%m/%Y'), valor.day, calendar.month_name[valor.month]   , valor.year)
    enlace.escribir_celda(valor.strftime('%d/%m/%Y')+" desde python","F5")
    
    celda_tabla = "G8"
    df = enlace.leer_tabla(celda_tabla)
    print(df.info())
    print(df)
    
    df2 = pd.DataFrame()
    n = 5
    m = 50
    for i in range(n):
        promedio = np.random.randint(10,100)
        desviacion = np.random.randint(1,10)
        df2[f"mean_{promedio}_std_{desviacion}"] = np.random.normal(promedio, desviacion , size=m)
        
    nombre_hoja = "Hoja2"    
    dir_celda = "$B$3"
    enlace.escribir_tabla(df2,dir_celda,nombre_hoja)
    


def leer_Bonos():
    enlace = xlwings_Excel('Calc_BondesD_v01.xlsm')
    celda_lect = "$A$1"
    nombre_hoja = "Bonos"
    df = enlace.leer_tabla(celda_lect,nombre_hoja)
    df['IDENTIFICACION'] = df['FECHA DE VENCIMIENTO'].apply(lambda x: "LD" + x.strftime('%y%m%d'))
    df = df[['IDENTIFICACION'] + [col for col in df.columns if col != 'IDENTIFICACION']]
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    carpeta = os.path.join(directorio_actual, 'info_Bonos')
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)  
    ruta_csv = os.path.join(carpeta, 'Bonos.csv')
    df.to_csv(ruta_csv, index=False)
    return df
    

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
    
    
    

# -------------------------------------------------------------------------------------
def Chequeo():   
    print("Todo Bien")
def main():
    try:
        Chequeo()
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    main()

        


