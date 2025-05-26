import asyncio
import nats
import json
import random

async def json_sender():
    json_data = {
        "id": random.randint(1, 100),
        "question": "Quel est le statut de ma demande ?",
        "code": "QUESTION"
    }
    return json.dumps(json_data)

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    print("Connected to NATS server")

    inbox = nc.new_inbox()

    # S'abonner à l'inbox pour recevoir la réponse
    sub = await nc.subscribe(inbox)

    # Envoyer la question sur le sujet "hotline" avec reply=inbox
    data = await json_sender()
    await nc.publish("hotline", data.encode(), reply=inbox)
    print(f"Envoyé: hotline -> {data}")

    # Attendre la réponse
    response = await sub.next_msg()
    print(f"Réponse reçue: {response.data.decode()}")


if __name__ == "__main__":
    asyncio.run(main())
