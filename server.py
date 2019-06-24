import asyncio
from protocol import Protocol
from game import Game

class Server(object):

    host = None
    port = None  
    game = None 
    server = None
    task = None


    def __init__(self, game, host, port):
        self.game = game
        self.host = host
        self.port = port


    def handle_data(self, data_type, data_size, socket, data):
        print(data, data.decode())
        data = data.decode()
        return Protocol.response(data)


    async def handle_connection(self, reader, writer):
        socket = writer.get_extra_info('socket')
        socket_serving = True
        while socket_serving:
            header = await reader.readline()        
            try:
                data_type, data_size = Protocol.parse_header(header)
            except:
                response = Protocol.error(Protocol.Errors.INVALID_HEADER)
                writer.write(response)
                await writer.drain()
                continue

            data = await reader.read(data_size)
            response = self.handle_data(data_type, data_size, socket, data)
            writer.write(response)
            await writer.drain()

        writer.close()


    async def run(self):
        self.server = await asyncio.start_server(
            self.handle_connection,
            host=self.host,
            port=self.port)

        await self.server.serve_forever()


async def main():
    game = Game()
    server = Server(game, "localhost", 5000) 
    await server.run()    

if __name__ == "__main__":
    asyncio.run(main())
