import asyncio
import nats

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")

    async def verifier_montant(msg):
        try:
            montant = int(msg.data.decode())
            if montant <= 10000:
                is_ok = True
            else:
                is_ok = False
        except Exception:
            is_ok = False
        response = '{"montant": ' + str(is_ok).lower() + '}'
        await msg.respond(response.encode())

    await nc.subscribe("argent.*.montant", cb=verifier_montant)
    print("service montant actif")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
