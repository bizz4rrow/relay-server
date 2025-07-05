import os
import asyncio
import websockets

connected = set()

async def handler(websocket, path):
    # Új kliens csatlakozott
    connected.add(websocket)
    try:
        async for message in websocket:
            # Amikor üzenet érkezik, továbbítjuk minden más kliensnek
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected.remove(websocket)

async def main():
    PORT = int(os.environ.get("PORT", 8080))
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Relay server running on port {PORT}")
        await asyncio.Future()  # fut örökké

if __name__ == "__main__":
    asyncio.run(main())
