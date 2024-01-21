'''Hash the passwords using hashlib library'''

import hashlib


def hash_password(password: str) -> str:
    '''
    Hashes a password using hashlib.

    Args:
        password (str): The password to be hashed.

    Uses the hashlib library to securely hash the provided password using SHA-256 algorithm.

    Returns:
        str: The hashed password as a string.
    '''
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password
