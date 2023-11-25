'''Test file for test_json_to_db_loader.py'''

import json

from config.message_prompts import LogMessage
from src.utils import json_to_db_loader


def test_load_quiz_data_from_json_success(mocker, sample_json_data, caplog):
    '''Test function to test load_quiz_data_from_json function'''

    mock_read_from_database = mocker.Mock()
    mock_write_to_database = mocker.Mock()

    mocker.patch('src.utils.json_to_db_loader.DAO.read_from_database', mock_read_from_database)
    mocker.patch('src.utils.json_to_db_loader.DAO.write_to_database', mock_write_to_database)
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(sample_json_data)))

    mock_read_from_database.return_value = [('AEcrFq',)]
    json_to_db_loader.load_quiz_data_from_json('test_admin')

    assert LogMessage.LOAD_QUIZ_DATA_FROM_JSON in caplog.text
    assert mock_read_from_database.call_count == 1
    assert mock_write_to_database.call_count == 9
