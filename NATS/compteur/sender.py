##### Création d'un compteur sur asynchronous NATS

import asyncio
import nats
import time


async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    print("Connected to NATS server")

    compteur = 0

    while True:
        try:
            await nc.publish("foo", str(compteur).encode())
            print('Message envoyé :', compteur)
            compteur += 2
            await time.sleep(10)

        except KeyboardInterrupt:
            print("Interruption du programme")
            break
        except Exception as e:
            print(f"Erreur : {e}")
            break

    await nc.close()

if __name__ == "__main__":
    asyncio.run(main())
