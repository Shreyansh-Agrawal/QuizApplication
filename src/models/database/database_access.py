'''Contains methods for establishing database connection'''

import logging
import os
from pathlib import Path
from typing import List, Tuple

import mysql.connector
from dotenv import load_dotenv

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)


class DatabaseAccess:
    '''A class for database methods.'''

    connection = None
    cursor = None

    def __init__(self) -> None:
        if DatabaseAccess.connection is None:
            try:
                DatabaseAccess.connection = mysql.connector.connect(
                    user=os.getenv('MYSQL_USER'),
                    password=os.getenv('MYSQL_PASSWORD'),
                    host=os.getenv('MYSQL_HOST'),
                    database=os.getenv('MYSQL_DB')
                )
                DatabaseAccess.cursor = DatabaseAccess.connection.cursor()
            except mysql.connector.Error as e:
                logger.exception(e)
                print(f'Exception inside DatabaseAccess __init__: {e}')
                raise mysql.connector.Error from e
            else:
                logger.debug("Connected to MySQL database successfully")

        self.connection = DatabaseAccess.connection
        self.cursor = DatabaseAccess.cursor

    def read_from_database(self, query: str, data: Tuple = None) -> List:
        '''Reads data from database.'''
        try:
            if not data:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, data)
        except mysql.connector.OperationalError as e:
            logger.exception(e)
            print(f'Exception in read_from_database: {e}')
            return []

        return self.cursor.fetchall()

    def write_to_database(self, query: str, data: Tuple = None) -> None:
        '''CREATE TABLE / Add / Update / Delete data from database.'''
        try:
            if not data:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, data)
        except mysql.connector.OperationalError as e:
            logger.exception(e)
            print(f'Exception in write_to_database: {e}')

        self.connection.commit()


db = DatabaseAccess()
