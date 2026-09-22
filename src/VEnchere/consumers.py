import json
from decimal import Decimal, InvalidOperation

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from .models import (
    Enchere,    
    Offre,
    Participation,
)


class EnchereConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.enchere_id = self.scope["url_route"]["kwargs"]["enchere_id"]

        self.groupe_enchere = f"enchere_{self.enchere_id}"

        self.user = self.scope["user"]

        # Vérifier l'authentification
        if not self.user.is_authenticated:
            await self.close()
            return

        # Vérifier que l'enchère existe
        existe = await self.verifier_enchere()

        if not existe:
            await self.close()
            return

        # Rejoindre le groupe
        await self.channel_layer.group_add(
            self.groupe_enchere,
            self.channel_name
        )

        await self.accept()

        print(
            f"WebSocket connecté : "
            f"{self.user.username} "
            f"→ enchère {self.enchere_id}"
        )


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.groupe_enchere,
            self.channel_name
        )

        print(
            f"WebSocket déconnecté : "
            f"{self.user.username}"
        )


    async def receive_json(self, content):

        print("========== OFFRE WEBSOCKET ==========")
        print("Données reçues :", content)

        montant = content.get("montant")

        if montant is None:
            await self.envoyer_erreur(
                "Le montant est obligatoire."
            )
            return

        try:

            montant = Decimal(str(montant))

        except (InvalidOperation, ValueError):

            await self.envoyer_erreur(
                "Le montant est invalide."
            )
            return

        resultat = await self.creer_offre(montant)

        if not resultat["success"]:

            await self.envoyer_erreur(
                resultat["message"]
            )

            return

        # Diffuser à TOUS les utilisateurs
        await self.channel_layer.group_send(

            self.groupe_enchere,

            {
                "type": "nouvelle_offre",

                "montant": str(
                    resultat["montant"]
                ),

                "utilisateur": resultat["utilisateur"],

                "date": resultat["date"],
            }
        )


    async def nouvelle_offre(self, event):

        await self.send_json({

            "type": "nouvelle_offre",

            "montant": event["montant"],

            "utilisateur": event["utilisateur"],

            "date": event["date"],
        })


    async def envoyer_erreur(self, message):

        await self.send_json({

            "type": "erreur",

            "message": message

        })


    @database_sync_to_async
    def verifier_enchere(self):

        return Enchere.objects.filter(
            id=self.enchere_id
        ).exists()


    @database_sync_to_async
    def creer_offre(self, montant):

        try:

            enchere = Enchere.objects.get(
                id=self.enchere_id
            )

        except Enchere.DoesNotExist:

            return {
                "success": False,
                "message": "Cette enchère n'existe pas."
            }

        profil = getattr(
            self.user,
            "profilutilisateur",
            None
        )

        if profil is None:

            return {
                "success": False,
                "message": "Votre profil n'existe pas."
            }

        # Vérifier rôle
        if profil.role != "Acheteur":

            return {
                "success": False,
                "message": "Seuls les acheteurs peuvent enchérir."
            }

        # Vérifier inscription
        inscrit = Participation.objects.filter(
            acheteur=profil,
            enchere=enchere
        ).exists()

        if not inscrit:

            return {
                "success": False,
                "message": "Vous devez être inscrit à cette enchère."
            }

        # Vérifier vendeur
        if enchere.vendeur == profil:

            return {
                "success": False,
                "message": "Vous ne pouvez pas enchérir sur votre propre vente."
            }

        # Vérifier statut
        if enchere.statut != "ouverte":

            return {
                "success": False,
                "message": "Cette enchère est fermée."
            }

        # Prix actuel
        prix_actuel = (
            enchere.prix_actuel
            if enchere.prix_actuel is not None
            else enchere.prix_depart
        )

        # Vérifier montant
        if montant <= prix_actuel:

            return {
                "success": False,
                "message": (
                    f"Votre offre doit être supérieure "
                    f"à {prix_actuel} Ar."
                )
            }

        # Créer l'offre
        offre = Offre.objects.create(
            montant=montant,
            utilisateur=profil,
            enchere=enchere
        )

        # Mettre à jour le prix actuel
        enchere.prix_actuel = montant
        enchere.save(
            update_fields=["prix_actuel"]
        )

        return {

            "success": True,

            "montant": offre.montant,

            "utilisateur": profil.user.username,

            "date": offre.horodatage.strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        }