import asyncio
import nats
import json

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"📩 Reçu sur '{subject}': {data}")

    try:
        json_data = json.loads(data)
        print(f"📦 JSON décodé: {json_data}")
    except Exception:
        error_response = {"status": "error", "message": "Invalid JSON"}
        await msg.respond(json.dumps(error_response).encode())

    code = json_data.get("code")
    if code == "QUESTION":
        result = "Bonjour !"
    elif code == "STATUS":
        result = "Tout fonctionne bien."
    else:
        result = "Code inconnu."

    response = {"status": "success", "result": result}
    await msg.respond(json.dumps(response).encode())

    print(f"✅ Réponse envoyée: {response}")

async def json_receiver():
    nc = await nats.connect("nats://192.168.19.130:4222")
    print("✅ Connecté au serveur NATS")

    # Crée une seule fois l'abonnement et envoi la reponse sur message_handler
    await nc.subscribe("hotline", cb=message_handler)

    # Ne fait rien d'autre, juste garde le serveur actif
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(json_receiver())
