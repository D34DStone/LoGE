import asyncio
import sys
import os
from config import Config

if __name__ == "__main__":
    os.chdir(Config.ROOT)
    sys.path.append(os.path.join(Config.ROOT, 'protocol'))
    from server.server import Server
    server = Server(None, Config) 
    asyncio.run(server.run())
