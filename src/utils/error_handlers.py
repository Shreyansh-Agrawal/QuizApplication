'''Functions to handle errors'''

import functools

from config.message_prompts import StatusCodes, ErrorMessage
from utils.custom_error import (
    CustomError,
    DataNotFoundError,
    DuplicateEntryError,
    InvalidCredentialsError,
    InvalidInputError,
)

def handle_bad_request(_err):
    '''Function to handle bad request'''
    error = CustomError(StatusCodes.BAD_REQUEST, message=ErrorMessage.BadRequest)
    return error.error_info, error.code

def handle_validation_error(err):
    '''Function to handle validation errors'''
    error = CustomError(StatusCodes.UNPROCESSABLE_ENTITY, message=str(err.message))
    return error.error_info, error.code

def handle_internal_server_error(_err):
    '''Function to handle server side errors'''
    error = CustomError(StatusCodes.INTERNAL_SERVER_ERROR, message=ErrorMessage.ServerError)
    return error.error_info, error.code


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
