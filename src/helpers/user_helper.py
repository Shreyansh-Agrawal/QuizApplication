'Helpers for user related management'

from dataclasses import astuple

import pymysql

from config.queries import Queries
from config.string_constants import ErrorMessage
from models.users.user import User


class UserHelper:
    'Helper class to save user to database'

    def __init__(self, database) -> None:
        self.db = database

    def save_user(self, entity: User) -> None:
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
        username = self.db.read(Queries.GET_USERNAME, (entity.username, ))
        if username:
            raise pymysql.IntegrityError(ErrorMessage.USER_EXISTS)
        self.db.write(Queries.INSERT_USER_DATA, user_data)
        self.db.write(Queries.INSERT_CREDENTIALS, credentials)
