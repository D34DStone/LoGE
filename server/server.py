import asyncio
from protocol import request_pb2


class Server:
    game = None
    server = None

    def __init__(self, game, config):
        self.game = game
        self.config = config

    async def run(self):
        self.server = await asyncio.start_server(self.handle_socket,
                                                 host=self.config.HOST,
                                                 port=self.config.PORT)

        await self.server.serve_forever()

    async def handle_socket(self, reader, writer):
        addr = writer.get_extra_info('peername')
        self.on_connect(addr)
        serving = True
        while serving:
            header = await reader.readline()
            data = await reader.readline()

            if not data:
                self.on_disconnect(addr)
                serving = False
            else:
                self.on_data(addr, header, data)
                writer.write(data)
                await writer.drain()

        writer.close()

    def on_connect(self, addr):
        self.game.on_connect(addr)

    def on_disconnect(self, addr):
        self.game.on_disconnect(addr)

    def on_data(self, addr, header, data):
        self.game.on_request(addr, header, data)
