'''Test file for user.py'''

from datetime import datetime

import pytest

from models.users.user import User
from models.users.super_admin import SuperAdmin
from models.users.admin import Admin
from models.users.player import Player


class TestUser:
    '''Test class containing tests for User class'''

    user_default_values_data = [
        ('super admin', 1),
        ('admin', 0),
        ('player', 1)
    ]

    def test_user_instance_creation(self, user_data):
        '''Test function to test User class instance creation'''

        role = 'user'
        user = User(user_data, role)

        assert user.name == user_data['name']
        assert user.email == user_data['email']
        assert user.username == user_data['username']
        assert user.password == user_data['password']
        assert datetime.strptime(user.registration_date, '%Y-%m-%d')

    @pytest.mark.parametrize('role, expected_is_password_changed', user_default_values_data)
    def test_user_default_values(self, user_data, role, expected_is_password_changed):
        '''Test function to test role and is_password_changed'''

        user = User(user_data, role)

        assert user.user_id is not None
        assert user.role == role
        assert user.is_password_changed == expected_is_password_changed


class TestSuperAdmin:
    '''Test class containing tests for SuperAdmin class'''

    def test_super_admin_instance_creation(self, user_data):
        '''Test function to test SuperAdmin class instance creation'''

        super_admin = SuperAdmin(user_data)

        assert super_admin.name == user_data['name']
        assert super_admin.email == user_data['email']
        assert super_admin.username == user_data['username']
        assert super_admin.password == user_data['password']
        assert super_admin.user_id is not None
        assert super_admin.role == 'super admin'
        assert super_admin.is_password_changed == 1
        assert datetime.strptime(super_admin.registration_date, '%Y-%m-%d')

    def test_super_admin_save_to_database(self, user_data, mocker):
        '''Test function to test SuperAdmin class save_to_database method'''

        mock_super_admin_manager = mocker.patch('models.user.UserManager')
        super_admin = SuperAdmin(user_data)
        super_admin.save_to_database()

        mock_super_admin_manager.assert_called_once_with(super_admin)
        mock_super_admin_manager().save_to_database.assert_called_once()


class TestAdmin:
    '''Test class containing tests for Admin class'''

    def test_admin_instance_creation(self, user_data):
        '''Test function to test Admin class instance creation'''

        admin = Admin(user_data)

        assert admin.name == user_data['name']
        assert admin.email == user_data['email']
        assert admin.username == user_data['username']
        assert admin.password == user_data['password']
        assert admin.user_id is not None
        assert admin.role == 'admin'
        assert admin.is_password_changed == 0
        assert datetime.strptime(admin.registration_date, '%Y-%m-%d')

    def test_admin_save_to_database(self, user_data, mocker):
        '''Test function to test Admin class save_to_database method'''

        mock_admin_manager = mocker.patch('models.user.UserManager')
        admin = Admin(user_data)
        admin.save_to_database()

        mock_admin_manager.assert_called_once_with(admin)
        mock_admin_manager().save_to_database.assert_called_once()


class TestPlayer:
    '''Test class containing tests for Player class'''

    def test_player_instance_creation(self, user_data):
        '''Test function to test Player class instance creation'''

        player = Player(user_data)

        assert player.name == user_data['name']
        assert player.email == user_data['email']
        assert player.username == user_data['username']
        assert player.password == user_data['password']
        assert player.user_id is not None
        assert player.role == 'player'
        assert player.is_password_changed == 1
        assert datetime.strptime(player.registration_date, '%Y-%m-%d')

    def test_player_save_to_database(self, user_data, mocker):
        '''Test function to test Player class save_to_database method'''

        mock_player_manager = mocker.patch('models.user.UserManager')
        player = Player(user_data)
        player.save_to_database()

        mock_player_manager.assert_called_once_with(player)
        mock_player_manager().save_to_database.assert_called_once()
