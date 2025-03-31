from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Affiche la page d'accueil
    path('signup/', views.signup_view, name='signup'),  # Route pour l'inscription
    path('signin/', views.signin_view, name='signin'),  # Route pour la connexion
    path('logout/', views.logout_view, name='logout'),  # Déconnexion
    path('profil/', views.update_view, name='profil'),  # Route vers /profil/
    path('produit/', views.produit_view, name='produit_view'),
    path('commande/', views.commande_view, name='commande_view'), 
    path('modifierPr/<int:id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimerPr/<int:id>/', views.supprimer_produit, name='supprimer_produit'),
    path('modifierCo/<int:id>/', views.modifier_commande, name='modifier_commande'),
    path('supprimerCo/<int:id>/', views.supprimer_commande, name='supprimer_commande'),
]