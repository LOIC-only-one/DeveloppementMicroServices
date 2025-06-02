import asyncio
import nats
import datetime

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")

    async def verifier_date(msg):
        try:
            date_str = msg.data.decode()
            print(f"Reçu date: {date_str}")


            date_obj = datetime.date.fromisoformat(date_str)
            
            aujourd_hui = datetime.date.today()
            date_limite = aujourd_hui - datetime.timedelta(days=10)

            correspond = date_obj >= date_limite

            resultat = '{ "date" : ' + str(correspond).lower() + ' }'
            
        except Exception as erreur_in:
            print(f"Erreur: {erreur_in}")
            resultat = '{ "date" : false }'

        await msg.respond(resultat.encode())

    await nc.subscribe("argent.*.date", cb=verifier_date)
    print("service date actif")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
