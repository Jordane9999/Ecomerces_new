from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.   
   
class Shopper(AbstractUser):
   number = models.CharField(max_length=150)
   
   def __str__(self):
      return self.number