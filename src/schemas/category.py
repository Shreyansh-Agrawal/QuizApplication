'Schema for Category data'

from marshmallow import fields, validate

from config.regex_patterns import RegexPattern
from schemas.config_schema import CustomSchema, ResponseSchema


class CategorySchema(CustomSchema):
    'Schema for Category data'

    category_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    admin_id = fields.Str(dump_only=True, validate=validate.Regexp(RegexPattern.ID_PATTERN))
    category_name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))


class CategoryUpdateSchema(CustomSchema):
    'Schema for Category update data'

    updated_category_name = fields.Str(required=True)


class CategoryResponseSchema(ResponseSchema):
    'Schema for response data of get all categories'
    
    data = fields.Nested(CategorySchema, many=True)
