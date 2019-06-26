from marshmallow import Schema, fields, ValidationError
from engine.object import ObjectField

class BaseChange(object):

    kind = "base"

    class Schema(Schema):
        kind = fields.Str(required=True)


class ChangeField(fields.Field):
    
    def _serialize(self, value, attr, obj):
        if not issubclass(type(value), BaseChange):
            raise ValidationError("Given object have to be subclass of `engine.commit_container.change.BaseChange`")

        data, err = value.Schema().dump(value)
        if err:
            raise ValidationError(str(err))

        return data


class ChangesField(fields.Field):

    def _serialize(self, value, attr, obj):
        return list(map(lambda change:
            ChangeField._serialize(self, change, attr, obj),
            value))
