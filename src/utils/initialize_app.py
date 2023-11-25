'''Runs at the start to create super admin and other tables in database'''

import hashlib
import logging
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

from config.message_prompts import DisplayMessage, Headers, LogMessage
from config.queries import InitializationQueries
from database.database_access import DatabaseAccess as DAO
from models.user import SuperAdmin
from utils.custom_error import DuplicateEntryError

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)


class Initializer:
    '''Class containing methods to create super admin'''

    @staticmethod
    def create_super_admin() -> None:
        '''method to create a super admin '''

        logger.debug(LogMessage.CREATE_ENTITY, Headers.SUPER_ADMIN)

        super_admin_data = {}
        super_admin_data['name'] = os.getenv('SUPER_ADMIN_NAME')
        super_admin_data['email'] = os.getenv('SUPER_ADMIN_EMAIL')
        super_admin_data['username'] = os.getenv('SUPER_ADMIN_USERNAME')

        password = os.getenv('SUPER_ADMIN_PASSWORD')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        super_admin_data['password'] = hashed_password
        super_admin = SuperAdmin(super_admin_data)
        try:
            super_admin.save_to_database()
        except sqlite3.IntegrityError as e:
            raise DuplicateEntryError('Super Admin Already exists!') from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.SUPER_ADMIN)
        print(DisplayMessage.CREATE_SUPER_ADMIN_SUCCESS_MSG)

    @staticmethod
    def initialize_app() -> None:
        '''method to initialize application'''

        InitializeDatabase.initialize_database()

        try:
            Initializer.create_super_admin()
        except DuplicateEntryError:
            logger.debug(LogMessage.SUPER_ADMIN_PRESENT)

        logger.debug(LogMessage.INITIALIZE_APP_SUCCESS)
        print(DisplayMessage.INITIALIZATION_SUCCESS_MSG)


class InitializeDatabase:
    '''Class to create tables for database'''

    @staticmethod
    def initialize_database() -> None:
        '''method to create tables in database'''

        DAO.write_to_database(InitializationQueries.CREATE_USERS_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_CREDENTIALS_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_SCORES_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_CATEGORIES_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_QUESTIONS_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_OPTIONS_TABLE)
