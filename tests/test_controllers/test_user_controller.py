'''Test file for user_controller.py'''

import mysql.connector
import pytest

from config.message_prompts import DisplayMessage, Headers, LogMessage
from controllers.user import UserController
from utils.custom_error import LoginError


class TestUserController:
    '''Test class containing test method to test User Controller methods'''

    username = 'test_user'
    role = 'test_role'
    email = 'test@email.com'
    data = [('test data')]
    user_controller = UserController()

    @pytest.fixture
    def mock_read_from_database(self, mocker):
        '''Test fixture to mock read_from_database method'''

        return mocker.patch('controllers.user_controller.db.read_from_database', return_value=self.data)

    @pytest.fixture
    def mock_write_to_database(self, mocker):
        '''Test fixture to mock write_to_database method'''

        return mocker.patch('controllers.user_controller.db.write_to_database')

    @pytest.fixture
    def mock_admin_class(self, mocker):
        '''Test fixture to mock Admin class'''

        return mocker.patch('controllers.user_controller.Admin')

    def test_get_player_scores_by_username(self, mock_read_from_database):
        '''Test method to test get_player_scores_by_username method'''

        expected = mock_read_from_database()
        result = self.user_controller.get_player_scores_by_username(self.username)
        assert result == expected

    def test_get_all_users_by_role(self, mock_read_from_database):
        '''Test method to test get_all_users_by_role method'''

        expected = mock_read_from_database()
        result = self.user_controller.get_all_users_by_role(self.role)
        assert result == expected

    def test_create_admin_success(self, mock_admin_class, caplog, capsys):
        '''Test method to test create admin success'''

        mock_admin = mock_admin_class()
        self.user_controller.create_admin(self.data)
        captured = capsys.readouterr()

        mock_admin.save_to_database.assert_called_once()
        assert LogMessage.CREATE_SUCCESS, Headers.ADMIN in caplog.text
        assert DisplayMessage.CREATE_ADMIN_SUCCESS_MSG in captured.out

    def test_create_admin_error(self, mock_admin_class):
        '''Test method to test create admin error'''

        mock_admin = mock_admin_class()
        mock_admin.save_to_database.side_effect = mysql.connector.IntegrityError

        with pytest.raises(LoginError):
            self.user_controller.create_admin(self.data)

    @pytest.mark.usefixtures('mock_write_to_database')
    def test_delete_user_by_email(self, caplog, capsys):
        '''Test method to test delete_user_by_email'''

        self.user_controller.delete_user_by_email(self.role, self.email)
        captured = capsys.readouterr()

        assert LogMessage.DELETE_SUCCESS, Headers.PLAYER in caplog.text
        assert DisplayMessage.DELETE_USER_SUCCESS_MSG.format(user=self.role.title(), email=self.email) in captured.out
