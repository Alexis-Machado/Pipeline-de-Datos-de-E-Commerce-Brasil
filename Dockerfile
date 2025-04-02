# Iniciamos desde la imagen oficial de Airflow en la versión 2.9.0
FROM apache/airflow:2.9.0

# Cambiamos al usuario 'airflow' (por defecto en la imagen de Airflow)
USER airflow

# Actualizamos pip a la última versión disponible
RUN pip install --upgrade pip

# Copiamos el archivo requirements.txt al directorio /opt/airflow dentro del contenedor
COPY requirements.txt /opt/airflow/requirements.txt

# Instalamos las dependencias listadas en requirements.txt
RUN pip install -r /opt/airflow/requirements.txt
