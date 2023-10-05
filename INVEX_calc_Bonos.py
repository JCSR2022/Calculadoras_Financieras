# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:27:44 2023

@author: jhonathan Santacana


Libreria para trabajar con bonos en general
"""

# Libraries to import
from datetime import  timedelta,datetime #, date 
import numpy as np
import pandas as pd
import re
import difflib

class Bono:
    """Clase para el manejo de informacion de los bonos"""

    # Dias en año
    days_year = 360
    
    formatos_fechas = ["%Y%m%d", "%Y/%m/%d", "%d/%m/%Y"]
    
    fechas_entrada = ['TimId','FechaEmision', 'FechaVcto', 'FechaUh', 'FechaPrecioMaximo'
                      ,'FechaPrecioMinimo', 'AuditFecha'] 
    
    enteros_entrada = ['Serie', 'MontoEmitido', 'MontoEnCirculacion', 'PlazoEmision',
                       'ValorNominal', 'DiasTranscCpn', 'CuponesEmision', 'CuponesCobrar',
                       'CambioDiario', 'ValorNominalActualizado', 'AuditId']
    
    decimales_entrada = ['PrecioLimpio', 'PrecioSucio', 'InteresesAcumulados', 'CuponActual', 
                         'Sobretasa', 'Subyacente', 'RendColocacion', 'StColocacion', 'TasaCupon', 
                         'HechoDeMkt', 'PrecioTeorico', 'PostCompra', 'PostVenta', 'YieldCompra', 
                         'YieldVenta', 'SpreadCompra', 'SpreadVenta', 'Bursatilidad', 'CambioSemanal', 
                         'PrecioMax12M', 'PrecioMin12M', 'Suspension', 'Volatilidad', 'Volatilidad2', 
                         'Duracion', 'DuracionMonet', 'Convexidad', 'Vari','DesviacionStand', 'Sensibilidad', 
                         'DuracionMacaulay', 'TasaDeRendimiento', 'DuracionEfectiva']
    
    str_entradas = ['TipoValor', 'Emisora', 'NombreCompleto', 'Sector', 'MonedaEmision', 'FrecCpn', 
                    'ReglaCupon', 'Mdys', 'SandP', 'Liquidez', 'CalificacionFitch', 'HrRatings', 
                    'Isin', 'CalificacionVerum', 'CalificacionDbrs', 'AuditUsuario']
    
    entradas_infoBono = fechas_entrada + enteros_entrada + decimales_entrada + str_entradas
    
   
    def __init__(self, infoBono = {}):
        """
        Constructor de la clase Bonos.
        Args:
            Se debe introducir un diccionario con las claves que se encuentran en 'entradas_infoBono'
            y los valores respectivos para coincidir en framework con el vector de INVEX.
        """
        try:
            # verificar entrada como diccionario
            if isinstance(infoBono, dict):
                if infoBono:
                    #Chequear que los nombres de las variables de entrada
                    infoBono_final = self.check_InfoBono(infoBono)
                    # Ajuste formatos en variables de entrada
                    self.revision_formatos(infoBono_final)
                else:
                    infoBono_final = infoBono
                self._infoBono = infoBono_final
            else:
                self._infoBono = {}
                raise ValueError("Introduzca las variables en forma de diccionario") 
                
                
            # inicializo diccionario donde se alamacenaran resultados de calculos
            self._ValCalBono = {}
        except Exception as e:
                print("Error init: ", e)


    def check_InfoBono(self,dicc):
        """
        Funcion para chequear que los nombres de las variables de entrada en el diccionario que se 
        introduce al instanciar la clase, coinciden con los nombres posibles del vector Invex
        """
        def NormalizadoEntrada(self,dicc):
            """
            Funcion para convertir nombres de calves a formato estandar, por ejemplo:
                'FREC. CPN' en 'FrecCpn'
                'CUPONES X COBRAR' en 'CuponesCobrar'
                segun mejor aproximacion a 'self.entradas_infoBono'
            """
            def NormalizadoClaves(ent):
                entradas_infoBono = self.entradas_infoBono
                # Convertir la entrada a minúsculas y eliminar espacios
                ent = ent.lower().replace(" ", "")
        
                # Buscar la mejor coincidencia en la lista de entradas
                mejor_coincidencia = difflib.get_close_matches(ent, entradas_infoBono, n=1)
        
                if mejor_coincidencia:
                    # Si se encontró una coincidencia cercana, devolverla
                    return mejor_coincidencia[0]
                else:
                    # Si no se encontró una coincidencia cercana, devolver la entrada original
                    return ent
            
            new_dicc = {}
            for key,value in dicc.items():
                new_dicc[NormalizadoClaves(key)] = value
            
            return new_dicc
        

        def RelacionFormatos(dicc):
            """
            Funcion para convertir las claves de un formato diferente al 
            establecido, si aparece un nuevo formato se agregaria a la lista en cada
            elemento del dicc_relacion_formatos.
        
            Entrada:
                infoBono (dicc), con claves que no coinciden con formato establecido
            Salida:
                dicc, con agregado de valores de entrada ajustados a las 
                claves establecidas como formato (al diccionario se le agregan las
                claves conocidas con los valores de las claves desconocidas)
        
            """
            dicc_relacion_formatos = {
                'FECHA': 'TimId',
                'S&P': 'SandP',
                'VAR': 'Vari'}
         
            nuevo_dicc ={}
            for dicckeys,diccvalue in dicc.items():
                if dicckeys in dicc_relacion_formatos.keys():
                    nuevo_dicc[dicc_relacion_formatos[dicckeys]] = diccvalue
                else:
                    nuevo_dicc[dicckeys] = diccvalue
                    
            return nuevo_dicc
     
        try:
            # Correcion con claves conocidas y su relacion con estandar
            dicc = RelacionFormatos(dicc)
            
            #Normalizado calves entrada
            dicc = NormalizadoEntrada(self,dicc)
            
            return dicc
        except Exception as e:
                print("Error RelacionFormatos: ", e)



    def revision_formatos(self,dicc):
        """
        funcion para ajustar los formatos de las variables de entrada
        entrada: diccionario con la informacion del bono (InfoBono)
        salida: Indirecta, se modifica el diccionario en la funcion ajsutando, por ejmplo, 
                las fechas se tendran en formato final  .date()      
        """
        def ajusteFrecCpn(texto):
            """Funcion para obtener numerico en un texto, 
            transforma la entrada str 'Cada XXX dia(s)' en un int XXX 
            de no encontrar texto devuelve la entrada"""
            if isinstance(texto, str):
                patron = r"(\d+)"
                coincidencias = re.findall(patron, texto)
                return int(coincidencias[0])
            else:
                return texto
                
        try:
            #Ajustes formatos numpy general
            for key, val in dicc.items(): 
                if isinstance(val,pd.Timestamp):
                    dicc[key] = val.date()
                if isinstance(val,np.int64):
                    dicc[key] = int(val)
                if isinstance(val,np.float64):
                    dicc[key] = float(val)
            
            #ajustes valores que deben ser enteros
            lista = self.enteros_entrada
            for key, value in dicc.items():
                if key in lista:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                dicc[key] =value        
            
            #ajuste fechas
            formatos_fechas = self.formatos_fechas
            lista = self.fechas_entrada
            for key, value in dicc.items():
                if key in lista:
                    if isinstance(value, int):
                        value = str(value)
                    if isinstance(value, str):
                        for formato in formatos_fechas:
                            try:
                                value = datetime.strptime(value, formato).date()
                                break
                            except ValueError:
                                pass
                    if isinstance(value, datetime):
                        value = value.date()
                    if isinstance(value, np.datetime64):
                        value = value.item()
                dicc[key] =value
                
                
            #ajustes valores que deben ser float
            lista = self.decimales_entrada
            for key, value in dicc.items():
                if key in lista:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                dicc[key] =value
            
            if 'FrecCpn' in dicc.keys():
                dicc['FrecCpn'] = ajusteFrecCpn(dicc['FrecCpn'])
            
        except Exception as e:
            print("Error revision_formatos: ", e)
            return None
    
    
    def verInfoBono(self):
        """
        Funcion para visualizar informacion que se tiene del Bono
        """
        return self._infoBono
    
    def verCalculos(self):
        """
        Funcion para visualizar informacion sobre valores calculados
        """
        return self._ValCalBono
    
    
    def modInfoBono(self,nuevo_val):
        """
        Funcion para modificar la informacion que se tiene del Bono
            -Si la clave ya existe cambiara el valor
            
            nota: las claves normalizadas son las utilizadas en funciones 
            posteriores.
            
            Entrada:
                Se debe introducir un diccionario con {calve:valor}
                    clave: key a introducir o modificar en infoBono
                    valor: valor a introducir
        """
        try:
            infoBono_nuevos = self.check_InfoBono(nuevo_val)
            self.revision_formatos(infoBono_nuevos)
                        
            for keydicc, valuedicc in infoBono_nuevos.items():
                self._infoBono[keydicc] = valuedicc
                    
        except Exception as e:
            print("Error: ", e)
            return None
        
    def calcInteresJ(self,VN,Nj,TCj):
        # Calculo de Intereses por pagar al final del periodo J 
        return VN*Nj*TCj/self.days_year
    
    
    def calcular_fechas_cupon(self, FechaVcto =None, FechaEmision=None, FechaInteres=None,FrecCpn=None,desde_FechaEmision=False):
        """
        Calcula las fechas de pago de cupones desde la fecha de vencimiento hasta la fecha de interés.
    
        Entrada:
            - FechaVcto (datetime): Fecha de vencimiento del cupón.
            - FechaEmision (datetime): Fecha de emisión del cupón o límite hasta el cual se desea calcular.
            - FechaInteres (datetime): Fecha para la cual se desea saber cuántos cupones faltan.
            - dias (int, opcional): Número de días en cada período de cupón. 
            - desde_emision: cuando False calcula las fechas desde la fecha de vencimiento contando los dias hacia atras
                             cuando True calcula las fechas desde la fecha de emision hacia adelante
        Salida:
            Lista con fechas de pago de cupón list[(datetime)].
        """
        
        if not FechaVcto: FechaVcto = self._infoBono['FechaVcto']
        if not FechaEmision: FechaEmision = self._infoBono['FechaEmision']
        if not FechaInteres: FechaInteres = self._infoBono['TimId']    
        if not FrecCpn:
            FrecCpn = self._infoBono['FrecCpn']
            # Verificar si 'FrecCpn' es un float y NaN
            if isinstance(FrecCpn, float) and np.isnan(FrecCpn):
                #No tienen cupones
                FrecCpn = self._infoBono['PlazoEmision']
            else:
                FrecCpn = self._infoBono['FrecCpn']
            
                
        # Verificamos que la fecha de interes este en el plazo del cupon 
        if ((FechaInteres >=  FechaEmision) and (FechaInteres <= FechaVcto)):
            
            # Calculo desde FechaEmision hacia adelante 
            if desde_FechaEmision:
                # Descartando cupones ya pagados
                IncIntervalo = FechaEmision
                while True:
                    finIntervalo = IncIntervalo + timedelta(days=FrecCpn)
                    if FechaInteres >= IncIntervalo and FechaInteres<=finIntervalo:
                        # Primera fecha cupon encontrada
                        fechas = [IncIntervalo]
                        break
                    else:
                        IncIntervalo = finIntervalo
                # Buscando Fechas cupon hasta el fin del plazo
                while True:
                    finIntervalo = fechas[-1] + timedelta(days=FrecCpn)
                    fechas.append(finIntervalo)
                    if finIntervalo >= FechaVcto:
                        fechas = fechas[:-1]+[FechaVcto]
                        break
                self._ValCalBono['fechasCupon']= fechas 
                return fechas
            
            
            # Calculo desde FechaVcto hacia atras 
            else:
                # Ultima fecha cupon
                fechas = [FechaVcto]
                while True:
                    # Encontrando cupon anterior
                    finIntervalo = fechas[-1]
                    IncIntervalo = finIntervalo - timedelta(days=FrecCpn)
                    fechas.append(IncIntervalo)
                    if FechaInteres >= IncIntervalo and FechaInteres<=finIntervalo:
                        fechas.reverse()
                        break
                self._ValCalBono['fechasCupon']= fechas
                return fechas


    def Num_cupones_por_liquidar(self):
        """
        Calculo para Número de cupones por liquidar, incluyendo el vigente, 
        equivalente a self._infoBono['CuponesCobrar']
        """
        try:
            cupones_por_liquidar = len(self.calcular_fechas_cupon()) - 1
            self._ValCalBono['CuponesCobrar']= cupones_por_liquidar
            
            if cupones_por_liquidar != self._infoBono['CuponesCobrar']:
                print("Revisar Num_cupones_por_liquidar")
                return self._infoBono['CuponesCobrar']
            else:
                return cupones_por_liquidar
        except Exception as e:
            print("Error Num_cupones_por_liquidar: ", e)
        
        
    def calcular_dias_ultimo_cupon(self, fechas_cupon=None, fecha_analisis=None, FrecCpn=None):
        """
        Calcula el número de días transcurridos desde el vencimiento del último cupón hasta la fecha indicada.
        Entradas:
            - fechas_cupon (list): Lista con fechas de pago de cupones, preferiblemente 
                                    obtenidas de la función "calcular_fechas_cupon".
            - fecha_analisis (datetime): Fecha para la cual se desea calcular el 
                                        número de días.(self._infoBono['TimId'])
            - FrecCpn (int, opcional): Número de días en cada período de cupón. 
        
        Devolución:
            DiasTranscCpn (int) = Número de días transcurridos desde pago ultimo cupon
        """
        try:
            if not fechas_cupon:  fechas_cupon = self.calcular_fechas_cupon()
            if not fecha_analisis: fecha_analisis = self._infoBono['TimId']
            if not FrecCpn: FrecCpn = self._infoBono['FrecCpn']
            
            # Verificar que la fecha de análisis esté en el intervalo de los cupones.
            if (fechas_cupon[0] < fecha_analisis) and (fecha_analisis < fechas_cupon[1]):
                dias_ultimo_cupon = (fecha_analisis - fechas_cupon[0]).days 
            else:
                dias_ultimo_cupon = 0
                
            self._ValCalBono['DiasTranscCpn']= dias_ultimo_cupon
            return dias_ultimo_cupon

                
        except Exception as e:
            print("Error calcular_dias_ultimo_cupon: ", e)        
    
    
    def calcular_fechas_ultimo_cupon(self,fechas_cupon=None, DiasTranscCpn=None):
        """
        funcion para encontrar las fechas de los dias despues del ultimo cupon hasta 
        un dia antes de la fecha en analisis
        Entrada:
            fecha_analisis (.date): corresponde a self._infoBono['TimId']
            dias_transcurridos (int): Se utiliza el obtenido en self.calcular_dias_ultimo_cupon()
                                     sin embargo debe ser igual a self._infoBono['DiasTranscCpn']
            
        """
        if not fechas_cupon:  fechas_cupon = self.calcular_fechas_cupon()
        if not DiasTranscCpn: DiasTranscCpn = self.calcular_dias_ultimo_cupon()
        
        
        Inicio_cuponVigente = fechas_cupon[0]
        vector_fechas = []
        for i in range(DiasTranscCpn):
            vector_fechas.append(Inicio_cuponVigente+timedelta(days=i))
        
        self._ValCalBono['fechas_ultimo_cupon']= vector_fechas
        
        return vector_fechas
    
            
    def calcular_Importe(self,Num_Titulos, precioSucio = None):
        """
        funcion para calcular el Importe de un grupo de bonos con la
        misma caracteristica.
        Entrada:
            PrecioSucio (float): Precio sucio Bono
            Num_titulos(int): cantidad de bonos 
        salida:
            Importe: Cantidad a Pagar
        """
        if not precioSucio: 
            precioSucio = self._ValCalBono['PrecioSucio']
            
        # afsasf
        
        return Num_Titulos*precioSucio
            
    
    
    
def main():
    pass
if __name__ == '__main__':
    main()    
    
    
    
        
        
    
        
        
        





















