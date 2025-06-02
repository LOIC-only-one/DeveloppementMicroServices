import nats
import asyncio

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    subjects = [
        "bonjour.strasbourg.matin",
        "bonjour.strasbourg.midi",
        "bonjour.colmar.matin"
    ]
    for i in range(10):
        for subject in subjects:
            msg = f"message {i+1} sur {subject}"
            await nc.publish(subject, msg.encode())
            print(f"envoye: {msg}")
    await nc.close()

if __name__ == "__main__":
    asyncio.run(main())