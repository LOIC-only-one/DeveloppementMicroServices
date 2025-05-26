import asyncio
import nats

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"\n📨 Nouveau message sur [{subject}]: {data}")

    action = input("Répondre (R), transférer (T), ignorer (Entrée) ? ").strip().upper()
    if action == "R":
        if msg.reply is None:
            print("⚠️ Pas de reply possible sur ce message.")
            return
        reply = input("Votre réponse : ")
        await msg.respond(reply.encode())
        print("✅ Réponse envoyée.")
    elif action == "T":
        new_subject = input("Sujet de transfert : ").strip()
        if new_subject:
            await msg._client.publish(new_subject, data.encode())
            print(f"✅ Message transféré sur {new_subject}.")

async def main():
    nc = await nats.connect("nats://192.168.19.130:4222")
    print("✅ Connecté au serveur NATS")

    channel = input("Entrez le sujet de l'abonnement (ex: chat.room1) : ").strip()
    await nc.subscribe(channel, cb=message_handler)
    print(f"✅ Abonné au sujet: {channel}")

    while True:
        send = input("Envoyer un message ? (O/N) : ").strip().upper()
        if send == "O":
            dest = input("Sujet de destination : ").strip()
            msg = input("Message : ")
            await nc.publish(dest, msg.encode())
            print(f"✅ Message envoyé sur {dest}")
        else:
            print("⏳ En attente de messages...")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
