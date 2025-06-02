import asyncio
import nats

numeros_valides = {
    "11111111", "22222222", "33333333",
    "44444444", "55555555", "66666666"
}

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")

    async def verifier_compte(msg):
        sujet = msg.subject
        parties = sujet.split(".")

        compte = parties[1]
        est_valide = compte in numeros_valides

        reponse = f'{{"compte": {str(est_valide).lower()}}}'
        await msg.respond(reponse.encode())

    await nc.subscribe("argent.*.compte", cb=verifier_compte)
    print("service compte actif")
    evenement = asyncio.Event() ## boucle infiinie
    await evenement.wait() 

if __name__ == "__main__":
    asyncio.run(main())
