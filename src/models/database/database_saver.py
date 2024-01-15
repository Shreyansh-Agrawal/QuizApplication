'''Contains DatabaseSaver Interface'''

from abc import ABC, abstractmethod


class DatabaseSaver(ABC):
    '''
    Contains DatabaseSaver Interface.

    This interface defines the structure for saving data to a database.

    Methods:
        save(): Abstract method that must be implemented by subclasses.
    '''

    @classmethod
    @abstractmethod
    def save(cls, entity) -> None:
        '''
        Abstract method to save entity to the database.

        This method must be implemented by subclasses to provide functionality for saving data to a database.
        '''
