'Routes for the Authentication related functionalities'

from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from controllers.auth_controller import AuthController
from database.database_access import DatabaseAccess
from schemas.auth import LoginSchema, RegistrationSchema
from utils.token_handler import get_jwt

router = APIRouter(tags=['Auth'])

db = DatabaseAccess()
auth_controller = AuthController(db)
user_dependency = Annotated[dict, Depends(get_jwt)]


@router.post('/register')
def register(player_data: RegistrationSchema, response: Response):
    'Register a new user'
    res = auth_controller.register(dict(player_data))
    response.status_code = res.status.code
    return res.message_info


@router.post('/login')
def login(login_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    'Login an existing user'
    res = auth_controller.login(login_data)
    response.status_code = res.status.code
    return res.message_info


@router.post('/logout')
def logout(claims: user_dependency, response: Response):
    'Logout a logged in user'
    jti = claims.get('jti')
    res = auth_controller.logout(jti)
    response.status_code = res.status.code
    return res.message_info


@router.post('/refresh')
def refresh(claims: user_dependency, response: Response):
    'Issue a non fresh access token'
    user_id = claims.get('sub')
    mapped_role = claims.get('cap')
    res = auth_controller.refresh(user_id, mapped_role)
    response.status_code = res.status.code
    return res.message_info
