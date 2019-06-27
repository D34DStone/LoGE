import asyncio 
import json
import enum
import functools
from protocol import Header, Error, make_request, parse_header


class State(enum.Enum):
    AUTHORIZATION = 1
    CREATING_PLAYER = 2
    GETTING_WORLD = 3
    UPDATE = 4


class NetworkClient(object):

    client = None 
    config = None
    state = None     
    is_working = False

    def __init__(self, config, client):
       self.state = State.AUTHORIZATION
       self.config = config
       self.client = client

    async def send_request(reader, writer, data, header=Header.REQUEST):
        req = make_request(Header.REQUEST, data)
        writer.write(req)
        await writer.drain()
        data_type, data_size = parse_header(await reader.readline())
        data = await reader.read(data_size)
        if data_type == Header.ERROR:
            raise ValueError("Error: " + data.decode())

        return data

    async def auth(self, reader, writer):
        print("Let auth!")
        pass

    async def create_player(self, reader, writer):
        print("Lets create player!")
        pass

    async def get_world(self, reader, writer):
        print("Lets get world!")

    async def update(self, reader, writer):
        print("Lets update world")

    state_handlers = {
            State.AUTHORIZATION : (auth, State.CREATING_PLAYER),
            State.CREATING_PLAYER : (create_player, State.GETTING_WORLD),
            State.GETTING_WORLD : (get_world, State.UPDATE),
            State.UPDATE : (update, State.UPDATE),
        }

    async def try_request(self, request_fun, next_state, fail_delay=1):
        try:
            await request_fun()
        except Exception as err:
            print(str(err))
            print(f"next try after {fail_delay} seconds...")
            await asyncio.sleep(fail_delay)
        else:
            self.state = next_state

    async def run(self):
        try:
            reader, writer = await asyncio.open_connection(self.config.SERVER_HOST, self.config.SERVER_PORT)
        except OSError:
            print("Con't connect to the server. Network Client ends his work.")
            return

        self.is_working = True
        while(self.is_working):
            handler, next_state = self.state_handlers[self.state]
            handler = functools.partial(handler, self, reader, writer)
            await self.try_request(handler, next_state)
            await asyncio.sleep(self.config.REQUEST_INTERVAL)
