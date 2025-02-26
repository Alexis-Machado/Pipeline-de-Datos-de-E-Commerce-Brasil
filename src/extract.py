# Importamos Dict de typing para anotar tipos de datos en las funciones (en este caso, diccionarios)
from typing import Dict

# Importamos la librería requests para realizar solicitudes HTTP a APIs externas
import requests

# Importamos el módulo json para convertir cadenas JSON a estructuras de datos de Python (como diccionarios)
import json

# Importamos DataFrame, read_csv y to_datetime de pandas para manipular datos en formato tabular,
# leer archivos CSV y convertir columnas a tipo datetime, respectivamente
from pandas import DataFrame, read_csv, to_datetime

# Función para leer datos de temperatura desde un archivo CSV y devolverlos como un DataFrame
def temp() -> DataFrame:
    """
    Obtiene los datos de temperatura desde un archivo CSV.

    Returns:
        DataFrame: Un DataFrame con los datos de temperatura.
    """
    # Lee el archivo CSV ubicado en "data/temperature.csv" y retorna el DataFrame resultante
    return read_csv("data/temperature.csv")

# Función para obtener los días festivos de Brasil desde una API pública y devolverlos como un DataFrame
def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    """
    Obtiene los días festivos de Brasil desde una API pública.

    Args:
        public_holidays_url (str): URL base de la API de días festivos.
        year (str): Año para el cual se deben obtener los días festivos.

    Raises:
        SystemExit: Si la solicitud HTTP falla.

    Returns:
        DataFrame: Un DataFrame con los días festivos, sin las columnas "types" y "counties".
    """
    
    # Realizamos una solicitud HTTP GET a la API, construyendo la URL con el año y el código de Brasil ("BR")
    response = requests.get(f"{public_holidays_url}/{year}/BR")

    try:
        # Verificamos que la respuesta HTTP sea exitosa; si no, lanza una excepción HTTPError
        response.raise_for_status()  # Lanzamos una excepción si la solicitud falla (por ejemplo, 404 o 500)
        
        # Convertimos el texto de la respuesta (en formato JSON) a un diccionario de Python
        data = json.loads(response.text)
        # Creamos un DataFrame a partir del diccionario obtenido de la respuesta JSON
        df = DataFrame(data)
        
        # Convertimos la columna "date" a tipo datetime para un manejo adecuado de las fechas
        df["date"] = to_datetime(df["date"])
        
        # Eliminamos las columnas "types" y "counties", ya que no son necesarias para el análisis
        df = df.drop(columns=["types", "counties"])

        # Imprimos un mensaje de éxito indicando que los días festivos fueron extraídos correctamente
        print("✅🎉 Días Festivos Extraídos Correctamente.")
        # Retornamos el DataFrame con los días festivos procesados
        return df

    except requests.exceptions.HTTPError as err:
        # Si ocurre un error HTTP, imprime un mensaje de error detallando el problema
        print(f"❌ Error al Obtener Días Festivos: {err}")
        # Finalizamos la ejecución del programa lanzando SystemExit con el error obtenido
        raise SystemExit(err)

# Función para extraer datos de múltiples archivos CSV y de una API externa, combinándolos en un diccionario de DataFrames
def extract(csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str) -> Dict[str, DataFrame]:
    """
    Extrae datos de múltiples archivos CSV y de una API externa.

    Args:
        csv_folder (str): Ruta de la carpeta donde están los archivos CSV.
        csv_table_mapping (Dict[str, str]): Diccionario que mapea nombres de archivos CSV a nombres de tablas.
        public_holidays_url (str): URL base de la API de días festivos.

    Returns:
        Dict[str, DataFrame]: Un diccionario con los nombres de las tablas como claves y los DataFrames como valores.
    """
    
    try:
        # Creamos un diccionario "dataframes" donde cada clave es el nombre de la tabla y cada valor es un DataFrame
        # obtenido leyendo el archivo CSV correspondiente (la ruta se construye concatenando "csv_folder" y el nombre del archivo CSV)
        dataframes = {
            table_name: read_csv(f"{csv_folder}/{csv_file}")
            for csv_file, table_name in csv_table_mapping.items()
        }
        # Imprimimos un mensaje de éxito indicando que los archivos CSV han sido extraídos correctamente
        print("✅🎉 Archivos CSV Extraídos Correctamente.")

        # Llamamos a la función get_public_holidays para obtener los días festivos para el año 2017
        holidays = get_public_holidays(public_holidays_url, "2017")
        # Agregamos el DataFrame de días festivos al diccionario "dataframes" bajo la clave "public_holidays"
        dataframes["public_holidays"] = holidays

        # Imprimimos un mensaje final de éxito indicando que la extracción de datos se completó correctamente
        print("✅🎉 Extracción Completada con Éxito.")
        # Retornamos el diccionario que contiene todos los DataFrames extraídos
        return dataframes

    except Exception as e:
        # Si ocurre cualquier error durante la extracción de datos, imprime un mensaje de error con los detalles
        print(f"❌ Error en la Extracción: {e}")
        # Retornamos un diccionario vacío para indicar que la extracción falló
        return {}
    
    
    # --------------------------------------------- REALIZADO ---------------------------------------------------
    
    # TODO: Implementa esta función.
    # Debes usar la biblioteca requests para obtener los días festivos públicos del año dado.
    # La URL es public_holidays_url/{year}/BR.
    # Debes eliminar las columnas "types" y "counties" del DataFrame.
    # Debes convertir la columna "date" a datetime.
    # Debes lanzar SystemExit si la solicitud falla. Investiga el método raise_for_status
    # de la biblioteca requests.
