from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from airflow.operators.mysql_operator import MySqlOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator

import mysql.connector as mysql
from sqlalchemy import create_engine, types, text
import pandas as pd
import json

import sys
sys.path.insert(0, "/airflow_postgres/dags/scripts")
import scripts.mysql_converter as mysql_converter

mysql_user = 'root'
mysql_password = 'mypass'
mysql_host = 'mysql-dbt'
mysql_db_name = 'tech_stack'
mysql_port = 3306

postgres_user = 'dbt'
postgres_password = 'mypass'
postgres_host = 'postgres-db'
postgres_db_name = 'tech_stack'
postgres_port = 5432

def create_mysql_connection():

    connection = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db_name}'
    engine = create_engine(connection)
    return engine

def get_table_names():
   engine = create_mysql_connection()
   conn = engine.connect()
   query = text(f'show tables')
   result = conn.execute(query)
   return ['Station_Summary', 'I80Stations']
   
def get_record(table_name):
   engine = create_mysql_connection()
   conn = engine.connect()
   query = text(f'SELECT COUNT(*) FROM {table_name}')
   result = conn.execute(query)
   return result.fetchone()[0]

def migrate_sql_statemtents(**kwargs):
  src_path = kwargs['src_path']
  tgt_path = kwargs['tgt_path']
  mysql_converter.convert_create_statements(src_path, tgt_path)

def migrate(**kwargs):
    table_name = kwargs['table_name']

    engine = create_mysql_connection()
    row_count = get_record_count(f'{table_name}')

    cur = 0
    while cur < row_count :
        query = f'select * from {table_name} Limit {cur}, {selec_batch_size}'
        result_df = pd.read_sql(query, con=engine)
        load_to_postgres(result_df, table_name)
        cur += selec_batch_size
    print("select statment finished")

def load_to_postgres(mysql_df, table_name):
    mysql_df.columns= mysql_df.columns.str.lower()
    conn_str = f'postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}'
    engine = create_engine(conn_str)
    mysql_df.to_sql(table_name.lower(), con=engine, index=False, if_exists='append')
