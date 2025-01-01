from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 12, 27),
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "catchup": False,
}


with DAG(dag_id='xcom_example', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    def push_function(**kwargs):
        message='This is the pushed message.'
        ti = kwargs['ti']
        ti.xcom_push(key="message", value=message)

    def pull_function(**kwargs):
        ti = kwargs['ti']
        pulled_message = ti.xcom_pull(key='message', task_ids='push_task')
        print("Pulled Message: '%s'" % pulled_message)

    t1 = PythonOperator(
        task_id='push_task',
        python_callable=push_function,
        provide_context=True)

    t2 = PythonOperator(
        task_id='pull_task',
        python_callable=pull_function,
        provide_context=True)

    t1 >> t2
