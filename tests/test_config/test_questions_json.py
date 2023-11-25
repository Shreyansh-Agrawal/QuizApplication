'''Test file for questions.json'''

import json


def test_json_file():
    '''Test function to test questions.json'''

    with open('src\\config\\questions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check the presence of the 'questions' key
    assert 'questions' in data

    # Validate the structure and content of individual questions
    questions = data['questions']

    # Ensure there are questions present
    assert len(questions) > 0

    for question in questions:
        # Ensure each question has the required fields
        assert 'question_id' in question
        assert 'question_text' in question
        assert 'question_type' in question
        assert 'category_id' in question
        assert 'category' in question
        assert 'admin_id' in question
        assert 'admin_username' in question
        assert 'options' in question

        # Ensure options are present and have the necessary structure
        assert 'answer' in question['options']
        assert 'option_id' in question['options']['answer']
        assert 'text' in question['options']['answer']

        # For multiple choice questions, ensure 'other_options' are present
        if question['question_type'] == 'mcq':
            assert 'other_options' in question['options']
            assert len(question['options']['other_options']) > 0
