'''Context Manager for the database'''

import logging
import os
from pathlib import Path
import pymysql
import mysql.connector
from dotenv import load_dotenv

from config.queries import InitializationQueries

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    '''
    A class for MySQL database connection
    Automatically opens, commits, and closes the connections
        
    Implements Connection through MySQL connection pools
    '''

    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT'))

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.setup_connection()

    def setup_connection(self) -> None:
        'sets up connection to MySQL'

        timeout = 10
        self.connection = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            user=DatabaseConnection.MYSQL_USER,
            password=DatabaseConnection.MYSQL_PASSWORD,
            host=DatabaseConnection.MYSQL_HOST,
            port=DatabaseConnection.MYSQL_PORT,
            read_timeout=timeout,
            write_timeout=timeout,
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(InitializationQueries.CREATE_DATABASE.format(DatabaseConnection.MYSQL_DB))
        self.cursor.execute(InitializationQueries.USE_DATABASE.format(DatabaseConnection.MYSQL_DB))

    def __enter__(self) -> mysql.connector.connection.MySQLConnection:
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type or exc_tb or exc_val:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
