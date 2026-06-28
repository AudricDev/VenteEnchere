from django.contrib import admin
from accounts.models import ProfilUtilisateur
from VEnchere.models import Categorie,Enchere
# Register your models here.
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('id','phone_number','role','avatar','user')
admin.site.register(ProfilUtilisateur,ProfilUtilisateurAdmin)
        
# affichage du categorie dans admin django
class CategorieAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('id','nom','slug')
admin.site.register(Categorie,CategorieAdmin)

# affichage de l'enchere dans admin
class EnchereAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('titre','description','prix_depart','prix_actuel','prix_reserve','date_debut','date_fin','statut','vendeur','categorie')
admin.site.register(Enchere, EnchereAdmin)
