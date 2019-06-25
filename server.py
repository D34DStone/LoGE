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
        return self.game.process_exnternal_request(socket, data_type, data_size, data)

    def handle_disconnection(self, addr):
        self.game.process_exnternal_request(addr, Header.DISCONNECTED)

    def handle_connection(self, addr):
        self.game.process_exnternal_request(addr, Header.CONNECTED)

    async def handle_socket(self, reader, writer):
        """Loop that handles single socket.
        """
        addr = writer.get_extra_info('peername')
        self.handle_connection(addr)
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
        self.server = await asyncio.start_server(self.handle_socket,
                                                 host=self.host,
                                                 port=self.port)

        await self.server.serve_forever()
