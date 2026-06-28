from django.contrib import admin
from accounts.models import ProfilUtilisateur
# Register your models here.
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('phone_number','role','avatar','user','date_creation')
admin.site.register(ProfilUtilisateur,ProfilUtilisateurAdmin)
        
        