'Generate random password'

import random
import string


def generate_password():
    'Generate a random password using string combinations'

    characters = string.ascii_letters + string.digits + '@#$&'
    password = ''.join(random.choice(characters) for _ in range(6))
    return password
