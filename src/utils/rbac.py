'Role Based Access'

import functools
import logging
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from config.string_constants import ErrorMessage, Roles, StatusCodes
from utils.custom_error import CustomError

logger = logging.getLogger(__name__)
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

ROLE_MAPPING = {
    Roles.SUPER_ADMIN: os.getenv('SUPER_ADMIN_MAPPING'),
    Roles.ADMIN: os.getenv('ADMIN_MAPPING'),
    Roles.PLAYER: os.getenv('PLAYER_MAPPING')
}


def access_level(roles: List):
    'A parameterised decorator to specify access levels'

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            mapped_roles = [ROLE_MAPPING.get(role) for role in roles]

            if claims["cap"] in mapped_roles:
                return func(*args, **kwargs)
            error = CustomError(status=StatusCodes.FORBIDDEN, message=ErrorMessage.FORBIDDEN)
            logger.error(error.message)
            return error.error_info, error.code

        return wrapper

    return decorator
