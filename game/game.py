from protocol import request_pb2
from engine.engine import Engine

class Game:

    sessions = dict()
    engine = None 

    def __init__(self, config):
        self.engine = Engine(config) 

    async def run(self):
        await self.engine.run()

    def on_request(self, addr, header, data) -> (bytes, bytes):
        request_header = request_pb2.Header()
        request_header.ParseFromString(data)

        if request_header.header not in self.request_handlers:
            header = request_pb2.Header()
            header.header = request_pb2.Header.ERROR
            response = request_pb2.ErrorResponse()
            response.msg = "Unknown request type"
            return header.SerializeToString(), response.SerializeToString()

        handler = self._request_handlers.get(request_header.header)
        return handler(self, addr, data)

    def on_connect(self, addr):
        print(f"<{addr}> connected")


    def on_disconnect(self, addr):
        print(f"<{addr}> disconnected")

    def _auth_handler(self, addr, data):
        print(f"{addr} wants to authrorize")

    def _init_player_handler(self, addr, data):
        print(f"{addr} wants to init player")

    _request_handlers = {
            request_pb2.Header.AUTH : _auth_handler,
            request_pb2.Header.INIT_PLAYER : _init_player_handler
            }
