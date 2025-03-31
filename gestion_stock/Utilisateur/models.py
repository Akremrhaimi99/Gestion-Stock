from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    groups = None  
    user_permissions = None  


class Produit(models.Model):
    code_prod = models.IntegerField()  
    nom_prod = models.CharField(max_length=255)  
    description = models.CharField(max_length=500)  
    quantite_pr = models.IntegerField()  
    prix = models.FloatField() 
    image = models.ImageField(upload_to='photos/%y/%m/%d', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return(self.nom_prod)



class Commande(models.Model):
    code_commande = models.IntegerField()  
    quantit_cmde = models.IntegerField()
    date_cmd = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return(self.produit.nom_prod)
