'Schema for Category data'

from marshmallow import Schema, fields, validate

from config.regex_patterns import RegexPattern


class CategorySchema(Schema):
    'Schema for Category data'

    category_id = fields.Str(dump_only=True)
    admin_id = fields.Str(dump_only=True)
    category_name = fields.Str(required=True, validate=validate.Regexp(RegexPattern.NAME_PATTERN))


class CategoryUpdateSchema(Schema):
    'Schema for Category update data'

    updated_category_name = fields.Str(required=True)
