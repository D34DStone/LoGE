from marshmallow import Schema, fields
from change import ChangeField, ChangesField


class Commit(object):

    id = None 
    changes = []

    def __init__(self, id):
        self.id = id

    def append_change(self, log):
        self.changes.append(log)


    class Schema(Schema):
        id = fields.Int(required=True)
        changes = ChangesField(required=True)
