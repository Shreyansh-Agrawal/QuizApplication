'Configurations for marshmallow schemas'

from marshmallow import Schema, fields

from config.string_constants import StatusCodes
from utils.custom_error import ValidationError


class CustomSchema(Schema):
    'Class to override default marshmallow validation error'

    def handle_error(self, error, data, many, **kwargs):
        'Method to override default marshmallow validation error'
        raise ValidationError(status=StatusCodes.UNPROCESSABLE_ENTITY, message=error)


class ResponseSchema(CustomSchema):
    'Class to define the general response schema'

    code = fields.Int(required=True)
    status = fields.Str(required=True)
    message = fields.Str(required=True)
    data = None
