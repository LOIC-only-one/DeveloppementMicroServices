import asyncio
import nats

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    sujets = [
        ("fr.grand_est.67.colmar", "hello_from_colmar"),
        ("fr.grand_est.67.strasbourg", "hello_from_strasbourg"),
        ("fr.grand_est.68.mulhouse", "hello_from_mulhouse"),
        ("fr.ile_de_france.75.paris", "hello_from_paris"),
        ("fr.bretagne.35.rennes", "hello_from_rennes"),
    ]
    for sujet, msg in sujets:
        await nc.publish(sujet, msg.encode())
        print(f"Envoyé: {sujet} -> {msg}")
    await nc.drain()

if __name__ == "__main__":
    asyncio.run(main())
