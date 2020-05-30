from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from djmoney.models.fields import MoneyField
from PIL import Image

# Create your models here.

CONDITION_CODE = (
    ("N", "New"),
    ("LN", "Like New"),
    ("ND", "New (With Defects"),
    ("VG", "Very Good"),
    ("G", "Good"),
    ("USE", "Heavily Used"),
)
CATEGORY_CODE = (
    ("lower", "Bottoms"),
    ("tops", "Tops"),
    ("outerwear", "Outerwear"),
    ("shoes", "Shoes"),
    ("misc", "Accessories and Misc"),
)


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to="product_pics")
    condition = models.CharField(null=True, choices=CONDITION_CODE, max_length=5)
    category = models.CharField(null=True, choices=CATEGORY_CODE, max_length=10)
    brand = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = MoneyField(decimal_places=2, default_currency="GBP", max_digits=11)
    size = models.CharField(max_length=200, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    colour = models.CharField(max_length=200, null=True, blank=True)
    in_stock = models.IntegerField(default=1, blank=True)
    for_sale = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, null=True)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    receipt = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        get_latest_by = "date_ordered"

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name: {self.customer.name} Email: {self.customer.email} Address:{self.address} Post Code: {self.postcode} City: {self.city}"

    def get_absolute_url(self):
        return reverse("checkout")

    def get_absolute_url(self):
        return reverse("shipping-update", kwargs={"pk": self.pk})
