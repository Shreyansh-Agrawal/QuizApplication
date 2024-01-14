'''Runs at the start to create super admin and other tables in database'''

import logging
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

from config.message_prompts import DisplayMessage, Headers, LogMessage
from config.queries import Queries
from models.database.database_access import db
from models.users.super_admin import SuperAdmin
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

        user = db.read(Queries.GET_USER_BY_ROLE, ('super admin', ))
        if user:
            return

        logger.debug(LogMessage.CREATE_ENTITY, Headers.SUPER_ADMIN)

        super_admin_data = {}
        super_admin_data['name'] = os.getenv('SUPER_ADMIN_NAME')
        super_admin_data['email'] = os.getenv('SUPER_ADMIN_EMAIL')
        super_admin_data['username'] = os.getenv('SUPER_ADMIN_USERNAME')
        password = os.getenv('SUPER_ADMIN_PASSWORD')
        super_admin_data['password'] = hash_password(password)
        super_admin = SuperAdmin(super_admin_data)

        try:
            super_admin.save_to_database()
        except mysql.connector.IntegrityError:
            logger.debug(LogMessage.SUPER_ADMIN_PRESENT)

        logger.debug(LogMessage.CREATE_SUCCESS, Headers.SUPER_ADMIN)
        print(DisplayMessage.CREATE_SUPER_ADMIN_SUCCESS_MSG)

    @staticmethod
    def initialize_app() -> None:
        '''
        Initializes the application by creating necessary tables and the super admin.
        Returns:
            None
        '''
        db.create_tables()
        Initializer.create_super_admin()

        logger.debug(LogMessage.INITIALIZE_APP_SUCCESS)
        print(DisplayMessage.INITIALIZATION_SUCCESS_MSG)
