import importlib
import asyncio 
from .game import Game
from .network_client import NetworkClient

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
        
        #self.network_client = NetworkClient(config)
        self.game_running = True    # Debug 
        self.game = Game(self.config, self)
        self.network_client = NetworkClient(self.config, self)

    def get_objects(self):
        return []

    async def run(self):
        await asyncio.gather(
            self.game.run(), 
            self.network_client.run())

