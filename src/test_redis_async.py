import asyncio
import redis.asyncio as redis


async def main():
    print("Connexion à Redis...")

    r = redis.Redis(
        host="127.0.0.1",
        port=6379,
        decode_responses=True,
    )

    try:
        resultat = await r.ping()
        print("Redis async :", resultat)

    except Exception as e:
        print("ERREUR :", type(e).__name__)
        print("DETAIL :", e)

    finally:
        await r.aclose()


asyncio.run(main())