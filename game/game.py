import asyncio
import json
import enum
import functools

from protocol import Header, Error
from . import request_schemas, response_schemas
from .creature import Creature
from .player import Player
from engine import Engine, API
from marshmallow import ValidationError

# debug
from marshmallow import pprint

class Game(object):
    
    ENGINE_ITERATE_INTERVAL = 1

    sessions = dict()
    engine = None
    api = None
    engine_is_working = False

    def __init__(self):
        self.engine = Engine()
        self.api = API(self.engine)

    async def run(self):
        """Coroutine that iterates engine. It is obvious to run it 
        if you want to run applicaion.
        """
        self.engine_is_working = True
        while self.engine_is_working:
            self.engine.iterate_world()
            await asyncio.sleep(Game.ENGINE_ITERATE_INTERVAL)

    def check_request(request_schema):
        """ Checks if given request is valid. An can be 
        serialized using given schema.

        Decorator has to be used only with request-handler functions.
        Validates request, at worst returns error header and messages, otherwise 
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
        """Decorator that checks if user authorized.

        Decorator has to be used only with request-handler functions.
        Actually checks if `authorized` key exists and its value equals `True`.
        At worst return corresponding error.
        """
        @functools.wraps(f)
        def wrapper(self, addr, request):
            if not self.sessions[addr].get("authorized"):
                return Header.ERROR, Error.FORBIDDEN_REQUEST
            else:
                return f(self, addr, request)

        return wrapper

    @check_request(request_schemas.AuthRequestSchema())
    def auth_handler(self, addr, request):
        self.sessions[addr]["uid"] = request["uid"]
        self.sessions[addr]["authorized"] = True
        self.sessions[addr]["last_commit"] = 0
        return Header.RESPONSE, "Authorized!"

    @check_request(request_schemas.EchoRequestSchema())
    @check_authorized
    def echo_handler(self, addr, request):
        echo = f"<{self.sessions[addr]['uid']}>: {request['data']}>"
        return Header.RESPONSE, echo

    @check_authorized
    def init_player_handler(self, addr, request):
        player = Player(addr)
        self.api.add_player(player)
        return Header.RESPONSE, "Player created."

    @check_request(request_schemas.MoveRequestSchema())
    @check_authorized
    def move_handler(self, addr, request):
        player_id = self.api.get_player_id(addr)
        self.api.move_object(player_id, request["x"], request["y"])

    @check_authorized
    def get_world_handler(self, addr, request):
        world = self.api.get_world_dump()
        response = dict(world=world)
        response, err = response_schemas.GetWorldSchema().dump(response)
        self.sessions[addr]["last_commit"] = self.api.get_last_commit_id()
        return Header.RESPONSE, json.dumps(response)

    @check_authorized
    def update_handler(self, addr, request):
        """ Attention, big kostyl! Fix it """
        commits = self.api.get_commits(start_from=self.sessions[addr]["last_commit"])
        from engine.commit_container.commit import Commit
        t, e = Commit.Schema(many=True).dump(commits["commits"])

        response = {
                "type" : "update",
                "commit_range" : {
                        "commits" : t
                    }
            }

        self.sessions[addr]["last_commit"] = self.api.get_last_commit_id()
        return Header.RESPONSE, json.dumps(response)

    request_handlers = {
                "auth" : auth_handler,
                "echo" : echo_handler,
                "init_player" : init_player_handler,
                "get_world" : get_world_handler,
                "update" : update_handler,
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

            data, err = request_schemas.BaseRequestSchema().load(request)
            if err or not data["request"] in self.request_handlers:
                return Header.ERROR, Error.WRONG_REQUEST 

            handler = self.request_handlers[data["request"]]
            return handler(self, addr, request)

        else:
            return Header.ERROR, Error.WRONG_REQUEST 
