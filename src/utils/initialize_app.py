'''Runs at the start to create super admin and other tables in database'''

import hashlib
import logging
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

from config.display_menu import DisplayMessage
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
    def create_super_admin():
        '''method to create a super admin '''

        logger.debug('Creating Super Admin')

        super_admin_data = {}
        super_admin_data['name'] = os.getenv('SUPER_ADMIN_NAME')
        super_admin_data['email'] = os.getenv('SUPER_ADMIN_EMAIL')
        super_admin_data['username'] = os.getenv('SUPER_ADMIN_USERNAME')

        password = os.getenv('SUPER_ADMIN_PASSWORD')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        super_admin_data['password'] = hashed_password
        super_admin = SuperAdmin(super_admin_data)
        try:
            super_admin.save_user_to_database()
        except sqlite3.IntegrityError as e:
            raise DuplicateEntryError('Super Admin Already exists!') from e

        logger.debug('Created Super Admin')
        print(DisplayMessage.CREATE_SUPER_ADMIN_SUCCESS_MSG)

    @staticmethod
    def initialize_app():
        '''method to initialize application'''

        InitializeDatabase.initialize_database()

        try:
            Initializer.create_super_admin()
        except DuplicateEntryError:
            logger.debug('Super Admin Present')

        logger.debug('Initialization Complete')
        print(DisplayMessage.INITIALIZATION_SUCCESS_MSG)


class InitializeDatabase:
    '''Class to create tables for database'''

    @staticmethod
    def initialize_database():
        '''method to create tables in database'''

        DAO.write_to_database(InitializationQueries.CREATE_USERS_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_CREDENTIALS_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_SCORES_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_CATEGORIES_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_QUESTIONS_TABLE)
        DAO.write_to_database(InitializationQueries.CREATE_OPTIONS_TABLE)
