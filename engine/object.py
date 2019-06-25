from marshmallow import Schema, fields, pprint

class Object(object):
    kind = "nested object"
    id = None 
    x = None 
    y = None

    class Schema(Schema):
        kind = fields.Str()
        x = fields.Int()
        y = fields.Int()


class Player(Object):
    kind = "player"
    uid = None

    def __init__(self, uid):
        self.uid = uid

    class Schema(Object.Schema):
        uid = fields.Int()
