# Informe Final del Proyecto: Desarrollo de Calculadoras Financieras Personalizadas

Por razones de confidencialidad el detalle de la implementacion no se puede compartir por este medio, sin embargo, el presente informe sirve para comprender la estructura de las solucion implemntada.

## Introducción

En el ámbito financiero, la toma de decisiones fundamentadas en análisis precisos y adaptados a las necesidades individuales de los usuarios es crucial. Con este propósito, se emprendió el proyecto de desarrollo de calculadoras financieras personalizadas. Este informe resume los logros, características clave y procesos implementados durante el ciclo de vida del proyecto.

## Objetivo del Proyecto

El objetivo principal de este proyecto es proporcionar a los usuarios una herramienta integral que les permita evaluar indicadores y rendimientos financieros específicos, ajustados a sus necesidades particulares. Se enfoca en el diseño y desarrollo de calculadoras financieras que abarquen diversos instrumentos, incluyendo Ms, UDIS, Revisables y Swaps.

## Características del Proyecto

### Instrumentos Financieros

Las calculadoras están diseñadas para trabajar con instrumentos financieros clave, ofreciendo un análisis exhaustivo de los siguientes activos: CETES, UDIBONOS, M_TasaFija, LD_BondesD, LF_Bondes_F, IM_bpag28, IS_bpag182, IQ_BPAG91, IQ_bpag91, así como análisis para swaps.

### Personalización

La flexibilidad es una prioridad, permitiendo a los usuarios adaptar las calculadoras a sus requerimientos específicos para obtener resultados personalizados y relevantes. Entre los cálculos para los diferentes activos se encuentran: cálculo de precio limpio y sucio, interés devengado, rendimiento y sobretasa según corresponda, sensibilidad, duración y convexidad. Todos los cálculos pueden ajustarse según el plazo y tasa para reportos.

### Escenarios de Fondeo

El proyecto abarca un escenario de fondeo definido internamente, combinado con el escenario implícito en la curva financiera. Esto garantiza cálculos precisos y realistas, fundamentales para la toma de decisiones informada.

### Herramientas de Implementación

La implementación se llevó a cabo utilizando el lenguaje de programación Python, aprovechando su potencial de expansión y flexibilidad. Se ha desarrollado una interfaz intuitiva que permite a los usuarios ingresar parámetros de manera sencilla, obteniendo resultados claros y comprensibles para facilitar la interpretación de la información financiera. El despliegue de la aplicación a través del explorador garantiza su compatibilidad con diversos sistemas operativos y versiones de software, asegurando una amplia accesibilidad y usabilidad.

### Desarrollo, Validación y Pruebas

En principio, se intentó desarrollar las calculadoras utilizando los manuales/notas técnicas de cálculos proporcionados por Banxico, encontrando que los resultados no correspondían a lo esperado. En segunda instancia, se intentó imitar las fórmulas del "Manual de Valuación de valores, documentos e instrumentos financieros PIP"; sin embargo, también se encontraron problemas, posiblemente porque las fórmulas mostradas en el manual no se han actualizado y no corresponden a las utilizadas en el sistema. Por último, se utilizaron varios modelos desarrollados en Excel para extraer de los mismos las fórmulas necesarias.

El trabajo más extenso consistió en llevar a cabo pruebas exhaustivas para garantizar la precisión y confiabilidad de los resultados generados por las calculadoras, ya que pequeños cambios en los procedimientos de cálculo, como redondeos o utilizar diferentes métodos de iteración, producen cambios significativos en los resultados.

Por razones ajenas a nuestro control, el proyecto culminó sin una etapa final de pruebas para asegurar la integridad de la información financiera proporcionada; sin embargo, la misma consistiría en confirmar con los diferentes usuarios los resultados obtenidos por sus propios archivos Excel y los de la calculadora. La forma modular como se diseñó la calculadora permite modificar los cálculos de forma muy precisa.

### Documentación

El presente informe tratará de servir como documentación detallada sobre el funcionamiento y la utilización de las calculadoras, facilitando su adopción y asegurando un uso eficiente por parte de los usuarios.



## Estructura del proyecto

La estructura del proyecto y la disposición de archivos reflejan un enfoque organizado y modular, facilitando el desarrollo, mantenimiento y expansión de la aplicación de calculadoras financieras personalizadas.

El proyecto se desenvuelve en el contexto de la carpeta "calculadoras", cuya estructura incluye diversos archivos y directorios esenciales para el desarrollo y funcionamiento de la aplicación financiera personalizada. A continuación, se detallan los elementos presentes en la mencionada carpeta:

1. **Archivos Principales:**
   - `C:\Calculadoras\app.py`: Este archivo constituye el componente central de la aplicación, desarrollado en Python con la biblioteca Dash, permitiendo el despliegue de la aplicación en cualquier explorador instalado en el servidor de ejecución. 

