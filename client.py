import asyncio 
import json
from protocol import Header, Error, make_request, parse_header

async def send_request(reader, writer, data, header=Header.REQUEST):
    req = make_request(Header.REQUEST, data)
    writer.write(req)
    await writer.drain()
    data_type, data_size = parse_header(await reader.readline())
    data = await reader.read(data_size)
    print(f"TYPE: {data_type}\n{data}\n")

async def loge_client(host, port):
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except OSError:
        print(f"Fatal error: Can't connect to {host}:{port}")
        return

    while(1):
        cmd = input()
        if cmd == "auth":
            request = json.dumps({
                "request" : "auth",
                "uid" : 123})
            await send_request(reader, writer, request)

        if cmd == "echo":
            request = json.dumps({
                "data" : "I am George :)",
                "request" : "echo"})
            await send_request(reader, writer, request)

        if cmd == "fake":
            request = json.dumps({"request": "auth"})
            await send_request(reader, writer, request)

        if cmd == "exit":
            break

if __name__ == "__main__":
    asyncio.run(loge_client(host="localhost", port=5000))
