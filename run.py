import asyncio
import sys
import os
from config import Config

async def main():
    os.chdir(Config.ROOT)
    sys.path.append(os.path.join(Config.ROOT, 'protocol'))
    from server.server import Server
    from game.game import Game
    game = Game(Config)
    server = Server(game, Config) 
    await asyncio.gather(game.run(), server.run())


if __name__ == "__main__":
    asyncio.run(main())
