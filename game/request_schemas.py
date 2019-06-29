from marshmallow import Schema, fields

class BaseRequestSchema(Schema):
    request = fields.Str(required=True)


class AuthRequestSchema(Schema):
    uid = fields.Int(required=True)


class EchoRequestSchema(Schema):
    data = fields.Str(required=True)


class MoveRequestSchema(Schema):
    x = fields.Int(required=True)
    y = fields.Int(required=True)
