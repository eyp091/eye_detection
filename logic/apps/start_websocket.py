import asyncio
import websockets

async def sendMessage(websocket, path=None):
    print(f"Yeni bir bağlantı: {path}")

    try:
        while True:
            message = "surucu yorgun"

            await websocket.send(message)
            await asyncio.sleep(1)
    except websockets.ConnectionClosed:
        print("Bağlantı kesildi")

async def websocketMain():
    print("Websocket sunucusu başlıyor...")
    async with websockets.serve(sendMessage, "0.0.0.0", 5000):
        print("Websocket sunucusu başlatıldı. Bağlantı bekleniyor...")
        await asyncio.Future()

asyncio.run(websocketMain())