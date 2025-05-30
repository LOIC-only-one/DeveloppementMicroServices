import asyncio
import nats

# NATS Python Cheat Sheet / Fiche de référence NATS en Python
# Requires: pip install nats-py

# Connexion au serveur NATS
async def run():
    nc = nats.NATS()
    await nc.connect("nats://localhost:4222")

    # Publication simple / Simple Publish
    await nc.publish("foo", b'Bonjour NATS!')

    # Abonnement simple / Simple Subscribe
    async def gestion_message(msg):
        sujet = msg.subject
        donnees = msg.data.decode()
        print(f"Message reçu sur '{sujet}': {donnees}")

    sid = await nc.subscribe("foo", cb=gestion_message)

    # Requête-Réponse / Request-Reply

    # Fonction de gestion pour répondre aux requêtes reçues sur le sujet "aide"
    async def gestion_reponse(msg):
        # Répondre au message reçu avec une réponse prédéfinie
        await msg.respond(b'Voici la reponse!')

    # S'abonner au sujet "aide" pour gérer les requêtes entrantes
    await nc.subscribe("aide", cb=gestion_reponse)

    # Envoyer une requête sur le sujet "aide" et attendre une réponse (timeout de 1 seconde)
    reponse = await nc.request("aide", b'Besoin d\'aide?', timeout=1)

    # Afficher la réponse reçue
    print(f"Réponse reçue: {reponse.data.decode()}")

    # Désabonnement / Unsubscribe
    await nc.unsubscribe(sid)

    # Fermeture de la connexion / Close connection
    await nc.drain()

if __name__ == "__main__":
    asyncio.run(run())
