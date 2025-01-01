from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators import DataTransferOperator


dag = DAG('custom_operator_data_transfer', schedule_interval=timedelta(1), start_date=datetime(2024, 12, 30), catchup=False)

t1 = DataTransferOperator(
        task_id='data_transfer',
        source_file_path = '/usr/local/airflow/plugins/source.txt',
        dest_file_path='/usr/local/airflow/plugins/destination.txt',
        delete_list = ['Airflow', 'is'],
        dag=dag
    )
