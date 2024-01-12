'''Test file for quiz_helper.py'''

import pytest

from config.message_prompts import DisplayMessage, Headers, LogMessage
from helpers.create_quiz_helper import CreateQuizHelper
from utils.custom_error import DataNotFoundError


class TestCreateQuizHelper:
    '''Test class containing test methods to test CreateQuizHelper methods'''

    username = 'test_username'
    role = 'player'
    header = ('header', )
    mock_data = [('test_data')]
    category_name = 'test_category_name'
    ques_type_data = [
        ('1', {'question_type': 'MCQ'}),
        ('2', {'question_type': 'T/F'}),
        ('3', {'question_type': 'ONE WORD'})
    ]
    create_option_data = [
        ('MCQ', ['Answer', 'Option 1', 'Option 2', 'Option 3'], 4),
        ('T/F', ['Answer'], 1),
        ('ONE WORD', ['Answer'], 1),
        ('Invalid', [], 0)
    ]
    create_quiz_helper = CreateQuizHelper()

    @pytest.fixture(autouse=True)
    def mock_read_from_database(self, mocker):
        '''Test fixture to mock read_from_database method'''

        mocker.patch('controllers.helpers.create_quiz_helper.db.read_from_database', return_value=self.mock_data)

    def test_get_all_categories(self):
        '''Test method to test get_all_categories'''

        result = self.create_quiz_helper.get_all_categories()
        assert result == self.mock_data

    def test_get_question_data(self, mocker, capsys, caplog):
        '''Test method to test get_question_data'''

        mocker.patch('controllers.helpers.create_quiz_helper.validations.regex_validator', side_effect=['1', 'test_question_text'])
        mocker.patch.object(CreateQuizHelper, 'get_all_categories', return_value=self.mock_data)

        result = self.create_quiz_helper.get_question_data(self.username)
        captured = capsys.readouterr()

        assert LogMessage.CREATE_ENTITY, Headers.QUES in caplog.text
        assert DisplayMessage.CREATE_QUES_MSG in captured.out
        assert result['question_text'] == 'test_question_text'.title()

    def test_get_question_data_invalid_category(self, mocker):
        '''Test method to test get_question_data when invalid category selected'''

        mocker.patch('controllers.helpers.create_quiz_helper.validations.regex_validator', side_effect=['-1', 'test_question_text'])
        mocker.patch.object(CreateQuizHelper, 'get_all_categories', return_value=self.mock_data)

        with pytest.raises(DataNotFoundError) as error_msg:
            self.create_quiz_helper.get_question_data(self.username)

        assert 'No such Category! Please choose from above!!' in str(error_msg.value)

    @pytest.mark.parametrize('user_input, expected_output', ques_type_data)
    def test_get_question_type(self, mocker, user_input, expected_output):
        '''Test method to test get_question_type'''

        mocker.patch('builtins.input', return_value=user_input)
        result = self.create_quiz_helper.get_question_type({})

        assert result == expected_output

    def test_get_question_type_invalid_type(self, mocker, capsys):
        '''Test method to test get_question_type when invalid type selected'''

        mocker.patch('builtins.input', side_effect=['invalid type', '1'])
        result = self.create_quiz_helper.get_question_type({})
        captured = capsys.readouterr()
        
        assert DisplayMessage.INVALID_QUES_TYPE_MSG in captured.out
        assert result == self.ques_type_data[0][1]

    @pytest.mark.parametrize('question_type, user_inputs, expected_options_length', create_option_data)
    def test_create_option(self, mocker, question_type, user_inputs, expected_options_length):
        '''Test method to test create_option'''

        question_data = {'question_type': question_type}
        mock_question = mocker.MagicMock()
        mocker.patch.object(CreateQuizHelper, 'get_question_type', return_value=question_data)
        mocker.patch('controllers.helpers.create_quiz_helper.Question', return_value=mock_question)
        mocker.patch('controllers.helpers.create_quiz_helper.validations.regex_validator', side_effect=user_inputs)
        mock_add_option = mocker.patch.object(mock_question, 'add_option')
        mocker.patch('controllers.helpers.create_quiz_helper.Option')

        result = self.create_quiz_helper.create_option(question_data)
        if question_type == 'Invalid':
            assert result is None
            assert not mock_add_option.called
        else:
            assert mock_add_option.call_count == expected_options_length
