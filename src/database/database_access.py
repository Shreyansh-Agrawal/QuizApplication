'''Contains methods for establishing database connection'''

import logging
import os
from pathlib import Path
from typing import List, Tuple

import mysql.connector
from dotenv import load_dotenv

from config.queries import InitializationQueries

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')


class DatabaseAccess:
    '''A class for database methods.'''

    connection = None
    cursor = None

    def __init__(self) -> None:
        if DatabaseAccess.connection is None:
            try:
                DatabaseAccess.connection = mysql.connector.connect(
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    host=MYSQL_HOST
                )
                DatabaseAccess.cursor = DatabaseAccess.connection.cursor(dictionary=True)
                DatabaseAccess.cursor.execute(InitializationQueries.CREATE_DATABASE.format(MYSQL_DB))
                DatabaseAccess.cursor.execute(InitializationQueries.USE_DATABASE.format(MYSQL_DB))
            except mysql.connector.Error as e:
                logger.exception(e)
                print(f'Exception inside DatabaseAccess __init__: {e}')
                raise mysql.connector.Error from e
            else:
                logger.debug("Connected to MySQL database successfully")

        self.connection = DatabaseAccess.connection
        self.cursor = DatabaseAccess.cursor

    def read(self, query: str, data: Tuple = None) -> List:
        '''Reads data from database.'''
        try:
            if not data:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, data)
        except mysql.connector.OperationalError as e:
            logger.exception(e)
            print(f'Exception in DatabaseAccess read: {e}')
            return []

        return self.cursor.fetchall()

    def write(self, query: str, data: Tuple = None) -> None:
        '''CREATE TABLE / Add / Update / Delete data from database.'''
        try:
            if not data:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, data)
        except mysql.connector.OperationalError as e:
            logger.exception(e)
            print(f'Exception in DatabaseAccess write: {e}')

        self.connection.commit()

    def create_tables(self) -> None:
        '''
        Creates necessary tables in the database for the application.

        Executes SQL queries to create required tables:
        - Users
        - Credentials
        - Scores
        - Categories
        - Questions
        - Options

        Returns: 
            None
        '''
        self.cursor.execute(InitializationQueries.CREATE_USERS_TABLE)
        self.cursor.execute(InitializationQueries.CREATE_CREDENTIALS_TABLE)
        self.cursor.execute(InitializationQueries.CREATE_SCORES_TABLE)
        self.cursor.execute(InitializationQueries.CREATE_CATEGORIES_TABLE)
        self.cursor.execute(InitializationQueries.CREATE_QUESTIONS_TABLE)
        self.cursor.execute(InitializationQueries.CREATE_OPTIONS_TABLE)
