from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.contrib.auth.models import User
from Stors.models import GroupeProduct

User = get_user_model()

# Create your views here.
def signup(request):
    categories = GroupeProduct.objects.all()
    context ={
        'categories':categories
    }
    if request.method == "POST":
        name = request.POST.get("name")
        prenom = request.POST.get("prenom")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        
        #Verrification des donner entrer par l'utilisateur
        if User.objects.filter(username=username):
            messages.error(request, "Ce Nom d'utilisatuer est deja Utiliser")
            return redirect("signup")
        
        if not username.isalnum():
            messages.error(request, "Ce Nom d'utilisateur doit etre en Alpha numerique")
            return redirect("signup")
        
        if User.objects.filter(first_name=name) and User.objects.filter(last_name=prenom):
            messages.error(request, "Ce Nom et Prénom sont deja Utiliser")
            return redirect("signup")
        
        if User.objects.filter(email=email):
            messages.error(request, "Ce Email est deja Utiliser")
            return redirect("signup")
        
        if password != password1 :
            messages.error(request, "Le Mot de Pass ne coinside pas")
            return redirect("signup")
        
        if not len(password) >= 8:
            messages.error(request, "Le Mot de Pass doit etre aumoin de huit(08) Carracterre")
            return redirect("signup")
        
        #Creer l'utilisateur
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = name
        user.last_name = prenom
        user.save()
        return redirect("login")
    
    return render(request, "accounts/signup.html", context)

#------------------------------------------------------------------------------------#
def login_user(request):
    categories = GroupeProduct.objects.all()
    context ={
        'categories':categories
    }
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")    
        user = authenticate(username=username, password=password)
        if user :
            login(request, user)
            return redirect("home")
        else :
            messages.error(request,"You have not account in this plateforme please create befor sigin")
    
    
    return render(request, "accounts/login.html", context)


#--------------------------------------------------------------------------------------#
def logout_user(request):
    logout(request)
    return redirect("home")