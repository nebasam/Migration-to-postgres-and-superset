from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta

default_args = {
    'owner': '10Academy',
    'depends_on_past': True,
    'start_date': datetime(2021, 9, 24),
    'email': ['neba.samuel17@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}
dag = DAG(
    'data_load_dag',
    default_args=default_args,
    description='An Airflow DAG to invoke simple dbt commands',
    schedule_interval='@once',
    # schedule_interval='*/ * * * *'
)


create_station_mysql_task = MySqlOperator(
    task_id='create_satations',
    mysql_conn_id='mysql_conn_id',
    sql='./create_station.sql',
    dag=dag
)


load_statation = MySqlOperator(
    task_id='load_station_data',
    mysql_conn_id='mysql_conn_id',
    sql='./insert_station.sql',
    dag=dag

)

create_station_summary_mysql_task = MySqlOperator(
    task_id='station_summary_creator',
    mysql_conn_id='mysql_conn_id',
    sql='./create_station_summary.sql',
    dag=dag
)


load_station_summary = MySqlOperator(
    task_id='station_summary_loader',
    mysql_conn_id='mysql_conn_id',
    sql='./insert_station_summary.sql',
    dag=dag
)
create_station_mysql_task >> load_statation
create_station_summary_mysql_task >> load_station_summary