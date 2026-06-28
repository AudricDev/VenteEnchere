from django.db import models
from django.contrib.auth.models import User
import uuid

#model profil pour ajout complémentaire de l'User
class ProfilUtilisateur(models.Model):
    ROLE_CHOICE = (
        ('Admin','Admin'),
        ('Vendeur','Vendeur'),
        ('Acheteur','Acheteur'),
    )
    #universal unique identifiant
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=20)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICE,
        default='Acheteur'
    )

    avatar = models.ImageField(
        upload_to='utilisateurs/',
        blank=True,
        null=True
    )

    date_creation = models.DateTimeField(auto_now_add=True, blank=True,null=True)

    def __str__(self):
        return self.user.username

