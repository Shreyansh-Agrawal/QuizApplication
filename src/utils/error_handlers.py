'''Functions to handle errors'''

import functools

from flask import jsonify

from utils.custom_error import DataNotFoundError, DuplicateEntryError, InvalidCredentialsError, InvalidInputError


def handle_internal_server_error(_err):
    '''Function to handle server side errors'''

    return jsonify({'code': 500, 'status': 'Something went wrong'}), 500


def handle_custom_errors(func):
    '''Decorator to handle custom exceptions'''

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except DuplicateEntryError as e:
            return e.error_info, e.code
        except DataNotFoundError as e:
            return e.error_info, e.code
        except InvalidCredentialsError as e:
            return e.error_info, e.code
        except InvalidInputError as e:
            return e.error_info, e.code
        return res

    return wrapper
