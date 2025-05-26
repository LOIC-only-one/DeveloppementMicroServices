import asyncio
import nats


async def cb(msg):
    print(f"Received a message: {msg.data.decode()}")

async def mafonction():
    nc = await nats.connect("nats://192.168.19.130:4222")

    ### ici on subscrit à un sujet
    await nc.subscribe("foo", cb=cb)
    print("Connected to NATS server")

    ### le try sert à garder le programme en vie
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass

    await nc.close()

if __name__ == "__main__":
    asyncio.run(mafonction())
