import sys
import os

# Añadimos la ruta contenedora de 'src' al sys.path
parent_path = '/opt/airflow'
if parent_path not in sys.path:
    sys.path.append(parent_path)

# Depuración: imprimir el sys.path y el contenido de la carpeta src
print("sys.path:", sys.path)
print("Contenido de /opt/airflow/src:", os.listdir('/opt/airflow/src'))

# Verificamos que __init__.py existe en la carpeta src
if '__init__.py' not in os.listdir('/opt/airflow/src'):
    raise FileNotFoundError("El archivo __init__.py no existe en /opt/airflow/src")

# Ahora podemos importar desde el paquete src
from src import something

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from pathlib import Path
import matplotlib

# Configuramos backend no interactivo para matplotlib
matplotlib.use('Agg')

try:
    from sqlalchemy import create_engine
    from src.config import DATASET_ROOT_PATH, PUBLIC_HOLIDAYS_URL, SQLITE_BD_ABSOLUTE_PATH, get_csv_to_table_mapping
    from src.extract import extract
    from src.load import load
    from src.transform import run_queries
    from src.plots import (
        plot_freight_value_weight_relationship,
        plot_global_amount_order_status,
        plot_real_vs_predicted_delivered_time,
        plot_revenue_by_month_year,
        plot_revenue_per_state,
        plot_top_10_least_revenue_categories,
        plot_top_10_revenue_categories,
        plot_top_10_revenue_categories_ammount,
        plot_delivery_date_difference,
        plot_order_amount_per_day_with_holidays,
    )
except Exception as e:
    print(f"Error al importar módulos: {e}")
    raise

# Creamos la base de datos SQLite si no existe
db_path = Path(SQLITE_BD_ABSOLUTE_PATH)
db_path.parent.mkdir(parents=True, exist_ok=True)
db_path.touch(exist_ok=True)

# Creamos la conexión a la base de datos
ENGINE = create_engine(f"sqlite:///{SQLITE_BD_ABSOLUTE_PATH}", echo=False)

# Definimos los argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definimos el DAG
with DAG(
    'olist_pipeline_dag',
    default_args=default_args,
    description='Pipeline ELT para el proyecto Olist',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2025, 3, 26),
    catchup=False,
) as dag:

    # Tarea 1: Extraer datos
    def extract_data():
        csv_folder = DATASET_ROOT_PATH
        public_holidays_url = PUBLIC_HOLIDAYS_URL
        csv_table_mapping = get_csv_to_table_mapping()
        dataframes = extract(csv_folder, csv_table_mapping, public_holidays_url)
        return dataframes

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    # Tarea 2: Cargar datos en la base de datos
    def load_data(**context):
        dataframes = context['task_instance'].xcom_pull(task_ids='extract_data')
        load(data_frames=dataframes, database=ENGINE)

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
    )

    # Tarea 3: Transformar datos
    def transform_data():
        query_results = run_queries(database=ENGINE)
        return query_results

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    # Tarea 4: Generar gráficos
    def generate_plots(**context):
        query_results = context['task_instance'].xcom_pull(task_ids='transform_data')
        
        plot_revenue_by_month_year(query_results['revenue_by_month_year'], 2017)
        plot_real_vs_predicted_delivered_time(query_results['real_vs_estimated_delivered_time'], 2017)
        plot_global_amount_order_status(query_results['global_ammount_order_status'])
        plot_revenue_per_state(query_results['revenue_per_state'])
        plot_top_10_least_revenue_categories(query_results['top_10_least_revenue_categories'])
        plot_top_10_revenue_categories(query_results['top_10_revenue_categories'])
        plot_top_10_revenue_categories_ammount(query_results['top_10_revenue_categories'])
        plot_freight_value_weight_relationship(query_results['get_freight_value_weight_relationship'])
        plot_delivery_date_difference(query_results['delivery_date_difference'])
        plot_order_amount_per_day_with_holidays(query_results['orders_per_day_and_holidays_2017'])

    plot_task = PythonOperator(
        task_id='generate_plots',
        python_callable=generate_plots,
        provide_context=True,
    )

    # Definimos el orden de ejecución de las tareas
    extract_task >> load_task >> transform_task >> plot_task

# Imprimimos el valor importado de something
print("Valor de something:", something)
