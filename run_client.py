import asyncio
from client import Client 

if __name__ == "__main__":
    client = Client('client.config')
    asyncio.run(client.run())
