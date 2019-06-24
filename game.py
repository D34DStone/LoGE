from request_schemas import *
from marshmallow import ValidationError
import json
import enum

# debug
from marshmallow import pprint

class Game(object):

    session = dict()

    def __init__(self):
        pass


    def process_external_request(self, socket, data):
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            print("Wrong json")
            return

        request, errors  = BaseRequestSchema().load(data)
        if errors:
            print("Wrong request")
            return

        pprint(request)

