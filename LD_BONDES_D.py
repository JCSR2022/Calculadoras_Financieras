# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 06:26:54 2023

@author: jhona
"""

from INVEX_calc_Bonos import Bono

import pandas as pd
import numpy as np
from datetime import  timedelta

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
            
            
            
            Fechas = self.calcular_fechas_ultimo_cupon()
            FrecCpn = self._infoBono['FrecCpn']
            FechaInteres =  self._infoBono['TimId']
            df_tabla_ri = self.df_tabla_ri
            tabla_ri = self.hallar_tabla_ri_fechas(Fechas, df_tabla_ri,FechaInteres,FrecCpn)
            valor_TCdev = self.calc_TCdev(tabla_ri) 
            VN = self._infoBono['ValorNominal']
            d_calc = self.calcular_dias_ultimo_cupon() 
            Idev =  self.calc_Interes(valor_TCdev,d_calc,VN)
            s = self._infoBono['Sobretasa'] 
            K = self.Num_cupones_por_liquidar()
            rvector = self._infoBono['TasaDeRendimiento']
            PrecioLimpioVector = self._infoBono['PrecioLimpio']
            tabla_ri = self.hallar_tabla_ri_fechas(Fechas, df_tabla_ri,FechaInteres,FrecCpn)
            valor_TCdev = self.calc_TCdev(tabla_ri) 
            PcalcVector= self.calc_Precio_Limpio_preliminar(rvector,s,valor_TCdev,Idev,d_calc,K,VN,FrecCpn)
            ctte = PrecioLimpioVector - PcalcVector
            self.ctte = ctte
            
        except Exception as e:
            print("Error init: ", e)
            self.df_tabla_ri = e
            
         
            
    
    def hallar_tabla_ri_fechas(self,fechas,df_tabla_ri,fechaInc,FrecCpn=28):
        """
        Encuentra los ri para cada 'Fecha' de la lista fechas 
        en el DataFrame 'df_tabla_ri' en la columna 'Fecha'.
        Si la 'Fecha' no se encuentra, busca en 'df_tabla_ri' la fecha 
        más cercana y devuelve ri.
        Args:
            fechas [list (pandas._libs.tslibs.timestamps.Timestamp)]: fechas a encontrar.
            df_tabla_ri (pd.DataFrame): El DataFrame que contiene los datos.
        Returns:
            ri: lista con los valores de ri para las fechas    """
        
        def Encuentra_ri_fecha(Fecha, df_tabla_ri):
            """
            Encuentra ri para la fecha 
            Args:
                Fecha (pandas._libs.tslibs.timestamps.Timestamp): La fecha a encontrar.
                df_tabla_ri (pd.DataFrame): El DataFrame que contiene los datos.
            Returns:
                ri para fecha
            """
            # Asegurar'Fecha' sea de tipo datetime
            df_tabla_ri['Fecha'] = pd.to_datetime(df_tabla_ri['Fecha'])
    
            # Ordenar el DataFrame por la columna 'Fecha' para facilitar la búsqueda
            df_tabla_ri = df_tabla_ri.sort_values(by='Fecha')
    
            # Intentar encontrar la fecha exacta
            exact_match = df_tabla_ri[df_tabla_ri['Fecha'] == Fecha]
    
            if not exact_match.empty:
                # Si se encuentra una coincidencia exacta, devolverla
                fecha = exact_match.iloc[0]['Fecha']
            else:
                # Si no se encuentra una coincidencia exacta, 
                # buscar la fecha más cercana anterior a 'Fecha'
                fecha = df_tabla_ri[df_tabla_ri['Fecha'] < Fecha].iloc[-1]['Fecha']
                
            ri = float(df_tabla_ri[df_tabla_ri['Fecha'] == fecha]['ri'])
            return ri
        
        # si no hay fechas, el ri no es vacio, sino por el contrario se colocan todos los ri para
        # el calculo de la TC del ultimo cupon.
        if not fechas:
            fechas = [fechaInc - timedelta(days=i+1) for i in range(FrecCpn)]
        
        ri = []
        for fecha in fechas:
            fecha = pd.to_datetime(fecha)
            ri.append(Encuentra_ri_fecha(fecha, df_tabla_ri)) 
        
        
        self._ValCalBono['hallar_tabla_ri_fechas'] = {'fechas':fechas ,
                                                  'df_tabla_ri': df_tabla_ri,
                                                  'fechaInc':fechaInc,
                                                  'FrecCpn':FrecCpn,
                                                  'ri':ri}
        return ri
    
    
    
    def calc_TCdev(self,ri):
        """
        Tasa de interés anual devengada
        Entradas:
            ri =  vector con la tasa de interes diaria para los dias del 
            periodo en analisis
        Salida:
            TCdev: (float) Tasa de interés anual devengada, expresada en porciento[%] 
            con redondeo a dos decimales.
        """
        diasAño = 360
        ri = np.array(ri)
        d = len(ri)
        TCdev = (np.prod(1 + ri / (diasAño*100))-1) * (diasAño*100)/d
        salida = float(TCdev)
        
        self._ValCalBono['calcTCdev'] = {'ri':ri, 'TCdev':salida}
        return salida
    
    
    
    def calc_Interes(self,TCj,Nj,VN):
        """
        Intereses se calculan considerando los días efectivamente transcurridos entre las
        fechas de pago de los mismos, tomando como base años de 360 días, y se liquidan al
        finalizar cada uno de los períodos de interés
        entrada:
            - TCJ(float) = Tasa de interés anual del cupón J para el periodo Nj, expresada en términos porcentuales [%] con
                    redondeo a dos decimales.
            - Nj (int): Número de días en período de cupón.
            - VN (float,): Valor nominal del bono. Valor por defecto: 100.
        Salida:
            Ij(Float) = Intereses por pagar al final del periodo J.
        """
        diasAño = 360
        
        Ij = VN*Nj*TCj/(diasAño*100)
        
        self._ValCalBono['calcInteres'] = {'TCj':TCj, 'Nj':Nj,'VN':VN,'Ij':Ij }
        return Ij
    
    
    def calc_Precio_Limpio_preliminar(self,r,s,TCdev,Idev,d,K,VN,Nj):
        """   Calcula el precio limpio de un bono a tasa fija.
        
            Entradas:
                - r (float): Rendimiento anual esperado por el inversionista expresada en porciento[%]. En vector'TasaDeRendimiento'
                - s (float): Sobretasa expresada en porciento[%] con redondeo dos decimales. En vector 'Sobretasa'
                - TCdev (float): Tasa de interés anual devengada, expresada en porciento[% ]con redondeo dos decimales. En vector 'CuponActual'
                - Idev (float) : Interes devengado en el periodo d. 
                - d (int): Número de días transcurridos del cupón vigente, vector 'DiasTranscCpn'
                - K (int): Número de cupones por liquidar, incluyendo el vigente, vector 'CuponesCobrar'
                - VN (int): Valor nominal del bono. Valor por defecto: 100. Vector: 'ValorNominal'
                - Nj (int): Número de días en cada período de cupón.  Vector: 'FrecCpn'
        """
        
        def CalcTC1(r,TCdev,d,Nj,diasAño):
            #Tasa anual esperada para el siguiente pago de intereses
            term1 = (1 + TCdev*d/(diasAño*100))
            term2 = (1+ r/(diasAño*100))**(Nj-d)
            #return round((term1 * term2 - 1) * (diasAño*100 / Nj),2)
            return (term1 * term2 - 1) * (diasAño*100 / Nj)
        
        def CalcTC(r,Nj,diasAño):
            #Tasa anual esperada para los pagos de intereses 2,3,…,K
            term1 = ( 1 + r/(diasAño*100))**Nj - 1 
            #return round(term1*diasAño*100/Nj,2)
            return term1*diasAño*100/Nj
        
        def calcular_Cj(TCj, VN, Nj ,diasAño):
            # Monto esperado del pago de intereses para el periodo j 
            return VN * Nj * TCj / (diasAño*100)
        
        def calcular_R(r,s,Nj,diasAño):
            #return round((1+(r+s)/(diasAño*100))**Nj-1,4)
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
            return P
            
        diasAño = 360
    
        TC = CalcTC(r,Nj,diasAño)
    
        TC1 = CalcTC1(r,TCdev,d,Nj,diasAño)
    
        C = calcular_Cj(TC,VN,Nj,diasAño)
    
        C1 = calcular_Cj(TC1,VN,Nj,diasAño)
    
        R = calcular_R(r,s,Nj,diasAño) 

        PrecioLimpio = calcular_precio_simple(C,C1,R, K, d,Idev,VN,Nj)
        
        
    
        
        self._ValCalBono['calc_Precio_Limpio_preliminar'] ={ 'r':r,
                                               's':s,
                                               'TCdev':TCdev,
                                               'Idev':Idev,
                                               'd':d,
                                               'K':K,
                                               'VN':VN,
                                               'Nj':Nj,
                                               'TC':TC,
                                               'TC1':TC1,
                                               'C':C,
                                               'C1':C1,
                                               'R':R,
                                               'PrecioLimpio':PrecioLimpio}
        
        
        return PrecioLimpio  
    
    
    
    def Precio_Limpio_Ajustado(self,r,s,TCdev,Idev,d,K,VN,FrecCpn):
        """Funcion para ajustar el calculo del precio con el offset del PrecioLimpioVector"""
        
        salida = self.calc_Precio_Limpio_preliminar(r,s,TCdev,Idev,d,K,VN,FrecCpn) + self.ctte

        return salida
        
        
        
    def calcPrecioLimpio(self):
        
        Fechas = self.calcular_fechas_ultimo_cupon()
        FrecCpn = self._infoBono['FrecCpn']
        FechaInteres =  self._infoBono['TimId']
        df_tabla_ri = self.df_tabla_ri
        tabla_ri = self.hallar_tabla_ri_fechas(Fechas, df_tabla_ri,FechaInteres,FrecCpn)
        
        valor_TCdev = self.calc_TCdev(tabla_ri) 
        
        VN = self._infoBono['ValorNominal']
        d_calc = self.calcular_dias_ultimo_cupon() 
        Idev =  self.calc_Interes(valor_TCdev,d_calc,VN)
        
        r = self._infoBono['TasaDeRendimiento']
        s = self._infoBono['Sobretasa'] 
        K_Calc = self.Num_cupones_por_liquidar()


        PrecioLimpio_Calc_final = self.Precio_Limpio_Ajustado(r,s,valor_TCdev,Idev,d_calc,K_Calc,VN,FrecCpn)
        
        self._ValCalBono['Precio_Limpio_Ajustado'] = {
                            'Fechas': Fechas,
                            'FrecCpn': FrecCpn,
                            'FechaInteres': FechaInteres,
                            'df_tabla_ri': df_tabla_ri,
                            'tabla_ri': tabla_ri,
                            'valor_TCdev': valor_TCdev,
                            'VN': VN,
                            'd_calc': d_calc,
                            'Idev': Idev,
                            'r': r,
                            's': s,
                            'K_Calc': K_Calc,
                            'PrecioLimpio_Calc_final': PrecioLimpio_Calc_final
}
        
        return PrecioLimpio_Calc_final
    
    
    
    def calcRendimiento(self):
        """
        Calcula la tasa de rendimiento dado el Precio Limpio, utilizando la funcion de precio limpio
        PrecioLimpioAjustado(r,PrecioLimpioVector,rvector,s,TCdev_Calc,Idev_Calc,d_Calc,K_Calc,VN,FrecCpn) y el metodo numerico de biseccion. 
        Entradas:
            - P (float): Valor precio limpio en pesos MXN.
            - s (float): Sobretasa expresada en porciento[%] con redondeo dos decimales. En vector 'Sobretasa'
            - TCdev (float): Tasa de interés anual devengada, expresada en porciento[% ]con redondeo dos decimales. En vector 'CuponActual'
            - Idev (float) : Interes devengado en el periodo d. 
            - d (int): Número de días transcurridos del cupón vigente, vector 'DiasTranscCpn'
            - K (int): Número de cupones por liquidar, incluyendo el vigente, vector 'CuponesCobrar'
            - VN (int): Valor nominal del bono. Valor por defecto: 100. Vector: 'ValorNominal'
            - FrecCpn (int): Número de días en cada período de cupón.  Vector: 'FrecCpn'
            
        Salida:
            r (float): Rendimiento anual esperado por el inversionista expresada en porciento[%]. En vector'TasaDeRendimiento'
        """
        
        P = self._infoBono['PrecioLimpio']
        s = self._infoBono['Sobretasa'] 
        
        Fechas = self.calcular_fechas_ultimo_cupon()
        FrecCpn = self._infoBono['FrecCpn']
        FechaInteres =  self._infoBono['TimId']
        df_tabla_ri = self.df_tabla_ri
        tabla_ri = self.hallar_tabla_ri_fechas(Fechas, df_tabla_ri,FechaInteres,FrecCpn)
        TCdev_Calc = self.calc_TCdev(tabla_ri) 
        
        VN = self._infoBono['ValorNominal']
        d_calc = self.calcular_dias_ultimo_cupon() 
        Idev_Calc =  self.calc_Interes(TCdev_Calc,d_calc,VN)
        K_Calc = self.Num_cupones_por_liquidar()
        
        # Precisión deseada para la convergencia
        precision = 1e-6
        # Límites iniciales para la bisección
        a = -10000
        b = 10000
        def objetivo(x):
            return  self.Precio_Limpio_Ajustado(x,s,TCdev_Calc,Idev_Calc,d_calc,K_Calc,VN,FrecCpn) - P
    
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
        
        
        self._ValCalBono['calcRendimiento'] = {
        'P': P,
        's': s,
        'Fechas': Fechas,
        'FrecCpn': FrecCpn,
        'FechaInteres': FechaInteres,
        'df_tabla_ri': df_tabla_ri,
        'tabla_ri': tabla_ri,
        'TCdev_Calc': TCdev_Calc,
        'VN': VN,
        'd_calc': d_calc,
        'Idev_Calc': Idev_Calc,
        'K_Calc': K_Calc,
        'precision': precision,
        'a': a,
        'b': b,
        'tasa_rendimiento': tasa_rendimiento
    }
        
        
        return tasa_rendimiento
    
    
    
        

   
            
            
            
