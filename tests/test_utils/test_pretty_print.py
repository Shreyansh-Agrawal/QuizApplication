'''Test file for pretty_print.py'''

from src.utils.pretty_print import pretty_print

pretty_print_headers_data = ('Name', 'Age', 'Role')

pretty_print_valid_data = [
    ('John', 25, 'SuperAdmin'),
    ('Mathew', 20, 'Admin'),
    ('Peter', 18, 'Player'),
]


def test_pretty_print_valid_data(capsys):
    '''Test function to test pretty print for valid data'''

    pretty_print(data=pretty_print_valid_data, headers=pretty_print_headers_data)
    captured = capsys.readouterr()

    assert 'SNo.' in captured.out
    assert 'John' in captured.out
    assert '18' in captured.out
