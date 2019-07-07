import asyncio
from server import Server
from game import Game 

async def main():
    game = Game()
    server = Server(game, "localhost", 5000)
    await asyncio.gather(server.run(), game.run())

if __name__ == "__main__":
    asyncio.run(main())
