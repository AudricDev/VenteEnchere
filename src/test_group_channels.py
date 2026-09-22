import asyncio

from channels_redis.core import RedisChannelLayer


async def main():

    print("Création du Channel Layer...")

    layer = RedisChannelLayer(
        hosts=[
            ("127.0.0.1", 6379)
        ]
    )

    channel = await layer.new_channel()

    groupe = "enchere_test"

    print("Channel :", channel)
    print("Groupe :", groupe)

    try:
        print("\n1. Ajout au groupe...")
        await layer.group_add(
            groupe,
            channel
        )
        print("Group_add OK")

        print("\n2. Envoi dans le groupe...")
        await layer.group_send(
            groupe,
            {
                "type": "nouvelle_offre",
                "montant": "15000000",
                "utilisateur": "test",
                "date": "20/09/2026 15:00:00"
            }
        )
        print("Group_send OK")

        print("\n3. Réception...")
        message = await layer.receive(channel)

        print("Réception OK")
        print("Message :", message)

        print("\n4. Suppression du groupe...")
        await layer.group_discard(
            groupe,
            channel
        )
        print("Group_discard OK")

    except Exception as e:
        print("\nERREUR :", type(e).__name__)
        print("DETAIL :", e)


asyncio.run(main())