'''Contains methods for establishing database connection'''

import logging
from typing import Dict, List, Tuple

from config.queries import InitializationQueries
from database.database_connection import DatabaseConnection

logger = logging.getLogger(__name__)


class DatabaseAccess:
    '''A class for database methods.'''

    def read(self, query: str, data: Tuple = None) -> List[Dict]:
        '''Reads data from database.'''

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            if not data:
                cursor.execute(query)
            else:
                cursor.execute(query, data)

            return cursor.fetchall()

    def write(self, query: str, data: Tuple = None) -> bool:
        '''CREATE TABLE / Add / Update / Delete data from database.'''

        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            if not data:
                cursor.execute(query)
            else:
                cursor.execute(query, data)
            cursor.execute('SELECT ROW_COUNT()')

            rows_affected = cursor.fetchone()['ROW_COUNT()']
            if rows_affected:
                return True
            return False

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
