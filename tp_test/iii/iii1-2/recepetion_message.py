import nats
import asyncio

async def traitement(msg):
    sujet, reponse, message = msg.subject, msg.reply, msg.data.decode()
    print(f"Reçu sur {sujet}: {message}")

    if '.requests' in sujet or '.inbox' in sujet:
        if reponse:
            reponse_message = f"reponse: {message}"
            await msg.respond(reponse_message.encode())
            print(f"reponse envoyee: {reponse_message}")

async def principal():
    nc = await nats.connect("nats://192.168.19.130:4222")
    await nc.subscribe("bonjour.strasbourg.matin", cb=traitement)
    print("en attente de messages sur 'bonjour.strasbourg.matin'")

    await asyncio.sleep(60 * 10)

if __name__ == "__main__":
    try:
        asyncio.run(principal())
    except KeyboardInterrupt:
        print("arret du programme")
    
    except Exception as erreur_inconnu:
        print(f"erreur inconnue: {erreur_inconnu}")