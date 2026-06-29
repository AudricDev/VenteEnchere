from django.contrib import admin
from accounts.models import ProfilUtilisateur
from VEnchere.models import *
# Register your models here.
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('id','phone_number','role','avatar','user')
admin.site.register(ProfilUtilisateur,ProfilUtilisateurAdmin)
        
# affichage du produit dans admin
class ProduitAdmin(admin.ModelAdmin):
    class Meta :
        list_display = ('nom','description','etat','marque','modele','couleur','poids','date_creation','reference')
admin.site.register(Produit, ProduitAdmin)

# affichage du categorie dans admin 
class CategorieAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('id','nom','slug')
admin.site.register(Categorie,CategorieAdmin)

# affichage de l'enchere dans admin
class EnchereAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('titre','description','prix_depart','prix_actuel','prix_reserve','date_debut','date_fin','statut','vendeur','categorie')
admin.site.register(Enchere, EnchereAdmin)

#  affichage de l'offre dans admin
class OffreAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('montant','horodatage','utilisateur','enchere')
admin.site.register(Offre, OffreAdmin)

#affichage du paiement dans admin
class PaiementAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('transaction_externe','montant_total','frais_plateforme','methode','statut','date_creation')
admin.site.register(Paiement,PaiementAdmin)

#affichage du transaction dans admin
class TransactionAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('enchere','acheteur','vendeur','paiement','date_cloture','est_livre')
admin.site.register(Transaction, TransactionAdmin)