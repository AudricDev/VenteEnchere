from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout

# Create your views here.
def index(request):
    return HttpResponse("index here bro")

def connexion(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(username = email, password = password).first()
        login(request,user)
        return render(request,'index.html')
    return render(request,'connexion.html')

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