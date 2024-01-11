'''Runs at the start to create super admin and other tables in database'''

import logging
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

from config.message_prompts import DisplayMessage, ErrorMessage, Headers, LogMessage
from config.queries import InitializationQueries, Queries
from models.database.database_access import db
from models.users.super_admin import SuperAdmin
from utils.custom_error import DuplicateEntryError
from utils.password_hasher import hash_password

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)


class Initializer:
    '''
    Contains methods to create a super admin and initialize the application.
    
    Methods:
        create_super_admin(): Creates a super admin account for the application.
        initialize_app(): Initializes the application by setting up necessary tables and the super admin.
    '''

    @staticmethod
    def create_super_admin() -> None:
        '''
        Creates a super admin account in the application.

        This method gathers necessary information to create a super admin:
        - Retrieves super admin details like name, email, username, and hashed password from environment variables.
        - Attempts to create a SuperAdmin instance and save it to the database.
        If a super admin with the same details already exists, it raises a DuplicateEntryError.

        Raises:
            DuplicateEntryError: If an attempt is made to create a super admin that already exists.

        Returns:
            None
        '''

        logger.debug(LogMessage.CREATE_ENTITY, Headers.SUPER_ADMIN)

        super_admin_data = {}
        super_admin_data['name'] = os.getenv('SUPER_ADMIN_NAME')
        super_admin_data['email'] = os.getenv('SUPER_ADMIN_EMAIL')
        super_admin_data['username'] = os.getenv('SUPER_ADMIN_USERNAME')
        password = os.getenv('SUPER_ADMIN_PASSWORD')
        super_admin_data['password'] = hash_password(password)
        super_admin = SuperAdmin(super_admin_data)

        try:
            user = db.read_from_database(Queries.GET_USER_BY_ROLE, ('super admin', ))
            if user:
                return
            super_admin.save_to_database()
        except mysql.connector.IntegrityError as e:
            raise DuplicateEntryError(
                ErrorMessage.ENTITY_EXISTS_ERROR.format(entity=Headers.SUPER_ADMIN)
            ) from e

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.SUPER_ADMIN)
        print(DisplayMessage.CREATE_SUPER_ADMIN_SUCCESS_MSG)

    @staticmethod
    def initialize_app() -> None:
        '''
        Initializes the application by creating necessary tables and the super admin.

        This method initiates the application by setting up essential components:
        - It initializes the database by creating required tables using InitializeDatabase.initialize_database().
        - Attempts to create a super admin using Initializer.create_super_admin() method.
        If a super admin already exists, it logs a debug message indicating its presence.

        Returns:
            None
        '''

        InitializeDatabase.initialize_database()

        try:
            Initializer.create_super_admin()
        except DuplicateEntryError:
            logger.debug(LogMessage.SUPER_ADMIN_PRESENT)

        logger.debug(LogMessage.INITIALIZE_APP_SUCCESS)
        print(DisplayMessage.INITIALIZATION_SUCCESS_MSG)


class InitializeDatabase:
    '''
    Contains methods to create tables for the database.

    Methods:
        initialize_database(): Creates tables in the database for the application.
    '''

    @staticmethod
    def initialize_database() -> None:
        '''
        Creates necessary tables in the database for the application.

        Executes SQL queries to create essential tables:
        - Users
        - Credentials
        - Scores
        - Categories
        - Questions
        - Options

        Returns: 
            None
        '''
        db.write_to_database(InitializationQueries.CREATE_USERS_TABLE)
        db.write_to_database(InitializationQueries.CREATE_CREDENTIALS_TABLE)
        db.write_to_database(InitializationQueries.CREATE_SCORES_TABLE)
        db.write_to_database(InitializationQueries.CREATE_CATEGORIES_TABLE)
        db.write_to_database(InitializationQueries.CREATE_QUESTIONS_TABLE)
        db.write_to_database(InitializationQueries.CREATE_OPTIONS_TABLE)
