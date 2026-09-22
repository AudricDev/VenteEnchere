import asyncio
from channels_redis.core import RedisChannelLayer


async def test():
    layer = RedisChannelLayer(
        hosts=[
            ("127.0.0.1", 6379),
        ]
    )

    print("Test envoi...")

    await layer.send(
        "test_channel",
        {
            "type": "test.message",
            "message": "hello",
        }
    )

    print("Envoi OK")

    message = await layer.receive("test_channel")

    print("Réception OK")
    print("Message :", message)


asyncio.run(test())