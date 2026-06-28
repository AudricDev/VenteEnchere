from django.db import models
from accounts.models import ProfilUtilisateur
import uuid
# Create your models here.
# modele catégorie
class Categorie(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom

# modele enchère
class Enchere(models.Model):

    STATUT = (
        ('ouverte','Ouverte'),
        ('terminee','Terminée'),
        ('annulee','Annulée'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix_depart = models.DecimalField(max_digits=12, decimal_places=2)
    prix_actuel = models.DecimalField(max_digits=12, decimal_places=2)
    prix_reserve = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(
        max_length=20,
        choices=STATUT,
        default='ouverte'
    )

    vendeur = models.ForeignKey(
        ProfilUtilisateur,
        on_delete=models.CASCADE,
        related_name='encheres'
    )

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.titre

#modele Media
class Media(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    image = models.ImageField(upload_to='encheres/')

    enchere = models.ForeignKey(
        Enchere,
        on_delete=models.CASCADE,
        related_name='images'
    )
    
    def __str__(self):
        return self.image 

#model offre
class Offre(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    montant = models.DecimalField(max_digits=12, decimal_places=2)

    horodatage = models.DateTimeField(auto_now_add=True)

    utilisateur = models.ForeignKey(
        ProfilUtilisateur,
        on_delete=models.CASCADE
    )

    enchere = models.ForeignKey(
        Enchere,
        on_delete=models.CASCADE,
        related_name='offres'
    )

    class Meta:
        ordering = ['-montant']