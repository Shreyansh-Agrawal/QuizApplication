'To generate access and refresh tokens'

import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, Dict

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt

from config.message_prompts import ErrorMessage, StatusCodes
from utils.blocklist import BLOCKLIST
from utils.custom_error import CustomError

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = 'HS256'
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/v1/login')


def create_access_token(identity: str, fresh: bool, additional_claims: Dict):
    'Create an access token'

    iat = datetime.utcnow()
    exp = iat + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = secrets.token_hex(16)
    payload = {
        'fresh': fresh,
        'iat': iat,
        'jti': jti,
        'type': 'access',
        'sub': identity,
        'exp': exp
    }
    payload.update(additional_claims)
    access_token = jwt.encode(payload, JWT_SECRET_KEY, ALGORITHM)
    return access_token


def create_refresh_token(identity: str, additional_claims: Dict):
    'Create a refresh token'

    iat = datetime.utcnow()
    exp = iat + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = secrets.token_hex(16)
    payload = {
        'fresh': False,
        'iat': iat,
        'jti': jti,
        'type': 'refresh',
        'sub': identity,
        'exp': exp
    }
    payload.update(additional_claims)
    refresh_token = jwt.encode(payload, JWT_SECRET_KEY)
    return refresh_token


def get_jwt(token: Annotated[str, Depends(oauth2_bearer)]) -> Dict:
    'Returns claims of a jwt token'
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY)
        check_token_in_blocklist(payload)
        return payload
    except ExpiredSignatureError as e:
        error = CustomError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_EXPIRED)
        raise HTTPException(status_code=error.code, detail=error.error_info) from e
    except JWTError as e:
        error = CustomError(StatusCodes.UNAUTHORIZED, message=str(e))
        raise HTTPException(status_code=error.code, detail=error.error_info) from e


def check_token_in_blocklist(payload: Dict):
    'Checks if token is in blocklist, if present aborts the request'
    jti = payload.get('jti')
    if jti in BLOCKLIST:
        error = CustomError(StatusCodes.UNAUTHORIZED, message=ErrorMessage.TOKEN_REVOKED)
        raise HTTPException(status_code=error.code, detail=error.error_info)
