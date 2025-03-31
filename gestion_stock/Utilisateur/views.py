from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from Utilisateur.models import User,Produit,Commande

# Create your views here.

def home_view(request):
    return render(request, 'home.html')

# Vue pour l'inscription
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Vérifie si l'email ou le nom d'utilisateur existe déjà
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Cet email est déjà utilisé.'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Ce nom d\'utilisateur est déjà pris.'})

        # Hachage du mot de passe avant de l'enregistrer
        hashed_password = make_password(password)

        # Créer un nouvel utilisateur dans la base de données
        user = User.objects.create(username=username, email=email, password=hashed_password)
        
        # Rediriger vers la page de connexion après l'inscription
        return redirect('signin')

    return render(request, 'signup.html')  # Affiche la page d'inscription si GET

def signin_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Si l'utilisateur est déjà connecté, redirige vers home

    if request.method == 'POST':
        # Déconnecter l'utilisateur actuel
        if request.user.is_authenticated:
            logout(request)
        # Traitement du formulaire de connexion
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')  # Redirige vers 'next' ou 'home' par défaut
            return redirect(next_url)  # Redirection après la connexion

        else:
            # Si l'authentification échoue
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
            return render(request, 'signin.html')

    return render(request, 'signin.html')  # Affiche la page de connexion si GET

def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('home')  # Redirige vers la page d'accueil après déconnexion


def update_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = request.user  # Récupérer l'utilisateur connecté
        
        # Vérification d'unicité des données
        if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            return render(request, 'profil.html', {'error': 'Cet username est déjà utilisé.'})
        if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            return render(request, 'profil.html', {'error': 'Cet email est déjà utilisé.'})

        # Hachage du mot de passe avant de l'enregistrer
        hashed_password = make_password(password)

        # Mettre à jour les informations utilisateur
        user.username = username
        user.email = email
        user.password = hashed_password
        user.save()


        # Message de succès et redirection
        return redirect('signin')

    return render(request, 'profil.html')


def produit_view(request):
    produits = Produit.objects.filter(user=request.user)
    if request.method == 'POST':
        code= request.POST['code_prod']
        nom  = request.POST['nom_prod']
        description = request.POST['description']
        quantite = request.POST['quantite_pr']
        prix = request.POST['prix']
        image = request.FILES['image']

        
       

        
        Produit.objects.create(
            code_prod=code,
            nom_prod=nom,
            description=description,
            quantite_pr=quantite,
            prix=prix,
            image=image,  
            user=request.user  
        )

        return redirect('produit_view')  

    return render(request, 'produit.html',{'produits': produits})       

def commande_view(request):
    commande = Commande.objects.filter(user=request.user)
    produits = Produit.objects.filter(user=request.user)  # Récupérer les produits pour la liste déroulante
    if request.method == 'POST':
        code_commande = request.POST['code_com']
        quantit_cmde  = request.POST['quantite_cmd']
        date_cmd= request.POST['date_cmd']
        produit_id = request.POST['produit']  # Récupérer l'ID du produit sélectionné
        
        # Vérifier que le produit existe avant de créer la commande
        produit = Produit.objects.get(id=produit_id)

       

        
        Commande.objects.create(
            code_commande=code_commande,
            quantit_cmde=quantit_cmde,
            date_cmd=date_cmd,
            produit=produit,  
            user=request.user  
        )

        return redirect('commande_view')  # Redirection vers 'enchere'

    return render(request, 'commande.html',{'commandes': commande, 'produits': produits})  

def modifier_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.code_prod = request.POST.get('code_prod', produit.code_prod)
        produit.nom_prod = request.POST.get('nom_prod', produit.nom_prod)
        produit.description = request.POST.get('description', produit.description)
        produit.quantite_pr = request.POST.get('quantite_pr', produit.quantite_pr)
        produit.prix = request.POST.get('prix', produit.prix)
        if 'image' in request.FILES:
            produit.image = request.FILES['image']
        produit.save()
        return redirect(produit_view)  # Remplacez par le nom de votre vue principale
    return render(request, 'produit_modifier.html', {'produit': produit})

def supprimer_produit(request, id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        produit.delete()
        return redirect(produit_view)  # Remplacez par le nom de votre vue principale
    return render(request, 'produit.html', {'produit': produit})




def modifier_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    produits = Produit.objects.filter(user=request.user)

    if request.method == 'POST':
        commande.code_commande = request.POST.get('code_com', commande.code_commande)
        commande.quantit_cmde = request.POST.get('quantit_cmde', commande.quantit_cmde)
        commande.date_cmd = request.POST.get('date', commande.date_cmd)
        
        produit_id = request.POST.get('produit')

        if produit_id:  # Vérifier que l'ID du produit est fourni
            # Convertir l'ID en une instance de Produit
            produit = get_object_or_404(Produit, id=produit_id)
            commande.produit = produit

        commande.save()
        return redirect(commande_view)  # Remplacez par le nom de votre vue principale
    return render(request, 'commande_modifier.html', {'commande': commande, 'produits': produits})

def supprimer_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    if request.method == 'POST':
        commande.delete()
        return redirect(commande_view)  # Remplacez par le nom de votre vue principale
    return render(request, 'commande.html', {'commande': commande})