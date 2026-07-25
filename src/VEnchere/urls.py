from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('connexion/',views.connexion,name='connexion'),
    path('deconnexion/',views.deconnexion,name='deconnexion'),
    path('inscription/',views.inscription,name='inscription'),
    path('detail_enchere/',views.detail_enchere,name='detail_enchere'),
    path('inscription_enchere/',views.inscription_enchere,name='inscription_enchere'),
    
]