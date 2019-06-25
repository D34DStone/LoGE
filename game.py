from request_schemas import *
from protocol import Header, Error
from marshmallow import ValidationError
import json
import enum
import functools

# debug
from marshmallow import pprint

class Game(object):
    
    sessions = dict()

    def check_request(request_schema):
        """ Checks if given request is valid.

        Decorator to be used only with request-handler functions:
        :param self: Self game object
        :param addr: Unique socket name
        :param request: Dict with request
        :return: Pair of header and message

        Validate request, at worst return error header and messages, otherwise 
        pass validated request to decorated function.
        """
        def decorator(f):
            @functools.wraps(f)
            def wrapper(self, addr, request):
                data, err = request_schema.load(request)
                if err:
                    return Header.ERROR, Error.WRONG_REQUEST
                else:
                    return f(self, addr, data)

            return wrapper
        return decorator

    @check_request(AuthRequestSchema())
    def auth_handler(self, addr, request):
        self.sessions[addr]["uid"] = request["uid"]
        return Header.RESPONSE, "Authorized!"

    @check_request(EchoRequestSchema())
    def echo_handler(self, addr, request):
        if not self.sessions[addr].get("uid"):
            return Header.ERROR, Error.FORBIDDEN_REQUEST

        echo = f"<{self.sessions[addr]['uid']}>: {request['data']}>"
        return Header.RESPONSE, echo

    def connection_handler(self, addr):
        print(f"<{addr}> Connected to the server")
        self.sessions[addr] = {}

    def disconnection_handler(self, addr):
        print(f"<{addr}> Disconnected from the server")
        del self.sessions[addr]

    request_handlers = {
                "auth" : auth_handler,
                "echo" : echo_handler
            }

    def process_exnternal_request(self, addr, data_type, data_size=0, data=bytes()):
        """Handles external request and returns result.

        :param addr: Unique network address of client (socket-address)
        :param data_type: Header with which request was sent
        :return: Returns protocol header and data of the response
        """
        if data_type == Header.CONNECTED:
            self.connection_handler(addr)
            return Header.EMPTY, bytes()

        elif data_type == Header.DISCONNECTED:
            self.disconnection_handler(addr)
            return Header.EMPTY, bytes()

        elif data_type == Header.REQUEST:
            try:
                request = json.loads(data)
            except json.decoder.JSONDecodeError:
                return Header.ERROR, Error.SERIALIZE_ERROR

            data, err = BaseRequestSchema().load(request)
            if err or not self.request_handlers.get(data["request"]):
                return Header.ERROR, Error.WRONG_REQUEST 

            handler = self.request_handlers[data["request"]]
            return handler(self, addr, request)

        else:
            return Header.ERROR, Error.WRONG_REQUEST 
