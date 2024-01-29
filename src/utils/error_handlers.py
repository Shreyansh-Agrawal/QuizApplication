'''Functions to handle errors'''

import functools
from fastapi import HTTPException

from fastapi.responses import JSONResponse

from config.message_prompts import StatusCodes, ErrorMessage
from utils.custom_error import (
    CustomError,
    DataNotFoundError,
    DuplicateEntryError,
    InvalidCredentialsError,
    InvalidInputError,
)


def handle_bad_request(req, _err):
    '''Function to handle bad request'''
    error = CustomError(StatusCodes.BAD_REQUEST, message=ErrorMessage.BAD_REQUEST)
    return JSONResponse(content=error.error_info, status_code=error.code)


def handle_validation_error(req, err):
    '''Function to handle validation errors'''
    error = CustomError(StatusCodes.UNPROCESSABLE_ENTITY, message=err.errors())
    return JSONResponse(content=error.error_info, status_code=error.code)


def handle_internal_server_error(req, _err):
    '''Function to handle server side errors'''
    error = CustomError(StatusCodes.INTERNAL_SERVER_ERROR, message=ErrorMessage.SERVER_ERROR)
    return JSONResponse(content=error.error_info, status_code=error.code)


def handle_http_exception(req, err):
    '''Function to handle HTTPException and format its data while returning'''
    return JSONResponse(content=err.detail, status_code=err.status_code)


def handle_custom_errors(func):
    '''Decorator to handle custom exceptions'''

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except DuplicateEntryError as e:
            raise HTTPException(status_code=e.code, detail=e.error_info) from e
        except DataNotFoundError as e:
            raise HTTPException(status_code=e.code, detail=e.error_info) from e
        except InvalidCredentialsError as e:
            raise HTTPException(status_code=e.code, detail=e.error_info) from e
        except InvalidInputError as e:
            raise HTTPException(status_code=e.code, detail=e.error_info) from e
        return res

    return wrapper
