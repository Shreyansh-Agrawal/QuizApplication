'''Test file for super_admin_menu.py'''

from config.message_prompts import DisplayMessage, Headers, LogMessage
from menu.super_admin_menu import SuperAdminMenu

class TestSuperAdminMenu:
    '''Test class containing test method to test super admin menu'''

    def test_super_admin_menu(self, mocker, caplog, capsys):
        '''Test function to test super_admin_menu function'''

        username = 'test_super_admin'

        mocker.patch('builtins.input', side_effect=['1', '2', '3', '4', 'q'])
        mock_user_handler = mocker.patch('menu.super_admin_menu.UserHandler')

        SuperAdminMenu.super_admin_menu(username)
        captured = capsys.readouterr()

        assert LogMessage.RUNNING_USER_MENU, Headers.SUPER_ADMIN in caplog.text
        assert DisplayMessage.DASHBOARD_MSG.format(user=Headers.SUPER_ADMIN) in captured.out
        assert DisplayMessage.USER_WELCOME_MSG.format(user=username) in captured.out
        mock_user_handler().handle_create_admin.assert_called_once()
        mock_user_handler().display_users_by_role.assert_called_once_with(role='admin')
        mock_user_handler().handle_delete_user_by_email.assert_called_once_with(role='admin')
