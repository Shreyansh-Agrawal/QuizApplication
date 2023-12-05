'''Custom Error Classes'''


class LoginError(Exception):
    '''
    Exception raised when login attempts are exhausted.

    This error occurs when the user exceeds the maximum number of login attempts allowed.
    It helps handle situations where login attempts are repeatedly unsuccessful.

    Args:
    - message (str): A descriptive message explaining the reason for the error.
    '''

    def __init__(self, message: str):
        super().__init__(f'{message}')


class DataNotFoundError(Exception):
    '''
    Exception raised when data is empty or not found.

    This error indicates that the requested data is not available or is empty.
    It's useful for situations where expected data is missing or couldn't be retrieved.

    Args:
    - message (str): A descriptive message explaining the absence or emptiness of the data.
    '''

    def __init__(self, message: str):
        super().__init__(f'{message}')


class InvalidInputError(Exception):
    '''
    Exception raised when invalid input is received.

    This error signifies that the input provided does not meet the expected criteria or is invalid.
    It helps handle situations where incorrect or unacceptable input is detected.

    Args:
    - message (str): A descriptive message explaining the reason for the invalid input.
    '''

    def __init__(self, message: str):
        super().__init__(f'{message}')


class DuplicateEntryError(Exception):
    '''
    Exception raised when a duplicate data entry is attempted.

    This error is raised when an attempt is made to insert duplicate data into a database
    or another data structure that prohibits duplicate entries.

    Args:
    - message (str): A descriptive message explaining the attempt to insert duplicate data.
    '''

    def __init__(self, message: str):
        super().__init__(f'{message}')
