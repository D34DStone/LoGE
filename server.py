import asyncio
from protocol import Header, Error, make_request, parse_header
from game import Game


class Server(object):
    """ Object that provides client-server communication througth 
    the sockets. Also parses incoming requests and seralize outcoming responses. 
    """

    def __init__(self, game, host, port):
        self.game = game
        self.host = host
        self.port = port

    def handle_data(self, data_type, data_size, socket, data):
        """Cals from `handle_connection` to process clients request.

        Actually pass it to game engine.
        """
        return self.game.process_exnternal_request(socket, data_size, data)

    def handle_disconnection(self, addr):
        """Cals from `handle_connection` to tell game engine that clinet disconnected.
        """
        pass

    async def handle_connection(self, reader, writer):
        """Loop that handles signle socket.
        """
        addr = writer.get_extra_info('peername')
        socket_serving = True
        while socket_serving:
            try:
                header = await reader.readline()
                try:
                    data_type, data_size = parse_header(header)

                except:
                    resp = make_request(Header.ERROR, Error.INVALID_HEADER)
                    writer.write(resp)

                else:
                    data = await reader.read(data_size)
                    data_type, data = self.handle_data(data_type, data_size,
                                                       addr, data)
                    resp = make_request(data_type, data)
                    writer.write(resp)
                    if data_type is Header.ABORT:
                        socket_serving = False

                finally:
                    await writer.drain()

            except ConnectionResetError:
                self.handle_disconnection(addr)
                socket_serving = False

        writer.close()

    async def run(self):
        self.server = await asyncio.start_server(self.handle_connection,
                                                 host=self.host,
                                                 port=self.port)

        await self.server.serve_forever()


async def main():
    game = Game()
    server = Server(game, "localhost", 5000)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
