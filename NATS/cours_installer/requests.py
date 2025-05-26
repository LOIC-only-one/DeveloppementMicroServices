import asyncio
import nats


async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")

    await nc.request("foo", b'Hello World')
    ## nc request sert à envoyer un message et à attendre une réponse

    await nc.close()

if __name__ == "__main__":
    asyncio.run(main())