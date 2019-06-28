from marshmallow import Schema, fields
from .change import BaseChange, ChangesField


class Commit(object):

    id = None
    changes = []

    def __init__(self, id):
        self.id = id
        self.changes = []

    def append_change(self, change):
        if not issubclass(type(change), BaseChange):
            raise ValueError(
                "given object have to be instance of object inheirted from `engine.BaseChange`"
            )

        self.changes.append(change)

    class Schema(Schema):
        id = fields.Int(required=True)
        changes = ChangesField(required=True)
