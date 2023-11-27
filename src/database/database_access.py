'''Contains methods for establishing database connection'''

import logging
import sqlite3
from typing import List, Tuple

from config.file_paths import FilePaths
from config.queries import InitializationQueries
from database.database_connection import DatabaseConnection

logger = logging.getLogger(__name__)


class DatabaseAccess:
    '''A class for database methods.'''

    @staticmethod
    def read_from_database(query: str, data: Tuple = None) -> List:
        '''Reads data from database.'''

        with DatabaseConnection(FilePaths.DATABASE_PATH) as connection:
            cursor = connection.cursor()
            try:
                if not data:
                    cursor.execute(query)
                else:
                    cursor.execute(query, data)
            except sqlite3.OperationalError as e:
                logger.exception(e)
                print(e)
                return []

            return cursor.fetchall()

    @staticmethod
    def write_to_database(query: str, data: Tuple = None) -> None:
        '''CREATE TABLE / Add / Update / Delete data from database.'''

        with DatabaseConnection(FilePaths.DATABASE_PATH) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(InitializationQueries.ENABLE_FOREIGN_KEYS)
                if not data:
                    cursor.execute(query)
                else:
                    cursor.execute(query, data)
            except sqlite3.OperationalError as e:
                logger.exception(e)
                print(e)
