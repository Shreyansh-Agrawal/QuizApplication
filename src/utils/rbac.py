'Role Based Access'

from functools import wraps
from typing import List

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from config.message_prompts import Roles

ROLE_MAPPING = {
    Roles.SUPER_ADMIN: 'SFAB6c',
    Roles.ADMIN: 'SHVpHQ',
    Roles.PLAYER: 'SSwYVW'
}

def access_level(roles: List):
    'A parameterised decorator to specify access levels'
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            mapped_roles = [ROLE_MAPPING.get(role) for role in roles]

            if claims["cap"] in mapped_roles:
                return func(*args, **kwargs)
            else:
                return jsonify(message="Forbidden"), 403
        return wrapper

    return decorator
