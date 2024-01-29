'Routes for the Category related functionalities'

from typing import Annotated

from fastapi import APIRouter, Depends, Response

from config.message_prompts import Roles
from controllers.category_controller import CategoryController
from database.database_access import DatabaseAccess
from schemas.category import CategorySchema, CategoryUpdateSchema
from utils.rbac import access_level
from utils.token_handler import get_jwt

router = APIRouter(tags=['Category'])

db = DatabaseAccess()
category_controller = CategoryController(db)
user_dependency = Annotated[dict, Depends(get_jwt)]


@router.get('/categories')
@access_level(roles=[Roles.SUPER_ADMIN, Roles.ADMIN, Roles.PLAYER])
def get_all_categories(claims: user_dependency, response: Response):
    'Get all categories details'
    res = category_controller.get_all_categories()
    response.status_code = res.status.code
    return res.message_info


@router.post('/categories')
@access_level(roles=[Roles.ADMIN])
def create_category(claims: user_dependency, category_data: CategorySchema, response: Response):
    'Create a new category'
    user_id = claims.get('sub')
    res = category_controller.create_category(dict(category_data), user_id)
    response.status_code = res.status.code
    return res.message_info


@router.patch('/categories/{category_id}')
@access_level(roles=[Roles.ADMIN])
def update_category(claims: user_dependency, category_data: CategoryUpdateSchema, category_id: str, response: Response):
    'Update an existing category'
    res = category_controller.update_category(dict(category_data), category_id)
    response.status_code = res.status.code
    return res.message_info


@router.delete('/categories/{category_id}')
@access_level(roles=[Roles.ADMIN])
def delete_category(claims: user_dependency, category_id: str, response: Response):
    'Delete an existing category'
    res = category_controller.delete_category(category_id)
    response.status_code = res.status.code
    return res.message_info
