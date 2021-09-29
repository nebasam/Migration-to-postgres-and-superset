from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta

default_args = {
    'owner': '10Academy',
    'depends_on_past': True,
    'start_date': datetime(2021, 9, 24),
    'email': ['neba.samuel17@gmail.com@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}
dag = DAG(
    'dbt_dag',
    default_args=default_args,
    description='An Airflow DAG to invoke simple dbt commands',
    schedule_interval='@once',
    # schedule_interval='*/1 * * * *'
)

dbt_debug = BashOperator(
    task_id='dbt_debug',
    bash_command='dbt debug',
    dag=dag
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run',
    dag=dag
)

docs = BashOperator(
    task_id='documentation',
    bash_command='dbt docs generate',
    dag=dag
)

dbt_debug >> dbt_run >> dbt_run >> docs