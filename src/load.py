# Importamos el tipo Dict del módulo typing para anotar tipos de datos en la función
from typing import Dict

# Importamos DataFrame de pandas para trabajar con estructuras de datos en forma de tabla
from pandas import DataFrame

# Importamos Engine desde SQLAlchemy para manejar la conexión a la base de datos SQLite
from sqlalchemy.engine.base import Engine

def load(data_frames: Dict[str, DataFrame], database: Engine):
    """
    Cargamos los DataFrames en la base de datos SQLite.
    
    Esta función itera sobre un diccionario donde cada clave es el nombre de la tabla y cada valor
    es un DataFrame. Utiliza el método to_sql de pandas para insertar cada DataFrame en la base de datos,
    reemplazando la tabla existente si es necesario.
    
    Args:
        data_frames (Dict[str, DataFrame]): Diccionario con nombres de tablas como claves y DataFrames como valores.
        database (Engine): Conexión a la base de datos SQLite.
    """
    
    # Verificamos si el diccionario 'data_frames' está vacío
    if not data_frames:
        # Imprimimos un mensaje de advertencia si no hay datos para cargar
        print("⚠️ No hay Datos para cargar en la Base de Datos 😢")
        # Terminamos la ejecución de la función ya que no hay datos que procesar
        return

    # Imprimimos un mensaje indicando el inicio del proceso de carga de Datos en la Base de Datos
    print("📥 Iniciando la carga de Datos en la Base de Datos...\n")

    # Recorremos cada par (nombre de tabla, DataFrame) en el diccionario 'data_frames'
    for table_name, df in data_frames.items():
        try:
            # Intentamos cargar el DataFrame en la base de datos usando to_sql de pandas:
            # - 'table_name' define el nombre de la tabla en la base de datos.
            # - 'con=database' indica la conexión a la base de datos.
            # - 'if_exists="replace"' reemplaza la tabla si ya existe.
            # - 'index=False' evita que el índice del DataFrame se guarde como una columna adicional.
            df.to_sql(table_name, con=database, if_exists="replace", index=False)
            # Si la carga es exitosa, imprime un mensaje confirmando la carga y muestra el número de registros insertados.
            print(f"✅ Tabla '{table_name}' Cargada Exitosamente con {len(df)} registros.")
        except Exception as e:
            # Si ocurre algún error durante la carga, captura la excepción y muestra un mensaje de error con detalles.
            print(f"❌ Error al Cargar la Tabla '{table_name}': {e}")

    # Imprimimos un mensaje final indicando que el proceso de carga de datos ha finalizado
    print("\n ✅🎉 Proceso de Carga Finalizado con Exito. 🚀 ")
    
    
    # --------------------------------------------- REALIZADO ---------------------------------------------------
    
    # TODO: Implementa esta función. Por cada DataFrame en el diccionario, debes
    # usar pandas.DataFrame.to_sql() para cargar el DataFrame en la base de datos
    # como una tabla.
    # Para el nombre de la tabla, utiliza las claves del diccionario `data_frames`.
