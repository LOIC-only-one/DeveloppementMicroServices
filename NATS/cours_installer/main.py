import asyncio
import nats

async def mafonction():

    nc = await nats.connect("nats://192.168.19.130:4222")
    print("Connected to NATS server")

    #inbox = await nc.subscribe("foo", cb=lambda msg: print(f"Received a message: {msg.data.decode()}"))
    #inbox sert à créer une boîte aux lettres pour recevoir les messages
    inbox = nc.new_inbox()

    await nc.publish("foo", b'Hello World', reply=inbox)
    
    print("Message published to 'foo' subject")
    print(inbox)
    await nc.close()

if __name__ == "__main__":
    asyncio.run(mafonction())