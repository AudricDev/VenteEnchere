from django.contrib import admin
from accounts.models import ProfilUtilisateur
# Register your models here.
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ('name','phone_number','role','avatar','user')
admin.site.register(ProfilUtilisateur,ProfilUtilisateurAdmin)
        
        