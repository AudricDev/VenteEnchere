import asyncio
from channels_redis.core import RedisChannelLayer


async def test():
    layer = RedisChannelLayer(
        hosts=[
            ("127.0.0.1", 6379),
        ]
    )

    groupe = "test_enchere"

    print("1. Création du channel...")

    channel_name = await layer.new_channel()

    print("Channel :", channel_name)

    print("2. Ajout au groupe...")

    await layer.group_add(
        groupe,
        channel_name
    )

    print("Group_add OK")

    print("3. Envoi dans le groupe...")

    await layer.group_send(
        groupe,
        {
            "type": "test.message",
            "message": "Bonjour depuis le groupe !",
        }
    )

    print("Group_send OK")

    print("4. Réception...")

    message = await layer.receive(channel_name)

    print("Réception OK")
    print("Message :", message)

    print("5. Suppression du groupe...")

    await layer.group_discard(
        groupe,
        channel_name
    )

    print("Group_discard OK")


asyncio.run(test())