# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 17:32:06 2023

@author: jhona

**libreria para calcular valores relacionados con bonos CETES. 
Los valores requeridos para el cálculo son:**

- **Valor Nominal (VN):** El valor nominal del bono, igual a 10 en el caso de CETES. En vector INVEX 'ValorNominal'
- **Número de Días (t):** El período en días hasta el vencimiento del bono. En vector INVEX "PlazoEmision".
- **Tasa de Rendimiento (r):** La tasa de rendimiento anualizada del bono en %. En vector INVEX 'TasaDeRendimiento'
- **Tasa de Descuento (b):** La tasa de descuento expresada en decimales, que es una tasa anualizada utilizada 
                            para calcular el precio del bono.No esta en vector INVEX.
- **Precio (P):** El precio del bono.  En vector INVEX 'PrecioLimpio'
- **Descuento (D):** El valor de descuento del bono. No esta en vector INVEX.
"""

from INVEX_calc_Bonos import Bono


class CETES(Bono):
    
    def calcPrecioLimpio(self,r = None,t = None,VN = None):
        """
        Calcula el Precio Limpio de un bono CETES.
        Args:
            r (float, optional): Tasa de rendimiento. 
            t (int, optional): El período en días hasta el vencimiento del bono
            VN (float, optional): Valor nominal del bono. 
        Salida:
            float: El Precio Limpio calculado.
        """
        dias_año = self.days_year
        if not t: t = (self._infoBono['FechaVcto'] - self._infoBono['TimId'] ).days
        if not VN: VN = self._infoBono['ValorNominal'] 
        if not r: r = self._infoBono['TasaDeRendimiento']/100

        P = VN / (1 + r * t / dias_año)
    
        #Se guarada los valores con los que se hizo el calculo
        self._ValCalBono['PrecioLimpio'] = {'PrecioLimpio':P,'TasaDeRendimiento':r,
                                              'PlazoEmision':t,'ValorNominal':VN}
        return round(P,6)
    
    
    def calcRendimiento(self,P = None,t = None,VN = None):
        """
        Calcula la Tasa de Rendimiento de un bono CETES.
        Args:
            P (float, optional): Precio Limpio del bono. 
            t (int, optional): El período en días hasta el vencimiento del bono
            VN (float, optional): Valor nominal del bono.
        Salida:
            float: La Tasa de Rendimiento calculada.
        """
        dias_año = self.days_year
        if not t: t = (self._infoBono['FechaVcto'] - self._infoBono['TimId'] ).days
        if not VN: VN = self._infoBono['ValorNominal'] 
        if not P: P =  self._infoBono['PrecioLimpio'] 
        
        r =((VN/P-1)*dias_año/t)*100
        
        #Se guarada los valores con los que se hizo el calculo
        self._ValCalBono['TasaDeRendimiento'] = {'PrecioLimpio':P,'TasaDeRendimiento':r,
                                              'PlazoEmision':t,'ValorNominal':VN}
        return round(r,3)
    
    
    def calcPlazoEmision(self,P = None,r = None,VN = None):
        """
        Calcula el período en días hasta el vencimiento del bono de un bono CETES.
        Args:
            P (float, optional): Precio Limpio del bono.
            r (float, optional): Tasa de rendimiento.
            VN (float, optional): Valor nominal del bono.
        Salida:
            float: La Tasa de Rendimiento calculada.
        """
        dias_año = self.days_year
        if not r: r = self._infoBono['TasaDeRendimiento']/100
        if not VN: VN = self._infoBono['ValorNominal'] 
        if not P: P =  self._infoBono['PrecioLimpio'] 
        
        PlazoEmision =((VN/P-1)*dias_año/r)*100
        
        #Se guarada los valores con los que se hizo el calculo
        self._ValCalBono['PlazoEmision'] = {'PrecioLimpio':P,
                                            'TasaDeRendimiento':r,
                                            'ValorNominal':VN}
        return round(PlazoEmision,3)
    
    
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
        if not PrecioSucio: PrecioSucio = self._infoBono['PrecioLimpio'] 
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
    
    
    def calcPrecioLimpio_TasaDescuento(self,b,t = None,VN = None):
        """
        Calcula el Precio Limpio de un bono CETES usando la tasa de descuento.
        Args:
            d (float, optional): Tasa de descuento. 
            t (int, optional): El período en días hasta el vencimiento del bono
            VN (float, optional): Valor nominal del bono. 
        Salida:
            float: El Precio Limpio calculado.
        """
        dias_año = self.days_year
        if not t: t = (self._infoBono['FechaVcto'] - self._infoBono['TimId'] ).days
        if not VN: VN = self._infoBono['ValorNominal']
        P = VN * (1 - b * t / dias_año)
    
        #Se guarada los valores con los que se hizo el calculo
        self._ValCalBono['PrecioLimpio'] = {'PrecioLimpio':P,'TasaDescuento':b,
                                              'PlazoEmision':t,'ValorNominal':VN}
        return P
            
    
    
    def calcTasaDescuento(self,r = None,t = None):
        """
        Calcula la Tasa de Descuento de un bono CETES.
        Args:
            r (float, optional): Tasa de rendimiento. 
            t (int, optional): El período en días hasta el vencimiento del bono 
            VN (float, optional): Valor nominal del bono.
        Salida:
            float: La Tasa de Descuento calculada.
        """
        dias_año = self.days_year
        if not t: t = (self._infoBono['FechaVcto'] - self._infoBono['TimId']).days
        if not r: r = self._infoBono['TasaDeRendimiento']/100
        
        b = r/(1+r*t/dias_año)
        
                
        #Se guarada los valores con los que se hizo el calculo        
        self._ValCalBono['TasaDescuento'] = {'TasaDeRendimiento':r,'PlazoEmision':t,
                                              'TasaDescuento':b}        
        return b
    
    def calcDescuento(self,P=None,VN = None):
        """
        Calcula el Descuento de un bono CETES.
        Args:
            P (float, optional): Precio Limpio del bono. 
            VN (float, optional): Valor nominal del bono. 
        Salida:
            float: El Descuento calculado.
        """
        if not VN: VN = self._infoBono['ValorNominal'] 
        if not P: P =  self._infoBono['PrecioLimpio'] 
        
        D = VN-P
        
        #Se guarada los valores con los que se hizo el calculo            
        self._ValCalBono['Descuento'] = {'PrecioLimpio':P,'Descuento':D,'ValorNominal':VN}              
        return D
    
    
    def calcRendimientoEquivalente(self,Pc,r = None,t = None,):
        """
        A partir del rendimiento de un CETE es posible obtener el rendimiento 
        implícito (también conocido como Rendimiento en Curva o Rendimiento Equivalente) 
        del mismo en un diferente plazo a vencimiento de acuerdo a la siguiente fórmula.
        
        entradas:
            r (float) = Tasa de rendimiento original del CETE en decimal.
            t (int)= Período en días hasta el vencimiento, con el que se calcula el rendimiento
            Pc (int) = Plazo en días que se desea cotizar en Curva
        salida:
            rc (float)= Rendimiento en curva o Rendimiento Equivalente en decimal.
        """
        dias_año = self.days_year
        if not r: r = self._infoBono['TasaDeRendimiento']/100
        if not t: t = (self._infoBono['FechaVcto'] - self._infoBono['TimId']).days
        
        rc = ( (1+r*t/dias_año)**(Pc/t) - 1 ) * dias_año/Pc
        #Se guarada los valores con los que se hizo el calculo            
        self._ValCalBono['RendimientoEquivalente'] = {'RendimientoEquivalente':rc,
                                                      'TasaDeRendimiento':r,'PlazoEmision':t}     
        return rc
        
    
    
    
    

def main():
    pass
if __name__ == '__main__':
    main()       
    
    
    