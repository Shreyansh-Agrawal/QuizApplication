'''Test file for app.py'''

from config.string_constants import DisplayMessage, LogMessage
from app import start_quiz_app


def test_application_entry_point_logging(mocker, capsys, caplog):
    '''Test function to test app.py'''

    mocker.patch('app.Initializer.initialize_app')
    mocker.patch('app.MainMenu.auth_menu')

    start_quiz_app()
    captured = capsys.readouterr()

    assert LogMessage.SYSTEM_START in caplog.text
    assert LogMessage.SYSTEM_STOP in caplog.text
    assert DisplayMessage.EXIT_MSG in captured.out

def test_application_entry_point_error(mocker, capsys, caplog):
    '''Test function to test app.py for error'''

    mocker.patch('app.Initializer.initialize_app')
    mocker.patch('app.MainMenu.auth_menu', side_effect=Exception('test_exception'))

    start_quiz_app()
    captured = capsys.readouterr()
    print(captured.out)
    assert 'test_exception' in caplog.text
    assert 'test_exception' in captured.out
