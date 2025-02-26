import pickle
from src.load import load
from src import config
from sqlalchemy import create_engine

# Crear la conexión a la base de datos SQLite
ENGINE = create_engine(f'sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}', echo=False)

# Cargar el archivo pickle con los DataFrames extraídos
with open('csv_dataframes.pkl', 'rb') as f:
    csv_dataframes = pickle.load(f)

# Ejecutar la carga de datos
load(csv_dataframes, ENGINE)

print("✅ Datos cargados en la base de datos correctamente 🚀")
