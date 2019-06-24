from request_schemas import *
from protocol import Header, Error
from marshmallow import ValidationError
import json
import enum

# debug
from marshmallow import pprint

class Game(object):
    
    sessions = dict()

    def auth_handler(self, addr, request):
        data, err = AuthRequestSchema().load(request)
        if err:
            return Header.ERROR, Error.WRONG_REQUEST

        self.sessions[addr]["uid"] = data["uid"]
        return Header.RESPONSE, "Authorized!"

    def echo_handler(self, addr, request):
        data, err = EchoRequestSchema().load(request)
        if err:
            return Header.ERROR, Error.WRONG_REQUEST

        echo = f"<{self.sessions[addr]['uid']}>: {request['data']}>"
        return Header.RESPONSE, echo

    request_handlers = {
                "auth" : auth_handler,
                "echo" : echo_handler
            }

    def process_exnternal_request(self, addr, datasize, data):
        """Handles external request and returns result.

        :param addr: Unique network address of client (socket-address)
        :return: Returns protocol header and data of the response
        """
        if not self.sessions.get(addr):
            self.sessions[addr] = {}

        try:
            request = json.loads(data)
        except json.decoder.JSONDecodeError:
            return Header.ERROR, Error.SERIALIZE_ERROR

        data, err = BaseRequestSchema().load(request)
        if err or not self.request_handlers.get(data["request"]):
            return Header.ERROR, Error.WRONG_REQUEST 

        handler = self.request_handlers[data["request"]]
        return handler(self, addr, request)
