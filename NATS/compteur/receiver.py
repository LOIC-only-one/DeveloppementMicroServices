import asyncio
import nats

def cb(msg):
    print(f"Received a message: {msg.data.decode()}")
    # On peut faire un traitement ici
    # Par exemple, incrémenter un compteur
    # ou faire une action spécifique en fonction du message reçu


async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    print("Connected to NATS server")

    await nc.subscribe("foo", cb=cb)

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass

    await nc.close()
if __name__ == "__main__":
    asyncio.run(main())
