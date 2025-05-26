import asyncio
import time
import nats

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")

    # S'abonne a tout les messages sous le sujet "fr.grand_est.*"
    # Cela inclut tous les messages sous "fr.grand_est.67.colmar", "fr.grand_est.68.mulhouse", etc.
    await nc.subscribe("fr.grand_est.*", cb=message_handler)

    await asyncio.Future()
    
if __name__ == "__main__":
    asyncio.run(main())