import asyncio
from websockets.server import serve

async def handler(ws):
    print("WS: conectado")

    await ws.send("nonce:" + str(state.New_nonce))

    async for msg in ws:
        print("WS mensaje:", msg)

async def start_ws_server():
    async with serve(handler, "127.0.0.1", 8765):
        await asyncio.Future()  # run forever
