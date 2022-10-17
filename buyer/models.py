from pyexpat import model
from django.db import models

from seller.models import Product

# Create your models here.
class Buyer(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    passwd = models.CharField(max_length=30)
    pic = models.FileField(upload_to='media', default='sad.jpg')

    def __str__(self):
        return self.email


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE )
    buyer = models.ForeignKey(Buyer, on_delete = models.CASCADE)

    

    
   