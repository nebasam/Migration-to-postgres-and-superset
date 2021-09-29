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
