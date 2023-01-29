from time import timezone
from django.db import models
from django.urls import reverse
from Shop.settings import AUTH_USER_MODEL

# Create your models here.

"""
Creer un groupe de produit
--------------------------
-Nom de la category
"""
class GroupeProduct(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


"""
Model de Produit
----------------
- Nom
- Prix
- La quantité en Stock
- Description
- Image

"""
class Product(models.Model):
    name = models.CharField(max_length=150)
    groupe = models.ForeignKey(GroupeProduct, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=False, null=False)
    
    def __str__(self):
        """
        En utilisants la methode suivante on peut afficher aussi d'autre donné
        return f"{self.name} {self.stock}"
        """
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})
    
    
    
# Article Commander (order)
"""

- Utilisateur
- Produit
- Quantiter
- Commandé ou non

"""

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        #return self.user
        return f"{self.product.name} ({self.quantity}) "
    
    

# Panier utilisateur (cart)
""" 
- Utilisateur
- Commandé ou non 
- Date de la comande

"""

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)    
    
    
    def __str__(self):
        return self.user.username
    
    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.orderer = True
            order.ordered_date = timezone.now()
            order.save() 
        
        self.orders.clear()
        return super().delete(*args, **kwargs)
    
    
class Contact(models.Model):
    email = models.EmailField()
    description = models.TextField()
    number = models.CharField(max_length=150)
