from marshmallow import Schema, fields
from engine.object import ObjectsField

class WorldSchema(Schema):

    last_commit_id = fields.Int(required=True)
    objects = ObjectsField(required=True)