2. **Estructura de Carpetas:**
   - `C:\Calculadoras\assets`: Directorio destinado a almacenar recursos adicionales necesarios para la interfaz de usuario.
   - `C:\Calculadoras\components`: Carpeta diseñada para almacenar componentes específicos de la aplicación, los cuales pueden ser modificados en fases posteriores del desarrollo.
   - `C:\Calculadoras\datasets`: Repositorio de archivos `.csv` o `.xlsm` que contienen información crítica para el funcionamiento de ciertos cálculos. Ejemplos incluyen "Conversion_UDIS_MXN" con estimados de precios de las UDIS y "vector_SWT_IRSTIIE".

3. **Documentación y Configuración:**
   - `C:\Calculadoras\Informe_final.ipynb`: Documento que recopila información detallada sobre el proyecto, proporcionando una visión integral de sus componentes y resultados.
   - `C:\Calculadoras\requiremen.txt` y `C:\Calculadoras\requiremen_general.txt`: Estos archivos contienen la información necesaria para definir el ambiente de trabajo, incluyendo la versión de Python y las bibliotecas utilizadas.

4. **Otros elementos:**
   - `C:\Calculadoras\__init__.py`: Archivo que indica que la carpeta "calculadoras" debe ser tratada como un paquete de Python.
   - `C:\Calculadoras\Calc_Bonos.xlsm` y `C:\Calculadoras\Monitor.xlsm`: Estos documentos Excel representan las versiones iniciales de las calculadoras, estableciendo una conexión entre Python y Excel a través de la herramienta xlwings.


5. **División de la Aplicación**:
   - *Back-end (C:\Calculadoras\Calc_Py):* Este conjunto de archivos actúa como bibliotecas donde se ajustan los cálculos para diferentes tipos de activos en evaluación, así como los requisitos necesarios para su ejecución.

   - *Front-end (app.py) y (C:\Calculadoras\pages):* La aplicación utiliza Dash para desplegar la interfaz en un explorador, accediendo a archivos ubicados en la carpeta "pages" para mostrar los cálculos correspondientes.



## Back-end:
El back-end se compone de un conjunto de archivos los cuales se describiran a continuacion:

### INVEX_calc_Bonos.py:

Este código en Python define una clase llamada `Bono` que se utiliza para manejar información relacionada con bonos financieros. La clase tiene varios métodos y funciones que realizan cálculos y manipulación de datos relacionados con bonos. Aquí hay una explicación detallada de cada parte del código:

- Atributos de Clase:
    - `days_year`: Representa la cantidad de días en un año (360).
    - `formatos_fechas`: Lista de formatos de fecha posibles para ser utilizados en la conversión de fechas.
    - `fechas_entrada`, `enteros_entrada`, `decimales_entrada`, `str_entradas`: Listas que contienen nombres de campos para diferentes tipos de datos (fechas, enteros, decimales y strings) que se esperan en la entrada y estan asociados a los nombres de las columnas que parecen en la tabla '"BIDWH.dwh.PIPVectorAnaliticoMD" de la base de datos "BIDWH":
    
    fechas_entrada = ['TimId','FechaEmision', 'FechaVcto'] 
    
    enteros_entrada = ['Serie','PlazoEmision','ValorNominal', 'DiasTranscCpn', 'CuponesEmision', 'CuponesCobrar']
    
    decimales_entrada = ['PrecioLimpio', 'PrecioSucio', 'InteresesAcumulados', 'CuponActual', 'Sobretasa', 'TasaCupon',    'TasaDeRendimiento']
    
    str_entradas = ['TipoValor', 'Emisora' ,'FrecCpn', 'ReglaCupon','ruta']


- Métodos:
1. **`__init__(self, infoBono={})`**: Constructor de la clase. Se inicializa con un diccionario llamado `infoBono` que contiene la información del bono. El método realiza una verificación de formato para los valores, donde las claves corresponden a las etiquetas definidias previamente, se ajusta las fechas, valores enteros y decimales según sea necesario.

2. **`ajustefechas(self, value)`**: Método para ajustar el formato de las fechas.

3. **`ajsuteEnteros(self, value)`**: Método para ajustar el formato de los valores enteros.

4. **`ajusteFloat(self, value)`**: Método para ajustar el formato de los valores decimales.

5. **`revision_formatos(self, dicc)`**: Función interna utilizada en el constructor para ajustar los formatos de las variables de entrada.

6. **`verInfoBono(self)`**: Método para visualizar la información del bono.

7. **`verCalculos(self)`**: Método para visualizar información sobre los valores calculados.

8. **`modInfoBono(self, nuevo_val)`**: Método para modificar la información del bono. Toma un diccionario como entrada y modifica el valor correspondiente en `_infoBono`.

9. **`calcInteresJ(self, VN, Nj, TCj)`**: Método para calcular los intereses por pagar al final del período J.

10. **`calcular_fechas_cupon(self, FechaVcto=None, FechaEmision=None, FechaInteres=None, FrecCpn=None, desde_FechaEmision=False)`**: Método para calcular las fechas de pago de cupones desde la fecha de vencimiento hasta la fecha de interés.

11. **`Num_cupones_por_liquidar(self)`**: Método para calcular el número de cupones por liquidar.

