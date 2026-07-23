from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
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