from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 12, 27),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": False,
}


with DAG(dag_id='variable_example', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    t1=BashOperator(task_id='print_path', bash_command='echo {{ var.value.source_path }}')
    t1
