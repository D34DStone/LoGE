import asyncio
from game import Game


class Header(object):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    ABORT = "ABORT"
    ERROR = "ERROR"


class Error(object):
    INVALID_HEADER = "INVALID_HEADER"


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

    @staticmethod
    def make_response(datatype, data):
        """ Take `str` header and `str` or `bytes` data, return bytes that you 
        already can write to socket 
        """
        if isinstance(data, str):
            data = data.encode()

        return f"{datatype} {len(data)}\n".encode() + data

    @staticmethod
    def parse_header(header):
        """ Takes bytes and trying to extract type and size of data. Return
        pair of `str` and `int`.
        """
        header = header.decode()
        header_words = header.split()
        assert len(header_words) > 0, "Header is empty"
        data_type = header_words[0]
        data_size = 0 if len(header_words) == 1 else int(header_words[1])
        return data_type, data_size

    def handle_data(self, data_type, data_size, socket, data):
        return Header.RESPONSE, "Echo: " + data.decode()

    def handle_disconnection(self, socket):
        print(f"{socket} DISCONNECTED")

    async def handle_connection(self, reader, writer):
        """ Coroutine that handles single socket. Calls `handle_data` and `handle_disconnection` during it's work.
        """
        socket = writer.get_extra_info('socket')
        socket_serving = True
        while socket_serving:
            try:
                header = await reader.readline()
                try:
                    data_type, data_size = Server.parse_header(header)

                except:
                    resp = Server.make_response(Header.ERROR,
                                                Error.INVALID_HEADER)
                    writer.write(resp)

                else:
                    data = await reader.read(data_size)
                    data_type, data = self.handle_data(data_type, data_size,
                                                       socket, data)
                    resp = Server.make_response(data_type, data)
                    writer.write(resp)
                    if data_type is Header.ABORT:
                        socket_serving = False

                finally:
                    await writer.drain()

            except ConnectionResetError:
                self.handle_disconnection(socket)
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
