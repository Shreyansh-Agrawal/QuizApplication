'''Custom Error Classes'''


class LoginError(Exception):
    '''Exception raised when Login attempts exhausted'''

    def __init__(self, message: str):
        super().__init__(f'{message}')


class DataNotFoundError(Exception):
    '''Exception raised when Data is Empty'''

    def __init__(self, message: str):
        super().__init__(f'{message}')


class InvalidInputError(Exception):
    '''Exception raised when received invalid input'''

    def __init__(self, message: str):
        super().__init__(f'{message}')


class DuplicateEntryError(Exception):
    '''Exception raised when a duplicate data is entered into db'''

    def __init__(self, message: str):
        super().__init__(f'{message}')
