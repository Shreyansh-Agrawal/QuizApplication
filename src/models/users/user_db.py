'''Contains UserManagerClass'''

from dataclasses import astuple

from config.queries import Queries
from models.database.database_access import db
from models.database.database_saver import DatabaseSaver
from models.users.user import User


class UserDB(DatabaseSaver):
    '''Class responsible for saving users to the database.'''

    @classmethod
    def save(cls, entity: User) -> None:
        '''
        Saves the user data and their credentials to the database.

        user_data = (
            user.user_id,
            user.name,
            user.email,
            user.role,
            user.registration_date
        )
        credentials = (
            user.user_id,
            user.username,
            user.password,
            user.is_password_changed
        )
        '''
        user_data = astuple(entity)[:5]
        credentials = (astuple(entity)[0], ) + astuple(entity)[5:]

        db.write(Queries.INSERT_USER_DATA, user_data)
        db.write(Queries.INSERT_CREDENTIALS, credentials)
