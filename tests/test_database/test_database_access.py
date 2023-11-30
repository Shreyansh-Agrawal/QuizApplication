'''Test file for database_access.py'''

import sqlite3

from src.database.database_access import DatabaseAccess


class TestDatabaseAccess:
    '''Test class containing test methods to test DatabaseAccess class methods'''

    query = "SELECT * FROM your_table"
    data = ('example', 'data')
    mock_fetchall_result = [('result1',), ('result2',)]

    def test_read_from_database_success(self, mock_db_connection):
        '''Test method to test read_from_database success'''

        mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = self.mock_fetchall_result

        result = DatabaseAccess.read_from_database(self.query, self.data)

        mock_cursor.execute.assert_called_once_with(self.query, self.data)
        mock_cursor.fetchall.assert_called_once()
        assert result == self.mock_fetchall_result

    def test_read_from_database_error(self, mock_db_connection, caplog):
        '''Test method to test read_from_database error'''

        mock_cursor = mock_db_connection
        mock_cursor.execute.side_effect = sqlite3.OperationalError('Mock Error')
        result = DatabaseAccess.read_from_database(self.query)

        mock_cursor.fetchall.assert_not_called()
        assert 'Mock Error' in caplog.text
        assert not result

    def test_write_to_database_success(self, mock_db_connection):
        '''Test method to test write_to_database success'''

        mock_cursor = mock_db_connection
        DatabaseAccess.write_to_database(self.query, self.data)

        assert mock_cursor.execute.call_count == 2

    def test_write_to_database_success_no_data(self, mock_db_connection):
        '''Test method to test write_to_database success with no data'''

        mock_cursor = mock_db_connection
        DatabaseAccess.write_to_database(self.query)

        assert mock_cursor.execute.call_count == 2

    def test_write_to_database_error(self, mock_db_connection, caplog):
        '''Test method to test write_to_database error'''

        mock_cursor = mock_db_connection
        mock_cursor.execute.side_effect = sqlite3.OperationalError('Mock Error')
        DatabaseAccess.write_to_database(self.query)

        assert 'Mock Error' in caplog.text
