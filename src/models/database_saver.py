'''Contains DatabaseSaver Interface'''

from abc import ABC, abstractmethod


class DatabaseSaver(ABC):
    '''Interface for saving to the database'''

    @abstractmethod
    def save_to_database(self) -> None:
        '''Abstract method to save to the database'''
        pass
