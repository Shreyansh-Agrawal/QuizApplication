'''Test file for app.py'''

from config.message_prompts import LogMessage
from src.app import start_quiz_app


def test_application_entry_point_logging(mocker, caplog):
    '''Test function to test app.py'''

    mocker.patch('src.app.Initializer.initialize_app')
    mocker.patch('src.app.auth_menu')
    start_quiz_app()
    assert LogMessage.SYSTEM_START in caplog.text
    assert LogMessage.SYSTEM_STOP in caplog.text
