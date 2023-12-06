'''Contains DatabaseSaver Interface'''

from abc import ABC, abstractmethod


class DatabaseSaver(ABC):
    '''
    Contains DatabaseSaver Interface.

    This interface defines the structure for saving data to a database.

    Methods:
        save_to_database(): Abstract method that must be implemented by subclasses.
    '''

    @abstractmethod
    def save_to_database(self) -> None:
        '''
        Abstract method to save data to the database.

        This method must be implemented by subclasses to provide functionality for saving data to a database.
        '''
