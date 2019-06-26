from marshmallow import Schema, fields
from engine import ObjectsField

class WorldDumpSchema(Schema):
    last_commit_id = fields.Int(required=True)
    width = fields.Int(required=True)
    height = fields.Int(required=True)
    objects = ObjectsField(required=True)
