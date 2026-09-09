from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
#@login_required
def index(request):
    product = Produit.objects.all()
    return render(request, 'index.html',{"products":product})

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

        # Vérifier si l'email existe déjà
        if User.objects.filter(email=email).exists():
            return render(request, "inscription.html", {
                "erreur": "Cette adresse email est déjà utilisée."
            })

        # Vérifier les mots de passe
        if mdp1 != mdp2:
            return render(request, "inscription.html", {
                "erreur": "Les mots de passe ne correspondent pas."
            })

        # Créer le User
        data = User.objects.create_user(
            username=email,
            email=email,
            password=mdp1
        )

        # Créer le profil
        ProfilUtilisateur.objects.create(
            user=data
        )

        # Connecter l'utilisateur
        login(request, data)

        return redirect("index")

    return render(request, "inscription.html")

def inscription_enchere(request):
    return render(request,'pages/incription_enchere.html')

def detail_enchere(request,id):
    detail = Produit.objects.filter(id=id).first()
    return render(request,
        'pages/detail_enchere.html',
        {"details":detail}
        )

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
    validations = []

    if request.method == "POST":

        # ==========================
        # INFORMATIONS VENDEUR
        # ==========================

        nomVendeur = request.POST.get("vendeur")
        emailVendeur = request.POST.get("email")
        phoneVendeur = request.POST.get("phone")

        print(f"telephone : {phoneVendeur}")


        # ==========================
        # INFORMATIONS PRODUIT
        # ==========================

        nom = request.POST.get("nomProduit")
        description = request.POST.get("descriptionProduit")
        marque = request.POST.get("marque")
        modele = request.POST.get("modele")
        poids = request.POST.get("poids")
        reference = request.POST.get("reference")
        categorie_id = request.POST.get("categories")

        photo_produit = request.FILES.get("photoProduit")


        # ==========================
        # VALIDATION VENDEUR
        # ==========================

        if not nomVendeur or not phoneVendeur:

            validations.append(
                "Complétez votre profil, c'est obligatoire !!!"
            )


        # ==========================
        # VALIDATION PRODUIT
        # ==========================

        if not nom or not description or not categorie_id:

            error.append(
                "N'oubliez pas de choisir la catégorie. "
                "Le nom et la description sont obligatoires !"
            )

        else:

            # Récupération de la catégorie
            categorie = get_object_or_404(
                Categorie,
                id=categorie_id
            )


            # ==========================
            # CREATION DU PRODUIT
            # ==========================

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


            # ==========================
            # CREATION DE LA PHOTO
            # ==========================

            if photo_produit:

                Produit_photo.objects.create(
                    name=nom,
                    image=photo_produit,
                    produit=produit
                )


            return redirect("index")


    categories = Categorie.objects.all()

    return render(
        request,
        "pages/creerEnchere.html",
        {
            "categories": categories,
            "errors": error,
            "infos": validations
        }
    )

    # validation enchere
    def validate_enchere(request):
        enchere = Enchere.objects.all()
        return render( request,
        "pages/creerEnchere.html",
        {
            "categories": categories,
            "errors": error
        }
)

@login_required
def modifier_profil_page(request):
    return render(request,"pages/modifier_profil.html")

@login_required
def modifier_profil(request):

    profil = request.user.profilutilisateur

    if request.method == "POST":

        # Informations User
        request.user.username = request.POST.get("username")
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")

        request.user.save()


        # Informations ProfilUtilisateur
        profil.phone_number = request.POST.get("phone_number")


        # Nouvelle photo
        if request.FILES.get("avatar"):
            profil.avatar = request.FILES.get("avatar")


        profil.save()

        return redirect("modifier_profil_page")


    context = {
        "profil": profil
    }

    return render(
        request,
        "modifier_profil.html",
        context
    )


@login_required
def produits_en_attente(request):

    profil = request.user.profilutilisateur

    produits = Produit.objects.filter(
        utilisateur=profil,
        statut_validation='attente'
    ).prefetch_related('photos').order_by('-date_creation')

    context = {
        'produits': produits
    }

    return render(
        request,
        'pages/produits_en_attente.html',
        context
    )










@login_required
def admin_dashboard(request):

    # Vérification du rôle
    profil = request.user.profilutilisateur

    if profil.role != "Admin":
        return redirect("index")


    # ==========================
    # STATISTIQUES
    # ==========================

    total_produits = Produit.objects.count()

    encheres_ouvertes = Enchere.objects.filter(
        statut="ouverte"
    ).count()

    total_utilisateurs = User.objects.count()

    produits_attente = Produit.objects.filter(
        statut_validation="attente"
    ).count()


    # ==========================
    # PRODUITS EN ATTENTE
    # ==========================

    produits_attente_liste = Produit.objects.filter(
        statut_validation="attente"
    ).select_related(
        "categorie",
        "utilisateur__user"
    ).prefetch_related(
        "photos"
    ).order_by(
        "-date_creation"
    )[:10]


    # ==========================
    # ENCHÈRES
    # ==========================

    encheres = Enchere.objects.filter(
        statut="ouverte"
    ).select_related(
        "vendeur__user",
        "produit"
    ).order_by(
        "date_fin"
    )[:10]


    # ==========================
    # UTILISATEURS
    # ==========================

    utilisateurs_recents = User.objects.select_related(
        "profilutilisateur"
    ).order_by(
        "-date_joined"
    )[:5]


    # ==========================
    # PAIEMENTS
    # ==========================

    paiements_recents = Paiement.objects.order_by(
        "-date_creation"
    )[:5]


    context = {
        "total_produits": total_produits,
        "encheres_ouvertes": encheres_ouvertes,
        "total_utilisateurs": total_utilisateurs,
        "produits_attente": produits_attente,

        "produits_attente_liste": produits_attente_liste,

        "encheres": encheres,

        "utilisateurs_recents": utilisateurs_recents,

        "paiements_recents": paiements_recents,
    }


    return render(
        request,
        "admin/dashboard.html",
        context
    )