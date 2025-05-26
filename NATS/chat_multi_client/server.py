import asyncio
import nats

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"\n📨 Nouveau message sur [{subject}]: {data}")

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    print("✅ Connecté au serveur NATS")

    await nc.subscribe("chat.>", cb=message_handler)

    # Garder le serveur en écoute
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
