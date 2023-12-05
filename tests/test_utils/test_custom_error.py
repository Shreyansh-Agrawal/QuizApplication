'''Test file for custom_error.py'''

from utils.custom_error import (
    DataNotFoundError,
    DuplicateEntryError,
    InvalidInputError,
    LoginError
)


def test_login_error():
    '''Test function to test LoginError'''

    message = 'Login attempts exhausted'
    error = LoginError(message)
    assert str(error) == message


def test_data_not_found_error():
    '''Test function to test DataNotFoundError'''

    message = 'Data is Empty'
    error = DataNotFoundError(message)
    assert str(error) == message


def test_invalid_input_error():
    '''Test function to test InvalidInputError'''

    message = 'Received invalid input'
    error = InvalidInputError(message)
    assert str(error) == message


def test_duplicate_entry_error():
    '''Test function to test DuplicateEntryError'''

    message = 'Duplicate data entered into db'
    error = DuplicateEntryError(message)
    assert str(error) == message
