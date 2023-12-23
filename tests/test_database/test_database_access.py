'''Test file for database_access.py'''

import sqlite3

import pytest

from database.database_access import DatabaseAccess


class TestDatabaseAccess:
    '''Test class containing test methods to test DatabaseAccess class methods'''

    query = 'SELECT * FROM test_table'
    data = ('example', 'data')
    mock_fetchall_result = [('result1',), ('result2',)]

    @pytest.fixture
    def mock_db_access(self, mocker):
        '''Test Fixture to mock db connection'''

        mock_cursor = mocker.Mock()
        mock_connection = mocker.Mock()
        mock_connection.cursor.return_value = mock_cursor
        mocker.patch('database.database_access.FilePaths')
        mocker.patch('sqlite3.connect', return_value=mock_connection)
        db_access = DatabaseAccess()

        return db_access

    def test_read_from_database_success(self, mock_db_access):
        '''Test method to test read_from_database success'''

        db_access = mock_db_access
        db_access.cursor.fetchall.return_value = self.mock_fetchall_result

        result = db_access.read_from_database(self.query, self.data)

        db_access.cursor.execute.assert_called_once_with(self.query, self.data)
        db_access.cursor.fetchall.assert_called_once()
        assert result == self.mock_fetchall_result

    def test_read_from_database_error(self, mock_db_access, caplog):
        '''Test method to test read_from_database error'''

        db_access = mock_db_access
        db_access.cursor.execute.side_effect = sqlite3.OperationalError('Mock Error')
        result = db_access.read_from_database(self.query)

        db_access.cursor.fetchall.assert_not_called()
        assert 'Mock Error' in caplog.text
        assert not result

    def test_write_to_database_success(self, mock_db_access):
        '''Test method to test write_to_database success'''

        db_access = mock_db_access
        db_access.write_to_database(self.query, self.data)

        assert db_access.cursor.execute.call_count == 2

    def test_write_to_database_success_no_data(self, mock_db_access):
        '''Test method to test write_to_database success with no data'''

        db_access = mock_db_access
        db_access.write_to_database(self.query)

        assert db_access.cursor.execute.call_count == 2

    def test_write_to_database_error(self, mock_db_access, caplog):
        '''Test method to test write_to_database error'''

        db_access = mock_db_access
        db_access.cursor.execute.side_effect = sqlite3.OperationalError('Mock Error')
        db_access.write_to_database(self.query)

        assert 'Mock Error' in caplog.text

    def test_init_exception_handling(self, mocker):
        '''Test method to test __init__ exception handling'''

        mock_connect = mocker.patch('sqlite3.connect')
        mock_connect.side_effect = sqlite3.Error('Mocked error')
        with pytest.raises(sqlite3.Error):
            DatabaseAccess()
