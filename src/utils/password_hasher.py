'''Hash the passwords using hashlib library'''

import hashlib


def hash_password(password: str):
    '''Function to hash password using hashlib'''

    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password
