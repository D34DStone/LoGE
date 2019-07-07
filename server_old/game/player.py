from marshmallow import fields
from .creature import Creature

class Player(Creature):

    kind = "player"
    user_addr = None

    def __init__(self, user_addr):
        self.user_addr = user_addr

    class Schema(Creature.Schema):
        user_addr = fields.Str(required=True)
