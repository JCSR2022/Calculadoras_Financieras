# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:17:38 2023

@author: jhona

Descripción técnica de los BONOS de desarrollo del gobierno federal con tasa de interés fija:

Los Bonos de Desarrollo del Gobierno Federal con Tasa de Interés Fija (BONOS) son emitidos y
colocados a plazos mayores a un año, pagan intereses cada seis meses y, a diferencia de los
BONDES, la tasa de interés se determina en la emisión del instrumento y se mantiene fija a lo largo
de toda la vida del mismo. 

- **Valor Nominal (VN):** El valor nominal del bono = 100 (cien pesos)
- **Período de Interés (Nj):** Los títulos devengan intereses en pesos cada seis meses. Esto es, cada 182 días o al plazo que sustituya a éste en caso de días inhábiles (Plazo en días del cupón J).
- **Tasa de interés anual del cupón (TC):**  La tasa de interés que pagan estos títulos es fijada por el Gobierno Federal en la emisión de la serie.
- **Intereses por pagar al final del periodo J (Ij):** Los intereses se calculan considerando los días efectivamente transcurridos entre las fechas de pago de los mismos, tomando como base años de 360 días, y se liquidan al finalizar cada uno de los períodos de interés.

"""
from INVEX_calc_Bonos import Bono
#import scipy.optimize as optimize

class M_TasaFija(Bono):
    
    
    def calcPrecioLimpio(self, TC = None, r = None,d = None, VN=None, Nj=None):
        """
        Calcula el precio limpio de un bono a tasa fija.
    
        Entradas:
            - TC (float): Tasa de interés anual del bono en decimal.
            - r (float): rendimiento anual esperado por el inversionista en decimal.
            - d (int): Número de días transcurridos del cupón vigente, equvalente a self._infoBono['DiasTranscCpn']
            - VN (float,): Valor nominal del bono. Valor por defecto: 100.
            - Nj (int): Número de días en cada período de cupón. 
    
        Salida:
            Precio limpio del bono.
        """
        # ----- Valores entrada datos: -------------
        diasAño = self.days_year
        if not TC: TC =  self._infoBono['TasaCupon']/100
        if not r: r = self._infoBono['TasaDeRendimiento']/100
        if not d: d = self.calcular_dias_ultimo_cupon() 
        if not VN: VN = self._infoBono['ValorNominal']
        if not Nj: Nj = self._infoBono['FrecCpn']
        
        # Número de cupones por liquidar, incluyendo el vigente  
        K = self.Num_cupones_por_liquidar()
        # --------------------------------------------
        
        def calcular_Cj(TC, VN, Nj,diasAño):
            return VN * Nj * TC / diasAño
    
        def calcular_R(r,Nj,diasAño):
            return r * Nj / diasAño
        
        def calcular_interes_devengado(TC, d, VN,diasAño):
            return VN * d * TC / diasAño
    
        def calcular_precio_simple(C, R, K, d, VN, Nj):
            """ 
            Cálculo del precio limpio de un bono a tasa fija según la fórmula (2) del APÉNDICE 2A
            Descripción técnica de los BONOS de desarrollo del gobierno federal con tasa de interés fija.
              
            """
            return (C + C * (1 / R - 1 / (R * (1 + R)**(K-1))) + VN / (1 + R)**(K-1)) / ((1 + R)**(1 - d / Nj)) - C * d / Nj
        
        C = calcular_Cj(TC,VN,Nj,diasAño)
        
        R = calcular_R(r,Nj,diasAño) 
        
        PrecioLimpio = calcular_precio_simple(C, R, K, d,VN,Nj)
   
        self._ValCalBono['PrecioLimpio'] = {'PrecioLimpio':PrecioLimpio,
                                            'TasaCupon':TC,
                                            'TasaDeRendimiento':r,
                                            'DiasTranscCpn':d,
                                            'CuponesCobrar':K,
                                            'FrecCpn':Nj,
                                            'ValorNominal':VN}
        return round(PrecioLimpio,6)
    


    def calcRendimiento(self, PrecioLimpio=None,TC=None,d=None,VN=None,Nj=None):
        """
        Calcula la tasa de rendimiento dado el Precio Limpio y la Sobretasa.
    
        Entradas:
            PrecioLimpio (float): Valor precio limpio en pesos MXN.
            s (float): Sobretasa expresada en porcentaje [%].
    
        Salida:
            Tasa de Rendimiento calculada.
        """
        diasAño = self.days_year
        if not PrecioLimpio: PrecioLimpio = self._infoBono['PrecioLimpio']
        if not TC: TC =  self._infoBono['TasaCupon']/100
        if not d: d = self.calcular_dias_ultimo_cupon() 
        if not VN: VN = self._infoBono['ValorNominal']
        if not Nj: Nj = self._infoBono['FrecCpn']    
        K = self.Num_cupones_por_liquidar()
    
        # Precisión deseada para la convergencia
        precision = 1e-6
    
        # Límites iniciales para la bisección 
        a = 0.01
        b = 0.2
        
        # Version resumida de funcion utilizada
        def calcPrecioLimpio(TC, r,d,K, VN, Nj,diasAño):
            """
            Calcula el precio limpio de un bono a tasa fija.
     
            """        
            def calcular_Cj(TC, VN, Nj,diasAño): return VN * Nj * TC / diasAño
            def calcular_R(r,Nj,diasAño): return r * Nj / diasAño
            def calcular_interes_devengado(TC, d, VN,diasAño): return VN * d * TC / diasAño
            
            def calcular_precio_simple(C, R, K, d, VN, Nj):
                return (C + C * (1 / R - 1 / (R * (1 + R)**(K-1))) + VN / (1 + R)**(K-1)) / ((1 + R)**(1 - d / Nj)) - C * d / Nj
            C = calcular_Cj(TC,VN,Nj,diasAño)
            R = calcular_R(r,Nj,diasAño) 
            PrecioLimpio = calcular_precio_simple(C, R, K, d,VN,Nj)
            return PrecioLimpio
    
    
        def objetivo(r):
            return calcPrecioLimpio(TC, r,d,K, VN, Nj,diasAño) - PrecioLimpio
    
        # Bisección
        while (b - a) / 2 > precision:
            c = (a + b) / 2
            
            
            if objetivo(c) == 0:
                break
            if objetivo(c) * objetivo(a) < 0:
                b = c
            else:
                a = c
                
        tasa_rendimiento = (a + b) / 2
        
        self._ValCalBono['TasaDeRendimiento'] = {'PrecioLimpio':PrecioLimpio,
                                            'TasaCupon':TC,
                                            'TasaDeRendimiento':tasa_rendimiento,
                                            'DiasTranscCpn':d,
                                            'CuponesCobrar':K,
                                            'FrecCpn':Nj,
                                            'ValorNominal':VN}
        return round(tasa_rendimiento*100, 3)
    
    
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
        
        self._ValCalBono['PrecioSucioReporto'] = {'TasaReporto':TasaReporto ,
                                                  'plazoReporto': plazoReporto,
                                                  'PrecioSucio':PrecioSucio,
                                                  'TasaDeRendimiento':r,
                                                  'PlazoEmision':t,
                                                  'ValorNominal':VN}
        return PrecioSucioReporto
    