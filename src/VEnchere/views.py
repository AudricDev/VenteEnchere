from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from decimal import Decimal
# Create your views here.
#@login_required
def index(request):

    encheres = Enchere.objects.filter(
        statut="ouverte"
    ).select_related(
        "produit",
        "produit__categorie",
        "vendeur__user"
    ).prefetch_related(
        "produit__photos"
    ).order_by("date_fin")

    return render(
        request,
        "index.html",
        {
            "encheres": encheres
        }
    )

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

@login_required
def detail_enchere(request, enchere_id):

    enchere = get_object_or_404(
        Enchere,
        id=enchere_id
    )

    profil = request.user.profilutilisateur

    inscrit = Participation.objects.filter(
        acheteur=profil,
        enchere=enchere
    ).exists()

    offres = Offre.objects.filter(
        enchere=enchere
    ).select_related(
        "utilisateur__user"
    ).order_by(
        "-montant"
    )

    return render(
        request,
        "pages/detail_enchere.html",
        {
            "enchere": enchere,
            "inscrit": inscrit,
            "offres": offres,
        }
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


@login_required
def inscrire_enchere(request, enchere_id):
    enchere = get_object_or_404(
        Enchere,
        id=enchere_id
    )
    profil = request.user.profilutilisateur

    if profil.role != "Acheteur":
        messages.error(
            request,
            "Seuls les acheteurs peuvent participer à une enchère."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    if enchere.vendeur == profil:
        messages.error(
            request,
            "Vous ne pouvez pas participer à votre propre enchère."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    if enchere.statut != "ouverte":
        messages.error(
            request,
            "Cette enchère n'est pas ouverte."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )
    participation = Participation.objects.create(
        acheteur=profil,
        enchere=enchere
    )
    # Vérification immédiate
    verification = Participation.objects.filter(
        acheteur=profil,
        enchere=enchere
    ).exists()

    messages.success(
        request,
        "Vous êtes maintenant inscrit à cette enchère."
    )

    return redirect(
        "detail_enchere",
        enchere_id=enchere.id
    )

# encherissement
@login_required
def faire_offre(request, enchere_id):
    print("========== FAIRE OFFRE ==========")
    print("Méthode :", request.method)
    print("Montant reçu :", request.POST.get("montant"))

    if request.method != "POST":
        return redirect(
            "detail_enchere",
            enchere_id=enchere_id
        )

    enchere = get_object_or_404(
        Enchere,
        id=enchere_id
    )

    profil = request.user.profilutilisateur

    # Vérifier le rôle
    if profil.role != "Acheteur":
        messages.error(
            request,
            "Seuls les acheteurs peuvent enchérir."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Le vendeur ne peut pas enchérir
    if enchere.vendeur == profil:
        messages.error(
            request,
            "Vous ne pouvez pas enchérir sur votre propre enchère."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Vérifier l'inscription
    inscrit = Participation.objects.filter(
        acheteur=profil,
        enchere=enchere
    ).exists()

    if not inscrit:
        messages.error(
            request,
            "Vous devez d'abord vous inscrire à cette enchère."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Vérifier le statut
    if enchere.statut != "ouverte":
        messages.error(
            request,
            "Cette enchère n'est pas ouverte."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Vérifier les dates
    maintenant = timezone.now()

    if maintenant < enchere.date_debut:
        messages.error(
            request,
            "Cette enchère n'a pas encore commencé."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    if maintenant >= enchere.date_fin:
        messages.error(
            request,
            "Cette enchère est terminée."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Récupérer le montant
    montant_saisi = request.POST.get("montant")

    if not montant_saisi:
        messages.error(
            request,
            "Veuillez saisir un montant."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Convertir en Decimal
    try:
        montant = Decimal(montant_saisi)
    except:
        messages.error(
            request,
            "Le montant saisi est invalide."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Déterminer le prix actuel
    prix_actuel = (
        enchere.prix_actuel
        if enchere.prix_actuel is not None
        else enchere.prix_depart
    )

    # Vérifier que l'offre est supérieure
    if montant <= prix_actuel:
        messages.error(
            request,
            f"Votre offre doit être supérieure à {prix_actuel} Ar."
        )
        return redirect(
            "detail_enchere",
            enchere_id=enchere.id
        )

    # Créer l'offre
    offre = Offre.objects.create(
        montant=montant,
        utilisateur=profil,
        enchere=enchere
    )

    print("========== OFFRE CRÉÉE ==========")
    print("ID :", offre.id)
    print("Montant :", offre.montant)
    print("Acheteur :", offre.utilisateur)
    print("Enchère :", offre.enchere)

    # Mettre à jour le prix actuel
    enchere.prix_actuel = montant
    enchere.save(update_fields=["prix_actuel"])

    messages.success(
        request,
        f"Votre offre de {montant} Ar a été enregistrée."
    )

    return redirect(
        "detail_enchere",
        enchere_id=enchere.id
    )