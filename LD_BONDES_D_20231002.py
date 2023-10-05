# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 06:26:54 2023

@author: jhona
"""

from INVEX_calc_Bonos import Bono

import pandas as pd
import numpy as np

class LD_BondesD(Bono):
    
    def __init__(self, infoBono = {}, archivo= None):
        """
        Constructor de la clase LD_BondesD.
        Args:
            Se debe tener una tabla con los valores  de Tasa de fondeo bancario, 
            Mediana ponderada por volumen, Tasa de interés en por ciento anual
            publicadas por Banxico, se establece como referencia.
            
            archivo: Nombre/direccion de Archivo preparado 
            con formato .csv con dos columnas: 'Fecha' y valores de ri'
        """
        super().__init__(infoBono)  # Llama al constructor de la clase Bono
        
        try:
            # nombre de archivo modelo para pruebas
            if not archivo: archivo = 'info_Bonos\\df_tabla_ri_14_09_2023.csv'
            self.df_tabla_ri = pd.read_csv(archivo) 
            self.df_tabla_ri['Fecha'] = pd.to_datetime(self.df_tabla_ri['Fecha'])
            
        except:
            self.df_tabla_ri = None
            
    
    def hallar_ri_para_fechas(self,lista_fechas = None, df_tabla_ri=None):
        """Funcion para encontrar los valores de Tasa de fondeo bancario, 
        para las fechas indicadas
        Entrada: 
            lista_fechas: lista de fechas , normalemnte desde ultimo cupon 
            hasta fecha en evaluacion, resultado de self.calcular_fechas_ultimo_cupon()
            df_tabla_ri:  tabla con los valores  de Tasa de fondeo bancario
        
        Salida:
            dataFrame Pandas con fechas y ri para cada fecha
        """
    
        if not df_tabla_ri:  df_tabla_ri = self.df_tabla_ri
        if not lista_fechas:  lista_fechas = self.calcular_fechas_ultimo_cupon()
        
        
        if lista_fechas:
            # Aseguramos que las Fechas a evaluar tengan el mismo formato
            fechas =[pd.to_datetime(fecha) for fecha in lista_fechas]
            ri = []
            # Primer valor de ri, se buscara hasta encontrar el ri a la fecha anterior de no tener ri para esa fecha
            fecha0 = fechas[0]
            while True:
                if df_tabla_ri[df_tabla_ri['Fecha'] == fecha0]['ri'].any():
                    ri.append(float(df_tabla_ri[df_tabla_ri['Fecha'] == fecha0]['ri']))
                    break
                else:
                    fecha0 = fecha0 - np.timedelta64(1, 'D')
            # Para el resto de los valores es parecido, si no existe un ri en la tabla se utilizara un r(i-1):
            for fecha in fechas[1:]:
                if df_tabla_ri[df_tabla_ri['Fecha'] == fecha]['ri'].any():
                    ri.append(float(df_tabla_ri[df_tabla_ri['Fecha'] == fecha]['ri']))
                else:
                    ri.append(ri[-1])
    
            df = pd.DataFrame({"Fecha": lista_fechas, "ri":ri })
        else:
            df = pd.DataFrame({"Fecha": [], "ri":[ ] })
        
        self._ValCalBono['df_Fechas_ri'] = {'df_tabla_ri': df,
                                            'lista_fechas': lista_fechas}
                                            
        return df
        

    def calc_TCdev(self, ri = None):
        """
        Tasa de interés anual devengada
        Entradas:
            ri =  vector con la tasa de interes diaria para los dias del periodo en analisis
        Salida:
            TCdev: (float) Tasa de interés anual devengada, expresada en porciento con redondeo a dos decimales.
        """
        diasAño = self.days_year
        
        if not ri: 
            df_Fechas_ri  = self.hallar_ri_para_fechas()
            ri = np.array(df_Fechas_ri['ri'])
            d = len(ri)
        
        # Si se esta evaluando en el dia del cupon, la TCdev para ese dia es cero
        if d == 0:
            TCdev = 0
        else:
            TCdev = (np.prod(1 + ri / (diasAño*100))-1) * (diasAño*100)/d
        
        
        self._ValCalBono['TCdev'] = {"TCdev": TCdev,
                                     "df_Fechas_ri":df_Fechas_ri}
        return round(float(TCdev),2)
    
    
    def calcInteres(self,TCj,Nj=None,VN=None):
        """
        Intereses se calculan considerando los días efectivamente transcurridos entre las
        fechas de pago de los mismos, tomando como base años de 360 días, y se liquidan al
        finalizar cada uno de los períodos de interés
        entrada:
            - TCJ(float) = Tasa de interés anual del cupón J, expresada en términos porcentuales con
                    redondeo a dos decimales.
            - Nj (int): Número de días en período de cupón.
            - VN (float,): Valor nominal del bono. Valor por defecto: 100.
                    
        Salida:
            Ij(Float) = Intereses por pagar al final del periodo J.
            
        """
        diasAño = self.days_year
        if not VN: VN = self._infoBono['ValorNominal']
        if not Nj: Nj = self._infoBono['FrecCpn']
        
        Ij = VN*Nj*TCj/(diasAño*100)
        return Ij
        
    
    def calcPrecioLimpio(self, r = None,s = None):
        """
        Calcula el precio limpio de un bono a tasa fija.
    
        Entradas:
            - r (float): rendimiento anual esperado por el inversionista expresada en porciento [%].
            - s (float): Sobretasa expresada en porciento [%] con redondeo dos decimales.
            - TCdev (float): Tasa de interés anual devengada, expresada en porciento [%] con redondeo dos decimales.
            - d (int): Número de días transcurridos del cupón vigente, equvalente a self._infoBono['DiasTranscCpn']
            - VN (float,): Valor nominal del bono. Valor por defecto: 100.
            - Nj (int): Número de días en cada período de cupón. 
    
        Salida:
            Precio limpio del bono.
        """
        
        # ----- Valores entrada datos: -------------
       
        if not r: r = self._infoBono['TasaDeRendimiento']
        if not s: s = self._infoBono['Sobretasa']
        
        d = self.calcular_dias_ultimo_cupon() 
        VN = self._infoBono['ValorNominal']
        Nj = self._infoBono['FrecCpn']
        TCdev = self.calc_TCdev()
        diasAño = self.days_year 
        K = self.Num_cupones_por_liquidar()

        # --------------------------------------------
        
        def CalcTC1(r,TCdev,d,Nj,diasAño):
            #Tasa anual esperada para el siguiente pago de intereses
            term1 = (1 + TCdev*d/(diasAño*100))
            term2 = (1+ r/(diasAño*100))**(Nj-d)
            return (term1 * term2 - 1) * (diasAño*100 / Nj)
            
            
        def CalcTC(r,Nj,diasAño):
            #Tasa anual esperada para los pagos de intereses 2,3,…,K
            term1 = ( 1 + r/(diasAño*100))**Nj - 1 
            return term1*diasAño*100/Nj
            
        
        def calcular_Cj(TCj, VN, Nj ,diasAño):
            # Monto esperado del pago de intereses para el periodo j 
            return VN * Nj * TCj / (diasAño*100)
   
    
        def calcular_R(r,s,Nj,diasAño):
            return (1+(r+s)/(diasAño*100))**Nj-1 
            
    
        def calcular_precio_simple(C,C1,R, K, d,Idev,VN,Nj):
            """ 
            Cálculo del precio limpio de un bono a tasa fija según la fórmula (2) del APÉNDICE 2A
            Descripción técnica de los BONOS de desarrollo del gobierno federal con tasa de interés fija.
              
            """
            term1 = C * ( 1/R - 1/(R * ((1 + R)**(K - 1))))
            term2 = VN /((1 + R)**(K - 1))
            den = (1+R)**(1-d/Nj)
            
            P = (C1 + term1 + term2) / den - Idev
            
            return round(P,6)
        
        TC = CalcTC(r,Nj,diasAño)
        
        TC1 = CalcTC1(r,TCdev,d,Nj,diasAño)
        
        C = calcular_Cj(TC,VN,Nj,diasAño)
        
        C1 = calcular_Cj(TC1,VN,Nj,diasAño)
        
        R = calcular_R(r,s,Nj,diasAño) 
        
        Idev = self.calcInteres(TCdev,d)
        
        PrecioLimpio = calcular_precio_simple(C,C1,R, K, d,Idev,VN,Nj)
        
        self._ValCalBono['PrecioLimpio'] = {"TCdev": TCdev,
                                            "Idev":Idev,
                                            "PrecioLimpio":PrecioLimpio,
                                            'DiasTranscCpn': d,
                                            'CuponesCobrar':K,
                                            'TasaDeRendimiento':r,
                                            'Sobretasa':s,
                                            'FrecCpn':Nj,
                                            'ValorNominal':VN
                                            }
        return round(PrecioLimpio,6)  
    
    
    
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
    
    
    

    
    def calcRendimiento(self, PrecioLimpio=None, s=None):
        """
        Calcula la tasa de rendimiento dado el Precio Limpio y la Sobretasa.
    
        Entradas:
            PrecioLimpio (float): Valor precio limpio en pesos MXN.
            s (float): Sobretasa expresada en porcentaje [%].
    
        Salida:
            Tasa de Rendimiento calculada.
        """
        if not PrecioLimpio: PrecioLimpio = self._infoBono['PrecioLimpio']
        if not s: s = self._infoBono['Sobretasa']
    
        # Precisión deseada para la convergencia
        precision = 1e-6
    
        def calcPrecioLimpio(r):
            # ----- Valores entrada datos: -------------
            s = self._infoBono['Sobretasa']
            d = self.calcular_dias_ultimo_cupon() 
            VN = self._infoBono['ValorNominal']
            Nj = self._infoBono['FrecCpn']
            TCdev = self.calc_TCdev()
            diasAño = self.days_year 
            K = self.Num_cupones_por_liquidar()
            # --------------------------------------------
            def CalcTC1(r,TCdev,d,Nj,diasAño):
                #Tasa anual esperada para el siguiente pago de intereses
                term1 = (1 + TCdev*d/(diasAño*100))
                term2 = (1+ r/(diasAño*100))**(Nj-d)
                return (term1 * term2 - 1) * (diasAño*100 / Nj)
            def CalcTC(r,Nj,diasAño):
                #Tasa anual esperada para los pagos de intereses 2,3,…,K
                term1 = ( 1 + r/(diasAño*100))**Nj - 1 
                return term1*diasAño*100/Nj
            def calcular_Cj(TCj, VN, Nj ,diasAño):
                # Monto esperado del pago de intereses para el periodo j 
                return VN * Nj * TCj / (diasAño*100)
            def calcular_R(r,s,Nj,diasAño):
                return (1+(r+s)/(diasAño*100))**Nj-1 
            def calcular_precio_simple(C,C1,R, K, d,Idev,VN,Nj):
                term1 = C * ( 1/R - 1/(R * ((1 + R)**(K - 1))))
                term2 = VN /((1 + R)**(K - 1))
                den = (1+R)**(1-d/Nj)
                P = (C1 + term1 + term2) / den - Idev
                return round(P,6)
            TC = CalcTC(r,Nj,diasAño)
            TC1 = CalcTC1(r,TCdev,d,Nj,diasAño)
            C = calcular_Cj(TC,VN,Nj,diasAño)
            C1 = calcular_Cj(TC1,VN,Nj,diasAño)
            R = calcular_R(r,s,Nj,diasAño) 
            Idev = self.calcInteres(TCdev,d)
            PrecioLimpio = calcular_precio_simple(C,C1,R, K, d,Idev,VN,Nj)
            return PrecioLimpio
        
    # Límites iniciales para la bisección
        a = 6
        b = 14
    
        def objetivo(r):
            return calcPrecioLimpio(r) - PrecioLimpio
    
        # Bisección
        while (b - a) / 2 > precision:
            c = (a + b) / 2
            print(c,objetivo(c),self.calcPrecioLimpio(c))
            if objetivo(c) == 0:
                break
            if objetivo(c) * objetivo(a) < 0:
                b = c
            else:
                a = c
        tasa_rendimiento = (a + b) / 2
    
        self._ValCalBono['TasaDeRendimiento'] = {
                                            "PrecioLimpio":PrecioLimpio,
                                            'TasaDeRendimiento':tasa_rendimiento,
                                            'Sobretasa':s,
                                            }
        
        return round(tasa_rendimiento, 3)
    
    