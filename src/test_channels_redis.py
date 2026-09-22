import asyncio

from channels_redis.core import RedisChannelLayer


async def main():
    print("Création du Channel Layer...")

    layer = RedisChannelLayer(
        hosts=[
            ("127.0.0.1", 6379)
        ]
    )

    try:
        print("Création du channel...")
        channel = await layer.new_channel()
        print("Channel :", channel)

        print("Envoi du message...")
        await layer.send(
            channel,
            {
                "type": "test.message",
                "message": "Bonjour depuis channels_redis !"
            }
        )
        print("Envoi OK")

        print("Réception du message...")
        message = await layer.receive(channel)

        print("Réception OK")
        print("Message :", message)

    except Exception as e:
        print("ERREUR :", type(e).__name__)
        print("DETAIL :", e)


asyncio.run(main())