'''Test file for database_access.py'''

import mysql.connector

import pytest

from models.database.database_access import DatabaseAccess


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
        mocker.patch('mysql.connector.connect', return_value=mock_connection)
        db_access = DatabaseAccess()

        return db_access

    def test_read_success(self, mock_db_access):
        '''Test method to test read success'''

        db_access = mock_db_access
        db_access.cursor.fetchall.return_value = self.mock_fetchall_result

        result = db_access.read(self.query, self.data)

        db_access.cursor.execute.assert_called_once_with(self.query, self.data)
        db_access.cursor.fetchall.assert_called_once()
        assert result == self.mock_fetchall_result

    def test_read_error(self, mock_db_access, caplog):
        '''Test method to test read error'''

        db_access = mock_db_access
        db_access.cursor.execute.side_effect = mysql.connector.OperationalError('Mock Error')
        result = db_access.read(self.query)

        db_access.cursor.fetchall.assert_not_called()
        assert 'Mock Error' in caplog.text
        assert not result

    def test_write_success(self, mock_db_access):
        '''Test method to test write success'''

        db_access = mock_db_access
        db_access.write(self.query, self.data)

        assert db_access.cursor.execute.call_count == 2

    def test_write_success_no_data(self, mock_db_access):
        '''Test method to test write success with no data'''

        db_access = mock_db_access
        db_access.write(self.query)

        assert db_access.cursor.execute.call_count == 2

    def test_write_error(self, mock_db_access, caplog):
        '''Test method to test write error'''

        db_access = mock_db_access
        db_access.cursor.execute.side_effect = mysql.connector.OperationalError('Mock Error')
        db_access.write(self.query)

        assert 'Mock Error' in caplog.text

    def test_init_exception_handling(self, mocker):
        '''Test method to test __init__ exception handling'''

        mock_connect = mocker.patch('mysql.connector.connect')
        mock_connect.side_effect = mysql.connector.Error('Mocked error')
        with pytest.raises(mysql.connector.Error):
            DatabaseAccess()
