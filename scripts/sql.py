from typing import Callable
from mysql.connector import connect, Error
import pandas as pd
from logger import Logger

logger = Logger().get_logger(__name__)


class Database_handler():
    def __init__(self, host: str = 'localhost', port: int = 3306, username: str = 'root', password: str = 'neba'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.working = False

        try:
            with connect(host=host, user=username, password=password, port=port) as connection:
                self.working = True
                logger.info(
                    f'SUCCESSFULLY CONNECTED TO DATABASE @{host}\n\tconnection -> {type(connection)} recieved')

        except Error as e:
            self.working = False
            logger.exception(f'FAILED TO CONNECT TO THE DATABASE @{host}')

    def sql_query(self, query: str, func: Callable[..., None] = None):
        create_db_query = "CREATE DATABASE online_movie_rating"
        drop_table_query = "DROP TABLE ratings"
        try:
            assert self.working
            with connect(host=self.host, port=self.port, user=self.username, password=self.password) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    if(func != None):
                        func(cursor)

        except AssertionError:
            logger.error(
                f'DATABASE CONNECTION NOT WORKING, INSTANTIATE CLASS WITH WORKING DATABASE HOST')

        except Error as e:
            logger.exception(f'FAILED TO PERFORM SQL QUERY\n\t -> {query}')

    def connect_db(self, database: str, func=None):
        try:
            with connect(host=self.host, user=self.username, password=self.password, port=self.port, database=database) as connection:
                if(func != None):
                    func(connection)

        except Error as e:
            print(e)

    def execute_query_on_db(self, query: str, database: str):
        def execute_func(connection):
            with connection.cursor() as cursor:
                cursor.execute(query)

        self.connect_db(database=database, func=execute_func)

    def insert_table(self, table_create_query: str, database: str):
        def execute_func(connection):
            with connection.cursor() as cursor:
                cursor.execute(table_create_query)
                connection.commit()

        self.connect_db(database=database, func=execute_func)

    def insert_values(self, database, insert_query: str, file_path: str):
        def execute_func(connection):
            if file_path.endswith('.txt'):
                with connection.cursor() as cursor:
                    with open(file_path, mode='r') as readfile:
                        for data in readfile:
                            data = self.format_text_data(data)
                            cursor.execute(insert_query, data)
                            connection.commit()

            elif file_path.endswith('.csv'):
                with connection.cursor() as cursor:
                    df = pd.read_csv(file_path, keep_default_na=False)
                    for _, row in df.iterrows():
                        data = (self.type_converter(row[0], int), self.type_converter(row[1], int), self.type_converter(row[2], str), self.type_converter(row[3], int), self.type_converter(row[4], int), self.type_converter(row[5], int),
                                self.type_converter(row[6], str), self.type_converter(row[7], float), self.type_converter(
                                    row[8], float), self.type_converter(row[9], float), self.type_converter(row[10], float), self.type_converter(row[11], str),
                                self.type_converter(row[12], int), self.type_converter(row[13], str), self.type_converter(row[14], str), self.type_converter(row[15], str), self.type_converter(
                                    row[16], int), self.type_converter(row[17], int)
                                )
                        print(data)

                        cursor.execute(insert_query, data)
                        connection.commit()
            else:
                raise Exception(
                    'UNSUPPORTED DATA TYPE PROVIDED, USE txt or csv FILE TYPES ONLY')

        self.connect_db(database=database, func=execute_func)

    def format_text_data(self, data):
        insert_values = data.strip().split(',')
        insert_values = [i if i != "" else None for i in insert_values]
        date, time = insert_values[0].split(" ")
        date = date.split('/')
        date.insert(0, date[2])
        date = '-'.join(date[:-1])
        insert_values.insert(1, time)
        insert_values[0] = date
        clean_data = [int(insert_values[2])]
        clean_data.extend(insert_values[:2])
        clean_data.extend(
            [float(i) if i != None else i for i in insert_values[3:]])

        return tuple(clean_data)

    def type_converter(self, value, new_type):
        try:
            if new_type == str and value == '':
                return None
            else:
                return new_type(value)
        except:
            return None


if __name__ == "__main__":
    sql = Database_handler(host='localhost', port=3306,
                      username='root', password='password')