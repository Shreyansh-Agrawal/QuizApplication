'''Custom Error Classes'''

from dataclasses import dataclass, field
from typing import NamedTuple


@dataclass
class CustomError(Exception):
    'A custom exception class for Errors'

    status: NamedTuple
    message: str
    code: int = field(init=False)

    def __post_init__(self) -> None:
        self.code = self.status.code

    @property
    def error_info(self):
        'Returns error message in a json format'

        return {
            'code': self.status.code,
            'status': self.status.status,
            'message': self.message
        }


class InvalidCredentialsError(CustomError):
    '''
    Exception raised when invalid credentials are given for login.

    This error occurs when the user give wrong credentials for login.
    It helps handle situations where either of the username or password is wrong.
    '''


class DataNotFoundError(CustomError):
    '''
    Exception raised when data is empty or not found.

    This error indicates that the requested data is not available or is empty.
    It's useful for situations where expected data is missing or couldn't be retrieved.
    '''


class InvalidInputError(CustomError):
    '''
    Exception raised when invalid input format is received.

    This error signifies that the input provided does not meet the expected criteria or is invalid.
    It helps handle situations where incorrect or unacceptable input is detected.
    '''


class DuplicateEntryError(CustomError):
    '''
    Exception raised when a duplicate data entry is attempted.

    This error is raised when an attempt is made to insert duplicate data into a database
    or another data structure that prohibits duplicate entries.
    '''


class ValidationError(CustomError):
    '''
    Exception raised when invalid input data is received.

    This error signifies that the input provided does not meet the expected criteria or is invalid.
    It helps handle situations where incorrect or unacceptable input is detected.
    '''
