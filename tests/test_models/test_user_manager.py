'''Test file for user_manager.py'''

from models.users.user_manager import UserManager


class TestUserManager:
    '''Test class containing tests for UserManager class'''

    def test_save_to_database(self, mock_user, mocker):
        '''Test function to test save_to_database implementation in UserManager Class'''

        mock_write = mocker.Mock()
        mocker.patch('models.user_manager.db.write', mock_write)
        user_manager_obj = UserManager(mock_user)
        user_manager_obj.save_to_database()

        assert user_manager_obj.user == mock_user
        assert mock_write.call_count == 2
