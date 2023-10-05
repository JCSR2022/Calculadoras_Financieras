# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 08:59:40 2023

@author: jhona

Calculos UDIBONOS

Los Bonos de Desarrollo del Gobierno Federal denominados en Unidades de Inversión
(UDIBONOS) fueron creados en 1996 y son instrumentos de inversión que protegen al
tenedor ante cambios inesperados en la tasa de inflación. Los UDIBONOS se colocan a
largos plazos y pagan intereses cada seis meses en función de una tasa de interés real fija
que se determina en la fecha de emisión del título.

- **Valor Nominal (VN):** El valor nominal del bono = 100 UDIS (cien Unidades de Inversión).
- **Período de Interés (Nj):** Los títulos devengan intereses en pesos cada seis meses.
     Esto es, cada 182 días o al plazo que sustituya a éste en caso de días inhábiles (Plazo en días del cupón J).
- **Tasa de interés anual del cupón (TC):**  La tasa de interés que pagan estos títulos es fijada 
    por el Gobierno Federal en la emisión de la serie.
- **Intereses por pagar al final del periodo J (Ij):** Los intereses se calculan considerando los 
días efectivamente transcurridos entre las fechas de pago de los mismos, tomando como base años 
de 360 días, y se liquidan al finalizar cada uno de los períodos de interés.
"""

from INVEX_calc_Bonos import Bono
import pandas as pd
import scipy.optimize as optimize


class UDIBONOS(Bono):
    
    def __init__(self, infoBono = {}, archivo= None):
        """
        Constructor de la clase UDIBONOS.
        Args:
            Se debe introducir una tabla de converision para los UDIBONOS
            se establece como referencia el formato de salida de consuta de
            Banxico con dos columnas 'Fecha' y	'SP68257'
            
            archivo: Nombre/direccion de archivo en formato excel para leer los datos
                    en forma estanadar el archivo de referencia debe estar en la misma
                    carpeta del ejecutable.
        """
        super().__init__(infoBono)  # Llama al constructor de la clase Bono
        
        try:
            # nombre de archivo modelo para pruebas
            if not archivo: archivo = 'info_Bonos\\UDIS_Consulta_20230924_Mod.xlsx'
            
            self.df_conversion = pd.read_excel(archivo) 
            
        except Exception as e:
                print("Error init: ", e)
                self.df_conversion = e
        
        
    def ConvertirUdisPesos(self,valor,conv=True, fechaInteres = None ):
        """
        Funcion para convertir precio de Udis a pesos MXN
        Entrada:
            valor (float): valor a convertir
            fechaInteres (.date): Fecha a la cual se hara la conversion
            conv (bool): Si True, convierte de Udis a pesos, 
                         Si False convierte de Pesos a udis
        Salida:
            (valor de entrada) * (Valor de Udis para la fecha en analsis)
            '2.7 DESCRIPCIÓN TÉCNICA DE LOS UDIBONOS:
                Conversión a moneda nacional:
            Para efectos de la colocación, pago de intereses y amortización, la conversión a moneda
            nacional se realiza al valor de la UDI vigente el día en que se hacen las liquidaciones
            correspondientes.'
        """
        try:
            if not fechaInteres: 
                fechaInteres = pd.to_datetime( self._infoBono['TimId'])
            else:
                fechaInteres = pd.to_datetime(fechaInteres)
                
                print(fechaInteres)
            
            conv_UdisPesos = float(self.df_conversion[self.df_conversion['Fecha']== fechaInteres]['SP68257'])
            
            if conv:
                salida = conv_UdisPesos*valor
            else:
                salida =  valor/conv_UdisPesos
            
            self._ValCalBono['ConvertirUdisPesos'] = {'valor':valor,
                                                'conv':conv,
                                                'fechaInteres':fechaInteres,
                                                'conv_UdisPesos':conv_UdisPesos,
                                                'salida':salida}
            return salida
            
        except Exception as e:
            self._ValCalBono['ConvertirUdisPesos'] = {'Error':e}
            print("Error ConvertirUdisPesos ", e)
            return 0
        
    
    def calcPrecioLimpio(self,TC=None,r=None,d=None,K=None,VN=None):
        """
        Calculo del precio limpio
        Entradas:
            TC(float): Tasa cupon anual en decimal, equivalente  a self._infoBono['TasaCupon']/100
            r(float):  rendimiento a vencimiento anual en decimal ,Tasa de interés relevante para descontar el cupón.
                        equivalente a self._infoBono['TasaDeRendimiento']/100
            d (int): Número de días transcurridos del cupón vigente, equvalente a self._infoBono['DiasTranscCpn']
            k (int): Número de cupones por liquidar, incluyendo el vigente, equivalente a self._infoBono['CuponesCobrar'] 
            VN (float): Valor nominal del Bono.
        """
        if not TC: TC = self._infoBono['TasaCupon']/100
        if not r: r = self._infoBono['TasaDeRendimiento']/100
        if not d: d = self.calcular_dias_ultimo_cupon() 
        if not K: K = len(self.calcular_fechas_cupon()) - 1
        if not VN: VN = self._infoBono['ValorNominal'] 
        
    
        def calc_C(TC,VN):
            return VN*182*TC/360
    
        def calc_R(r):
            return r*182/360
        
        C = calc_C(TC,VN) 
        R = calc_R(r)
        
        num1 = 1/R - 1/(R*(1+R)**(K-1))
        num2 = VN/((1+R)**(K-1))
        den = (1+R)**(1-d/182)
        
        PrecioLimpioUdis = (C + C*num1+num2)/den - C*d/182
        
        PrecioLimpioMXN = self.ConvertirUdisPesos(PrecioLimpioUdis)
        
        self._ValCalBono['PrecioLimpio'] = {'PrecioLimpio':PrecioLimpioMXN,
                                            'PrecioLimpioUDIS':PrecioLimpioUdis,
                                            'TasaCupon':TC,
                                            'TasaDeRendimiento':r,
                                            'DiasTranscCpn':d,
                                            'CuponesCobrar':K,
                                            'ValorNominal':VN}
        return   round(PrecioLimpioMXN,6)
    
    
    
    def calcRendimiento(self,PrecioLimpio=None,TC=None,d=None,K=None):
        """
        Por revisar
        Entrada:
            PrecioLimpio(float): Valor precio limpio en pesos MXN
            
        """
        if not PrecioLimpio: 
            PrecioLimpioMXN = self._infoBono['PrecioLimpio']
            PrecioLimpio = self.ConvertirUdisPesos(PrecioLimpioMXN, False)
        
        if not TC: TC = self._infoBono['TasaCupon']/100
        if not d: d = self.calcular_dias_ultimo_cupon() 
        if not K: K = len(self.calcular_fechas_cupon()) - 1
    
        def rendimientoVencimiento(PrecioLimpio,TC,d,K):
            def calcular_precio_limpio(TC,r,d,K,VN=100):
                def calc_C(TC,VN=100):
                    return VN*182*TC/360
                def calc_R(r):
                    return r*182/360
                C = calc_C(TC,VN) 
                R = calc_R(r)
                num1 = 1/R - 1/(R*(1+R)**(K-1))
                num2 = VN/((1+R)**(K-1))
                den = (1+R)**(1-d/182)
                return (C + C*num1+num2)/den - C*d/182
    
            # Definicion de función objetivo que encuentra la tasa de rendimiento
            def objetivo(r):
                return calcular_precio_limpio(TC,r,d,K) - PrecioLimpio

            # Encontrar la tasa de rendimiento utilizando scipy.optimize.newton
            # Suponemos siempre una tasa inicial del 10%
            tasa_rendimiento = optimize.newton(objetivo, 0.1)  
            return tasa_rendimiento
    
    
        tasa_rendimiento = rendimientoVencimiento(PrecioLimpio,TC,d,K)
    
        self._ValCalBono['PrecioLimpio'] = {'PrecioLimpio':PrecioLimpioMXN,
                                            'PrecioLimpioUDIS':PrecioLimpio,
                                            'TasaCupon':TC,
                                            'TasaDeRendimiento':tasa_rendimiento,
                                            'DiasTranscCpn':d,
                                            'CuponesCobrar':K}
        
        return round(tasa_rendimiento*100,3)
    
    
    
    def CalcRegresos(self, TasaReporto, plazoReporto,PrecioSucio = None,r = None,t = None,VN = None):
        """
        Calculos para regresos, calcula el valor futuro del precio del CETE con la tasa de reporto 
        y por el lapso del prestamo a reporto.
        Entradas : 
            - TasaReporto (float): Tasa de reporto en %
            - plazoReporto (int): Cantidad de dias del prestamo a reporto
            - PrecioSucio (float, optional): Se toma de la informacion de Bono
                                    (En caso de CETES es el mismo precio limpio)
            - Rendimiento (float, optional): rendimiento anual esperado por el inversionista en %.
            - t (int, optional): El período en días hasta el vencimiento del bono
            - VN (float, optional): Valor nominal del bono.
        """
        if not PrecioSucio: PrecioSucio = self._infoBono['PrecioSucio'] 
        if not r: r = self._infoBono['TasaDeRendimiento']/100 
        if not t: t = (self._infoBono['FechaVcto'] - self._infoBono['TimId'] ).days
        if not VN: VN = self._infoBono['ValorNominal'] 
        
        
        
        
        def PrecioFuturo(Precio,TasaReporto, plazoReporto):
            return ((1+TasaReporto/360)**plazoReporto)*Precio
        
        TasaReporto = TasaReporto/100
        
        PrecioSucioReporto = PrecioFuturo(PrecioSucio,TasaReporto, plazoReporto)
        #RendimientoReporto = self.calcRendimiento(PrecioSucioReporto)
        
        self._ValCalBono['PrecioSucioReporto'] = {'TasaReporto':TasaReporto ,
                                                  'plazoReporto': plazoReporto,
                                                  'PrecioSucio':PrecioSucio,
                                                  'TasaDeRendimiento':r,
                                                  'PlazoEmision':t,
                                                  'ValorNominal':VN}
        
        return PrecioSucioReporto# , RendimientoReporto



