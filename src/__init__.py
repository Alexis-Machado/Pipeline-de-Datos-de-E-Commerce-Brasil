# Definimos la variable "something" para que pueda importarse con "from src import something"
something = "Este es el valor de something"

# Reexportamos algunas variables y funciones desde config.py
from .config import DATASET_ROOT_PATH, PUBLIC_HOLIDAYS_URL, SQLITE_BD_ABSOLUTE_PATH, get_csv_to_table_mapping
