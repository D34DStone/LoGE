from .commit_container import BaseChange
from .object import ObjectField


class CreateChange(BaseChange):

    kind = "create"
    object = None

    def __init__(self, object):
        self.object = object

    class Schema(BaseChange.Schema):
        object = ObjectField(required=True)


class MoveChange(BaseChange):

    kind = "move"
    object_id = None
    x = None 
    y = None

    def __init__(self, object_id, x, y):
        self.object_id = object_id
        self.new_x = x
        self.new_y = y

    class Schema(BaseChange.Schema):
        object_id = fields.Int(required=True)
        x = fields.Int(required=True)
        y = fields.Int(required=True)
