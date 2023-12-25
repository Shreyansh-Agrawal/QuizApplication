'''Contains methods for establishing database connection'''

import logging
import sqlite3
from typing import List, Tuple

from config.file_paths import FilePaths
from config.queries import InitializationQueries

logger = logging.getLogger(__name__)


class DatabaseAccess:
    '''A class for database methods.'''

    def __init__(self) -> None:
        try:
            self.database_path = FilePaths.DATABASE_PATH
            self.connection = sqlite3.connect(self.database_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            logger.exception(e)
            print(f'Exception inside DatabaseAccess __init__: {e}')
            raise sqlite3.Error from e

    def read_from_database(self, query: str, data: Tuple = None) -> List:
        '''Reads data from database.'''
        try:
            if not data:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, data)
        except sqlite3.OperationalError as e:
            logger.exception(e)
            print(f'Exception in read_from_database: {e}')
            return []

        return self.cursor.fetchall()

    def write_to_database(self, query: str, data: Tuple = None) -> None:
        '''CREATE TABLE / Add / Update / Delete data from database.'''
        try:
            self.cursor.execute(InitializationQueries.ENABLE_FOREIGN_KEYS)
            if not data:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, data)
        except sqlite3.OperationalError as e:
            logger.exception(e)
            print(f'Exception in write_to_database: {e}')

        self.connection.commit()


db = DatabaseAccess()
