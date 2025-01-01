from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 12, 27),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": False,
}

with DAG(dag_id='dummy_operator_example', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    t1 = BashOperator(task_id='print_date1', bash_command='date')
    t2 = BashOperator(task_id='print_date2', bash_command='date')
    t3 = BashOperator(task_id='print_date3', bash_command='date')
    t4 = BashOperator(task_id='print_date4', bash_command='date')
    t5 = BashOperator(task_id='print_date5', bash_command='date')
    t6 = BashOperator(task_id='print_hi1', bash_command="echo 'Hi'")
    t7 = BashOperator(task_id='print_hi2', bash_command="echo 'Hi'")
    t8 = BashOperator(task_id='print_hi3', bash_command="echo 'Hi'")
    t9 = BashOperator(task_id='print_hi4', bash_command="echo 'Hi'")
    t10 = BashOperator(task_id='print_hi5', bash_command="echo 'Hi'")
    td = DummyOperator(task_id='dummy', dag=dag)

    [t1, t2, t3, t4, t5] >> td >> [t6, t7, t8, t9, t10]
