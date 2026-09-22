from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('connexion/',views.connexion,name='connexion'),
    path('deconnexion/',views.deconnexion,name='deconnexion'),
    path('inscription/',views.inscription,name='inscription'),
    path('inscription_enchere/',views.inscription_enchere,name='inscription_enchere'),
    path('pageCreerEnchere/',views.pageCreerEnchere,name='pageCreerEnchere'),
    path('profil/',views.modifier_profil_page,name='modifier_profil_page'),
    path('modifier_profil/',views.modifier_profil,name='modifier_profil'),
    path('mes-produits/en-attente/',views.produits_en_attente, name='produits_en_attente'),
    path('ajouter_produit/',views.ajouter_produit,name='ajouter_produit'),
    path(
        "administration/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),    
    path(
    "enchere/<uuid:enchere_id>/inscription/",
    views.inscrire_enchere,
    name="inscrire_enchere"
),
    path(
    "enchere/<uuid:enchere_id>/",
    views.detail_enchere,
    name="detail_enchere"
),
path(
    "enchere/<uuid:enchere_id>/offre/",
    views.faire_offre,
    name="faire_offre"
),
]