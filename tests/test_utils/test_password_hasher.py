'''Test file for password_hasher.py'''

import hashlib
from utils.password_hasher import hash_password


def test_hash_password():
    '''Test function to test hash_password function with known string'''

    password = 'TestPassword123'
    expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    assert hash_password(password) == expected_hash


def test_hash_password_with_empty_string():
    '''Test function to test hash_password function with empty string'''

    password = ''
    expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    assert hash_password(password) == expected_hash
