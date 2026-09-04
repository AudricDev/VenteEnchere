from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('connexion/',views.connexion,name='connexion'),
    path('deconnexion/',views.deconnexion,name='deconnexion'),
    path('inscription/',views.inscription,name='inscription'),
    path('detail_enchere/',views.detail_enchere,name='detail_enchere'),
    path('inscription_enchere/',views.inscription_enchere,name='inscription_enchere'),
    path('pageCreerEnchere/',views.pageCreerEnchere,name='pageCreerEnchere'),
    path('profil/',views.modifier_profil_page,name='modifier_profil_page'),
    path('modifier_profil/',views.modifier_profil,name='modifier_profil'),
    
    path('ajouter_produit/',views.ajouter_produit,name='ajouter_produit'),
    
]