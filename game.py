from request_schemas import *
from protocol import Header, Error
from engine.engine import Engine 
from marshmallow import ValidationError
import asyncio
import json
import enum
import functools

# debug
from marshmallow import pprint

class Game(object):
    
    ENGINE_ITERATE_INTERVAL = 1

    sessions = dict()
    engine = None

    def __init__(self):
        self.engine = Engine()

    async def run(self):
        """Coroutine that provides entery point to world
        update.
        """
        engine_is_working = True
        print("Engine was launched")
        while engine_is_working:
            self.engine.iterate_world()
            await asyncio.sleep(Game.ENGINE_ITERATE_INTERVAL)

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

    def check_authorized(f):
        """ Decorator that checks if user authorized.

        Decorator to be used only with request-handler functions:
        :param self: Self game object
        :param addr: Unique socket name
        :param request: Dict with request
        :return: Pair of header and message

        Actually check if there is `uid` key in his session.
        At worst return corresponding error.
        """
        @functools.wraps(f)
        def wrapper(self, addr, request):
            if not self.sessions[addr].get("authorized"):
                return Header.ERROR, Error.FORBIDDEN_REQUEST
            else:
                return f(self, addr, request)

        return wrapper

    @check_request(AuthRequestSchema())
    def auth_handler(self, addr, request):
        self.sessions[addr]["authorized"] = True
        self.sessions[addr]["uid"] = request["uid"]
        return Header.RESPONSE, "Authorized!"

    @check_request(EchoRequestSchema())
    @check_authorized
    def echo_handler(self, addr, request):
        echo = f"<{self.sessions[addr]['uid']}>: {request['data']}>"
        return Header.RESPONSE, echo

    @check_authorized
    def init_player_handler(self, addr, request):
        self.engine.create_player(self.sessions[addr]["uid"])
        return Header.RESPONSE, "Mb it realy has created player. Who knows..."

    @check_authorized
    def get_world_handler(self, addr, request):
        last_commit_id, world = self.engine.get_world_dump()
        return Header.RESPONSE, json.dumps(world)

    request_handlers = {
                "auth" : auth_handler,
                "echo" : echo_handler,
                "init_player" : init_player_handler,
                "get_world" : get_world_handler
            }

    def connection_handler(self, addr):
        print(f"<{addr}> Connected to the server")
        self.sessions[addr] = {}

    def disconnection_handler(self, addr):
        print(f"<{addr}> Disconnected from the server")
        del self.sessions[addr]

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
            if err or not data["request"] in self.request_handlers:
                return Header.ERROR, Error.WRONG_REQUEST 

            handler = self.request_handlers[data["request"]]
            return handler(self, addr, request)

        else:
            return Header.ERROR, Error.WRONG_REQUEST 
