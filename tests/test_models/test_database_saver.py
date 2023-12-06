'''Test file for database_saver.py'''

import pytest

from models.database_saver import DatabaseSaver


class ConcreteDatabaseSaver(DatabaseSaver):
    '''Concrete class that inherits from the abstract class and implements the abstract method.'''

    def save_to_database(self) -> None:
        pass


class TestDatabaseSaver:
    '''Test class to test DatabaseSaver class'''

    def test_instantiation_raises_error(self):
        '''Test function to ensure that attempting to instantiate abstract class raises a TypeError.'''

        with pytest.raises(TypeError):
            DatabaseSaver() # pylint: disable=abstract-class-instantiated

    def test_save_to_database_implementation(self):
        '''Test function to test save_to_database implementation'''

        concrete_obj = ConcreteDatabaseSaver()
        concrete_obj.save_to_database()
