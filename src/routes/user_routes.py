'Routes for the User related functionalities'

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from config.message_prompts import Roles
from controllers.user_controller import UserController
from database.database_access import DatabaseAccess
from schemas.user import AdminSchema, UserUpdateSchema
from utils.rbac import access_level
from utils.token_handler import get_jwt

router = APIRouter(tags=['User'])

db = DatabaseAccess()
user_controller = UserController(db)
user_dependency = Annotated[dict, Depends(get_jwt)]


@router.get('/profile/me')
@access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
def get_user_profile_data(claims: user_dependency, response: Response):
    'Get user profile data'
    user_id = claims.get('sub')
    res = user_controller.get_user_profile_data(user_id)
    response.status_code = res.status.code
    return res.message_info


@router.patch('/profile/me')
@access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
def update_user_data(claims: user_dependency, user_data: UserUpdateSchema, response: Response):
    'Update user profile'
    user_id = claims.get('sub')
    res = user_controller.update_user_data(user_id, dict(user_data))
    response.status_code = res.status.code
    return res.message_info


@router.get('/players')
@access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN])
def get_all_players(claims: user_dependency, response: Response):
    'Get all player details'
    res = user_controller.get_all_players()
    response.status_code = res.status.code
    return res.message_info


@router.get('/admins')
@access_level(roles=[Roles.SUPER_ADMIN])
def get_all_admins(claims: user_dependency, response: Response):
    'Get all admin details'
    res = user_controller.get_all_admins()
    response.status_code = res.status.code
    return res.message_info


@router.post('/admins')
@access_level(roles=[Roles.SUPER_ADMIN])
def create_admin(claims: user_dependency, admin_data: AdminSchema, response: Response):
    'Create a new admin account'
    res = user_controller.create_admin(dict(admin_data))
    response.status_code = res.status.code
    return res.message_info


@router.delete('/admins/{admin_id}')
@access_level(roles=[Roles.SUPER_ADMIN])
def delete_admin_by_id(claims: user_dependency, admin_id: str, response: Response):
    'Delete an existing admin'
    res = user_controller.delete_admin_by_id(admin_id)
    response.status_code = res.status.code
    return res.message_info


@router.delete('/players/{player_id}')
@access_level(roles=[Roles.ADMIN])
def delete_player_by_id(claims: user_dependency, player_id: str, response: Response):
    'Delete an existing player'
    res = user_controller.delete_player_by_id(player_id)
    response.status_code = res.status.code
    return res.message_info
