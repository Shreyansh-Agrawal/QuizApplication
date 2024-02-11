'''Functions to handle errors'''

import functools
import logging

from config.string_constants import ErrorMessage, LogMessage, StatusCodes
from utils.custom_error import (
    CustomError,
    DataNotFoundError,
    DuplicateEntryError,
    InvalidCredentialsError,
    InvalidInputError
)

logger = logging.getLogger(__name__)


def handle_bad_request(err):
    '''Function to handle bad request'''

    logger.exception(err)
    error = CustomError(status=StatusCodes.BAD_REQUEST, message=ErrorMessage.BAD_REQUEST)
    return error.error_info, error.code


def handle_invalid_url(err):
    '''Function to handle invalid url'''

    logger.exception(err)
    error = CustomError(status=StatusCodes.NOT_FOUND, message=ErrorMessage.INVALID_URL)
    return error.error_info, error.code


def handle_validation_error(err):
    '''Function to handle validation errors'''

    logger.exception(err)
    error = CustomError(status=StatusCodes.UNPROCESSABLE_ENTITY, message=str(err.message))
    return error.error_info, error.code


def handle_internal_server_error(err):
    '''Function to handle server side errors'''

    logger.exception(err)
    error = CustomError(status=StatusCodes.INTERNAL_SERVER_ERROR, message=ErrorMessage.SERVER_ERROR)
    return error.error_info, error.code


def handle_custom_errors(func):
    '''Decorator to handle custom exceptions'''

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        try:
            logger.info(LogMessage.FUNCTION_CALL, func.__name__, func.__module__)
            res = func(*args, **kwargs)

        except DuplicateEntryError as e:
            logger.error(e.message)
            return e.error_info, e.code

        except DataNotFoundError as e:
            logger.error(e.message)
            return e.error_info, e.code

        except InvalidCredentialsError as e:
            logger.error(e.message)
            return e.error_info, e.code

        except InvalidInputError as e:
            logger.error(e.message)
            return e.error_info, e.code

        return res

    return wrapper
