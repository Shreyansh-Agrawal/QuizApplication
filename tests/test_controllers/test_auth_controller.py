'''Test file for auth_controller.py'''

import mysql.connector

import pytest

from config.message_prompts import DisplayMessage, LogMessage
from controllers.auth import Authentication
from utils.custom_error import LoginError


class TestAuthController:
    '''Test class containing test methods to test login and signup methods'''

    player_data = {
        'name': 'test name', 
        'email': 'test@email.com', 
        'username': 'test user', 
        'password': 'test_password'
    }
    username = 'test_username'
    password = 'test_password'
    user_data = [('hashed_password', 'role', '1')]
    auth_controller = Authentication()

    def test_login_success(self, mocker, capsys, caplog):
        '''Test method to test login success'''

        mocker.patch('controllers.auth_controller.hash_password', return_value = 'hashed_password')
        mocker.patch('controllers.auth_controller.db.read_from_database', return_value = self.user_data)

        result = self.auth_controller.login(self.username, self.password)
        _ , role, is_password_changed = self.user_data[0]
        expected_result = (self.username, role, is_password_changed)
        captured = capsys.readouterr()

        assert LogMessage.LOGIN_INITIATED in caplog.text
        assert DisplayMessage.LOGIN_SUCCESS_MSG in captured.out
        assert result == expected_result

    def test_login_failure(self, mocker, capsys):
        '''Test method to test login failure'''

        mocker.patch('controllers.auth_controller.hash_password', return_value = 'hashed_password')
        mocker.patch('controllers.auth_controller.db.read_from_database', return_value = None)

        result = self.auth_controller.login(self.username, self.password)
        captured = capsys.readouterr()

        assert DisplayMessage.AUTH_INVALIDATE_MSG in captured.out
        assert not result

    def test_login_wrong_password(self, mocker, capsys):
        '''Test method to test login for wrong password'''

        user_data = [('another_hashed_password', 'role', '1')]
        mocker.patch('controllers.auth_controller.hash_password', return_value = 'hashed_password')
        mocker.patch('controllers.auth_controller.db.read_from_database', return_value = user_data)

        result = self.auth_controller.login(self.username, self.password)
        captured = capsys.readouterr()

        assert DisplayMessage.AUTH_INVALIDATE_MSG in captured.out
        assert not result

    def test_signup_success(self, mocker, capsys, caplog):
        '''Test method to test signup success'''

        mocker.patch('controllers.auth_controller.hash_password', return_value = 'hashed_password')
        mock_player = mocker.patch('controllers.auth_controller.Player')

        result = self.auth_controller.signup(self.player_data)
        captured = capsys.readouterr()

        assert LogMessage.SIGNUP_INITIATED in caplog.text
        assert LogMessage.SIGNUP_SUCCESS in caplog.text
        assert DisplayMessage.SIGNUP_SUCCESS_MSG in captured.out
        assert result == self.player_data['username']
        mock_player().save_to_database.assert_called_once()

    def test_signup_user_exists(self, mocker):
        '''Test method to test signup for error'''

        mocker.patch('controllers.auth_controller.hash_password', return_value = 'hashed_password')
        mock_player = mocker.patch('controllers.auth_controller.Player')
        mock_player().save_to_database.side_effect = mysql.connector.IntegrityError

        with pytest.raises(LoginError):
            self.auth_controller.signup(self.player_data)
