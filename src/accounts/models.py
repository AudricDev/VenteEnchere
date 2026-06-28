from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProfilUtilisateur(models.Model):
    ROLE_CHOICE = (
        ('Admin','Admin'),
        ('Vendeur','Vendeur'),
        ('Acheteur','Acheteur'),
    )
    name = models.CharField(max_length=50,blank=True)
    phone_number = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=ROLE_CHOICE, default='Acheteur')
    avatar = models.ImageField(upload_to='Utilisateur', blank=True, null=True)
    
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=True,null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ProfilUtilisateur'
        verbose_name_plural = 'ProfilUtilisateurs'