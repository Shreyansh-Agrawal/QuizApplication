'''Context Manager for the database'''

import logging
import os

import mysql.connector

from config.queries import InitializationQueries

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
    MYSQL_POOL_NAME = 'quizapp_pool'
    MYSQL_POOL_SIZE = 3

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.setup_connection()

    def setup_connection(self) -> None:
        'sets up connection to MySQL'

        self.connection = mysql.connector.connect(
            user=DatabaseConnection.MYSQL_USER,
            password=DatabaseConnection.MYSQL_PASSWORD,
            host=DatabaseConnection.MYSQL_HOST,
            pool_name=DatabaseConnection.MYSQL_POOL_NAME,
            pool_size=DatabaseConnection.MYSQL_POOL_SIZE
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
