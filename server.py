import os
import asyncio
import websockets

PORT = int(os.environ.get("PORT", 3000))
clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Relay server running on port {PORT}")
        await asyncio.Future()  # futás végtelen ideig

asyncio.run(main())
