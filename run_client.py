import asyncio
from client import Client 

if __name__ == "__main__":
    client = Client('client.config')
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("...exit")