12. **`calcular_dias_ultimo_cupon(self, fechas_cupon=None, fecha_analisis=None, FrecCpn=None)`**: Método para calcular el número de días transcurridos desde el vencimiento del último cupón hasta la fecha indicada.

13. **`calcular_fechas_ultimo_cupon(self, fechas_cupon=None, DiasTranscCpn=None)`**: Método para encontrar las fechas de los días después del último cupón hasta un día antes de la fecha de análisis.

14. **`calcular_Importe(self, Num_Titulos, precioSucio=None)`**: Método para calcular el importe de un grupo de bonos con la misma característica.


### ENLACE_INVEX_calc_Bonos.py

Esta libreria se creo como una herramienta para cargar información sobre bonos y tasas financieras desde una base de datos, realizar cálculos financieros y descargar datos adicionales de tasas desde la API del Banco de México (Banxico). A continuación, se presenta una descripción general de las clases, métodos y funciones:

#### Métodos y funciones:

1. **`__init__(self, ruta=None)`:**
   - Inicializa la clase y establece la conexión con la base de datos. Puede recibir una ruta opcional, la cual indicara a la libreria como acceder a archivos .csv o .xls externos que sean necesarios para los calculos.
   - En esta seccion tambien se defienen los paramatros para en el enalce con la base de datos de INVEX, de existir cambios con respecto a lso permisos de usurio asigando se debe modificar aqui:
       info_conexion = {   "server" : "TPPBIDB01\BI",
                        "database" : "BIDWH",
                        "username" : "UsrCB",
                        "password" : "Us12#CB1nV3x",
                        "tabla" : "BIDWH.dwh.PIPVectorAnaliticoMD",
                        "tabla_tiempo":"bidwh.dwh.DimTiempo",
                        "tabla_swaps":"BIDWH.DWH.CBSwapOISIRS"}
    - Igualmente, para acceder a traves de una api la informacion de la pagina oficial de Banxico se creo un token segun las instrucciones de Banxico (https://www.banxico.org.mx/SieAPIRest/service/v1/token), de tener fallas con esa conexion se debe generar un token nuevo. 
    token = "7a88e6c15ce06f1de7f2283ff90689e8d48f4f9ed61265d9161f590cc3bb42d9"

2. **`cargarBonos(self, tipo_bono, FechaValuacion=None)`:**
   - Carga datos de bonos de la base de datos según el tipo de bono y la fecha de valuación.

3. **`cargarInfoBono(self, num_serie)`:**
   - Carga información detallada sobre un bono específico utilizando el número de serie.

4. **`cargarTasaFondeoTIIE_1dia(self)`:**
   - Carga la tasa de fondeo interbancaria (TIIE) a un día desde la base de datos.

5. **`cargarTasaFondeoPonderada(self)`:**
   - Carga la tasa ponderada de fondeo bancario desde la base de datos.

6. **`cargarValorDeUDIS(self)`:**
   - Carga el valor de las Unidades de Inversión (UDIS) desde la base de datos.

7. **`cargarTabla_IRS(self, FechaReporte)`:**
   - Carga la tabla de tasas de intercambio (IRS) desde la base de datos para una fecha específica.

8. **`cargar_df_vector_para_swaps(self)`:**
   - Carga un DataFrame con información relevante para cálculos relacionados con swaps.

9. **`cargarDiasInhabiles(self, fechaInicio=None, fechaFin=None)`:**
   - Calcula los días inhábiles combinando información de la base de datos y cálculos de festivos y fines de semana.

10. **`descarga_serie_BXM(self, idSerie, fechaInicio, fechaFin, token)`:**
    - Descarga datos de una serie específica desde la API del Banco de México (Banxico).

11. **`BMX_TasaFondeoTIIE_1dia(self)`:**
    - Descarga la tasa de fondeo interbancaria (TIIE) a un día desde la API del Banco de México (Banxico).

12. **`BMX_TasaPonderadaFondeoBancario(self)`:**
    - Descarga la tasa ponderada de fondeo bancario desde la API del Banco de México (Banxico).

13. **`BMX_UDIS(self)`:**
    - Descarga datos de las Unidades de Inversión (UDIS) desde la API del Banco de México (Banxico).

14. **`cargarUDIS_TablaProyeccion(self, ruta=None)`:**
    - Carga una tabla de proyección de valores de UDIS desde un archivo Excel.


### Librerias ajustadas a tipo de Bono
​
Para cada tipo de Bono se desarrollo una libreria especifica que permitia hacer los calculos ajustados al tipo de activo, por lo que existen los siguientes archivos: BI_CETES.py, IM_BPAG28.py, IQ_BPAG91.py, IS_BPAG182.py, LD_BONDES_D.py, LF_BONDES_F.py, M_TASA_FIJA.py, S_UDIBONOS.py.
A continuación, proporcionaré una breve explicación de cada una de las funciones y métodos presentes en la clase `M_TasaFija` sin embargo los mismos
se repiten en los otros activos solo que las formulas o metodos de calculo difieren:
​
1. **Módulos e Importaciones:**
   - Se importan las clases `Bono` y `Enlace_INVEX_calc_Bonos` desde los módulos correspondientes. 
​
2. **Inicialización de la Clase:**
   - El constructor `__init__` inicializa una instancia de la clase `M_TasaFija`. Llama al constructor de la clase base `Bono` utilizando `super().__init__(infoBono)`, heredando todas las propiedades de la clase 'Bono'.
   - Se instancia un objeto `Enlace_INVEX_calc_Bonos` qe permitira acceder a informacion necesaria desde base de datos Invex u otros enlaces externos.
   - Se cargan los días inhabiles en el rango de fechas entre `FechaEmision` y `FechaVcto`.
​
3. **Método `PrecioLimpio`:**
   - Calcula el precio limpio de un bono a tasa fija utilizando varias funciones y métodos internos. Se basa en fórmulas específicas y toma parámetros como la tasa de cupón, rendimiento, días transcurridos del cupón, valor nominal, etc.
   
4. **Método `df_calcAmortizacionPagos`:**
   - Calcula la tabla de amortización de pagos para el bono y almacena el resultado en un DataFrame (`df_AmortizacionPagos`), pasando por crear un DataFrame base para la construcción del flujo de pagos de los cupones. Utiliza las fechas de pago de cupones generadas por el método `calcular_fechas_cupon` y ajusta las fechas si caen en días inhabiles. Calcula (df_Cj) el monto esperado del pago de intereses para un periodo de cupón específico, (df_Fj) el factor de descuento para el flujo de efectivo en un periodo específico entre otros elementos de la tabla de amortizacion.
​
5. **Método `df_calcPrecioLimpio`:**
   - Calcula el precio limpio del bono utilizando la tabla de amortización de pagos.
​
6. **Método `calcInteresDevengado`:**
    - Calcula los intereses acumulados hasta la fecha de interés.
​
7. **Método `df_calcPrecioSucio`:**
    - Calcula el precio sucio del bono sumando el precio limpio y los intereses devengados.
​
8. **Método `df_Rendimiento`:**
    - Utiliza el método de la raíz para calcular el rendimiento del bono dados el precio limpio y la fecha de interés.
​
9. **Método `df_RendimientoPrecioSucio`:**
    - Calcula el rendimiento del bono teniendo en cuenta el precio sucio y los intereses devengados.
​
10. **Método `sobretasa`:**
    - Devuelve la sobretasa del bono.
​
11. **Método `valorFuturo`:**
    - Calcula el valor futuro compuesto dado un valor actual, tasa de interés y periodo.
​
12. **Método `calcPrecioRegreso`:**
    - Calcula el precio para regresos considerando la tasa de reporto y el plazo del préstamo.
​
13. **Método `calcRendimientoRegreso`:**
    - Calcula el rendimiento para regresos teniendo en cuenta la tasa de reporto y el plazo del préstamo. Utiliza un método iterativo para ajustar la tasa de rendimiento.
    
14. **`calcSobretasaRegreso`** : Este método calcula la sobretasa al regreso de un bono. Toma como entrada la tasa de reporto, el plazo de reporto, y opcionalmente el precio al regreso, rendimiento al regreso y fecha de interés. Si no se proporcionan el precio y el rendimiento al regreso, se calculan utilizando otros métodos internos (`calcPrecioRegreso` y `calcRendimientoRegreso`). Luego, se utiliza esta información junto con la tasa de rendimiento actual y la sobretasa inicial para calcular la sobretasa al regreso.
​
15. **`valorPresente`** : Calcula el valor presente de un monto dado, descontándolo con la tasa de mercado y la sobretasa del bono. Puede tomar tasas de mercado y sobretasa opcionales, y si no se proporcionan, utiliza los valores actuales del bono.
​
16. **`Duracion`** : Calcula la duración de un bono. Utiliza funciones internas (`df_calcPrecioSucio` y `df_calcAmortizacionPagos`) para obtener el precio sucio y la amortización de pagos del bono. Luego, calcula la duración de los cupones y la duración del valor nominal presente para obtener la duración total.
​
17. **`Dur_modificada`**: Calcula la duración modificada del bono utilizando la duración y las tasas de mercado del bono.
​
18. **`Div01`** : Calcula la Div01 del bono, que es una medida de sensibilidad a cambios en los rendimientos. Utiliza la duración modificada y el precio sucio del bono.
​
19. **`convexidad`** : Calcula la convexidad del bono. Utiliza funciones internas (`df_calcAmortizacionPagos` y `df_calcPrecioSucio`) para obtener la amortización de pagos y el precio sucio del bono. Luego, calcula la convexidad de los cupones y la convexidad del valor nominal presente para obtener la convexidad total.
​
20. **`DuracionRegreso`** : Calcula la duración al regreso de un bono. Utiliza funciones internas y la información del bono para calcular la duración del regreso.
​
21. **`Dur_modificada_Regreso`** : Calcula la duración modificada al regreso de un bono utilizando la duración al regreso y las tasas de mercado.
​
22. **`Div01_Regreso`** : Calcula la Div01 al regreso de un bono, utilizando la duración modificada al regreso y el precio sucio del bono.
​
23. **`convexidad_Regreso`** : Calcula la convexidad al regreso de un bono. Utiliza funciones internas y la información del bono para calcular la convexidad del regreso.
​

### Calc_Bonos.py  y  ENLACE_xlwings_Excel.py

Los archivos calc_Bonos.py y  ENLACE_xlwings_Excel.py son scripts elaborado en las primeras etapas del proyecto, utiliza clases y métodos para interactuar con hojas de cálculo de Excel y realizar los cálculos financieros específicos para diferentes tipos de bonos. Aquí hay un resumen de algunas de las funciones y operaciones principales que realiza:

- Importa clases y funciones de otros módulos, como ENLACE_xlwings_Excel, ENLACE_INVEX_calc_Bonos, BI_CETES, S_UDIBONOS, etc.

- Define un diccionario llamado RelacionCeldasExcel_Variables que asigna nombres a celdas de Excel para facilitar la referencia y poder modificar facilmente en el excel donde se desea visualizar las entradas y salidas.


### monitor.py

Esta libreria parece se enfoca en la construcion de la tabla conocida como monitor de mercado, para todos los bonos de un tipo especifico, realiza cálculos y análisis sobre todos los nodos de un tipo de bonos. Aquí hay una descripción de las funciones y métodos presentes en el código, tiene metodos y 


1. **`Crear_enlace_invex_Bonos(tipo_bono, FechaValuacion)`**: Crea y devuelve un objeto de la clase `Enlace_INVEX_calc_Bonos` para el tipo de bono y fecha de valuación dados.

2. **`CargarBonoEnEvaluacion(enlace_Invex, num_serie)`**: Carga la información de un bono utilizando el objeto `enlace_Invex` y el número de serie proporcionado. Devuelve un objeto correspondiente al tipo de bono.

3. **`Fecha_Mes_Anio(fecha_str)`**: Convierte una cadena de fecha en formato '%y%m%d' a '{dia}_{nombre_mes}_{anio}'. Devuelve un string.

4. **`obtener_rendimiento_regreso(enlace_Invex, num_serie, Anio, TasaReporto)`**: Calcula y devuelve el rendimiento de regreso para un bono específico en un año y tasa de reporto dada.

5. **`rendimiento_regreso_app(enlace_Invex, num_serie, fecha_finreporto, TasaReporto)`**: Versión de la función anterior diseñada para ser llamada desde la aplicación, toma una fecha de fin de reporto en lugar de un año.

6. **`obtener_sobretasa_regreso(enlace_Invex, num_serie, Anio, TasaReporto)`**: Calcula y devuelve la sobretasa de regreso para un bono específico en un año y tasa de reporto dada.

7. **`sobretasa_regreso_app(enlace_Invex, num_serie, fecha, TasaReporto)`**: Versión de la función anterior diseñada para ser llamada desde la aplicación, toma una fecha de fin de reporto en lugar de un año.

8. **`Obtener_Carry(TasaDeRendimiento, Regreso)`**: Calcula y devuelve el "Carry" (diferencia entre el regreso y la tasa de rendimiento, multiplicado por 100) si el regreso es diferente de cero; de lo contrario, devuelve cero.

9. **`calc_df_Monitor(FechaValuacion, tipo_bono, Fondeo_Anio)`**: Calcula un DataFrame llamado "Monitor" que contiene información sobre tasas de rendimiento, regresos, y "Carry" para distintos años de fondeo.

10. **`calc_df_Monitor_app(FechaValuacion, tipo_bono, Fondeo_periodos)`**: Versión de la función anterior diseñada para ser llamada desde la aplicación, toma una tabla de fechas de fondeo y tasas correspondientes en lugar de años.

11. **`calcMonitor()`**: Función destinada a ser llamada desde Excel. Utiliza las funciones anteriores para calcular y escribir en Excel un DataFrame llamado "df_Monitor".

12. **`calcMonitor_app(FechaValuacion, tipo_bono, tabla_fechas_Fondeo)`**: Versión de la función anterior diseñada para ser llamada desde la aplicación, toma una tabla de fechas de fondeo y tasas correspondientes en lugar de años.

13. **`intervalos_periodos(fecha_incio, periodo, num_periodos)`**: Devuelve una lista de fechas de fin de reporto en función del periodo y número de periodos proporcionados.


### CALC_SWAPS_IRS.py


Este código es para realizar cálculos y análisis financieros relacionados con swaps de tasa de interés. A continuación, proporcionaré una explicación general y detallada de las funciones y métodos presentes en el código.

1. **__init__ Clase `Calculos_Swaps_IRS`:**
   - El constructor `__init__`  inicializa varios atributos y carga la Tabla_IRS  desde el  módulo ENLACE_INVEX_calc_Bonos haciendo enlace con la tabla 'BIDWH.DWH.CBSwapOISIRS' de la base de datos .
   - Inicializa varios DataFrames y variables para almacenar resultados y parámetros.
   - Define métodos para realizar cálculos específicos relacionados con swaps de tasa de interés.

2. **Métodos Cálculos de SWAPS** ('crear_df_cuadro_swap_dias', 'calcular_tasa_fwd', 'interpolacion', 'crear_df_vector_desde_BD_Invex', 'cargar_vector_SWT_IRSTIIE', 'crear_df_interpolado_dias_tasa_cero', 'const_Tipos_interpolacion', 'buscar_en_df', 'crear_vector_interpolado', 'crear_info_bono_Generico', 'crear_df_vector', 'crear_df_cuadro_swap'). Estos métodos realizan cálculos y operaciones específicos relacionados con la segunda versión de los cálculos de swaps, que involucran la manipulación de DataFrames y la interpolación de datos. como observacion general se puede observar la evolucion de los calculos a lo largo del tiempo, ya que se dejaron los métodos de  versiones diferentes de cálculos de swaps.


    2.1. *crear_info_bono_Generico:*
   - Descripción general: Este método  está destinado a la creación de información relacionada con bonos genéricos. incluye parámetros como la duración del bono, tasas de interés, fechas de vencimiento, etc. Devuelva un objeto que contiene la información generada del bono.

    2.2. *const_Tipos_interpolacion:*
    - Este método es una función que genera un diccionario de diferentes tipos de interpolación, donde las claves son nombres de métodos de interpolación y los valores son las condiciones asociadas a esos métodos. Los métodos de interpolación incluyen 'interp1d_quadratic', 'CubicSpline', 'Akima1DInterpolator', y 'PchipInterpolator'. Por defecto se utiliza 'CubicSpline' que es la forma de interpolacion que se ajusta a los resultados obtenidos con los excel de prueba.

    2.3. *interpolacion:*
    - Este método realiza la interpolación de un vector interpolado en función de un nombre dado para el tipo de interpolación ('nombre_tipo_interpolacion'). La interpolación se realiza utilizando una función ('y_f') asociada al tipo de interpolación y se actualiza el vector interpolado con los resultados.

    2.4. *crear_vector_interpolado*
    - Este método crea un vector interpolado inicial utilizando un DataFrame de datos de entrada ('df_vector') o generándolo internamente si no se proporciona. Luego, aplica la interpolación según el tipo seleccionado ('seleccion_interpolacion') o utiliza el tipo predeterminado definido en la clase.

    2.5. *crear_df_cuadro_swap:*
    - Este método crea un DataFrame ('df_cuadro_swap') que contiene información sobre tasas cero, tasas forward, y otros valores relacionados con los plazos de un swap. Utiliza interpolación para calcular tasas cero y factores de descuento.

    2.6. *crear_df_interpolado_dias_tasa_cero:*
    - Este método crea un DataFrame interpolado de tasas cero en función de los días, utilizando un DataFrame de cuadro swap ('df_cuadro_swap') o generándolo internamente si no se proporciona.

    2.7. *crear_df_cuadro_swap_dias:*
    - Este método crea un DataFrame ('df_swap_dias') que contiene información sobre tasas cero, tasas forward y otros valores relacionados con los días de un swap. Utiliza la interpolación de tasas cero y otros cálculos relacionados. 

    2.8. *crear_tabla_swap_TIIE_FWD:*
    - Este método crea una tabla de swaps comparando diferentes intervalos de forward y tenor. Utiliza funciones y datos previamente calculados sobre tasas cero y tasas forward.

    2.9. *calcular_Spreads:*
    - Este método calcula spreads entre diferentes tasas de un DataFrame de tabla swap TIIE vs. forward. Toma como entrada un intervalo de tasas en formato de string y devuelve el spread correspondiente.

    2.10. *crear_TIIE_28dias_implicita:*
    - Este método crea un DataFrame ('df_TIIE_28dias_implicita') que contiene información sobre tasas TIIE a 28 días implícitas en diferentes intervalos de tiempo. Utiliza datos de tasas forward y otros cálculos.


## Front-end:
El Frot-end se realizo utilizando la libreria dash de python, y se compone de un conjunto de archivos los cuales se describiran a continuacion:

### app.py

Este código utiliza Dash, un marco de trabajo para crear aplicaciones web interactivas con Python. Dash simplifica la creación de interfaces de usuario web al integrar componentes HTML, CSS y JavaScript directamente en código Python. El script define y ejecuta una aplicación Dash que consiste en una interfaz gráfica dividida en dos secciones principales: un sidebar (barra lateral que permite moverse en los diferentes tipos de calculadora) y un área de contenido para desplegar las opciones de la calculadora.

Aquí hay una explicación general del código:

- **Estructura de la Interfaz Gráfica:**
   - La interfaz gráfica se estructura utilizando el contenedor `dbc.Container` con varias filas (`dbc.Row`) y columnas (`dbc.Col`).
   - La primera fila contiene una imagen (`html.Img`) y un título (`html.Div`) centrado, formando el encabezado.
   - La segunda fila incluye una línea horizontal (`html.Hr`).
   - La tercera fila está dividida en dos columnas. La primera columna (`dbc.Col`) contiene el `sidebar`, mientras que la segunda columna contiene el `dash.page_container`.

- **Configuración del Servidor y Ejecución de la Aplicación:**
   - Se utiliza `app.run_server` para ejecutar la aplicación. El parámetro `debug` se establece en `False` para deshabilitar el modo de depuración. La aplicación se ejecuta en el host '127.0.0.20' en el puerto 8055. Si se desea desplegarla bajo otra direccion ip y puerto simplemente se debe modificar estos valores.


### pg2.py ('SWAPS')

Este código crea una aplicación web interactiva que permite a los usuarios cargar datos, realizar cálculos financieros para swaps IRS (Interest Rate Swaps), y visualizar resultados a través de tablas y gráficos. Las funciones callback aseguran que la aplicación responda de manera dinámica a las interacciones del usuario. Aquí una explicación general del código, seguida de una descripción detallada de los componentes principales:

**Explicación General:**

1. **Importación de Bibliotecas y Módulos:**
   - Se importan las bibliotecas necesarias, como Dash, Pandas, Plotly Express, y otras.
   - También se importan módulos definidos en archivos separados, como `components` y los modulos creados en el back end como `Calc_Py.CALC_SWAPS_IRS`.

2. **Inicialización de Objetos y Variables:**
   - Se inicializan objetos y variables necesarios para el funcionamiento de la aplicación.
   - Se crea una instancia de la clase `Calculos_Swaps_IRS` del módulo `Calc_Py.CALC_SWAPS_IRS`.
   - Se definen opciones de inicializacion para componentes.

3. **Definición de Diseño (Layout):**
   - Se crea un contenedor (`layout`) utilizando el framework Dash Bootstrap Components (`dbc`).
   - El diseño contiene varias filas y columnas, y se organizan componentes como botones, tablas, gráficos y otros elementos dentro del diseño.

4. **Callbacks (Funciones Reactivas):**
   - Se definen múltiples funciones callback utilizando el decorador `@callback`. Estas funciones se activan en respuesta a eventos específicos, como clics en botones o cambios en el contenido de ciertos elementos.
   - Los callbacks actualizan dinámicamente diferentes partes de la aplicación, como tablas, gráficos, y opciones de visualización.

### Descripción Detallada de Componentes Principales:

1. **RadioItems (`Botones seleccion de carga`):**
   - Este componente de botones de radio permite al usuario seleccionar entre modos de carga manual para el cual se debe llenar el vector escenario de fondeo definido SWTIRSTIIE manualmente, carga desde archivo con formato como el que parece en documento 'C:\Calculadoras\datasets\df_vector.csv\  o modo automático conectando directamente a la base de datos de INVEX.

2. **Button (`CALCULAR`):**
   - Botón para realizar los cálculos. Activa los callbacks que ejecutan los cálculos y actualizan los elementos relacionados.

3. **Upload (`ENTRADA_DIR_ARCHIVO_CARGAR`):**
   - Componente de carga de archivos que aparece al seleccionar la opcion en los botones de seleccion de cargapara cargar datos desde un archivo, .

4. **DataTables (`DF_VECTOR`, `TABLA_SWAP_TIIE_FWD`, `DF_SPREADS`, etc.):**
   - Tablas interactivas de Dash para visualizar y editar datos.

5. **Dropdown (`DROPDOWN_LISTA`):**
   - Menú desplegable que permite al usuario seleccionar las tablas o gráficos que desea visualizar.

9. **Callbacks Específicos (`actualizar_tiie_dia`, `visualizar_tipos_interpolacion`, etc.):**
   - Funciones callback específicas que responden a eventos y actualizan componentes específicos de la aplicación.


### pg3.py ('MONITOR REGRESOS')

Aplicación web interactiva que permite a los usuarios cargar datos, realizar cálculos financieros relacionados con bonos y tasas de interés, utilizando la clase `Calc_Py.Monitor` para realizar los cálculos específicos. La aplicación es interactiva y permite jugar con los periodos de analisis, tipo de bono, fechas de reporto y tasa de interes de reporto para los periodos. Los resultados de los cálculos se muestran en una tabla que se actualiza dinámicamente.

**Explicación General:**


1. **Inicialización de Objetos y Variables:**
   - Se define una lista de tipos de bonos (`tipos_bonos`), los años de análisis (`anios_analisis`), y otros datos necesarios.
   - Se utiliza el framework Dash Bootstrap Components (`dbc`) para la construcción del layout.

2. **Definición de Diseño (Layout):**
   - Se crea un diseño (`layout`) que contiene varios componentes, como filas (`dbc.Row`), columnas (`dbc.Col`), y elementos como botones, menús desplegables, y tablas.
   - La página se registra como "MONITOR REGRESOS".

3. **Callbacks (Funciones Reactivas):**
   - Se definen funciones callback utilizando el decorador `@callback`. Estas funciones se activan en respuesta a eventos específicos, como clics en botones o cambios en el contenido de ciertos elementos.
   - Los callbacks actualizan dinámicamente diferentes partes de la aplicación, como tablas y datos de monitorización.

### Descripción Detallada de Componentes Principales:

1. **DatePickerSingle (`Fecha inicio de Analisis`):**
   - Selector de fecha que permite al usuario elegir la fecha de inicio para el análisis.

2. **Dropdowns (`dropdown_periodos_analisis`, `dropdown_numero_periodos`, `dropdown_tipos_bonos`):**
   - Menús desplegables que permiten al usuario elegir diferentes opciones, como el período de análisis, el número de períodos, y el tipo de bono.

3. **Button (`boton_calcular_monitor`):**
   - Botón que activa el cálculo de monitorización en respuesta a clics.

4. **DataTable (`tabla_fechas_tasa`, `tabla_monitor`):**
   - Tablas interactivas de Dash para visualizar y editar datos. `tabla_fechas_tasa` se utiliza para introducir fechas y tasas, mientras que `tabla_monitor` muestra los resultados del cálculo.


### pg4.py ('GENERAL BONOS')

Este código esta diseñado para realizar análisis general de bonos, con funciones para cargar información sobre bonos, realizar cálculos específicos y visualizar resultados. A continuación, se proporciona un resumen y descripción detallada:

**Resumen General:**

1. **Importación de Bibliotecas y Módulos:**
   - Se importan bibliotecas como Pandas, Dash, y módulos específicos (`Calc_Py.Calc_Bonos`).
   - Se utiliza Dash Bootstrap Components (`dbc`) para el diseño.

2. **Inicialización de Objetos y Variables:**
   - Se define la ruta del archivo de datos, una lista de tipos de bonos, y otras variables necesarias.

3. **Definición de Diseño (Layout):**
   - El diseño (`layout`) incluye varios elementos, como selección de fecha, menús desplegables para tipos y series de bonos, botones de cálculo, y secciones para visualización de resultados.

4. **Callbacks (Funciones Reactivas):**
   - Se definen múltiples funciones callback utilizando el decorador `@callback`. Estas funciones se activan en respuesta a eventos específicos, como clics en botones o cambios en el contenido de ciertos elementos.
   - Los callbacks actualizan dinámicamente diferentes partes de la aplicación, como tablas y gráficos.

### Descripción Detallada de Componentes Principales:

1. **DatePickerSingle (`Fecha incio de Analisis`):**
   - Selector de fecha que permite al usuario elegir la fecha de inicio para el análisis de bonos. Esta es la fecha a la que iniciara el reporto.

2. **Dropdowns (`dropdown_tipos_bonos_GENERAL_BONOS`, `dropdown_series_bono_GENERAL_BONOS`, `dropdown_periodos_reporto`):**
   - Menús desplegables para seleccionar el tipo de bono, la serie de bono, y el período de reporto. Se conecta con la base de datos de INVEX para desplegar la informacion del bono en analisis.

3. **Button (`boton_calcular_GENERAL_BONOS`):**
   - Botón que activa el cálculo del reporto en respuesta a clics.

4. **DataTables (`df_info_serie_selecccionado`, `df_info_reporto`, `df_respuesta_reporto`, `df_vectorInvex`, `df_AmortizacionPagos`):**
   - Tablas interactivas de Dash para visualizar y editar datos. Cada tabla tiene su función específica en la visualización de resultados y cálculos.

5. **Callbacks Específicos (`calcular_reporto`, `actualizar_info_reporto`, `actualizar_df_info_reporto`, etc.):**
   - Funciones callback específicas que realizan cálculos y actualizan dinámicamente diferentes secciones de la aplicación en respuesta a eventos.


## Comentarios Finales y Recomendaciones:

- El desarrollo del proyecto se llevó a cabo siguiendo las mejores prácticas de programación y código limpio. Las funciones y métodos fueron segmentados de manera óptima, permitiendo una revisión, mejora y expansión continua del mismo.

- Se utilizaron las bibliotecas del back-end para realizar cálculos y obtener información detallada sobre bonos. Estos procesos están separados del despliegue y visualización, lo que facilita la adición o eliminación de funcionalidades.

- Se procuró que la nomenclatura de los métodos, funciones, clases y bibliotecas fuera lo más explícita posible. Además, se incluyeron comentarios internos en las funciones complejas para explicar los procedimientos y cálculos realizados.

- La aplicación fue diseñada para ser interactiva, permitiendo a los usuarios ajustar diversos parámetros y realizar análisis específicos de bonos.

- Se ha dedicado una sección específica para la visualización de diferentes tablas y gráficos generados durante los cálculos.

- Como recomendación, se sugiere llevar a cabo una etapa final de prueba para confirmar la precisión de los cálculos. Además, se puede considerar la incorporación de gráficas o tablas adicionales que sean útiles para los usuarios en la interfaz de despliegue.



- Trabaja con las funciones imortadas como: Excel_EntSal, cargarBonos (Carga la información de bonos desde una conexion MS SQL predefinada, la presenta en excel y la almacena en un DataFrame) , buscarInfoBono (Busca información específica sobre un bono utilizando su número de serie.) , calculoPrecio (Realiza cálculos relacionados con el precio limpio, intereses devengados y precio sucio de los diferentes tipos de bonos.), calculoRendimiento, calculoRegresos, calculoSensibilidad, entre otras. 

