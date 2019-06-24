from marshmallow import Schema, fields

class BaseRequestSchema(Schema):
    uid     = fields.Int(required=True)
    request = fields.Str(required=True)
