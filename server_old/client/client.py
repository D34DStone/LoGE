import importlib
import asyncio 
import json
from .game import Game
from .network_client import NetworkClient

from marshmallow import pprint

class Client(object):

    config = None
    game_running = False
    objects = {}

    def __init__(self, configf):
        try:
            self.config = importlib.import_module(configf).Config
        except:
            print("Can't load config")
            exit(1)
        
        self.game = Game(self.config, self)
        self.network_client = NetworkClient(self.config, self)

    def get_objects(self):
        return self.objects

    async def handle_move(self, v):
        data = {
                "request" : "move",
                "x" : v[0],
                "y" : v[1]
            }
        data = json.dumps(data)
        await self.network_client.send_request(data)

    def handle_world(self, world):
        self.objects = world["objects"]
        self.game_running = True

    def handle_change(self, change):
        if change["kind"] == "create":
            self.objects.append(change["object"])
        if change["kind"] == "move":
            oid = change["object_id"]
            obj = self.objects[oid]
            obj.update({
                "x" : change["x"],
                "y" : change["y"]})

    def handle_changes(self, commits):
        for c in commits:
            changes = c["changes"]
            for change in changes:
                self.handle_change(change)

    async def run(self):
        await asyncio.gather(
            self.game.run(), 
            self.network_client.run())

