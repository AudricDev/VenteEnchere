from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
#@login_required
def index(request):
    return render(request, 'index.html')

def connexion(request):
    errors = []
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # user = User.objects.filter(username=email).first()
        user = authenticate(request, username=email,password=password)

        print(f" information : {user}")
        print(f" email saisi : {email}")
        print(f" password : {password}")

        if user is not None:
            login(request,user)
            return redirect("index")
        else :
            errors.append(f'information incorrect : {user}')
    return render(request,'connexion.html',{"errors":errors})

def deconnexion(request):
    logout(request)
    return redirect('connexion')

def inscription(request):
    if request.method == "POST":
        email = request.POST.get("email")
        mdp1 = request.POST.get("mdp1")
        mdp2 = request.POST.get("mdp2")
        if mdp1 == mdp2:
            data = User.objects.create_user(
                username = email,
                email = email,
                password = mdp1
            )
            data.save()
            login(request, data)
            return render(request,'index.html')
    return render(request,'inscription.html')

def inscription_enchere(request):
    return render(request,'pages/incription_enchere.html')

def detail_enchere(request):
    return render(request,'pages/detail_enchere.html')

# création d'enchere
def pageCreerEnchere(request):
    cat = Categorie.objects.all()
    profil = ProfilUtilisateur.objects.all()
    return render(request,'pages/creerEnchere.html', {
        "categories":cat,
        "profils":profil
        })

@login_required
def ajouter_produit(request):
    error = []
    if request.method == "POST":

        nom = request.POST.get("nomProduit")
        description = request.POST.get("descriptionProduit")
        marque = request.POST.get("marque")
        modele = request.POST.get("modele")
        poids = request.POST.get("poids")
        reference = request.POST.get("reference")
        categorie_id = request.POST.get("categories")


        if nom == '' or description == '':
            errors = error.append("Nom et description obligatoire !")
        else:
            categorie = get_object_or_404(
                Categorie,
                id=categorie_id
            )
            produit = Produit.objects.create(
                nom=nom,
                description=description,
                marque=marque,
                modele=modele,
                poids=poids,
                reference=reference,
                categorie=categorie,
                utilisateur=request.user.profilutilisateur
            )
            return redirect("index")
    categories = Categorie.objects.all()


    return render(
        request,
        "pages/creerEnchere.html",
        {
            "categories": categories,
            "errors": error
        }
    )