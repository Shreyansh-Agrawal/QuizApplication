'''Test file for pretty_print.py'''

from src.config.message_prompts import DisplayMessage
from src.utils.pretty_print import pretty_print

pretty_print_headers_data = ('Name', 'Age', 'Role')

pretty_print_valid_data = [
    ('John', 25, 'SuperAdmin'),
    ('Mathew', 20, 'Admin'),
    ('Peter', 18, 'Player'),
]

pretty_print_invalid_data = ['1', (1, )]


def test_pretty_print_valid_data(mocker, capsys):
    '''Test function to test pretty print for valid data'''

    mocker.patch('src.utils.pretty_print.tabulate', return_value = 'tabulate table')

    pretty_print(data=pretty_print_valid_data, headers=pretty_print_headers_data)
    captured = capsys.readouterr()

    assert 'tabulate table' in captured.out


def test_pretty_print_invalid_data(mocker, capsys):
    '''Test function to test pretty print for valid data'''

    mock_tabulate = mocker.patch('src.utils.pretty_print.tabulate')
    mock_tabulate.side_effect = ValueError('test errror')

    pretty_print(data=pretty_print_invalid_data, headers=pretty_print_headers_data)
    captured = capsys.readouterr()

    assert DisplayMessage.TABULATE_ERROR_MSG in captured.out
