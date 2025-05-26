import asyncio
import nats
import time

### * Permet de remplacer n'importe quel mot dans le sujet ex : fr.*.67.colmar
### fr.grand_est.67.colmar fr.grand_est.67.colmar.>
### Si utilise > : fr.grand_est.67.colmar.nord

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    print("Connected to NATS server")

    await nc.subscribe("fr.*.*.strasbourg", cb=message_handler)

if __name__ == "__main__":
    asyncio.run(main())
