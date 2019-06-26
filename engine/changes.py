from .commit_container import BaseChange
from .object import ObjectField


class CreateChange(BaseChange):

    kind = "create"
    object = None

    def __init__(self, object):
        self.object = object

    class Schema(BaseChange.Schema):
        object = ObjectField(required=True)
