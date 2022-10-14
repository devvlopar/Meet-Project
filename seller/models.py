from django.db import models

# Create your models here.
class Seller(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='seller_profile', default='sad.jpg')
    gst_number = models.CharField(max_length=15, null= True, blank= True)

    def __str__(self) -> str:
        return self.first_name


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null = True, blank = True)
    price = models.FloatField(default = 0.0)
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 0)
    pic = models.FileField(upload_to='products', default='sad.jpg')

    def __str__(self) -> str:
        return self.name


