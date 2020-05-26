from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name  = models.CharField(max_length=200,null=True)
    email  = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION_CODE = (
        ('N','New'),
        ('LN','Like New'),
        ('ND','New (With Defects'),
        ('VG','Very Good'),
        ('G','Good'),
        ('USE','Heavily Used'),
    )
    CATEGORY_CODE=(
        ('lower','Bottoms'),
        ('tops','Tops'),
        ('outerwear','Outerwear'),
        ('shoes','Shoes'),
        ('misc','Accessories and Misc')
    )
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='product_pics')
    condition=models.CharField(null=True,choices=CONDITION_CODE,max_length=5)
    category=models.CharField(null=True,choices=CATEGORY_CODE,max_length=10)
    brand= models.CharField(max_length=200, null=True,blank=True)
    description =models.TextField(null=True,blank=True)
    price = models.FloatField()
    size=models.CharField(max_length=200, null=True,blank=True)
    date_posted=models.DateTimeField(default=timezone.now)
    colour=models.CharField(max_length=200, null=True,blank=True)
    in_stock=models.IntegerField(default=1,blank=True)
    for_sale = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.brand} - {self.name}'

    def save(self):
        super().save()
        img =Image.open(self.image.path)

        if img.height > 600 or img.width >600:
            output_size=(600,600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})