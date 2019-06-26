from marshmallow import Schema, fields, ValidationError


class Object(object):
    kind = "object"
    id = None
    x = None
    y = None

    class Schema(Schema):
        kind = fields.Str()
        id = fields.Str()
        x = fields.Int()
        y = fields.Int()


class ObjectField(fields.Field):
    """Custom marshmallow field.
    Implements polymorphic serialization of object inhreirted from `engine.object.Object`
    """

    def _serialize(self, value, attr, obj):
        if not issubclass(type(value), Object):
            raise ValidationError(
                "Given object have to be inheirted from `engine.object.Object`"
            )

        data, err = value.Schema().dump(value)
        if err:
            raise ValidationError(str(err))

        return data


class Player(Object):
    kind = "player"
    uid = None

    def __init__(self, uid):
        self.uid = uid

    class Schema(Object.Schema):
        uid = fields.Int()
