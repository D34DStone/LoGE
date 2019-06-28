from marshmallow import Schema, fields
from engine import ObjectsField
from engine import api_schemas


class GetWorldSchema(Schema):
    type = fields.Str(default="get_world")
    world = fields.Nested(api_schemas.WorldSchema())


class UpdateSchema(Schema):
    type = fields.Str(default="update")
    commit_range = fields.Nested(api_schemas.CommitRangeSchema())
