'Role Based Access'

import functools
import logging
import os
from typing import List

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from config.string_constants import ErrorMessage, Roles, StatusCodes
from utils.custom_error import CustomError

logger = logging.getLogger(__name__)

ROLE_MAPPING = {
    Roles.SUPER_ADMIN: os.getenv('SUPER_ADMIN_MAPPING'),
    Roles.ADMIN: os.getenv('ADMIN_MAPPING'),
    Roles.PLAYER: os.getenv('PLAYER_MAPPING')
}


def access_level(roles: List, check_fresh=False):
    'A parameterised decorator to specify access levels'

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request(fresh=check_fresh)
            claims = get_jwt()
            mapped_roles = [ROLE_MAPPING.get(role) for role in roles]

            if claims["cap"] in mapped_roles:
                return func(*args, **kwargs)

            error = CustomError(status=StatusCodes.FORBIDDEN, message=ErrorMessage.FORBIDDEN)
            logger.error(error.message)
            return error.error_info, error.code

        return wrapper

    return decorator
