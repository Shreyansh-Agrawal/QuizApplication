'''Test file for file_paths.py'''


def test_file_paths(file_paths_attributes):
    '''Test FilePaths to check if the '''

    required_file_paths = [
        'DATABASE_PATH',
        'QUESTIONS_JSON_PATH'
    ]

    for file_path in required_file_paths:
        assert file_path in file_paths_attributes
