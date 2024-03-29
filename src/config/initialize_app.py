'''Runs at the start to create super admin and other tables in database'''

import logging
import os

import mysql.connector

from config.string_constants import Headers, LogMessage, Roles
from config.queries import Queries
from database.database_access import DatabaseAccess
from helpers.user_helper import UserHelper
from models.users.super_admin import SuperAdmin
from utils.password_hasher import hash_password

logger = logging.getLogger(__name__)


class Initializer:
    '''
    Contains methods to create a super admin and initialize the application.
    
    Methods:
        create_super_admin(): Creates a super admin account for the application.
        initialize_app(): Initializes the application by setting up necessary tables and the super admin.
    '''

    def __init__(self, db: DatabaseAccess) -> None:
        self.db = db
        self.user_helper = UserHelper(self.db)

    def create_super_admin(self) -> None:
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

        user = self.db.read(Queries.GET_USER_BY_ROLE, (Roles.SUPER_ADMIN, ))
        if user:
            return

        logger.info(LogMessage.CREATE_ENTITY, Headers.SUPER_ADMIN)

        super_admin_data = {}
        super_admin_data['name'] = os.getenv('SUPER_ADMIN_NAME')
        super_admin_data['email'] = os.getenv('SUPER_ADMIN_EMAIL')
        super_admin_data['username'] = os.getenv('SUPER_ADMIN_USERNAME')
        password = os.getenv('SUPER_ADMIN_PASSWORD')
        super_admin_data['password'] = hash_password(password)
        super_admin = SuperAdmin.get_instance(super_admin_data)

        try:
            self.user_helper.save_user(super_admin)
        except mysql.connector.IntegrityError as e:
            logger.exception(e)

        logger.info(LogMessage.CREATE_SUCCESS, Headers.SUPER_ADMIN)

    def initialize_app(self) -> None:
        '''
        Initializes the application by creating necessary tables and the super admin.
        Returns:
            None
        '''
        self.db.create_tables()
        self.create_super_admin()

        logger.info(LogMessage.INITIALIZE_APP_SUCCESS)
