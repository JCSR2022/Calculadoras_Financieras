# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 06:21:43 2023

@author: EXT_JSANTA
"""


from INVEX_calc_Bonos import Bono

#import pandas as pd
#import numpy as np
#from datetime import  timedelta

class IM_bpag28(Bono):
    
    def __init__(self, infoBono = {}, archivo= None):
        """
        Constructor de la clase BPAG28
        Args:
            La complicacion de los bonos BPAG es que su TC es el maximo entre 
            Tasa Cetes y Tasa de fondeo, sin embargo ese calculo no se hara
            por que se tomara la TC dircto del Vector.
        """
        super().__init__(infoBono)  # Llama al constructor de la clase Bono
        
        try:
            # Calculo constante ajuste off set precio calculo y vector.
            PrecioLimpioVector = self._infoBono['PrecioLimpio']
            r = self._infoBono['TasaDeRendimiento']
            s = self._infoBono['Sobretasa'] 
            TC = self._infoBono['CuponActual']
            Nj = self._infoBono['FrecCpn']
            VN = self._infoBono['ValorNominal']
            d = self.calcular_dias_ultimo_cupon() 
            K = self.Num_cupones_por_liquidar()
            PcalcVector=  self.precioLimpio(r,s,TC,d,K,Nj,VN)
            ctte = PrecioLimpioVector - PcalcVector
            self.ctte = ctte
            
        except Exception as e:
            print("Error init: ", e)
            self.df_tabla_ri = e
            
         

    
    def precioLimpio(self,r,s,TC,d,K,Nj,VN):
        """
        Entradas:
            - r (float): Rendimiento anual esperado por el inversionista expresada en porciento[%]. En vector'TasaDeRendimiento'
            - s (float): Sobretasa expresada en porciento[%] con redondeo dos decimales. En vector 'Sobretasa'
            - TC(float) = Tasa de interés anual del cupón J para el periodo Nj, expresada en términos porcentuales [%] con
                    redondeo a dos decimales. self._infoBono['TasaCupon']
            - d (int): Número de días transcurridos del cupón vigente, vector 'DiasTranscCpn'
            - K (int): Número de cupones por liquidar, incluyendo el vigente, vector 'CuponesCobrar'
            - VN (int): Valor nominal del bono. Valor por defecto: 100. Vector: 'ValorNominal'
            - Nj (int): Número de días en cada período de cupón.  Vector: 'FrecCpn'
        """
        
        def calcCj(TI1,Nj,VN):
            return VN*Nj*TI1/(360*100)
        
        def calcR(TI,s,Nj):
            return (TI + s)*Nj/(360*100)

        def calcP(C1,C,R,K,d,Nj,VN):
            term1 = C*( (1/R) - (1 / (R * (1+ R)**(K-1) ) ) )
            term2 = VN / ((1+R)**(K-1))
            den = (1+R)**(1-d/Nj)
            return (C1 + term1 + term2)/den -C1*d/Nj
        
        C1 = calcCj(TC,Nj,VN)
        C = calcCj(r,Nj,VN)
        R = calcR(r,s,Nj)
        precioLimpio = calcP(C1,C,R,K,d,Nj,VN)
        
        self._ValCalBono['calc_Precio_Limpio_preliminar'] ={ 
                                               'r':r,
                                               's':s,
                                               'TC':TC,
                                               'd':d,
                                               'K':K,
                                               'VN':VN,
                                               'Nj':Nj,
                                               'C':C,
                                               'C1':C1,
                                               'R':R,
                                               'PrecioLimpio':precioLimpio}
        return precioLimpio
    
    
    def calcPrecioLimpio(self):
        
        r = self._infoBono['TasaDeRendimiento']
        s = self._infoBono['Sobretasa'] 
        TC = self._infoBono['CuponActual']
        Nj = self._infoBono['FrecCpn']
        VN = self._infoBono['ValorNominal']
        d = self.calcular_dias_ultimo_cupon() 
        K = self.Num_cupones_por_liquidar()

        return self.precioLimpio(r,s,TC,d,K,Nj,VN)+ self.ctte 
    
    
    def calc_IntDev(self,TCj,d,VN):
        """
        Intereses se calculan considerando los días efectivamente transcurridos entre las
        fechas de pago de los mismos, tomando como base años de 360 días, y se liquidan al
        finalizar cada uno de los períodos de interés
        entrada:
            - TCj (float): Tasa de interés anual devengada, expresada en porciento[% ]con redondeo dos decimales. En vector 'CuponActual'
            - d (int): Número de días transcurridos del cupón vigente, vector 'DiasTranscCpn'
            - VN (float,): Valor nominal del bono. Valor por defecto: 100.
        Salida:
            Ij(Float) = Intereses por pagar al final del periodo J.
        """
        diasAño = 360
        Ij = VN*d*TCj/(diasAño*100)
        
        self._ValCalBono['calcInteres'] = {'TCj':TCj, 'd':d,'VN':VN,'Ij':Ij }
        return Ij
    
    
    def  precioSucio(precioLimpio,Interesdevengado):
        return precioLimpio+Interesdevengado
        
    
    
    def rendimiento(self,P,s,TC,d,K,Nj,VN):
        
        # Precisión deseada para la convergencia
        precision = 1e-6
        
        # Límites iniciales para la bisección
        a = -10000
        b = 10000
    
        def objetivo(x):
            return  self.precioLimpio(x,s,TC,d,K,Nj,VN) +self.ctte - P  
    
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
        
        
        self._ValCalBono['rendimiento'] = {
                                    'P': P,
                                    's': s,
                                    'TC': TC,
                                    'd': d,
                                    'K': K,
                                    'Nj': Nj,
                                    'VN': VN,
                                    'tasa_rendimiento': tasa_rendimiento
                                    }
        return tasa_rendimiento
        
        
    
    
    def calcRendimiento(self,precio =None):
        """
        Calcula la tasa de rendimiento dado el Precio Limpio, utilizando la funcion de precio limpio
        PrecioLimpioAjustado(r,PrecioLimpioVector,rvector,s,TCdev_Calc,Idev_Calc,d_Calc,K_Calc,VN,FrecCpn) y el metodo numerico de biseccion. 
        Entradas:
            - P (float): Valor precio limpio en pesos MXN.
            - s (float): Sobretasa expresada en porciento[%] con redondeo dos decimales. En vector 'Sobretasa'
            - TC (float): Tasa de interés anual devengada, expresada en porciento[% ]con redondeo dos decimales. En vector 'CuponActual'
            - d (int): Número de días transcurridos del cupón vigente, vector 'DiasTranscCpn'
            - K (int): Número de cupones por liquidar, incluyendo el vigente, vector 'CuponesCobrar'
            - VN (int): Valor nominal del bono. Valor por defecto: 100. Vector: 'ValorNominal'
            - Nj (int): Número de días en cada período de cupón.  Vector: 'FrecCpn'
            
        Salida:
            r (float): Rendimiento anual esperado por el inversionista expresada en porciento[%]. En vector'TasaDeRendimiento'
        """
        
        if not precio: 
            P = self._infoBono['PrecioLimpio'] 
        else: 
            P = precio

        s = self._infoBono['Sobretasa'] 
        TC = self._infoBono['CuponActual']
        Nj = self._infoBono['FrecCpn']
        VN = self._infoBono['ValorNominal']
        d = self.calcular_dias_ultimo_cupon() 
        K = self.Num_cupones_por_liquidar()

        
        
        salida = self.rendimiento(P,s,TC,d,K,Nj,VN)
        
        return salida
        
     
    
    
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


# -------------------------------------------------------------------------------------
def Chequeo():   
    
    BonoEnEvaluacion = IM_bpag28()
    
    
    #Ejmplo  Serie: 250206  TmId:20231005
    BonoEnEvaluacion.modInfoBono({'TasaDeRendimiento': 11.4})
    BonoEnEvaluacion.modInfoBono({ 'Sobretasa': 0.16  })
    BonoEnEvaluacion.modInfoBono({ 'CuponActual': 11.23  })
    BonoEnEvaluacion.modInfoBono({ 'DiasTranscCpn': 14  })
    BonoEnEvaluacion.modInfoBono({ 'CuponesCobrar': 18  })
    BonoEnEvaluacion.modInfoBono({ 'FrecCpn':  28 })
    BonoEnEvaluacion.modInfoBono({ 'ValorNominal':  100 })
    print(BonoEnEvaluacion.verInfoBono())
    print("Serie: 250206  TmId:20231005, precioLimpio:",BonoEnEvaluacion.calcPrecioLimpio(), "esperado:",99.797742 )
    


    #Ejemplo norma
    r = 4.45        
    s = 0.20
    TC = 4.47
    d = 21    
    K = 39
    Nj =28
    VN = 100
    print("Ejemplo Norma: precioLimpio= ", BonoEnEvaluacion.precioLimpio(r,s,TC,d,K,Nj,VN)," Val esp: ", 99.44553)
    
    
    
    

def main():
    try:
        Chequeo()
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    main()
