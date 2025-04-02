from typing import Dict
from pandas import DataFrame
from sqlalchemy.engine.base import Engine

def load(data_frames: Dict[str, DataFrame], database: Engine):
    """
    Cargamos los DataFrames en la base de datos SQLite.

    Para cada DataFrame en el diccionario, se obtiene una conexión raw (DBAPI)
    a partir del Engine de SQLAlchemy y se utiliza para cargar la tabla mediante
    pandas.DataFrame.to_sql(), que requiere una conexión que tenga el método .cursor().

    Args:
        data_frames (Dict[str, DataFrame]): Diccionario con nombres de tablas como claves y DataFrames como valores.
        database (Engine): Conexión a la base de datos SQLite.
    """
    if not data_frames:
        print("⚠️ No hay Datos para cargar en la Base de Datos 😢")
        return

    print("📥 Iniciando la carga de Datos en la Base de Datos...\n")

    for table_name, df in data_frames.items():
        try:
            # Obtenemos una conexión raw que implementa la interfaz DBAPI (por ejemplo, con .cursor())
            raw_conn = database.raw_connection()
            try:
                # Utilizamos raw_conn en to_sql()
                df.to_sql(table_name, con=raw_conn, if_exists="replace", index=False)
                raw_conn.commit()  # Commit para guardar los cambios en caso de SQLite
                print(f"✅ Tabla '{table_name}' Cargada Exitosamente con {len(df)} registros.")
            finally:
                raw_conn.close()
        except Exception as e:
            print(f"❌ Error al Cargar la Tabla '{table_name}': {e}")

    print("\n ✅🎉 Proceso de Carga Finalizado con Éxito. 🚀 ")
