'''Contains methods for establishing database connection'''

import logging
from typing import List, Tuple

import mysql.connector

from config.queries import InitializationQueries
from database.database_connection import DatabaseConnection

logger = logging.getLogger(__name__)


class DatabaseAccess:
    '''A class for database methods.'''

    def read(self, query: str, data: Tuple = None) -> List:
        '''Reads data from database.'''

        with DatabaseConnection() as connection:
            cursor = connection.cursor(dictionary=True)
            try:
                if not data:
                    cursor.execute(query)
                else:
                    cursor.execute(query, data)
            except mysql.connector.OperationalError as e:
                logger.exception(e)
                return []
            return cursor.fetchall()

    def write(self, query: str, data: Tuple = None) -> None:
        '''CREATE TABLE / Add / Update / Delete data from database.'''

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            try:
                if not data:
                    cursor.execute(query)
                else:
                    cursor.execute(query, data)
                cursor.execute('SELECT ROW_COUNT()')
                rows_affected = cursor.fetchone()[0]
                if rows_affected:
                    return True
            except mysql.connector.OperationalError as e:
                logger.exception(e)

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
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(InitializationQueries.CREATE_USERS_TABLE)
            cursor.execute(InitializationQueries.CREATE_CREDENTIALS_TABLE)
            cursor.execute(InitializationQueries.CREATE_SCORES_TABLE)
            cursor.execute(InitializationQueries.CREATE_CATEGORIES_TABLE)
            cursor.execute(InitializationQueries.CREATE_QUESTIONS_TABLE)
            cursor.execute(InitializationQueries.CREATE_OPTIONS_TABLE)
