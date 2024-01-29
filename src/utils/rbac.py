'Role Based Access'

import functools
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import HTTPException

from config.message_prompts import ErrorMessage, Roles, StatusCodes
from utils.custom_error import CustomError

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
            claims = kwargs.get('claims')
            mapped_roles = [ROLE_MAPPING.get(role) for role in roles]
            if claims.get('cap') in mapped_roles:
                return func(*args, **kwargs)
            error = CustomError(StatusCodes.FORBIDDEN, message=ErrorMessage.FORBIDDEN)
            raise HTTPException(status_code=error.code, detail=error.error_info)

        return wrapper

    return decorator
