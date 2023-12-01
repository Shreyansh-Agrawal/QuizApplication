'''Contains UserManagerClass'''

from config.queries import Queries
from database.database_access import DatabaseAccess as DAO


class UserManager:
    '''
    Manager class responsible for saving users to the database.

    Attributes:
        user (User): The user object to be managed.
    '''

    def __init__(self, user) -> None:
        self.user = user

    def save_to_database(self) -> None:
        '''Saves the user and their credentials to the database. '''

        user_data = (
            self.user.user_id,
            self.user.name,
            self.user.email,
            self.user.role,
            self.user.registration_date
        )

        credentials = (
            self.user.user_id,
            self.user.username,
            self.user.password,
            self.user.is_password_changed
        )

        DAO.write_to_database(Queries.INSERT_USER_DATA, user_data)
        DAO.write_to_database(Queries.INSERT_CREDENTIALS, credentials)
