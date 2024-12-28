from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from dagutils import store_data_cleaner

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 12, 27),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": False,
}

with DAG(dag_id="store_dag", default_args=default_args, schedule_interval=timedelta(days=1),template_searchpath=['/usr/local/airflow/sql_files']) as dag:

    t1=BashOperator(task_id='check_file_exists', bash_command='shasum /usr/local/airflow/store_files_airflow/raw_store_transactions.csv', retries=2, retry_delay=timedelta(seconds=5))
    t2=PythonOperator(task_id='clean_raw_csv', python_callable=store_data_cleaner)
    t3=MySqlOperator(task_id='create_mysql_table', mysql_conn_id='mysql_conn', sql='create_table.sql')
    t4=MySqlOperator(task_id='truncate_table', mysql_conn_id='mysql_conn', sql='truncate_table.sql')
    t5=MySqlOperator(task_id='insert_into_table', mysql_conn_id='mysql_conn', sql='insert_into_table.sql')
    t6=MySqlOperator(task_id='select_from_table', mysql_conn_id="mysql_conn", sql="select_from_table.sql")

    t1 >> t2 >> t3 >> t4 >> t5 >> t6
