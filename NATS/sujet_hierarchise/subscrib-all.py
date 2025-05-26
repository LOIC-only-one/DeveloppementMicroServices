import asyncio
import nats

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")

    async def message_handler_1(msg):
        print(f"Abonné a reçu: {msg.subject} -> {msg.data.decode()}")

    # Abonné 1 : tous les messages sous fr.grand_est.67.colmar
    await nc.subscribe("fr.grand_est.67.colmar", cb=message_handler_1)

    # Garde le programme en vie pour recevoir les messages
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())