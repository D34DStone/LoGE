import asyncio 
import json
import enum
import functools
from protocol import Header, Error, make_request, parse_header

from marshmallow import pprint # DEBUG


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
    reader = None 
    writer = None

    def __init__(self, config, client):
       self.state = State.AUTHORIZATION
       self.config = config
       self.client = client

    async def send_request(self, data, header=Header.REQUEST):
        req = make_request(Header.REQUEST, data)
        self.writer.write(req)
        await self.writer.drain()
        data_type, data_size = parse_header(await self.reader.readline())
        data = await self.reader.read(data_size)
        if data_type == Header.ERROR:
            raise ValueError("Error: " + data.decode())

        return data

    async def auth(self):
        resp = await self.send_request(json.dumps({"request" : "auth", "uid" : 123}))

    async def create_player(self):
        resp = await self.send_request(json.dumps({"request" : "init_player"}))
        await asyncio.sleep(0.2)

    async def get_world(self):
        resp = await self.send_request(json.dumps({"request" : "get_world"}))
        resp = json.loads(resp)
        world = resp["world"]
        self.client.handle_world(world)
        
    async def update(self):
        resp = await self.send_request(json.dumps({"request" : "update"}))
        resp = json.loads(resp)
        new_commits = resp["commit_range"]["commits"]
        self.client.handle_changes(new_commits)

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
            raise err
            print(str(err))
            print(f"next try after {fail_delay} seconds...")
            await asyncio.sleep(fail_delay)
        else:
            self.state = next_state

    async def run(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.config.SERVER_HOST, self.config.SERVER_PORT)
        except OSError:
            print("Can't connect to the server. Network Client ends his work.")
            return

        self.is_working = True
        while(self.is_working):
            handler, next_state = self.state_handlers[self.state]
            handler = functools.partial(handler, self)
            await self.try_request(handler, next_state)
            await asyncio.sleep(self.config.REQUEST_INTERVAL)
